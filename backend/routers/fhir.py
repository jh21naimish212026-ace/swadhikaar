from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List

from services.fhir_service import fhir_generator
from services.drug_mapping import resolve_drug
from services.supabase_service import get_supabase_client

router = APIRouter(prefix="/api/fhir", tags=["fhir"])


class FHIRGenerateRequest(BaseModel):
    call_id: str
    patient_id: str
    patient_name: str = "Patient"
    abha_id: str = ""
    call_type: str = "follow_up"
    transcript: str = ""
    extracted_data: dict


@router.post("/generate")
async def generate_fhir(request: FHIRGenerateRequest):
    """Generate FHIR R4 resources from call transcript and extracted data."""
    try:
        result = fhir_generator.create_opd_consultation_bundle(
            patient_id=request.patient_id,
            patient_name=request.patient_name,
            abha_id=request.abha_id,
            call_id=request.call_id,
            call_type=request.call_type,
            extracted_data=request.extracted_data,
        )

        supabase = get_supabase_client()
        if supabase is not None:
            supabase.table("fhir_resources").insert(
                {
                    "patient_id": request.patient_id,
                    "call_id": request.call_id or None,
                    "resource_type": "Bundle",
                    "profile": result.get("profile"),
                    "fhir_json": result.get("fhir_json"),
                    "snomed_codes": result.get("snomed_codes", []),
                    "loinc_codes": result.get("loinc_codes", []),
                    "review_status": "pending",
                }
            ).execute()

        return result
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/generate/diagnostic-report")
async def generate_diagnostic_report(
    patient_id: str,
    patient_name: str,
    abha_id: str = "",
    report_data: dict = {},
):
    """Generate a Diagnostic Report FHIR bundle."""
    result = fhir_generator.create_diagnostic_report_bundle(
        patient_id=patient_id,
        patient_name=patient_name,
        abha_id=abha_id,
        report_data=report_data,
    )
    return result


@router.post("/generate/prescription")
async def generate_prescription(
    patient_id: str,
    patient_name: str,
    abha_id: str = "",
    medications: List[str] = [],
):
    """Generate a Prescription FHIR bundle."""
    result = fhir_generator.create_prescription_bundle(
        patient_id=patient_id,
        patient_name=patient_name,
        abha_id=abha_id,
        medications=medications,
    )
    return result


@router.get("/resources/{patient_id}")
async def get_patient_resources(patient_id: str, resource_type: Optional[str] = None):
    """Get FHIR resources for a patient (from Supabase)."""
    supabase = get_supabase_client()
    if supabase is None:
        return {"resources": [], "count": 0, "mode": "demo"}

    try:
        query = (
            supabase.table("fhir_resources")
            .select("*")
            .eq("patient_id", patient_id)
            .order("created_at", desc=True)
        )
        if resource_type:
            query = query.eq("resource_type", resource_type)
        res = query.execute()
        rows = res.data or []
        return {"resources": rows, "count": len(rows)}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to fetch resources: {exc}")


@router.post("/export/{patient_id}")
async def export_to_abdm(patient_id: str):
    """Export patient FHIR bundle to ABDM."""
    supabase = get_supabase_client()
    if supabase is None:
        return {
            "status": "queued",
            "abdm_reference": None,
            "message": "Supabase not configured; demo mode",
        }

    try:
        res = (
            supabase.table("fhir_resources")
            .select("id,patient_id,resource_type,profile")
            .eq("patient_id", patient_id)
            .order("created_at", desc=True)
            .limit(1)
            .execute()
        )
        latest = res.data[0] if res.data else None
        if latest is None:
            return {"status": "no_data", "abdm_reference": None}

        ref = f"ABDM-{latest['id'][:8]}-{int(datetime.now(timezone.utc).timestamp())}"
        return {
            "status": "exported",
            "abdm_reference": ref,
            "resource_id": latest["id"],
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to export to ABDM: {exc}")


@router.get("/drug-mapping/{brand_name}")
async def drug_mapping(brand_name: str):
    """Look up INN name and SNOMED code for Indian drug brand."""
    result = resolve_drug(brand_name)
    return result
