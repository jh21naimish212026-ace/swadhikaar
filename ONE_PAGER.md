# Swadhikaar — Indic Voice AI Patient Engagement Platform

**PS-3 | HackMatrix 2.0 | Co-organised by Jilo Health & NJACK, IIT Patna**

---

| | |
|---|---|
| **Team Name** | Swadhikaar |
| **Team Leader** | [Your Full Name] |
| **Contact** | [Phone] · [hackathon email] |
| **Participants** | [Your Full Name] (Solo) |
| **Hackathon Email** | swadhikaar2026@gmail.com |
| **GitHub** | https://github.com/[your-username]/swadhikaar |

---

## Selected Problem Statement

**PS-3** — Build an Indic Voice AI-Driven Patient Engagement Platform for SME hospitals.

## About Solution

SME hospitals in India cannot scale patient follow-ups — staff is limited, post-visit data stays unstructured, and high-risk patients fall through the cracks. **Swadhikaar** is an AI voice engagement platform that automatically calls patients in Hindi/English, extracts structured clinical signals from natural conversation, triages by severity (LOW → CRITICAL), and surfaces actionable escalations on role-based dashboards in realtime. It covers **6 end-to-end care workflows**: Screening→OPD, OPD→IPD, Post-discharge Recovery, Chronic Disease Management, Follow-ups, and Newborn Vaccination Tracking — enabling care teams to do 10x more without additional hiring.

## Different Use of AI

| AI Layer | Type | Technology | Purpose |
|---|---|---|---|
| **Voice Conversation Agent** | API + Engineered Prompts | LiveKit Agents SDK + Gemini 2.5 Flash Native Audio | Conducts multilingual health conversations with **7 clinically-scoped prompt personas** (one per care pathway) |
| **Structured Clinical Extraction** | API | Gemini LLM in-context | Extracts symptoms, vitals, medication adherence, severity from unstructured voice into structured JSON |
| **Risk Triage Classification** | Trained Model | scikit-learn (trained on 240-patient health camp dataset) | Classifies patient risk as LOW/MODERATE/HIGH/CRITICAL using demographics + vitals + history |
| **FHIR R4 Resource Generation** | API | fhir.resources (Python) | Auto-generates ABDM-compliant FHIR bundles (OPD, Diagnostic, Prescription, Health Document) with SNOMED/LOINC coding |
| **Indic Language Pipeline** | Govt API | Bhashini (STT/TTS) | Hindi speech-to-text and text-to-speech for voice agent |

> **Key distinction:** We don't use a single generic chatbot. Each care pathway has a dedicated AI persona with clinical context, patient history injection, and structured extraction schema — making outputs medically actionable, not conversational.

## Technology Stack

```
Frontend:    Next.js 16 + React 19 + shadcn/ui + Tailwind CSS v4
Backend:     FastAPI (voice pipeline + FHIR + triage + risk APIs)
Database:    Supabase PostgreSQL (Mumbai region) — 15 tables, RLS-enabled
Voice:       LiveKit Agents SDK v1.4.4 + WebRTC (demo) / SIP-Twilio (production)
AI/LLM:      Gemini 2.5 Flash Native Audio (realtime voice)
STT/TTS:     Bhashini API (Government of India)
ML:          scikit-learn (risk prediction model)
Standards:   FHIR R4 (ABDM profiles), SNOMED CT, LOINC
Compliance:  DPDP Act 2023 — consent management, audit logs, data deletion
```

## Backend Logics and Data Structure

**Data Flow:**
```
Workflow Trigger → LiveKit Voice Call → AI Conversation → Structured Extraction
→ Supabase (voice_calls + escalations) → Realtime Dashboard → Doctor Action → FHIR Bundle
```

**Schema — 15 tables across 4 domains:**

| Domain | Tables | Purpose |
|---|---|---|
| **Clinical** | patients, vitals, symptoms, risk_scores, doctors | Patient health records and risk profiles |
| **Voice** | voice_calls, escalations | Call data, transcripts, severity-based escalation queue |
| **Compliance** | consent_records, audit_logs, fhir_resources | DPDP consent, activity audit trail, FHIR bundles |
| **Operations** | workflows, newborns, vaccination_schedules, caregivers | Automation rules, NIP vaccination tracking, caregiver linkage |

**Key patterns:** Row-Level Security (RLS) per role, Supabase Realtime subscriptions for live escalation feeds, human-in-the-loop approval (doctors Approve/Correct/Reject AI extractions).

## Solution Economics (Cost & Scalability)

| Metric | AI-Powered (Swadhikaar) | Manual (Status Quo) |
|---|---|---|
| **Cost per follow-up call** | ₹1.5 – ₹3 | ₹25 – ₹40 |
| **Monthly cost (1,000 patients)** | ~₹8,000 – ₹12,000 | ~₹2,50,000+ (5 FTEs) |
| **Patients per coordinator** | 500+ | 40–50 |
| **Scale factor** | 10x patients, same infra | Linear headcount growth |
| **Break-even** | ~200 calls/month vs 1 FTE | — |
| **Infra scaling** | Supabase + LiveKit auto-scale | Physical call center |

## Explain Solution in Workflow

```
1. TRIGGER    →  Workflow fires (scheduled follow-up / post-discharge day / vaccination due date)
2. CALL       →  Voice agent dials patient in Hindi/English via LiveKit WebRTC
3. CONVERSE   →  AI conducts context-aware health conversation using patient history
4. EXTRACT    →  Symptoms, vitals, severity extracted as structured clinical data
5. TRIAGE     →  Risk classified: LOW → log, MODERATE → flag, HIGH/CRITICAL → escalate
6. ESCALATE   →  Escalation card appears on doctor dashboard in realtime
7. ACT        →  Doctor reviews AI summary + transcript + e-Rx draft → Approve / Correct / Reject
8. RECORD     →  FHIR R4 bundle generated, audit log written, consent tracked (DPDP)
```

**6 Use Cases, One Platform:**
1. **Screening → OPD** — Health camp screening referral follow-up
2. **OPD → IPD** — Outpatient to inpatient escalation outreach
3. **Recovery Protocol** — Post-discharge monitoring (Day 1/3/7/14/30)
4. **Chronic Disease Mgmt** — Diabetes, hypertension, cardiac monthly check-ins
5. **Follow-up** — Automated outbound follow-up calls
6. **Newborn Vaccination** — NIP India schedule (0–12 months) reminders + tracking

## Demo URL

> **[Insert deployed URL here]**
>
> Test credentials: `patient@swadhikaar.in` / `patient123` · `coordinator@swadhikaar.in` / `coordinator123` · `admin@swadhikaar.in` / `admin123`

## Innovation

- **Voice-first, not chat-first** — serves low-literacy, elderly, and rural populations where text-based engagement fails
- **7 clinically-scoped AI personas** — not one generic bot, but dedicated conversation agents per care pathway with patient history context injection
- **Human-in-the-loop trust model** — AI extracts and triages; doctors decide. No blind automation in healthcare
- **DPDP Act + ABDM/FHIR native** — built for Indian regulatory reality from day one, not retrofitted
- **10x cost reduction** — ₹1.5/call vs ₹25–40 manual, enabling population-scale follow-up without call center hiring
- **Production-ready architecture** — browser WebRTC demo today, SIP/Twilio telephony bridge for real-world deployment with zero core logic changes
