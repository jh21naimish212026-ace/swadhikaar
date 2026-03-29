import os
import time
import json
import logging
import asyncio

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/api/voice", tags=["voice"])
logger = logging.getLogger("swadhikaar.voice")

# Lazy LiveKit SDK import — may not be installed
try:
    from livekit import api as lk_api
    LIVEKIT_AVAILABLE = True
except ImportError:
    LIVEKIT_AVAILABLE = False

# Cached Supabase client for voice router
_sb_client = None

def _get_supabase():
    global _sb_client
    if _sb_client is not None:
        return _sb_client
    url = os.getenv("SUPABASE_URL", "")
    key = os.getenv("SUPABASE_KEY", "")
    if not url or not key:
        return None
    try:
        from supabase import create_client
        _sb_client = create_client(url, key)
        return _sb_client
    except Exception:
        return None


async def _build_patient_context(patient_id: str) -> dict:
    """Query Supabase for patient's full clinical context: vitals, symptoms,
    risk scores, and recent call history.

    All 5 queries run in PARALLEL via asyncio.to_thread for ~3x speedup.
    Returns enrichment dict for room metadata."""
    sb = _get_supabase()
    if sb is None:
        return {}

    # Define each query as a sync function for asyncio.to_thread
    def q_vitals():
        return sb.table("health_vitals").select("*").eq("patient_id", patient_id) \
            .order("recorded_at", desc=True).limit(1).execute()

    def q_symptoms():
        return sb.table("symptoms").select("*").eq("patient_id", patient_id) \
            .order("recorded_at", desc=True).limit(1).execute()

    def q_risks():
        return sb.table("risk_assessments").select("*").eq("patient_id", patient_id) \
            .order("assessed_at", desc=True).limit(1).execute()

    def q_calls():
        return sb.table("voice_calls").select("call_type,status,severity,transcript,created_at") \
            .eq("patient_id", patient_id).order("created_at", desc=True).limit(3).execute()

    def q_newborns():
        return sb.table("newborns").select("*").eq("parent_patient_id", patient_id).limit(1).execute()

    # Run ALL queries concurrently — ~3x faster than sequential
    try:
        vr, sr, rr, cr, nr = await asyncio.gather(
            asyncio.to_thread(q_vitals),
            asyncio.to_thread(q_symptoms),
            asyncio.to_thread(q_risks),
            asyncio.to_thread(q_calls),
            asyncio.to_thread(q_newborns),
        )
    except Exception as exc:
        logger.warning("Failed to enrich patient context: %s", exc)
        return {}

    ctx: dict = {}

    # Process vitals
    if vr.data:
        v = vr.data[0]
        ctx["systolic_bp"] = v.get("systolic_bp")
        ctx["diastolic_bp"] = v.get("diastolic_bp")
        ctx["blood_glucose"] = v.get("blood_glucose")
        ctx["bmi"] = v.get("bmi")
        ctx["heart_rate"] = v.get("heart_rate")
        ctx["oxygen_saturation"] = v.get("oxygen_saturation")

    # Process symptoms
    if sr.data:
        s = sr.data[0]
        active_symptoms = []
        for key in ["chest_discomfort", "breathlessness", "palpitations",
                    "fatigue_weakness", "dizziness_blackouts", "stress_anxiety"]:
            val = s.get(key, "")
            if val and val.lower() not in ("none", "no", "never", ""):
                active_symptoms.append(f"{key.replace('_', ' ')}: {val}")
        if active_symptoms:
            ctx["active_symptoms"] = ", ".join(active_symptoms)
        ctx["family_history"] = s.get("family_history", "")
        ctx["diet_quality"] = s.get("diet_quality", "")
        ctx["sleep_duration"] = s.get("sleep_duration", "")

    # Process risk assessments
    if rr.data:
        r = rr.data[0]
        ctx["heart_risk"] = f"{r.get('heart_risk_level', 'N/A')} ({r.get('heart_risk_score', 'N/A')})"
        ctx["diabetic_risk"] = f"{r.get('diabetic_risk_level', 'N/A')} ({r.get('diabetic_risk_score', 'N/A')})"
        ctx["hypertension_risk"] = f"{r.get('hypertension_risk_level', 'N/A')} ({r.get('hypertension_risk_score', 'N/A')})"

    # Process call history
    if cr.data:
        history_lines = []
        for c in cr.data:
            date = c["created_at"][:10] if c.get("created_at") else "?"
            transcript_preview = (c.get("transcript") or "")[:200].replace("\n", " ")
            history_lines.append(
                f"{date} | {c.get('call_type','?')} | severity={c.get('severity','?')} | {transcript_preview}"
            )
        ctx["call_history"] = "\n".join(history_lines)
        ctx["total_previous_calls"] = str(len(cr.data))

    # Process newborn data
    if nr.data:
        baby = nr.data[0]
        ctx["baby_name"] = baby.get("baby_name", "Baby")
        ctx["baby_gender"] = baby.get("gender", "")
        ctx["birth_hospital"] = baby.get("birth_hospital", "")
        ctx["baby_dob"] = baby.get("date_of_birth", "")
        # Calculate baby age
        if baby.get("date_of_birth"):
            from datetime import date
            dob = date.fromisoformat(baby["date_of_birth"])
            age_days = (date.today() - dob).days
            if age_days < 30:
                ctx["baby_age"] = f"{age_days} days"
            elif age_days < 365:
                ctx["baby_age"] = f"{age_days // 30} months"
            else:
                ctx["baby_age"] = f"{age_days // 365} years"

        # Next due vaccine (runs sync since we already have baby data)
        try:
            vsr = sb.table("vaccination_schedules").select("*") \
                .eq("newborn_id", baby["id"]) \
                .in_("status", ["pending", "overdue"]) \
                .order("due_date").limit(1).execute()
            if vsr.data:
                vax = vsr.data[0]
                ctx["next_vaccine"] = vax.get("vaccine_name", "")
                ctx["vaccine_due_date"] = vax.get("due_date", "")
                ctx["vaccine_dose"] = str(vax.get("dose_number", 1))
        except Exception as exc:
            logger.warning("Vaccination query failed: %s", exc)

    # Remove None values
    return {k: v for k, v in ctx.items() if v is not None}


class StartCallRequest(BaseModel):
    patient_id: str
    patient_name: str = "Patient"
    abha_id: str = ""
    language: str = "hindi"
    call_type: str = "follow_up"
    phone_number: Optional[str] = None  # E.164 format: "+919876543210"
    # Optional patient context for the agent's system prompt
    age: Optional[int] = None
    gender: Optional[str] = None
    health_camp: Optional[str] = None
    risk_level: Optional[str] = None
    risk_score: Optional[float] = None
    systolic_bp: Optional[int] = None
    diastolic_bp: Optional[int] = None
    blood_glucose: Optional[int] = None
    bmi: Optional[float] = None
    medications: Optional[str] = None
    doctor_name: Optional[str] = None
    primary_condition: Optional[str] = None
    # Vaccination-specific fields
    baby_name: Optional[str] = None
    baby_age: Optional[str] = None
    baby_gender: Optional[str] = None
    next_vaccine: Optional[str] = None
    vaccine_dose: Optional[str] = None
    vaccine_due_date: Optional[str] = None
    birth_hospital: Optional[str] = None

class CallResponse(BaseModel):
    call_id: str
    status: str
    livekit_token: Optional[str] = None
    livekit_url: Optional[str] = None


@router.post("/start", response_model=CallResponse)
async def start_call(request: StartCallRequest):
    """Start a voice call with a patient via LiveKit."""
    livekit_url = os.getenv("LIVEKIT_URL", "")
    api_key = os.getenv("LIVEKIT_API_KEY", "")
    api_secret = os.getenv("LIVEKIT_API_SECRET", "")

    if not livekit_url or not api_key or not api_secret:
        # Demo mode — return placeholder
        return CallResponse(
            call_id=f"demo-{int(time.time())}",
            status="demo_mode",
            livekit_token=None,
            livekit_url=None,
        )

    if not LIVEKIT_AVAILABLE:
        raise HTTPException(status_code=500, detail="LiveKit SDK not installed")

    room_name = f"swadhikaar-{request.patient_id}-{int(time.time())}"

    # Generate participant token for the browser client
    token = lk_api.AccessToken(api_key, api_secret)
    token.with_identity(f"patient-{request.patient_id}")
    token.with_name(request.patient_name)
    token.with_grants(lk_api.VideoGrants(
        room_join=True,
        room=room_name,
    ))

    # Room metadata carries patient context → the agent reads this
    # Enrich with clinical history from Supabase (queries run in parallel)
    base_metadata = {k: v for k, v in request.model_dump().items() if v is not None}
    enriched = await _build_patient_context(request.patient_id)
    room_metadata = json.dumps({**base_metadata, **enriched})

    # Create room with metadata via LiveKit API
    lkapi = lk_api.LiveKitAPI(livekit_url, api_key, api_secret)
    try:
        await lkapi.room.create_room(
            lk_api.CreateRoomRequest(
                name=room_name,
                metadata=room_metadata,
                agents=[
                    lk_api.RoomAgentDispatch(agent_name="", metadata=room_metadata)
                ],
            )
        )

        # If phone_number provided, create SIP participant for outbound dialing
        if request.phone_number:
            sip_trunk_id = os.getenv("SIP_TRUNK_ID", "")
            if not sip_trunk_id:
                raise HTTPException(
                    status_code=400,
                    detail="SIP_TRUNK_ID not configured. Run POST /api/voice/sip/setup first.",
                )
            await lkapi.sip.create_sip_participant(
                lk_api.CreateSIPParticipantRequest(
                    sip_trunk_id=sip_trunk_id,
                    sip_call_to=request.phone_number,
                    room_name=room_name,
                    participant_identity=f"phone-{request.patient_id}",
                    participant_name=request.patient_name,
                )
            )
    finally:
        await lkapi.aclose()

    return CallResponse(
        call_id=room_name,
        status="dialing" if request.phone_number else "connecting",
        livekit_token=None if request.phone_number else token.to_jwt(),
        livekit_url=livekit_url,
    )

@router.post("/end/{call_id}")
async def end_call(call_id: str):
    """End an active voice call."""
    # TODO: Delete LiveKit room to force disconnect
    return {"call_id": call_id, "status": "ended"}

@router.get("/status/{call_id}")
async def call_status(call_id: str):
    """Get status of an active call."""
    return {"call_id": call_id, "status": "active", "duration_seconds": 0}

@router.get("/token")
async def get_livekit_token(patient_id: str, room: str):
    """Generate LiveKit token for browser-based voice."""
    api_key = os.getenv("LIVEKIT_API_KEY", "")
    api_secret = os.getenv("LIVEKIT_API_SECRET", "")
    livekit_url = os.getenv("LIVEKIT_URL", "")

    if not api_key or not api_secret:
        return {"token": "demo-token", "room": room, "url": livekit_url}

    if not LIVEKIT_AVAILABLE:
        raise HTTPException(status_code=500, detail="LiveKit SDK not installed")

    token = lk_api.AccessToken(api_key, api_secret)
    token.with_identity(f"patient-{patient_id}")
    token.with_grants(lk_api.VideoGrants(
        room_join=True,
        room=room,
    ))

    return {"token": token.to_jwt(), "room": room, "url": livekit_url}


@router.post("/sip/setup")
async def setup_sip_trunk():
    """One-time: Register Twilio SIP trunk with LiveKit Cloud."""
    livekit_url = os.getenv("LIVEKIT_URL", "")
    api_key = os.getenv("LIVEKIT_API_KEY", "")
    api_secret = os.getenv("LIVEKIT_API_SECRET", "")
    sip_uri = os.getenv("SIP_TRUNK_URI", "")
    sip_user = os.getenv("SIP_TRUNK_USERNAME", "")
    sip_pass = os.getenv("SIP_TRUNK_PASSWORD", "")
    caller_id = os.getenv("SIP_TRUNK_CALLER_ID", "")

    if not all([livekit_url, api_key, api_secret, sip_uri]):
        raise HTTPException(
            status_code=400,
            detail="Missing required env vars: LIVEKIT_URL, API_KEY, API_SECRET, SIP_TRUNK_URI",
        )

    if not LIVEKIT_AVAILABLE:
        raise HTTPException(status_code=500, detail="LiveKit SDK not installed")

    lkapi = lk_api.LiveKitAPI(livekit_url, api_key, api_secret)
    try:
        trunk = await lkapi.sip.create_sip_outbound_trunk(
            lk_api.CreateSIPOutboundTrunkRequest(
                trunk=lk_api.SIPOutboundTrunkInfo(
                    name="twilio-swadhikaar",
                    address=sip_uri,
                    numbers=[caller_id] if caller_id else [],
                    auth_username=sip_user,
                    auth_password=sip_pass,
                )
            )
        )
        return {
            "trunk_id": trunk.sip_trunk_id,
            "status": "created",
            "message": f"Save this trunk_id as SIP_TRUNK_ID in your .env: {trunk.sip_trunk_id}",
        }
    finally:
        await lkapi.aclose()
