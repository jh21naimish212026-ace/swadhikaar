# HackMatrix 2.0 — Swadhikaar
## Indic Voice AI-Driven Patient Engagement Platform (PS-3)
### IIT Patna | Jilo Health Hackathon

---

## Problem Summary
SME hospitals in India face unstructured data, limited workforce, and operational overload. They need automated, multilingual patient engagement that scales without hiring large teams. The platform must align with India's ABDM ecosystem and produce FHIR R4-compliant structured output.

---

## Architecture

### Project Structure
```
hackmatrix/
├── templates/
│   └── landing/              # Static landing page (pre-built template)
│       ├── index.html
│       ├── index.css
│       └── index.js
├── frontend/                 # Next.js app (dashboard, agent, workflows)
│   ├── app/
│   │   ├── (auth)/           # Login with role selection
│   │   ├── patient/          # Patient portal (read-only)
│   │   ├── doctor/           # Doctor view (action-oriented)
│   │   ├── admin/            # Admin + Care Coordinator dashboard
│   │   │   ├── dashboard/    # Reporting & analytics
│   │   │   ├── workflows/    # Workflow builder
│   │   │   ├── patients/     # Patient management
│   │   │   └── consent/      # DPDP consent manager
│   │   └── agent/            # Voice AI demo (LiveKit room)
│   └── components/
├── backend/                  # FastAPI (voice orchestration + FHIR)
│   ├── voice_agent/          # LiveKit Agents pipeline
│   │   ├── agent.py
│   │   ├── prompts/
│   │   └── plugins/
│   ├── fhir/                 # ABDM FHIR R4 mapping
│   ├── escalation/           # Triage & alert engine
│   └── services/
├── supabase/                 # Supabase config (MANDATORY backend)
│   ├── migrations/
│   ├── seed.sql
│   └── functions/            # Edge functions
├── dataset/
│   └── PS-3-Use-case-database-1.csv
├── docs/
│   ├── one-pager.md          # Deliverable: One Pager
│   ├── cost-scalability.md   # Deliverable: Cost & Scalability
│   └── ai-components.md      # Deliverable: AI Component Explanation
└── PLAN.md
```

### System Flow
```
┌─────────────────────────────────────────────────────────────┐
│            LANDING PAGE (Static HTML/CSS/JS)                 │
│   FuseHealth-style template at /                             │
│   CTAs → "Login" / "Try Voice Agent" / "Dashboard"           │
└──────────┬───────────────────────┬──────────────────────────┘
           │                       │
           ▼                       ▼
┌──────────────────────┐  ┌────────────────────────────────────┐
│  NEXT.JS APP         │  │     VOICE AI ENGINE                │
│  (Role-Based)        │  │     (LiveKit Agents + FastAPI)      │
│                      │  │                                    │
│  /patient/*          │  │  ┌────────┐ ┌───────┐ ┌────────┐  │
│  • My Health Records │  │  │  STT   │→│  LLM  │→│  TTS   │  │
│  • Call History      │  │  │Bhashini│ │Gemini │ │Bhashini│  │
│  • Upcoming Calls    │  │  └────────┘ └───┬───┘ └────────┘  │
│  • Consent Status    │  │                 │                  │
│                      │  │    Structured Data Extraction      │
│  /doctor/*           │  │         │                          │
│  • My Patients       │  │         ▼                          │
│  • Escalation Queue  │  │    FHIR R4 (ABDM Profiles)         │
│  • Call Transcripts  │  │    SNOMED/LOINC Coding             │
│  • Review & Correct  │  │                                    │
│    AI Extractions    │  │         │                          │
│                      │  │         ▼                          │
│  /admin/*            │  │    Human Review + Feedback Loop     │
│  • All Patients      │  │    (Doctor corrects → AI improves)  │
│  • Analytics         │  └──────────┬─────────────────────────┘
│  • Workflow Builder  │             │
│  • FHIR Reports      │             │
│  • Consent Manager   │             │
│  • Care Coordination │             │
└──────────┬───────────┘             │
           │                         │
           ▼                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    SUPABASE (Mandatory)                       │
│  ┌──────────┐ ┌───────────┐ ┌──────────┐ ┌──────────────┐  │
│  │   Auth   │ │ Database  │ │ Realtime │ │   Storage    │  │
│  │ (Roles)  │ │(PostgreSQL│ │(Escalation│ │(Recordings  │  │
│  │ Patient  │ │ + FHIR    │ │ Alerts)  │ │ Transcripts)│  │
│  │ Doctor   │ │ tables)   │ │          │ │              │  │
│  │ Admin    │ │           │ │          │ │              │  │
│  └──────────┘ └───────────┘ └──────────┘ └──────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Routing Strategy
| URL | Served By | Who Uses It |
|-----|-----------|-------------|
| `/` | Static HTML | Anyone (marketing/intro) |
| `/login` | Next.js + Supabase Auth | All roles |
| `/patient/*` | Next.js | Patients (read-only portal) |
| `/doctor/*` | Next.js | Doctors + Care coordinators (action-oriented) |
| `/admin/*` | Next.js | Hospital admins (full control + care coordination) |
| `/agent` | Next.js + LiveKit | Demo / live voice interaction |
| `/api/*` | FastAPI | Voice pipeline + FHIR mapping |

---

## Tech Stack

| Component | Technology | Why |
|-----------|-----------|-----|
| Landing Page | **Static HTML/CSS/JS** | Pre-built template, zero dev time |
| Voice Pipeline | **LiveKit Agents SDK (Python)** | Real-time voice, WebRTC, familiar. Demo = browser-based. Production = SIP/Twilio telephony bridge |
| STT (Indic) | **Bhashini API** (free, govt) | Built for Indian languages, Hindi+regional, code-switching |
| TTS (Indic) | **Bhashini TTS** / Google TTS | Free, Hindi/Tamil/Bengali/Marathi voices |
| LLM | **Gemini 2.0 Flash** (free tier) | Generous quota, great structured extraction |
| Fast LLM | **Groq (Llama 3)** | Ultra-fast inference for real-time voice |
| Backend DB | **Supabase** (MANDATORY) | Auth, PostgreSQL, Realtime subscriptions, Storage |
| Voice Orchestration | **FastAPI** | LiveKit Agents requires Python runtime — cannot run in Supabase Edge Functions. FastAPI is ONLY for voice pipeline; all data/auth/storage is Supabase |
| Frontend | **Next.js + shadcn/ui** | Rapid dashboard development |
| FHIR | **fhir.resources (Python)** | FHIR R4 ABDM profile mapping |
| FHIR Terminology | **SNOMED CT + LOINC** | Medical coding standards (organizer requirement) |

### External Tools, APIs & Models (Transparency Requirement)
> *"Any external datasets, APIs, LLMs, or pre-trained NLP/Voice models used must be clearly documented"*

| Category | Tool/Service | Purpose | License/Access |
|----------|-------------|---------|----------------|
| **Dataset** | PS-3-Use-case-database-1.csv | Health camp patient data (provided by organizers) | Hackathon-provided |
| **LLM** | Google Gemini 2.0 Flash | Conversation management, structured data extraction, FHIR mapping | Free tier API |
| **LLM** | Groq (Llama 3 70B) | Fast inference for real-time voice pipeline | Free tier API |
| **STT** | Bhashini API (Govt of India) | Indic language speech-to-text | Free (govt platform) |
| **TTS** | Bhashini TTS / Google Cloud TTS | Indic language text-to-speech | Free tier |
| **Voice Infra** | LiveKit Cloud + Agents SDK | WebRTC voice rooms, agent pipeline | Open source SDK + free cloud tier |
| **Backend** | Supabase | Auth, PostgreSQL, Realtime, Storage | Free tier (mandatory per hackathon) |
| **Frontend** | Next.js, shadcn/ui, Tailwind CSS | UI framework + component library | Open source (MIT) |
| **FHIR** | fhir.resources (Python) | FHIR R4 resource validation & serialization | Open source |
| **Icons** | Iconify | Icon web component | Open source |
| **Landing** | FuseHealth Telehealth Template (Aura) | Landing page template (pre-built) | Template license |

---

## Voice Call Architecture: Demo vs Production

> **Critical clarification**: LiveKit is WebRTC (browser-to-browser), NOT a telephony dialer.

### Hackathon Demo (What judges see)
```
Patient opens /agent in browser → Clicks "Start Call"
    → LiveKit WebRTC room created
    → Bhashini STT listens via browser mic
    → Gemini processes and responds
    → Bhashini TTS speaks via browser speaker
    → Structured data flows to Supabase → Dashboard updates live
```
- Judge can test voice AI live in-browser
- Simultaneously watch the doctor dashboard update in real-time (split screen demo)
- No phone number needed — pure browser experience

### Production Vision (What we pitch for scalability)
```
System triggers outbound call via Twilio/SIP trunk
    → LiveKit SIP bridge connects telephony to WebRTC
    → Same voice pipeline (STT → LLM → TTS)
    → Patient answers regular phone call
    → Works on any phone — feature phone, smartphone, landline
```
- LiveKit has native SIP support for production telephony
- Twilio SIP trunk = ~$0.013/min for outbound calls in India
- This is an architecture slide in the pitch, not a demo feature

---

## Language Selection Mechanism

### How the system knows which language to speak

```
                Patient Profile
                      │
        ┌─────────────┼──────────────┐
        │             │              │
   From Profile    Auto-Detect    User Choice
   (preferred      (STT detects   (Voice prompt:
    language        language in    "Hindi ke liye 1
    stored in       first 5 sec   dabayein, Tamil
    patient DB)     of speech)     ke liye 2...")
        │             │              │
        └─────────────┴──────┬───────┘
                             │
                    Language Set for Session
                    STT model + TTS voice +
                    LLM system prompt all
                    switch to that language
```

### Supported Languages (MVP)
| Language | STT | TTS | LLM Prompt | Priority |
|----------|-----|-----|-----------|----------|
| **Hindi** | Bhashini | Bhashini | Full support | P0 (demo) |
| **Hindi+English mix** | Bhashini | Bhashini | Full support | P0 (demo) |
| **Bengali** | Bhashini | Bhashini | Supported | P1 |
| **Tamil** | Bhashini | Bhashini | Supported | P1 |
| **Marathi** | Bhashini | Bhashini | Supported | P2 |

### Multi-Language Voice Prompt Examples

**Hindi:**
```
"Namaste! Yeh Swadhikaar se call hai. Aapka health camp mein screening
hua tha. Kya aap theek hain?"
```

**Bengali:**
```
"Namaskar! Ei call Swadhikaar theke. Apnar health camp-e screening
hoyechhilo. Apni ki bhalo achen?"
```

**Tamil:**
```
"Vanakkam! Idhu Swadhikaar-il irundhu call. Ungal health camp-il
screening nadandhadhu. Neenga eppadi irukkeenga?"
```

---

## Stakeholder Mapping (From PS-3)

| Stakeholder | Role in System | Interface |
|-------------|---------------|-----------|
| **Post-discharge patients** | Receive recovery protocol voice calls, view health data | Patient portal (lightweight PHR) + voice calls |
| **Chronic care patients** | Receive regular check-in calls, report readings via voice | Patient portal (lightweight PHR) + voice calls |
| **Hospital administrators** | Manage workflows, view analytics, consent management, FHIR exports | Admin dashboard |
| **Care coordination teams** | Monitor escalations, assign patients to doctors, manage follow-up schedules | Admin dashboard (care coordination view) |
| **Doctors** | Review AI extractions, act on escalations, view patient transcripts | Doctor portal |

> Note: Our Patient Portal functions as a **lightweight PHR (Personal Health Record)** app — aligned with the ABDM PHR building block.

---

## Role-Based System

### Patient Portal (`/patient/*`)
```
┌──────────────────────────────────────┐
│  My Health Overview                   │
│  ┌────────┐ ┌────────┐ ┌──────────┐ │
│  │ BP     │ │ Sugar  │ │ Overall  │ │
│  │ 139/85 │ │ 114    │ │ Moderate │ │
│  └────────┘ └────────┘ └──────────┘ │
│                                      │
│  Recent Calls                        │
│  📞 24 Mar - Follow-up (completed)   │
│  📞 20 Mar - Medication check (done) │
│                                      │
│  Upcoming                            │
│  📅 27 Mar - Monthly check-in call   │
│                                      │
│  My Consents (DPDP)                  │
│  ✅ Health follow-up calls - Active  │
│  ✅ Data sharing with doctor - Active│
│  [Revoke Consent] [Request Deletion] │
│                                      │
│  My Reports (FHIR)                   │
│  📄 Health Camp Report - Gandhi Maidan│
└──────────────────────────────────────┘
```

### Doctor Portal (`/doctor/*`)
```
┌──────────────────────────────────────┐
│  🔴 Escalation Queue (3 urgent)      │
│  ├─ Ramesh K. - Severe chest pain    │
│  ├─ Sita D. - BP spike 192/115      │
│  └─ Amit S. - Missed 3 follow-ups   │
│                                      │
│  My Patients (24 assigned)           │
│  [Search] [Filter: High Risk ▼]      │
│                                      │
│  Call Transcripts + AI Review        │
│  📞 Ramesh K. - "sir dard aur chakkar│
│     aa raha hai pichle 3 din se"     │
│     → AI Extracted: headache+dizziness│
│     → Duration: 3 days               │
│     → FHIR: Condition created        │
│     [✅ Approve] [✏️ Correct] [❌ Reject]│
│                                      │
│  Today's Schedule                    │
│  09:00 - 12 automated follow-ups     │
│  14:00 - 5 chronic care check-ins    │
└──────────────────────────────────────┘
```

### Admin Portal (`/admin/*`)
```
┌──────────────────────────────────────┐
│  Dashboard                           │
│  Calls: 847 | Response: 72% | 🔴 12  │
│  ┌──────────────────────────────────┐│
│  │ Risk Distribution [PIE CHART]    ││
│  │ Low: 45% | Moderate: 38% | Hi:17││
│  └──────────────────────────────────┘│
│  ┌──────────────────────────────────┐│
│  │ Camp-wise Breakdown [BAR CHART]  ││
│  │ Gandhi Maidan | Digha Slum |     ││
│  │ Aashrya OAH  | Disha DDC  |     ││
│  └──────────────────────────────────┘│
│                                      │
│  AI Accuracy (Feedback Loop)         │
│  Approved: 89% | Corrected: 8% |    │
│  Rejected: 3%                        │
│                                      │
│  Workflow Builder                    │
│  [+ New Workflow]                    │
│  • Screening→OPD (active)            │
│  • Post-Discharge (active)           │
│  • Chronic Monthly (active)          │
│                                      │
│  Care Coordination                   │
│  Unassigned patients: 5              │
│  Pending follow-ups: 18             │
│                                      │
│  Consent Manager (DPDP Act)          │
│  Active: 234 | Pending: 12 | Rev: 3 │
│                                      │
│  FHIR Reports                        │
│  📊 Export ABDM Bundle | Audit Log   │
└──────────────────────────────────────┘
```

---

## Human Augmentation & Feedback Loop

> *From organizer slides (PS-2 pattern applied to PS-3): Every AI pipeline should end with human review + feedback loop*

```
Voice AI extracts structured data from patient call
                    │
                    ▼
    ┌───────────────────────────────┐
    │  AI Extraction (auto-saved)   │
    │  Symptom: Headache            │
    │  SNOMED: 25064002             │
    │  Duration: 1 week             │
    │  Severity: Moderate           │
    │  Medication: None             │
    └───────────────┬───────────────┘
                    │
                    ▼
    ┌───────────────────────────────┐
    │  Doctor Review (Human Layer)  │
    │                               │
    │  [✅ Approve] — AI was correct │
    │  [✏️ Correct] — Fix extraction │
    │    e.g., "Not headache, it's  │
    │    migraine (SNOMED: 37796009)"│
    │  [❌ Reject] — Bad extraction  │
    └───────────────┬───────────────┘
                    │
                    ▼
    ┌───────────────────────────────┐
    │  Feedback Loop                │
    │  • Corrections stored in DB   │
    │  • Admin sees AI accuracy %   │
    │  • Correction patterns inform │
    │    prompt tuning over time    │
    │  • Audit trail maintained     │
    └───────────────────────────────┘
```

This gives judges:
- **Completeness**: Not just AI output, but human-in-the-loop verification
- **Originality**: Most hackathon teams won't have a feedback mechanism
- **Real-world viability**: No hospital will trust pure AI — they need review capability

---

## Escalation & Triage System

### How Real Healthcare Triage Works (Our Implementation)

```
Voice AI detects severity during patient call
                    │
    ┌───────────────┼───────────────────┐
    │               │                   │
    ▼               ▼                   ▼
LEVEL 1          LEVEL 2            LEVEL 3
(Immediate)      (Within 1hr)       (Routine)

Patient told:    Dashboard          Logged in
"Turant hospital  alert +           patient record
jayein ya 108     SMS to care       for next
call karein"      coordinator       scheduled
                                    follow-up
    │               │
    ▼               ▼
Auto-create      Care team
FHIR Flag        reviews &
(priority:       assigns to
urgent)          doctor
    │               │
    ▼               ▼
Supabase         Doctor sees
Realtime →       in escalation
Dashboard        queue with
red banner       full context
+ sound alert    + transcript
```

### Severity Detection Rules
| Signal from Voice Call | Severity | Action |
|----------------------|----------|--------|
| Severe chest pain / can't breathe | CRITICAL | Level 1: Immediate patient guidance + all alerts |
| New symptoms + HIGH risk score | HIGH | Level 2: SMS + dashboard alert to care team |
| Missed medication 3+ days | MODERATE | Level 2: Dashboard flag for doctor |
| Allergy reaction reported | HIGH | Level 1: Patient guidance + FHIR AllergyIntolerance created |
| Stable, no complaints | LOW | Level 3: Log and continue schedule |
| Missed 3+ follow-up calls | MODERATE | Level 2: Flag for care coordinator outreach |

---

## ABDM & FHIR Compliance (From Organizer Slides)

### ABDM Alignment
- **ABHA Health ID**: Each patient record linked to ABHA ID (simulated for demo with format XX-XXXX-XXXX-XXXX). Production: mobile OTP + demographic matching for ABHA linking.
- **HIP (Health Information Provider)**: Our platform acts as HIP — we generate and serve health records
- **HIU (Health Information User)**: Our dashboard acts as HIU — doctors/admins request and view patient data
- **HIE-CM (Consent Manager)**: Consent flow managed through our platform, aligned with ABDM consent architecture

### ABDM Consent Flow (5-Step Architecture)
| Step | ABDM Standard | Our Implementation |
|------|--------------|-------------------|
| 1. **Request** | HIU asks for data scope + purpose | Voice AI states purpose before collecting data: "Hum aapki health jaankari collect karenge follow-up ke liye" |
| 2. **Approve** | Citizen grants via Consent Manager | Patient gives verbal consent (recorded + timestamped) OR approves via patient portal |
| 3. **Orchestrate** | Gateway routes request to HIPs | Supabase Edge Function routes data requests between services |
| 4. **Package** | HIP encrypts data (FHIR bundle) | FHIR R4 bundles generated with proper ABDM profiles |
| 5. **Deliver** | Data flows to HIU (encrypted) | Doctor/admin receives FHIR data via Supabase RLS-protected queries |

### ABDM-Specific FHIR R4 Profiles We Implement
| Profile | Our Use Case | Generated When |
|---------|-------------|----------------|
| **OPD Consultation Note** | Post-screening follow-up findings | Voice call extracts symptoms |
| **Diagnostic Report Bundle** | Health camp vitals + risk scores | CSV data ingestion |
| **Health Document Record** | Discharge summaries, referral notes | Recovery protocol calls |
| **Prescription Bundle** | Medication adherence tracking | Voice confirms/denies meds |
| **AllergyIntolerance** | Allergy info collected during voice calls | Patient reports allergy via voice |

### FHIR Terminology (SNOMED + LOINC) — Complete Dataset Mapping
| Dataset Field | LOINC/SNOMED Code | Display |
|--------------|-------------------|---------|
| systolic_bp | LOINC: 8480-6 | Systolic blood pressure |
| diastolic_bp | LOINC: 8462-4 | Diastolic blood pressure |
| heart_rate | LOINC: 8867-4 | Heart rate |
| respiratory_rate | LOINC: 9279-1 | Respiratory rate |
| temperature | LOINC: 8310-5 | Body temperature |
| blood_glucose | LOINC: 2339-0 | Glucose [Mass/volume] in Blood |
| bmi | LOINC: 39156-5 | Body mass index |
| height | LOINC: 8302-2 | Body height |
| weight | LOINC: 29463-7 | Body weight |
| oxygen_saturation | LOINC: 2708-6 | Oxygen saturation |
| waist_circumference | LOINC: 56086-2 | Waist circumference |
| waist_to_height_ratio | Custom (no standard LOINC) | Waist to height ratio — use FHIR Observation with `text` coding |
| perfusion_index | LOINC: 61006-3 | Perfusion index (Pulse oximetry) |
| chest_discomfort | SNOMED: 29857009 | Chest pain |
| breathlessness | SNOMED: 267036007 | Dyspnea |
| palpitations | SNOMED: 80313002 | Palpitations |
| fatigue_weakness | SNOMED: 84229001 | Fatigue |
| dizziness | SNOMED: 404640003 | Dizziness |

### Indian Brand-Name Drug Mapping
> *From organizer slide: "India uses 100k+ brand names, not standard INN/RxNorm codes"*

When voice AI collects medication info:
- Patient says: "Crocin le raha hoon" (brand name)
- System maps: Crocin → Paracetamol (INN) → SNOMED: 387517004
- FHIR MedicationStatement uses both: brand name (text) + INN code (coding)
- Maintain a mapping table: `drug_brand_mapping (brand_name, inn_name, snomed_code)`

### DPDP Act 2023 Compliance
- **Explicit consent** before any voice call (verbal consent recorded + timestamped)
- **Purpose limitation** — consent specifies exact purpose (follow-up, health reminder, data collection)
- **Granular consent management** in admin dashboard + patient portal
- **Audit logs** for all data access and processing
- **Data minimization** — only collect what's needed for the use case
- **Right to erasure** — patient can request data deletion via portal
- **Consent revocation** — patient can revoke consent anytime, system stops all calls

---

## Use Case Flows (Mapped to Dataset)

### Diverse Handling Per Health Camp Type
> *Evaluation parameter: "Accuracy & Diversity — coverage of diverse data and use cases"*

| Health Camp | Patient Profile | Voice AI Approach | Key Focus |
|-------------|----------------|-------------------|-----------|
| **Gandhi Maidan** | General population, health screening | Standard follow-up, OPD referral | BP/diabetes risk triage |
| **Digha Slum** | Low-income, limited healthcare access | Simpler language, emergency guidance emphasis | Accessibility, immediate risk detection |
| **Aashrya Old Age Home** | Elderly, multiple comorbidities | Slower speech, empathetic tone, caregiver involvement | Chronic disease management, medication adherence |
| **Disha Deaddiction Center** | Addiction recovery patients | Sensitivity to mental health, lifestyle monitoring | Stress/anxiety tracking, relapse prevention |

The Voice AI adapts its conversation style, speed, and focus areas based on the patient's health camp origin and risk profile.

### 1. Screening → OPD Triage
- Health camp data ingested (CSV upload to Supabase)
- Risk scores already computed in dataset (heart/diabetic/hypertension)
- **HIGH risk** → Voice AI calls in Hindi: "Aapka BP bahut zyada hai, kripya OPD jayein"
- **MODERATE risk** → Scheduled follow-up voice call within 48hrs
- **LOW risk** → Health tips via voice reminder
- All interactions → FHIR Diagnostic Report Bundle
- Doctor reviews AI extractions → Approves/Corrects → Feedback loop

### 2. OPD → IPD Escalation
- Post-OPD voice follow-up collects structured symptom data
- If symptoms escalate → auto-flag via triage system (Level 1/2)
- Data mapped to FHIR OPD Consultation Note
- Doctor reviews before IPD admission decision

### 3. Recovery Protocol
- Post-discharge automated voice calls (Day 1, 3, 7, 14, 30)
- Medication adherence check → FHIR Prescription Bundle + brand-to-INN mapping
- Wound/recovery status → structured questions
- Deviation alerts → triage system

### 4. Chronic Disease Management
- Monthly/weekly automated check-ins for diabetic/hypertensive patients
- Voice-based collection: glucose readings, BP readings, symptoms
- Trend analysis on dashboard (per-patient + per-camp aggregate)
- Smart escalation when readings cross thresholds
- Adapted for elderly patients (Aashrya) vs general population (Gandhi Maidan)

### 5. Follow-up
- Missed appointment reminders
- Lab result notifications
- Next visit scheduling via voice

---

## Voice AI Engine Design

### Conversation Flow (Example: Post-Screening Follow-up in Hindi)

```
AI: "Namaste! Yeh Swadhikaar se call hai. Aapka health camp mein
     screening hua tha. Aapka blood pressure thoda zyada tha.
     Kya aap abhi theek hain?"

Patient: "Haan, par kabhi kabhi sir mein dard hota hai"

AI: [Extracts: symptom=headache, frequency=sometimes]
    [SNOMED: 25064002 - Headache]
    "Aapko sir dard kitne dinon se ho raha hai?"

Patient: "Pichle ek hafte se"

AI: [Extracts: duration=1 week]
    "Kya aap koi dawai le rahe hain?"

Patient: "Haan, Crocin le raha hoon"

AI: [Extracts: medication=Crocin → Paracetamol (INN) → SNOMED:387517004]
    "Kya aapko kisi cheez se allergy hai?"

Patient: "Haan, Amoxicillin se"

AI: [Creates FHIR AllergyIntolerance: Amoxicillin → SNOMED:372687004]
    → Creates FHIR Condition (headache, 1 week duration)
    → Creates FHIR MedicationStatement (Paracetamol)
    → Creates FHIR AllergyIntolerance (Amoxicillin)
    → Triage: HIGH risk + new symptoms = Level 2 alert
    → SMS to care team + dashboard notification
    → Doctor receives for review [Approve/Correct/Reject]
    → Tells patient: "Hum aapke doctor ko inform kar rahe hain.
       Kripya jaldi OPD visit karein."
```

### Code-Switching Support (Hindi + English)
- STT handles: "Mera BP check karwaya tha, woh 140 over 90 tha"
- LLM responds naturally in mixed language
- Bhashini API specifically built for Indic code-switching

---

## Innovation Angles (Judging Edge)

1. **Indic Code-Switching**: Natural Hindi+English mix that patients actually speak
2. **Voice → FHIR Pipeline**: Every voice interaction auto-generates ABDM-compliant FHIR resources with SNOMED/LOINC coding
3. **Real Healthcare Triage**: Multi-level severity detection → patient guidance + care team alerts (not just logging)
4. **Human-in-the-Loop (Feedback Loop)**: Doctors review, correct, and approve AI extractions — builds trust and improves accuracy over time
5. **DPDP Compliant**: Full ABDM consent flow (5-step) with audit trails
6. **Supabase Realtime Escalation**: Live alerts via Supabase Realtime — doctor's dashboard updates instantly
7. **Role-Based UX**: Patient/Doctor/Admin see exactly what they need
8. **Diverse Camp Handling**: AI adapts tone, speed, and focus based on patient demographics (elderly, slum, deaddiction, general)
9. **Brand-to-INN Drug Mapping**: Handles India-specific medication naming (Crocin → Paracetamol)
10. **Dataset-Driven Demo**: Real health camp data powering realistic patient journeys

---

## Cost & Scalability Model (Deliverable #5)

### Per-Call Cost Breakdown
| Component | Cost per Call (est.) | Notes |
|-----------|---------------------|-------|
| Bhashini STT | Free | Govt API, no per-call charge |
| Bhashini TTS | Free | Govt API |
| Gemini Flash | ~$0.0001 | ~500 tokens/call, free tier covers 1500 RPM |
| Groq (fallback) | Free tier | 14,400 req/day free |
| LiveKit Cloud | ~$0.002 | Per-minute voice room |
| Supabase | Free tier | Up to 500MB DB, 2GB storage |
| **Total per call** | **~$0.003** | **Practically free at MVP scale** |

### Scaling Projections
| Scale | Calls/Day | Monthly Cost | Infrastructure |
|-------|-----------|-------------|----------------|
| 1 SME hospital (demo) | 50 | ~$5 | Free tiers sufficient |
| 10 SME hospitals | 500 | ~$45 | Supabase Pro ($25) + minimal API costs |
| 100 SME hospitals | 5,000 | ~$450 | Dedicated Supabase + LiveKit scaling |
| 1000 hospitals (national) | 50,000 | ~$4,500 | Multi-region, enterprise tiers |

### Why This Scales for India
- Bhashini is govt-backed — designed for national scale
- No per-patient app install needed — just phone calls
- Supabase auto-scales PostgreSQL
- LiveKit handles concurrent voice sessions
- One deployment serves multiple hospitals (multi-tenant)

---

## Deliverables Checklist (From Organizer Slides)

| # | Deliverable | Status | Notes |
|---|-------------|--------|-------|
| 1 | **One Pager** | [ ] | Problem + solution + architecture in 1 page |
| 2 | **Live Functioning MVP** | [ ] | Web app + voice agent working end-to-end |
| 3 | **End-to-End Workflow Demo** | [ ] | Screening data → voice call → dashboard → escalation → doctor review |
| 4 | **AI Component Explanation** | [ ] | STT/LLM/TTS pipeline, FHIR extraction, severity detection, feedback loop |
| 5 | **Cost & Scalability Estimation** | [ ] | Per-call cost model + scaling projections (see above) |
| 6 | **Code (GitHub Repo)** | [ ] | Public repo with detailed README + external tools documented |
| 7 | **5-6 Slide Pitch** | [ ] | Problem → Solution → Demo → Impact → Scalability |

---

## MVP Build Order (1 week, solo dev)

### Phase 1: Foundation (Day 1-2) ✅ COMPLETE
- [x] Set up monorepo structure
- [x] Landing page: FuseHealth-style clone at / (pixel-perfect, CSS grid bg, dashboard mockup, pricing, footer)
- [x] Database schema: 001_initial_schema.sql (patients, health_vitals, risk_assessments, symptoms, voice_calls, fhir_resources, ai_feedback, drug_brand_mapping, workflows, escalations, consents, audit_log + RLS + indexes)
- [x] Supabase Auth with role-based demo login (patient/doctor/admin via cookie bypass)
- [x] Seed data script (backend/seed_data.py — reads CSV, generates synthetic Indian patient profiles)
- [x] Next.js scaffold with shadcn/ui + role-based routing (all /patient/*, /doctor/*, /admin/* routes)
- [x] FastAPI server scaffold (main.py with 5 routers: voice, fhir, triage, patients, risk_router)
- [x] Defensive Supabase client (fallback values so build works without env vars)
- [x] **Connect real Supabase project** (project ref: etdkljfgtbnbcdlqioht, .env.local + .env created)
- [x] **Run seed_data.py** — 120 patients, 115 vitals/risks/symptoms, 3 doctors, 345 consents seeded

### Phase 2: Voice AI Engine (Day 3-4) — CODE WRITTEN, NOT TESTED
- [x] LiveKit Agents setup (voice_agent/agent.py)
- [x] Bhashini STT plugin (voice_agent/plugins/bhashini.py)
- [x] System prompts for Hindi voice conversations (voice_agent/prompts/system_prompts.py)
- [x] Gemini/Groq LLM integration in agent
- [x] FHIR service (services/fhir_service.py)
- [x] Drug brand mapping service (services/drug_mapping.py)
- [x] Risk model service (services/risk_model.py)
- [x] Triage severity detection (services/triage_service.py)
- [x] Frontend /agent page with LiveKit room component
- [ ] **Get API keys** (Bhashini, Gemini, LiveKit Cloud, Groq)
- [ ] **Test voice pipeline end-to-end** (STT → LLM → TTS → extraction)
- [ ] **Train risk prediction model** (sklearn on CSV data, export pickle)

### Phase 3: Dashboard & Workflows (Day 5-6) — WIRED TO LIVE DATA
- [x] Patient portal (dashboard, records, calls, consent pages)
- [x] Doctor portal (dashboard, patients, escalations, review pages)
- [x] Admin dashboard (dashboard, patients, consent, coordination, reports, workflows)
- [x] Supabase hooks (usePatients, useVitals, useRiskAssessments, useCallLogs, useEscalations, useFHIRResources, useConsents, useWorkflows, useRealtimeEscalations, useDoctors, usePatientNames)
- [x] Mutation helpers (updateEscalationStatus, updateFHIRReviewStatus, revokeConsent, createAuditLog)
- [x] **Wire dashboards to live Supabase data** — all pages now query real DB with fallback to demo data
- [ ] **Test Supabase Realtime** escalation alerts (needs connected project)
- [ ] **Add charts/visualizations** to admin dashboard (risk distribution, camp-wise, AI accuracy)

### Phase 4: Polish & Deliverables (Day 7) — NOT STARTED
- [ ] End-to-end demo flow (screening → voice call → dashboard → escalation → doctor review)
- [ ] One Pager document (docs/one-pager.md)
- [ ] AI Component Explanation document (docs/ai-components.md)
- [ ] Cost & Scalability Estimation document (docs/cost-scalability.md)
- [ ] 5-6 slide pitch deck
- [ ] README with setup/usage + external tools documentation
- [ ] Pre-record backup demo video
- [ ] Edge case handling + error states

---

## Key Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| Bhashini API latency/limits | Fallback to Google Cloud STT/TTS (free tier) or Groq Whisper |
| Supabase learning curve | Supabase has great docs + JS SDK; auth/realtime are easy to integrate |
| FHIR complexity | Focus on 5 ABDM profiles (OPD Note, Diagnostic Report, Health Doc, Prescription, AllergyIntolerance) |
| Solo developer bandwidth | Priority: Voice engine > Workflow builder > Dashboard > Feedback Loop > Docs (workflow builder is REQUIRED deliverable) |
| Demo reliability | Pre-record backup video; scripted test scenarios; demo accounts |
| DPDP compliance depth | Implement consent collection + audit logs; skip full DPO appointment for MVP |
| Bhashini API access | Apply early; have Groq Whisper + Google TTS as backup pipeline |
| Drug brand mapping completeness | Start with top 50 common Indian brands; expandable lookup table |
| Feedback loop complexity | Keep it simple: Approve/Correct/Reject buttons + store corrections |

---

## Dataset Summary

`PS-3-Use-case-database-1.csv` — 120+ patient records from 5+ health camps:
- **Vitals**: BP, HR, RR, SpO2, temp, glucose, BMI, height, weight, waist circumference, perfusion index, waist-to-height ratio
- **Risk Scores**: Heart (0-100), Diabetic (0-100), Hypertension (0-100)
- **Risk Levels**: Low, Moderate, High for each category + overall
- **Symptoms**: chest_discomfort, breathlessness, palpitations, fatigue_weakness, dizziness_blackouts
- **Lifestyle**: sleep_duration, stress_anxiety, physical_inactivity, diet_quality, family_history
- **Health Camps**: Gandhi Maidan (general), Digha Slum (low-income), Aashrya Old Age Home (elderly), Disha Deaddiction Center (addiction recovery)
- **Timestamps**: All records have updated_at timestamps for temporal analysis

---

## Supabase Database Schema (Core Tables)

```sql
-- Patients (from dataset + voice-collected)
patients (id, abha_id, name, phone, language, health_camp, camp_type, risk_level, overall_risk_score, consent_status, assigned_doctor_id)

-- Health Vitals (from dataset)
health_vitals (id, patient_id, systolic_bp, diastolic_bp, heart_rate, respiratory_rate, oxygen_saturation, temperature, blood_glucose, height, weight, bmi, bmi_category, waist_circumference, waist_to_height_ratio, perfusion_index, recorded_at)

-- Risk Assessments (from dataset)
risk_assessments (id, patient_id, heart_risk_score, heart_risk_level, diabetic_risk_score, diabetic_risk_level, hypertension_risk_score, hypertension_risk_level, overall_risk_category, overall_risk_score)

-- Symptoms (from dataset)
symptoms (id, patient_id, chest_discomfort, breathlessness, palpitations, fatigue_weakness, dizziness_blackouts, sleep_duration, stress_anxiety, physical_inactivity, diet_quality, family_history)

-- Voice Calls
voice_calls (id, patient_id, call_type, use_case, status, transcript, extracted_data, severity, started_at, ended_at)

-- FHIR Resources
fhir_resources (id, patient_id, call_id, resource_type, profile, fhir_json, snomed_codes, loinc_codes, review_status, reviewed_by, reviewed_at)

-- AI Feedback (Doctor Review)
ai_feedback (id, fhir_resource_id, doctor_id, action, original_extraction, corrected_extraction, correction_notes, created_at)

-- Drug Brand Mapping
drug_brand_mapping (id, brand_name, inn_name, snomed_code)

-- Workflows
workflows (id, name, trigger_type, trigger_config, actions, conditions, camp_type, is_active)

-- Escalations
escalations (id, patient_id, call_id, severity_level, status, assigned_to, resolved_at, resolution_notes)

-- Consents (DPDP)
consents (id, patient_id, purpose, scope, consent_mode, granted_at, revoked_at)

-- Audit Log
audit_log (id, user_id, action, resource_type, resource_id, timestamp, details)
```

## Dataset Usage Beyond Seeding
> *PS-3: "Download the dataset to fine-tune your models"*

The dataset (120+ records) is too small for LLM fine-tuning. Instead, we use it intelligently:

### 1. Risk Prediction Model (trained on dataset)
- Train a **lightweight scikit-learn classifier** on the dataset
- Input: vitals (BP, HR, glucose, BMI, etc.) + symptoms
- Output: overall_risk_category (Low/Moderate/High)
- This lets us re-score risk when Voice AI collects new readings from a patient
- Model exported as pickle, loaded by FastAPI at runtime
- **This fulfills the "fine-tune your models" requirement**

### 2. Context-Aware Voice Conversations
- Before calling a patient, the LLM receives their health camp data as context
- "This patient had BP 160/84, glucose 186, BMI 25.1, heart risk HIGH, diabetic risk HIGH"
- Conversation adapts: asks about BP medication, diabetes management, etc.

### 3. Demographic Analysis for Workflow Triggers
- Dataset grouped by health camp → different risk distributions
- Gandhi Maidan: 40% moderate, 20% high → general screening workflows
- Aashrya Old Age Home: 60% high risk → aggressive follow-up workflows
- Enables camp-type-specific workflow templates

### 4. Dashboard Analytics
- Real data powers risk distribution charts, camp-wise breakdowns, trend analysis
- Not mock data — actual patient vitals driving visualizations

---

## Synthetic Patient Profiles (For Demo)

The dataset has vitals/risk scores but NO patient identifiers. For demo purposes, we generate:

```python
# Seed script generates synthetic patient profiles
# Linked to real vitals data from the dataset
{
    "name": "Ramesh Kumar",            # Generated (faker-hindi)
    "phone": "+91-9876543210",          # Generated
    "abha_id": "91-1234-5678-9012",     # Simulated format
    "language": "hindi",                 # Inferred from health camp location
    "health_camp": "Gandhi Maidan Morning Jilo Health",  # From dataset
    # ... all vitals/risk scores from actual CSV row
}
```

Language inference from health camp:
| Health Camp | Location | Default Language |
|------------|----------|-----------------|
| Gandhi Maidan | Patna, Bihar | Hindi |
| Digha Slum | Patna, Bihar | Hindi/Bhojpuri |
| Aashrya Old Age Home | Bihar | Hindi |
| Disha Deaddiction Center | Bihar | Hindi |

(All camps are in Bihar → Hindi is primary. For demo diversity, we assign some patients Bengali/Tamil to showcase multilingual capability.)

---

## Supabase Row Level Security (RLS)

Critical for DPDP compliance and role-based access:

```sql
-- Patients can only see their own data
CREATE POLICY "patients_own_data" ON patients
  FOR SELECT USING (auth.uid() = user_id);

-- Doctors can see assigned patients only
CREATE POLICY "doctors_assigned_patients" ON patients
  FOR SELECT USING (
    assigned_doctor_id = auth.uid()
    OR EXISTS (SELECT 1 FROM escalations WHERE patient_id = patients.id AND assigned_to = auth.uid())
  );

-- Admins can see all
CREATE POLICY "admins_all" ON patients
  FOR ALL USING (
    EXISTS (SELECT 1 FROM auth.users WHERE id = auth.uid() AND raw_user_meta_data->>'role' = 'admin')
  );

-- Audit log: append-only, readable by admins
CREATE POLICY "audit_append" ON audit_log
  FOR INSERT WITH CHECK (true);
CREATE POLICY "audit_read_admin" ON audit_log
  FOR SELECT USING (
    EXISTS (SELECT 1 FROM auth.users WHERE id = auth.uid() AND raw_user_meta_data->>'role' = 'admin')
  );
```

---

## Demo Script (For Judges — "Testable Live")

### Scenario: End-to-End Screening → Escalation → Doctor Review

**Setup**: Two browser windows side by side

| Step | Action | Window 1 (Patient/Voice) | Window 2 (Dashboard) |
|------|--------|--------------------------|---------------------|
| 1 | Login as Admin | - | Admin dashboard loads, shows patient list |
| 2 | Show data ingestion | - | Point out 120+ patients from CSV, risk distribution chart |
| 3 | Pick HIGH risk patient | - | Click "Ramesh Kumar" — show vitals, risk score HIGH |
| 4 | Login as Patient | Open /agent page | - |
| 5 | Start voice call | Click "Start Call" — voice AI greets in Hindi | Call status appears on dashboard |
| 6 | Speak as patient | Say "Haan, sir mein dard ho raha hai" | Real-time transcript appears |
| 7 | AI extracts data | AI asks follow-up questions | Structured extraction shows: Headache, SNOMED coded |
| 8 | Severity detected | AI says "Hum aapke doctor ko inform kar rahe hain" | 🔴 Escalation alert appears (Supabase Realtime) |
| 9 | Login as Doctor | - | Switch to doctor portal — escalation queue shows Ramesh |
| 10 | Review AI extraction | - | Click transcript → see AI extractions → click [Approve] or [Correct] |
| 11 | Show FHIR output | - | Click "FHIR Reports" → show generated FHIR bundle with SNOMED/LOINC |
| 12 | Show consent | Switch to patient portal | Patient's consent status visible |

**Total demo time: ~5 minutes**

---

## Pitch Deck Structure (5-6 Slides)

| Slide | Content | Duration |
|-------|---------|----------|
| **1. Problem** | SME hospitals: unstructured data, no follow-up capacity, patients lost to follow-up. Stats: 90% of high-risk health camp patients never visit OPD. $110B healthcare data market, India 30-35% share. | 1 min |
| **2. Solution** | Swadhikaar: AI voice agent that calls patients in their language, collects structured data, and alerts care teams. Show system architecture diagram. | 1 min |
| **3. Live Demo** | Split-screen: voice call + dashboard updating in real-time. Show end-to-end flow from the demo script above. | 3 min |
| **4. Tech Deep-Dive** | Voice pipeline (STT→LLM→TTS), FHIR mapping with SNOMED/LOINC, feedback loop, ABDM alignment. AI component explanation. | 1 min |
| **5. Impact & Scale** | Cost model (~$0.003/call), scaling projections, DPDP compliance, multi-tenant architecture. Why this works for India specifically. | 1 min |
| **6. Team & Ask** | Solo-built MVP in 1 week. Roadmap: telephony integration, more languages, EMR integrations. | 30 sec |

---

## Updated Priority Order (Workflow Builder is REQUIRED)

> PS-3 Expected Deliverables explicitly lists: "Patient engagement workflow builder"
> It is NOT optional — it must ship in the MVP.

**Revised priority (non-negotiable deliverables first):**
1. Voice AI Engine (core product) — Day 3-4
2. Workflow Builder (required deliverable) — Day 4-5
3. Dashboard + Reporting (required deliverable) — Day 5-6
4. Doctor Review/Feedback Loop (differentiator) — Day 6
5. Docs + Polish — Day 7

---



*Status: FINALIZED (v3) — Double-audited against all requirement sources*
*Project Name: Swadhikaar*
