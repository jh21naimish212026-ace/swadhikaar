"""Risk prediction API endpoint."""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from services.risk_model import predict_risk

router = APIRouter(prefix="/api/risk", tags=["risk"])


class RiskPredictionRequest(BaseModel):
    systolic_bp: Optional[int] = None
    diastolic_bp: Optional[int] = None
    heart_rate: Optional[int] = None
    respiratory_rate: Optional[int] = None
    oxygen_saturation: Optional[int] = None
    blood_glucose: Optional[int] = None
    bmi: Optional[float] = None
    waist_circumference: Optional[float] = None
    perfusion_index: Optional[float] = None
    waist_to_height_ratio: Optional[float] = None
    chest_discomfort: Optional[str] = "none"
    breathlessness: Optional[str] = "none"
    palpitations: Optional[str] = "none"
    fatigue_weakness: Optional[str] = "normal"
    dizziness_blackouts: Optional[str] = "never"
    sleep_duration: Optional[str] = ">7"
    stress_anxiety: Optional[str] = "calm"
    physical_inactivity: Optional[str] = "active"
    diet_quality: Optional[str] = "balanced"
    family_history: Optional[str] = "none"


@router.post("/predict")
async def predict(request: RiskPredictionRequest):
    """Predict cardiovascular, diabetic, and hypertension risk scores."""
    data = request.model_dump()
    result = predict_risk(data)
    return result
