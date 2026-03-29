from datetime import datetime, timezone
import re

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List

from services.triage_service import assess_triage
from services.supabase_service import get_supabase_client

router = APIRouter(prefix="/api/triage", tags=["triage"])

UUID_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$",
    re.IGNORECASE,
)


class TriageRequest(BaseModel):
    patient_id: str
    call_id: Optional[str] = None
    symptoms: List[str] = []
    vitals: Optional[dict] = None
    medications_missed: int = 0
    patient_risk_level: str = "Moderate"
    patient_age: Optional[int] = None
    call_transcript: str = ""


class EscalationResult(BaseModel):
    severity: str
    severity_level: str
    reason: str
    recommended_action: str
    needs_escalation: bool
    response_target: str
    matched_triggers: List[str]


@router.post("/assess", response_model=EscalationResult)
async def assess(request: TriageRequest):
    """Assess patient triage level based on symptoms and vitals."""
    result = assess_triage(
        symptoms=request.symptoms,
        vitals=request.vitals,
        medications_missed=request.medications_missed,
        patient_risk_level=request.patient_risk_level,
        patient_age=request.patient_age,
        call_transcript=request.call_transcript,
    )
    return result


@router.post("/escalate")
async def create_escalation(patient_id: str, call_id: str, severity: str, reason: str):
    """Create a new escalation alert."""
    supabase = get_supabase_client()
    if supabase is None:
        return {"escalation_id": "demo", "status": "open", "mode": "demo"}

    severity_up = severity.upper()
    severity_level = (
        "3" if severity_up == "CRITICAL" else "2" if severity_up == "HIGH" else "1"
    )

    payload = {
        "patient_id": patient_id,
        "call_id": call_id if UUID_RE.match(call_id or "") else None,
        "severity": severity_up,
        "severity_level": severity_level,
        "reason": reason,
        "status": "open",
    }

    try:
        res = supabase.table("escalations").insert(payload).execute()
        row = res.data[0] if res.data else None
        return {"escalation_id": row.get("id") if row else None, "status": "open"}
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail=f"Failed to create escalation: {exc}"
        )


@router.get("/escalations")
async def list_escalations(
    status: Optional[str] = "open", severity: Optional[str] = None
):
    """List escalations with optional filters."""
    supabase = get_supabase_client()
    if supabase is None:
        return {"escalations": [], "count": 0, "mode": "demo"}

    try:
        query = supabase.table("escalations").select("*").order("created_at", desc=True)
        if status:
            query = query.eq("status", status)
        if severity:
            query = query.eq("severity", severity.upper())
        res = query.execute()
        rows = res.data or []
        return {"escalations": rows, "count": len(rows)}
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail=f"Failed to list escalations: {exc}"
        )


@router.post("/escalations/{escalation_id}/resolve")
async def resolve_escalation(escalation_id: str, notes: str = ""):
    """Resolve an escalation."""
    supabase = get_supabase_client()
    if supabase is None:
        return {"escalation_id": escalation_id, "status": "resolved", "mode": "demo"}

    try:
        supabase.table("escalations").update(
            {
                "status": "resolved",
                "resolution_notes": notes or None,
                "resolved_at": datetime.now(timezone.utc).isoformat(),
            }
        ).eq("id", escalation_id).execute()
        return {"escalation_id": escalation_id, "status": "resolved"}
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail=f"Failed to resolve escalation: {exc}"
        )
