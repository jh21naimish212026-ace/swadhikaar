"""
FHIR R4 Resource Generator for Swadhikaar
Generates ABDM-compliant FHIR bundles from voice call extractions.

Supported ABDM Profiles:
- OPD Consultation Note
- Diagnostic Report Bundle
- Prescription Bundle
- Health Document Record
- AllergyIntolerance
"""

import uuid
from datetime import datetime, timezone
from typing import Optional

from fhir.resources.patient import Patient
from fhir.resources.observation import Observation
from fhir.resources.condition import Condition
from fhir.resources.encounter import Encounter
from fhir.resources.bundle import Bundle, BundleEntry
from fhir.resources.medicationstatement import MedicationStatement
from fhir.resources.allergyintolerance import AllergyIntolerance
from fhir.resources.diagnosticreport import DiagnosticReport
from fhir.resources.composition import Composition, CompositionSection
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.codeablereference import CodeableReference
from fhir.resources.coding import Coding
from fhir.resources.reference import Reference
from fhir.resources.narrative import Narrative
from fhir.resources.humanname import HumanName
from fhir.resources.identifier import Identifier


# SNOMED CT code mappings for common symptoms
SNOMED_SYMPTOMS = {
    "headache": ("25064002", "Headache"),
    "dizziness": ("404640003", "Dizziness"),
    "chest_pain": ("29857009", "Chest pain"),
    "breathlessness": ("267036007", "Breathlessness"),
    "fatigue": ("84229001", "Fatigue"),
    "palpitations": ("80313002", "Palpitations"),
    "nausea": ("422587007", "Nausea"),
    "fever": ("386661006", "Fever"),
    "cough": ("49727002", "Cough"),
    "anxiety": ("48694002", "Anxiety"),
    "insomnia": ("193462001", "Insomnia"),
    "abdominal_pain": ("21522001", "Abdominal pain"),
    "back_pain": ("161891005", "Back pain"),
    "leg_pain": ("57676002", "Leg pain"),
    "hypertension": ("38341003", "Hypertension"),
    "diabetes": ("44054006", "Diabetes mellitus"),
    "hyperglycemia": ("80394007", "Hyperglycemia"),
    "medication_nonadherence": ("129834002", "Non-adherence to medication"),
}

# SNOMED CT codes for medications (brand → INN → SNOMED)
SNOMED_MEDICATIONS = {
    "paracetamol": ("387517004", "Paracetamol"),
    "crocin": ("387517004", "Paracetamol"),
    "dolo": ("387517004", "Paracetamol"),
    "ibuprofen": ("387207008", "Ibuprofen"),
    "combiflam": ("387207008", "Ibuprofen+Paracetamol"),
    "metformin": ("372567009", "Metformin"),
    "glycomet": ("372567009", "Metformin"),
    "amlodipine": ("386864001", "Amlodipine"),
    "amlong": ("386864001", "Amlodipine"),
    "atenolol": ("387506000", "Atenolol"),
    "telmisartan": ("387069000", "Telmisartan"),
    "telma": ("387069000", "Telmisartan"),
    "aspirin": ("387458008", "Aspirin"),
    "ecosprin": ("387458008", "Aspirin"),
    "azithromycin": ("396001008", "Azithromycin"),
    "amoxicillin": ("372687004", "Amoxicillin"),
    "augmentin": ("96068000", "Amoxicillin+Clavulanate"),
    "pantoprazole": ("395821003", "Pantoprazole"),
    "atorvastatin": ("373444002", "Atorvastatin"),
    "atorva": ("373444002", "Atorvastatin"),
    "glimepiride": ("386966003", "Glimepiride"),
    "amaryl": ("386966003", "Glimepiride"),
    "losartan": ("373567002", "Losartan"),
    "losar": ("373567002", "Losartan"),
    "cetirizine": ("372523007", "Cetirizine"),
    "insulin_glargine": ("411529005", "Insulin Glargine"),
    "lantus": ("411529005", "Insulin Glargine"),
}

# LOINC codes for vitals
LOINC_VITALS = {
    "blood_pressure": ("85354-9", "Blood pressure panel"),
    "systolic_bp": ("8480-6", "Systolic blood pressure"),
    "diastolic_bp": ("8462-4", "Diastolic blood pressure"),
    "heart_rate": ("8867-4", "Heart rate"),
    "respiratory_rate": ("9279-1", "Respiratory rate"),
    "oxygen_saturation": ("59408-5", "Oxygen saturation"),
    "temperature": ("8310-5", "Body temperature"),
    "blood_glucose": ("15074-8", "Glucose [Moles/volume] in Blood"),
    "body_weight": ("29463-7", "Body weight"),
    "body_height": ("8302-2", "Body height"),
    "bmi": ("39156-5", "Body mass index"),
}


def _uuid() -> str:
    return str(uuid.uuid4())


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class FHIRGenerator:
    """Generates FHIR R4 resources from extracted voice call data."""

    def create_patient_resource(
        self,
        patient_id: str,
        name: str,
        abha_id: str = "",
        phone: str = "",
        language: str = "hi",
    ) -> Patient:
        """Create a FHIR Patient resource."""
        name_parts = name.split(" ", 1)
        family_name = name_parts[1] if len(name_parts) > 1 else None
        patient = Patient(
            id=patient_id,
            identifier=[
                Identifier(system="https://healthid.abdm.gov.in", value=abha_id)
            ] if abha_id else [],
            name=[HumanName(
                given=[name_parts[0]],
                family=family_name,
                text=name,
            )],
            language=language,
        )
        return patient

    def create_vitals_observations(
        self,
        patient_id: str,
        vitals: dict,
    ) -> list[Observation]:
        """Create FHIR Observation resources for vital signs."""
        observations = []
        patient_ref = Reference(reference=f"Patient/{patient_id}")

        vital_mappings = {
            "systolic_bp": ("8480-6", "Systolic blood pressure", "mm[Hg]"),
            "diastolic_bp": ("8462-4", "Diastolic blood pressure", "mm[Hg]"),
            "heart_rate": ("8867-4", "Heart rate", "/min"),
            "respiratory_rate": ("9279-1", "Respiratory rate", "/min"),
            "oxygen_saturation": ("59408-5", "Oxygen saturation", "%"),
            "temperature": ("8310-5", "Body temperature", "degF"),
            "blood_glucose": ("15074-8", "Blood glucose", "mg/dL"),
            "bmi": ("39156-5", "BMI", "kg/m2"),
        }

        for key, (loinc_code, display, unit) in vital_mappings.items():
            value = vitals.get(key)
            if value is not None:
                obs = Observation(
                    id=_uuid(),
                    status="final",
                    code=CodeableConcept(coding=[
                        Coding(system="http://loinc.org", code=loinc_code, display=display)
                    ]),
                    subject=patient_ref,
                    valueQuantity={"value": float(value), "unit": unit, "system": "http://unitsofmeasure.org", "code": unit},
                    effectiveDateTime=_now_iso(),
                )
                observations.append(obs)

        return observations

    def create_condition(
        self,
        patient_id: str,
        symptom_key: str,
        clinical_status: str = "active",
    ) -> Optional[Condition]:
        """Create a FHIR Condition resource for a symptom/diagnosis."""
        snomed = SNOMED_SYMPTOMS.get(symptom_key.lower())
        if not snomed:
            return None

        code, display = snomed
        patient_ref = Reference(reference=f"Patient/{patient_id}")

        condition = Condition(
            id=_uuid(),
            clinicalStatus=CodeableConcept(coding=[
                Coding(system="http://terminology.hl7.org/CodeSystem/condition-clinical", code=clinical_status)
            ]),
            code=CodeableConcept(coding=[
                Coding(system="http://snomed.info/sct", code=code, display=display)
            ], text=display),
            subject=patient_ref,
            recordedDate=_now_iso(),
        )
        return condition

    def create_medication_statement(
        self,
        patient_id: str,
        medication_name: str,
        status: str = "active",
    ) -> Optional[MedicationStatement]:
        """Create a FHIR MedicationStatement from medication name (handles brand→INN mapping)."""
        med_key = medication_name.lower().replace(" ", "_").replace("-", "_")
        snomed = SNOMED_MEDICATIONS.get(med_key)

        if not snomed:
            # Try partial match
            for key, val in SNOMED_MEDICATIONS.items():
                if key in med_key or med_key in key:
                    snomed = val
                    break

        code_concept = CodeableConcept(text=medication_name)
        if snomed:
            sct_code, sct_display = snomed
            code_concept = CodeableConcept(
                coding=[Coding(system="http://snomed.info/sct", code=sct_code, display=sct_display)],
                text=f"{medication_name} ({sct_display})",
            )

        patient_ref = Reference(reference=f"Patient/{patient_id}")
        med_stmt = MedicationStatement(
            id=_uuid(),
            status="recorded",
            medication=CodeableReference(concept=code_concept),
            subject=patient_ref,
            dateAsserted=_now_iso(),
        )
        return med_stmt

    def create_allergy_intolerance(
        self,
        patient_id: str,
        substance_name: str,
        reaction_description: str = "",
    ) -> AllergyIntolerance:
        """Create a FHIR AllergyIntolerance resource."""
        substance_key = substance_name.lower().replace(" ", "_")
        snomed = SNOMED_MEDICATIONS.get(substance_key)

        code_concept = CodeableConcept(text=substance_name)
        if snomed:
            sct_code, sct_display = snomed
            code_concept = CodeableConcept(
                coding=[Coding(system="http://snomed.info/sct", code=sct_code, display=sct_display)],
                text=substance_name,
            )

        patient_ref = Reference(reference=f"Patient/{patient_id}")
        allergy = AllergyIntolerance(
            id=_uuid(),
            clinicalStatus=CodeableConcept(coding=[
                Coding(system="http://terminology.hl7.org/CodeSystem/allergyintolerance-clinical", code="active")
            ]),
            type=CodeableConcept(coding=[
                Coding(system="http://terminology.hl7.org/CodeSystem/allergy-intolerance-type", code="allergy")
            ]),
            code=code_concept,
            patient=patient_ref,
            recordedDate=_now_iso(),
        )
        return allergy

    def create_encounter(
        self,
        patient_id: str,
        call_id: str,
        call_type: str = "follow_up",
    ) -> Encounter:
        """Create a FHIR Encounter for a voice call."""
        patient_ref = Reference(reference=f"Patient/{patient_id}")
        encounter = Encounter(
            id=_uuid(),
            status="completed",
            class_fhir=[CodeableConcept(coding=[
                Coding(system="http://terminology.hl7.org/CodeSystem/v3-ActCode", code="VR", display="Virtual")
            ])],
            type=[CodeableConcept(coding=[
                Coding(system="http://snomed.info/sct", code="185317003", display="Telephone encounter")
            ], text=f"Voice AI {call_type}")],
            subject=patient_ref,
        )
        return encounter

    def create_opd_consultation_bundle(
        self,
        patient_id: str,
        patient_name: str,
        abha_id: str,
        call_id: str,
        call_type: str,
        extracted_data: dict,
    ) -> dict:
        """
        Create a complete OPD Consultation Note bundle.

        extracted_data format:
        {
            "symptoms": ["headache", "dizziness"],
            "medications": ["Crocin", "Telma"],
            "allergies": ["Amoxicillin"],
            "vitals": {"systolic_bp": 140, "diastolic_bp": 90, ...},
            "severity": "HIGH",
        }
        """
        entries = []
        snomed_codes = []
        loinc_codes = []

        # Patient
        patient = self.create_patient_resource(patient_id, patient_name, abha_id)
        entries.append(BundleEntry(resource=patient, fullUrl=f"urn:uuid:{patient_id}"))

        # Encounter
        encounter = self.create_encounter(patient_id, call_id, call_type)
        entries.append(BundleEntry(resource=encounter, fullUrl=f"urn:uuid:{encounter.id}"))

        # Vitals → Observations
        vitals = extracted_data.get("vitals", {})
        for obs in self.create_vitals_observations(patient_id, vitals):
            entries.append(BundleEntry(resource=obs, fullUrl=f"urn:uuid:{obs.id}"))
            if obs.code and obs.code.coding:
                loinc_codes.append(obs.code.coding[0].code)

        # Symptoms → Conditions
        for symptom in extracted_data.get("symptoms", []):
            condition = self.create_condition(patient_id, symptom)
            if condition:
                entries.append(BundleEntry(resource=condition, fullUrl=f"urn:uuid:{condition.id}"))
                if condition.code and condition.code.coding:
                    snomed_codes.append(condition.code.coding[0].code)

        # Medications → MedicationStatements
        for med in extracted_data.get("medications", []):
            med_stmt = self.create_medication_statement(patient_id, med)
            if med_stmt:
                entries.append(BundleEntry(resource=med_stmt, fullUrl=f"urn:uuid:{med_stmt.id}"))
                if med_stmt.medication and med_stmt.medication.concept and med_stmt.medication.concept.coding:
                    snomed_codes.append(med_stmt.medication.concept.coding[0].code)

        # Allergies → AllergyIntolerance
        for allergy in extracted_data.get("allergies", []):
            ai = self.create_allergy_intolerance(patient_id, allergy)
            entries.append(BundleEntry(resource=ai, fullUrl=f"urn:uuid:{ai.id}"))
            if ai.code and ai.code.coding:
                snomed_codes.append(ai.code.coding[0].code)

        # Create Bundle
        bundle = Bundle(
            id=_uuid(),
            type="document",
            timestamp=_now_iso(),
            entry=entries,
        )

        return {
            "fhir_json": bundle.model_dump(exclude_none=True),
            "profile": "opd_consultation_note",
            "snomed_codes": list(set(snomed_codes)),
            "loinc_codes": list(set(loinc_codes)),
            "resource_count": len(entries),
        }

    def create_diagnostic_report_bundle(
        self,
        patient_id: str,
        patient_name: str,
        abha_id: str,
        report_data: dict,
    ) -> dict:
        """
        Create a Diagnostic Report Bundle.

        report_data format:
        {
            "report_name": "Blood Sugar Panel",
            "observations": [
                {"key": "blood_glucose", "value": 126, "unit": "mg/dL"},
            ],
        }
        """
        entries = []
        loinc_codes = []
        observation_refs = []

        # Patient
        patient = self.create_patient_resource(patient_id, patient_name, abha_id)
        entries.append(BundleEntry(resource=patient, fullUrl=f"urn:uuid:{patient_id}"))

        patient_ref = Reference(reference=f"Patient/{patient_id}")

        # Observations
        for obs_data in report_data.get("observations", []):
            key = obs_data.get("key", "")
            value = obs_data.get("value")
            unit = obs_data.get("unit", "")

            loinc_entry = LOINC_VITALS.get(key)
            if loinc_entry and value is not None:
                loinc_code, display = loinc_entry
                obs = Observation(
                    id=_uuid(),
                    status="final",
                    code=CodeableConcept(coding=[
                        Coding(system="http://loinc.org", code=loinc_code, display=display)
                    ]),
                    subject=patient_ref,
                    valueQuantity={"value": float(value), "unit": unit, "system": "http://unitsofmeasure.org", "code": unit},
                    effectiveDateTime=_now_iso(),
                )
                entries.append(BundleEntry(resource=obs, fullUrl=f"urn:uuid:{obs.id}"))
                loinc_codes.append(loinc_code)
                observation_refs.append(Reference(reference=f"Observation/{obs.id}"))

        # DiagnosticReport
        report_name = report_data.get("report_name", "Diagnostic Report")
        dr = DiagnosticReport(
            id=_uuid(),
            status="final",
            code=CodeableConcept(text=report_name),
            subject=patient_ref,
            effectiveDateTime=_now_iso(),
            result=observation_refs if observation_refs else None,
        )
        entries.append(BundleEntry(resource=dr, fullUrl=f"urn:uuid:{dr.id}"))

        bundle = Bundle(
            id=_uuid(),
            type="document",
            timestamp=_now_iso(),
            entry=entries,
        )

        return {
            "fhir_json": bundle.model_dump(exclude_none=True),
            "profile": "diagnostic_report_bundle",
            "loinc_codes": list(set(loinc_codes)),
            "resource_count": len(entries),
        }

    def create_prescription_bundle(
        self,
        patient_id: str,
        patient_name: str,
        abha_id: str,
        medications: list[str],
    ) -> dict:
        """
        Create a Prescription Bundle (MedicationStatement list).

        medications: list of drug names (brand or INN), e.g. ["Crocin", "Telma 40"]
        """
        entries = []
        snomed_codes = []

        # Patient
        patient = self.create_patient_resource(patient_id, patient_name, abha_id)
        entries.append(BundleEntry(resource=patient, fullUrl=f"urn:uuid:{patient_id}"))

        for med in medications:
            med_stmt = self.create_medication_statement(patient_id, med)
            if med_stmt:
                entries.append(BundleEntry(resource=med_stmt, fullUrl=f"urn:uuid:{med_stmt.id}"))
                if med_stmt.medication and med_stmt.medication.concept and med_stmt.medication.concept.coding:
                    snomed_codes.append(med_stmt.medication.concept.coding[0].code)

        bundle = Bundle(
            id=_uuid(),
            type="document",
            timestamp=_now_iso(),
            entry=entries,
        )

        return {
            "fhir_json": bundle.model_dump(exclude_none=True),
            "profile": "prescription_bundle",
            "snomed_codes": list(set(snomed_codes)),
            "resource_count": len(entries),
        }

    def create_health_document_record(
        self,
        patient_id: str,
        patient_name: str,
        abha_id: str,
        call_id: str,
        title: str,
        summary_text: str,
        section_entries: list[dict],
    ) -> dict:
        """
        Create a Health Document Record (Composition resource in a Bundle).

        section_entries: list of dicts with keys "title" and "text"
        """
        entries = []

        # Patient
        patient = self.create_patient_resource(patient_id, patient_name, abha_id)
        entries.append(BundleEntry(resource=patient, fullUrl=f"urn:uuid:{patient_id}"))

        patient_ref = Reference(reference=f"Patient/{patient_id}")

        # Build sections
        sections = []
        for sec in section_entries:
            sections.append(CompositionSection(
                title=sec.get("title", "Section"),
                text=Narrative(status="generated", div=f"<div xmlns='http://www.w3.org/1999/xhtml'>{sec.get('text', '')}</div>"),
            ))

        composition = Composition(
            id=_uuid(),
            status="final",
            type=CodeableConcept(coding=[
                Coding(system="http://loinc.org", code="34117-2", display="History and physical note")
            ], text=title),
            subject=patient_ref,
            date=_now_iso(),
            author=[Reference(reference=f"Device/voice-ai-{call_id}")],
            title=title,
            text=Narrative(
                status="generated",
                div=f"<div xmlns='http://www.w3.org/1999/xhtml'>{summary_text}</div>",
            ),
            section=sections if sections else None,
        )
        entries.append(BundleEntry(resource=composition, fullUrl=f"urn:uuid:{composition.id}"))

        bundle = Bundle(
            id=_uuid(),
            type="document",
            timestamp=_now_iso(),
            entry=entries,
        )

        return {
            "fhir_json": bundle.model_dump(exclude_none=True),
            "profile": "health_document_record",
            "resource_count": len(entries),
        }


# Module-level singleton
fhir_generator = FHIRGenerator()
