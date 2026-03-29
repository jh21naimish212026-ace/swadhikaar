"""
Swadhikaar Triage Engine
Multi-layer healthcare triage for voice AI escalation.

Severity Levels:
- CRITICAL (Level 1): Immediate response < 5 minutes
  → Chest pain, severe breathlessness, fainting, stroke symptoms

- HIGH (Level 2): Response < 1 hour
  → BP spike (>180/120), blood glucose >300, persistent vomiting, severe headache

- MODERATE (Level 3): Response < 24 hours
  → Missed medications 3+ days, worsening symptoms, abnormal vitals

- LOW: Next scheduled follow-up
  → Mild symptoms, stable vitals, medication questions
"""

import logging
from typing import Optional
from datetime import datetime, timezone

logger = logging.getLogger("triage")


# Critical symptom keywords (Hindi + English)
CRITICAL_KEYWORDS = {
    "chest_pain", "chest pain", "seene mein dard", "chhaati mein dard",
    "severe_breathlessness", "saans nahi aa rahi", "saans lene mein bahut mushkil",
    "fainting", "behosh", "gir gaya", "gir gayi",
    "stroke", "haath pair chal nahi rahe", "bolne mein dikkat",
    "seizure", "daure", "fits",
    "unconscious", "hosh nahi",
    "severe_bleeding", "khoon beh raha hai",
    "heart_attack", "dil ka daura",
}

HIGH_KEYWORDS = {
    "persistent_headache", "lagaatar sir dard", "bohut dard",
    "severe_dizziness", "bahut chakkar", "aankhon ke aage andhera",
    "high_bp", "bp bahut zyada",
    "high_sugar", "sugar bahut zyada", "blood glucose high",
    "missed_medication", "dawai nahi li", "dawai bhool gaya",
    "vomiting", "ulti", "bar bar ulti",
    "chest_discomfort", "seene mein taklif",
    "palpitations", "dil bahut tez dhadak raha",
    "difficulty_breathing", "saans mein taklif",
}

MODERATE_KEYWORDS = {
    "headache", "sir dard",
    "mild_dizziness", "thoda chakkar",
    "fatigue", "thakan", "kamzori",
    "mild_pain", "thoda dard",
    "poor_sleep", "neend nahi aati",
    "anxiety", "ghabrahat", "tension",
    "cold", "sardi", "khaansi",
    "appetite_loss", "bhookh nahi lagti",
}


class TriageAssessment:
    """Result of a triage assessment."""

    def __init__(
        self,
        severity: str,
        severity_level: str,
        reason: str,
        recommended_action: str,
        needs_escalation: bool,
        response_target: str,
        matched_triggers: list[str],
    ):
        self.severity = severity
        self.severity_level = severity_level
        self.reason = reason
        self.recommended_action = recommended_action
        self.needs_escalation = needs_escalation
        self.response_target = response_target
        self.matched_triggers = matched_triggers

    def to_dict(self) -> dict:
        return {
            "severity": self.severity,
            "severity_level": self.severity_level,
            "reason": self.reason,
            "recommended_action": self.recommended_action,
            "needs_escalation": self.needs_escalation,
            "response_target": self.response_target,
            "matched_triggers": self.matched_triggers,
        }


class TriageEngine:
    """Multi-layer triage engine for patient escalation."""

    def assess(
        self,
        symptoms: list[str],
        vitals: Optional[dict] = None,
        medications_missed: int = 0,
        patient_risk_level: str = "Moderate",
        patient_age: Optional[int] = None,
        call_transcript: str = "",
    ) -> TriageAssessment:
        """
        Assess triage level based on symptoms, vitals, and context.

        Args:
            symptoms: List of symptom strings (can be English keys or Hindi text)
            vitals: Dict with keys like systolic_bp, diastolic_bp, blood_glucose, etc.
            medications_missed: Number of days medications were missed
            patient_risk_level: Patient's baseline risk (Low, Moderate, High)
            patient_age: Patient age (elderly patients get elevated severity)
            call_transcript: Raw transcript text for keyword detection
        """
        matched_triggers = []
        vitals = vitals or {}

        # === Check for CRITICAL symptoms ===
        critical_matches = self._check_keywords(symptoms, call_transcript, CRITICAL_KEYWORDS)
        if critical_matches:
            matched_triggers.extend(critical_matches)
            return TriageAssessment(
                severity="CRITICAL",
                severity_level="LEVEL_1",
                reason=f"Critical symptoms detected: {', '.join(critical_matches)}",
                recommended_action="Immediate doctor notification. Patient advised to visit ER / call emergency services.",
                needs_escalation=True,
                response_target="< 5 minutes",
                matched_triggers=matched_triggers,
            )

        # === Check critical vitals ===
        vitals_critical = self._check_critical_vitals(vitals)
        if vitals_critical:
            matched_triggers.extend(vitals_critical)
            return TriageAssessment(
                severity="CRITICAL",
                severity_level="LEVEL_1",
                reason=f"Critical vital signs: {', '.join(vitals_critical)}",
                recommended_action="Immediate medical attention required. Alert assigned doctor.",
                needs_escalation=True,
                response_target="< 5 minutes",
                matched_triggers=matched_triggers,
            )

        # === Check for HIGH symptoms ===
        high_matches = self._check_keywords(symptoms, call_transcript, HIGH_KEYWORDS)

        # Vitals that indicate HIGH severity
        vitals_high = self._check_high_vitals(vitals)
        if vitals_high:
            high_matches.extend(vitals_high)

        # Medication non-adherence
        if medications_missed >= 3:
            high_matches.append(f"medication_missed_{medications_missed}_days")

        # Elderly patients with HIGH baseline risk get elevated
        if patient_age and patient_age >= 65 and patient_risk_level == "High":
            high_matches.append("elderly_high_risk")

        if high_matches:
            matched_triggers.extend(high_matches)
            return TriageAssessment(
                severity="HIGH",
                severity_level="LEVEL_2",
                reason=f"High severity indicators: {', '.join(high_matches)}",
                recommended_action="Alert assigned doctor within 1 hour. Schedule urgent follow-up.",
                needs_escalation=True,
                response_target="< 1 hour",
                matched_triggers=matched_triggers,
            )

        # === Check for MODERATE symptoms ===
        moderate_matches = self._check_keywords(symptoms, call_transcript, MODERATE_KEYWORDS)

        # Moderate vitals
        vitals_moderate = self._check_moderate_vitals(vitals)
        if vitals_moderate:
            moderate_matches.extend(vitals_moderate)

        # Missed medications (1-2 days)
        if 1 <= medications_missed < 3:
            moderate_matches.append(f"medication_missed_{medications_missed}_days")

        if moderate_matches:
            matched_triggers.extend(moderate_matches)
            return TriageAssessment(
                severity="MODERATE",
                severity_level="LEVEL_3",
                reason=f"Moderate concerns: {', '.join(moderate_matches)}",
                recommended_action="Schedule follow-up call within 24 hours. Add to doctor review queue.",
                needs_escalation=False,
                response_target="< 24 hours",
                matched_triggers=matched_triggers,
            )

        # === LOW / No concerns ===
        return TriageAssessment(
            severity="LOW",
            severity_level="LEVEL_3",
            reason="No significant concerns detected. Patient reports stable condition.",
            recommended_action="Continue scheduled follow-up as per workflow.",
            needs_escalation=False,
            response_target="Next scheduled call",
            matched_triggers=[],
        )

    def _check_keywords(
        self, symptoms: list[str], transcript: str, keyword_set: set
    ) -> list[str]:
        """Check symptoms and transcript against a keyword set."""
        matches = []
        transcript_lower = transcript.lower()

        for symptom in symptoms:
            symptom_lower = symptom.lower().replace(" ", "_")
            if symptom_lower in keyword_set or symptom.lower() in keyword_set:
                matches.append(symptom)

        # Also check raw transcript for Hindi keywords
        for keyword in keyword_set:
            if " " in keyword and keyword in transcript_lower:
                if keyword not in matches:
                    matches.append(keyword)

        return matches

    def _check_critical_vitals(self, vitals: dict) -> list[str]:
        """Check for life-threatening vital signs."""
        alerts = []

        systolic = vitals.get("systolic_bp")
        diastolic = vitals.get("diastolic_bp")
        if systolic and systolic > 200:
            alerts.append(f"BP_critical_{systolic}/{diastolic or '?'}")
        if diastolic and diastolic > 130:
            alerts.append(f"diastolic_critical_{diastolic}")

        glucose = vitals.get("blood_glucose")
        if glucose and glucose > 400:
            alerts.append(f"glucose_critical_{glucose}")
        if glucose and glucose < 50:
            alerts.append(f"hypoglycemia_critical_{glucose}")

        spo2 = vitals.get("oxygen_saturation")
        if spo2 and spo2 < 88:
            alerts.append(f"SpO2_critical_{spo2}")

        hr = vitals.get("heart_rate")
        if hr and (hr > 150 or hr < 40):
            alerts.append(f"heart_rate_critical_{hr}")

        temp = vitals.get("temperature")
        if temp and temp > 104:
            alerts.append(f"fever_critical_{temp}")

        return alerts

    def _check_high_vitals(self, vitals: dict) -> list[str]:
        """Check for high-severity vital signs."""
        alerts = []

        systolic = vitals.get("systolic_bp")
        diastolic = vitals.get("diastolic_bp")
        if systolic and 180 <= systolic <= 200:
            alerts.append(f"BP_high_{systolic}/{diastolic or '?'}")
        if diastolic and 110 <= diastolic <= 130:
            alerts.append(f"diastolic_high_{diastolic}")

        glucose = vitals.get("blood_glucose")
        if glucose and 300 <= glucose <= 400:
            alerts.append(f"glucose_high_{glucose}")
        if glucose and 50 <= glucose < 70:
            alerts.append(f"glucose_low_{glucose}")

        spo2 = vitals.get("oxygen_saturation")
        if spo2 and 88 <= spo2 < 92:
            alerts.append(f"SpO2_low_{spo2}")

        hr = vitals.get("heart_rate")
        if hr and (120 <= hr <= 150 or 40 <= hr < 50):
            alerts.append(f"heart_rate_abnormal_{hr}")

        return alerts

    def _check_moderate_vitals(self, vitals: dict) -> list[str]:
        """Check for moderately abnormal vital signs."""
        alerts = []

        systolic = vitals.get("systolic_bp")
        diastolic = vitals.get("diastolic_bp")
        if systolic and 140 <= systolic < 180:
            alerts.append(f"BP_elevated_{systolic}/{diastolic or '?'}")

        glucose = vitals.get("blood_glucose")
        if glucose and 200 <= glucose < 300:
            alerts.append(f"glucose_elevated_{glucose}")

        spo2 = vitals.get("oxygen_saturation")
        if spo2 and 92 <= spo2 < 95:
            alerts.append(f"SpO2_borderline_{spo2}")

        return alerts


# Convenience function
def assess_triage(
    symptoms: list[str],
    vitals: Optional[dict] = None,
    medications_missed: int = 0,
    patient_risk_level: str = "Moderate",
    patient_age: Optional[int] = None,
    call_transcript: str = "",
) -> dict:
    """Quick triage assessment — returns dict."""
    engine = TriageEngine()
    result = engine.assess(
        symptoms=symptoms,
        vitals=vitals,
        medications_missed=medications_missed,
        patient_risk_level=patient_risk_level,
        patient_age=patient_age,
        call_transcript=call_transcript,
    )
    return result.to_dict()
