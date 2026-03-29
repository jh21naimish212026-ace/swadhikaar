from fastapi import APIRouter, HTTPException
from typing import Optional

from services.supabase_service import get_supabase_client

router = APIRouter(prefix="/api/patients", tags=["patients"])


@router.get("/")
async def list_patients(
    camp_type: Optional[str] = None, risk_level: Optional[str] = None
):
    """List patients with optional filters"""
    supabase = get_supabase_client()
    if supabase is None:
        return {"patients": [], "count": 0, "mode": "demo"}

    try:
        query = supabase.table("patients").select("*").order("created_at", desc=True)
        if camp_type:
            query = query.eq("camp_type", camp_type)
        if risk_level:
            query = query.eq("risk_level", risk_level)
        res = query.execute()
        rows = res.data or []
        return {"patients": rows, "count": len(rows)}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to list patients: {exc}")


@router.get("/{patient_id}")
async def get_patient(patient_id: str):
    """Get patient details with vitals and risk assessment"""
    supabase = get_supabase_client()
    if supabase is None:
        return {"patient": None, "mode": "demo"}

    try:
        patient_res = (
            supabase.table("patients")
            .select("*")
            .eq("id", patient_id)
            .limit(1)
            .execute()
        )
        patient = patient_res.data[0] if patient_res.data else None
        if patient is None:
            return {"patient": None}

        vitals = (
            supabase.table("health_vitals")
            .select("*")
            .eq("patient_id", patient_id)
            .order("recorded_at", desc=True)
            .limit(1)
            .execute()
            .data
        )
        risk = (
            supabase.table("risk_assessments")
            .select("*")
            .eq("patient_id", patient_id)
            .order("assessed_at", desc=True)
            .limit(1)
            .execute()
            .data
        )
        patient["latest_vitals"] = vitals[0] if vitals else None
        patient["latest_risk"] = risk[0] if risk else None
        return {"patient": patient}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to fetch patient: {exc}")


@router.get("/{patient_id}/vitals")
async def get_vitals(patient_id: str):
    """Get patient vital history"""
    supabase = get_supabase_client()
    if supabase is None:
        return {"vitals": [], "mode": "demo"}

    try:
        res = (
            supabase.table("health_vitals")
            .select("*")
            .eq("patient_id", patient_id)
            .order("recorded_at", desc=True)
            .execute()
        )
        rows = res.data or []
        return {"vitals": rows}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to fetch vitals: {exc}")


@router.get("/{patient_id}/calls")
async def get_calls(patient_id: str):
    """Get patient call history"""
    supabase = get_supabase_client()
    if supabase is None:
        return {"calls": [], "mode": "demo"}

    try:
        res = (
            supabase.table("voice_calls")
            .select("*")
            .eq("patient_id", patient_id)
            .order("created_at", desc=True)
            .execute()
        )
        rows = res.data or []
        return {"calls": rows}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to fetch calls: {exc}")
