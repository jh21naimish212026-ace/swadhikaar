# Swadhikaar — 5-Slide Hackathon Pitch Deck Guide

> HackMatrix 2.0 | IIT Patna | Jilo Health | PS-3
> Built by Ace (Solo Developer)

---

## Judge Evaluation Criteria (from organizer slides)

| Criteria            | What They Score                                      |
| ------------------- | ---------------------------------------------------- |
| Accuracy & Diversity | Coverage of all 6 use cases, diverse data handling   |
| Completeness        | Live functioning MVP, end-to-end workflow, testable  |
| Originality         | New backend logic, AI capabilities, not a thin wrapper |
| Scalability & Cost  | Cost-effectiveness, scalability estimation           |
| Innovation          | New and innovative workflow ideas                    |

## Required Deliverables

1. One Pager
2. A Live functioning MVP
3. End to End workflow demo
4. AI component explanation
5. Cost & Scalability estimation
6. Code (GitHub Repo)
7. **5-6 slide pitch** <-- this document

---

## Design System (match organizer slide aesthetic)

- **Background**: Dark / near-black (#0a0a0a or similar)
- **Accent color**: Green/teal (single accent, monochromatic)
- **Font**: Clean sans-serif (Inter, Geist, or similar)
- **Icons**: Lucide style (matches shadcn)
- **Max words per slide body**: 30-40
- **Screenshots**: Real UI, wrapped in browser-frame mockups, with numbered callout annotations
- **Diagrams**: Clean horizontal layers, not spaghetti arrows

---

## Timing Breakdown (5 minutes total)

| Slide | Time | Purpose                              |
| ----- | ---- | ------------------------------------ |
| 1     | 0:45 | Emotional hook, establish urgency    |
| 2     | 1:00 | What you built, 6 use cases, core flow |
| 3     | 1:30 | Visual proof + live demo transition  |
| 4     | 1:00 | Technical credibility, compliance    |
| 5     | 0:45 | Close with numbers and vision        |

---

---

# SLIDE 1 — THE PROBLEM

## Title

**"1 Doctor. 2,000 Patients. 0 Follow-Up Calls."**

## Layout

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│          "1 Doctor. 2,000 Patients.                          │
│                0 Follow-Up Calls."                           │
│                                                              │
│   ┌─────────────────────────────────────────────────────┐    │
│   │  HERO STAT (large, centered)                        │    │
│   │                                                     │    │
│   │  "60% of post-discharge complications in India      │    │
│   │   are preventable with timely follow-up"            │    │
│   └─────────────────────────────────────────────────────┘    │
│                                                              │
│   ┌───────────────┐  ┌───────────────┐  ┌───────────────┐   │
│   │ icon          │  │ icon          │  │ icon          │   │
│   │ Unstructured  │  │ Zero Follow-  │  │ Delayed       │   │
│   │ patient data  │  │ up capacity   │  │ Escalation    │   │
│   │ after health  │  │ (staff        │  │ = preventable │   │
│   │ camps         │  │ bottleneck)   │  │ deaths        │   │
│   └───────────────┘  └───────────────┘  └───────────────┘   │
│                                                              │
│   "Before" flow (subtle, bottom):                            │
│   Health Camp → Paper Form → Filing Cabinet → ??? → Lost     │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Content

### Hero Stat (big, centered, top)
> 60% of post-discharge complications in India are preventable with timely follow-up

### 3 Pain Points (with icons, in a row)

1. **Unstructured Data** — Health camps produce paper/CSV chaos, no structured records
2. **Zero Follow-up Capacity** — Limited staff, zero outbound calls, patients fall through cracks
3. **Delayed Escalation** — High-risk patients not flagged until it's too late

### "Before" Flow (subtle bottom strip)
```
Health Camp → Paper Form → Filing Cabinet → ??? → Patient Lost to Follow-Up
```

## What NOT to include
- No tech stack mentions (zero jargon)
- No solution yet (build tension first)
- No team intro slide (mention solo verbally in 3 seconds)

## Speaker Script
> "In India's SME hospitals, the bottleneck isn't intent — it's bandwidth. A single doctor manages thousands of patients and has zero capacity for outbound follow-up. After every health camp, data sits in paper forms and messy CSVs. Nobody calls back. The result? Missed interventions, preventable complications, and patients who simply fall through the cracks."

---

---

# SLIDE 2 — THE SOLUTION

## Title

**"Swadhikaar: Voice-First Patient Engagement OS"**

## Layout

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│   "Swadhikaar: Voice-First Patient Engagement OS"            │
│                                                              │
│   ┌─────────────────────────────────────────────────────┐    │
│   │  ONE-LINER (large, prominent):                      │    │
│   │  "AI calls patients in their language.              │    │
│   │   Extracts clinical signals. Routes urgency         │    │
│   │   to doctors. In real time."                        │    │
│   └─────────────────────────────────────────────────────┘    │
│                                                              │
│   6 USE CASE PILLS (horizontal row):                         │
│   [Screening→OPD] [OPD→IPD] [Recovery] [Chronic]            │
│   [Follow-up] [Vaccination]                                  │
│                                                              │
│   HOW IT WORKS (4-step horizontal flow):                     │
│                                                              │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────┐  │
│   │ AI Calls │ →  │Structured│ →  │  Risk    │ →  │Doctor│  │
│   │ Patient  │    │Extraction│    │ Triage   │    │Dash- │  │
│   │(Hindi/En)│    │(symptoms,│    │(LOW →    │    │board │  │
│   │          │    │ vitals)  │    │CRITICAL) │    │(act) │  │
│   └──────────┘    └──────────┘    └──────────┘    └──────┘  │
│                                                              │
│   Badge: "Human-in-the-loop: Doctors review. AI assists.     │
│           Never autonomous."                                 │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Content

### One-Liner (hero text)
> AI calls patients in their language. Extracts clinical signals. Routes urgency to doctors. In real time.

### 6 Use Case Pills (horizontal badges/chips)

| # | Use Case | Short Label |
|---|----------|-------------|
| 1 | Screening to OPD referral | Screening → OPD |
| 2 | OPD to IPD escalation | OPD → IPD |
| 3 | Post-discharge recovery monitoring | Recovery Protocol |
| 4 | Chronic disease management | Chronic Care |
| 5 | Automated follow-up calls | Follow-Up |
| 6 | Newborn vaccination reminders | Vaccination Agent |

### 4-Step Flow Diagram (horizontal, with icons + arrows)

```
Step 1              Step 2               Step 3              Step 4
AI Calls Patient → Structured         → Risk Triage       → Doctor Dashboard
(Hindi/English)    Extraction            (LOW/MODERATE/      (Approve / Correct
                   (symptoms, vitals,     HIGH/CRITICAL)       / Reject / Act)
                    compliance)
```

### Human-in-the-Loop Badge
> Doctors review and approve. AI assists, never decides autonomously.

## What NOT to include
- Don't list every feature (this is "what" not "how")
- No UI screenshots yet (save for slide 3)
- No specific APIs or SDK names

## Speaker Script
> "Swadhikaar is an AI-first voice engagement layer for Indian healthcare. It calls patients in Hindi or English, extracts structured health signals from natural conversation, triages risk across four severity levels in real time, and surfaces urgent cases to doctors on their dashboard — who always have the final say. We cover all 6 use cases from the problem statement end-to-end: from health camp screening to newborn vaccination tracking."

---

---

# SLIDE 3 — PRODUCT WALKTHROUGH

## Title

**"Three Roles. One Platform."**

> **This is your HIGHEST-IMPACT slide.** Judges want to see a real, working product.

## Layout

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│   "Three Roles. One Platform."                               │
│                                                              │
│   ┌────────────────┐ ┌────────────────┐ ┌────────────────┐   │
│   │  PATIENT        │ │  DOCTOR         │ │  ADMIN          │   │
│   │  PORTAL         │ │  DASHBOARD      │ │  OPERATIONS     │   │
│   │                 │ │                 │ │                 │   │
│   │ [SCREENSHOT]    │ │ [SCREENSHOT]    │ │ [SCREENSHOT]    │   │
│   │                 │ │                 │ │                 │   │
│   │ ① SOS Button    │ │ ① Escalation    │ │ ① 6 Workflow    │   │
│   │ ② Vitals Cards  │ │   Queue         │ │   Configs       │   │
│   │ ③ Voice Widget  │ │ ② AI Co-Pilot   │ │ ② ROI Metrics   │   │
│   │ ④ Hindi Toggle  │ │   (4 tabs)      │ │ ③ Compliance    │   │
│   │ ⑤ Consent Mgmt  │ │ ③ Vaccination   │ │ ④ Live Feed     │   │
│   │                 │ │   Tracker       │ │                 │   │
│   └────────────────┘ └────────────────┘ └────────────────┘   │
│                                                              │
│   ─────────────────────────────────────────────────────────   │
│   "Live demo: voice call → extraction → triage →             │
│    escalation → doctor action — all in < 60 seconds"         │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Screenshots to Capture (take these BEFORE making the PPT)

### Screenshot 1 — Patient Portal
- Dashboard with vitals cards (BP, glucose, BMI, risk score)
- SOS emergency button visible
- Voice widget visible (bottom right)
- Consent management section
- Hindi/English toggle in header
- **Annotate**: number callouts pointing to SOS, vitals, voice widget, Hindi toggle, consent

### Screenshot 2 — Doctor Dashboard
- Escalations table showing patient list with severity colors
- AI Clinical Co-Pilot Sheet open (showing AI Summary tab)
- The 4 tabs visible: AI Summary, Transcript, e-Rx Draft, ABDM FHIR
- Vaccination tracker card
- **Annotate**: number callouts pointing to escalation queue, AI co-pilot tabs, vaccination section

### Screenshot 3 — Admin Operations
- Workflows page with all 6 use case workflow cards
- ROI metrics (cost savings, call volume, engagement rate)
- Compliance status cards
- Workflow toggle switches
- **Annotate**: number callouts pointing to workflow cards, ROI numbers, compliance badges

## Feature Callout Table

| Patient Portal | Doctor Dashboard | Admin Operations |
|----------------|-----------------|------------------|
| ① SOS Emergency Button | ① Escalation Priority Queue | ① 6 Workflow Configurations |
| ② Vitals Cards (BP, glucose, BMI) | ② AI Clinical Co-Pilot (4 tabs) | ② ROI Metrics Dashboard |
| ③ Voice Widget (WebRTC) | ③ Newborn Vaccination Tracker | ③ Compliance Status |
| ④ Hindi/English Toggle | ④ Patient Risk Levels | ④ Live Escalation Feed |
| ⑤ DPDP Consent Management | ⑤ Human Review Actions | ⑤ Dialect Analytics |

## Bottom Banner
> Live demo: voice call → extraction → triage → escalation → doctor action — all in < 60 seconds

## What NOT to include
- No code snippets
- No more than 1 screenshot per role (pick the best view)
- No landing page screenshot (judges don't care about marketing pages)
- No wireframes or mockups — only REAL screenshots

## Speaker Script
> "Patients see their vitals, manage consent under the DPDP Act, and talk directly to the AI voice agent — with a one-tap SOS for emergencies. Doctors get a priority queue of escalations. For each case, an AI-generated clinical co-pilot gives them four tabs: AI summary, full transcript, draft e-prescription, and an ABDM FHIR bundle — all reviewable before any action is taken. Admins configure and toggle workflows per use case and see system-wide ROI. Let me show you this live."

## Pro Tip
> If allowed, transition to a 30-60 second LIVE DEMO here. A real voice call producing a real escalation is worth more than any slide. Keep it tight: start call → say symptoms → show escalation appear on doctor dashboard.

---

---

# SLIDE 4 — ARCHITECTURE & AI INTELLIGENCE

## Title

**"Built for Healthcare-Grade Operations"**

> This slide proves you're not a thin wrapper. Judges score **Originality** and **Innovation** here.

## Layout

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│   "Built for Healthcare-Grade Operations"                    │
│                                                              │
│   ┌─────────────────────────────────────┐  ┌─────────────┐  │
│   │  ARCHITECTURE DIAGRAM (left 60%)    │  │ DIFFER-     │  │
│   │                                     │  │ ENTIATORS   │  │
│   │  ┌─────────────────────────────┐    │  │ (right 40%) │  │
│   │  │ FRONTEND                    │    │  │             │  │
│   │  │ Next.js + shadcn/ui         │    │  │ ① Indic     │  │
│   │  │ Patient │ Doctor │ Admin    │    │  │   Voice     │  │
│   │  ├─────────────────────────────┤    │  │             │  │
│   │  │ VOICE PIPELINE              │    │  │ ② FHIR R4   │  │
│   │  │ FastAPI + LiveKit Agents    │    │  │   + ABDM    │  │
│   │  │ Bhashini │ Gemini 2.5 Flash │    │  │             │  │
│   │  │ 7 Clinical Prompt Personas  │    │  │ ③ DPDP Act  │  │
│   │  ├─────────────────────────────┤    │  │   Compliant │  │
│   │  │ DATA + COMPLIANCE           │    │  │             │  │
│   │  │ Supabase (mandatory)        │    │  │ ④ 4-Level   │  │
│   │  │ 15 Tables │ RLS │ RPC       │    │  │   Triage    │  │
│   │  │ FHIR Gen │ Audit │ Consent  │    │  │             │  │
│   │  └─────────────────────────────┘    │  │             │  │
│   └─────────────────────────────────────┘  └─────────────┘  │
│                                                              │
│   Small FHIR snippet (bottom right, like organizer slides):  │
│   { "resourceType": "Bundle", "type": "document", ... }     │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Architecture Diagram (3 horizontal layers)

```
┌──────────────────────────────────────────────────────────────┐
│  FRONTEND — Next.js 15 + shadcn/ui + Tailwind                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ Patient      │  │ Doctor       │  │ Admin        │       │
│  │ Portal       │  │ Dashboard    │  │ Console      │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
├──────────────────────────────────────────────────────────────┤
│  VOICE PIPELINE — FastAPI + LiveKit Agents SDK v1.4.4        │
│  ┌────────────┐  ┌────────────────┐  ┌───────────────────┐  │
│  │ Bhashini   │  │ Gemini 2.5     │  │ 7 Prompt Personas │  │
│  │ STT / TTS  │  │ Flash Native   │  │ (context-aware)   │  │
│  │ (Hindi/En) │  │ Audio          │  │                   │  │
│  └────────────┘  └────────────────┘  └───────────────────┘  │
├──────────────────────────────────────────────────────────────┤
│  DATA + COMPLIANCE — Supabase                                │
│  ┌──────┐ ┌─────┐ ┌──────┐ ┌───────┐ ┌─────────┐ ┌──────┐ │
│  │ 15   │ │ RLS │ │ FHIR │ │ Audit │ │ Consent │ │ RPC  │ │
│  │Tables│ │     │ │ Gen  │ │ Logs  │ │ Flows   │ │      │ │
│  └──────┘ └─────┘ └──────┘ └───────┘ └─────────┘ └──────┘ │
└──────────────────────────────────────────────────────────────┘
```

## 4 Differentiator Callout Boxes

### ① Indic Voice Pipeline
- Bhashini (govt API) for native Hindi STT/TTS
- Not translate-and-speak — real multilingual voice
- Fallback: Groq Whisper + Google TTS

### ② FHIR R4 + ABDM Alignment
- Structured clinical output, not text dumps
- ABDM-specific profiles: OPD notes, prescriptions, immunization records
- SNOMED/LOINC coding
- Show a small FHIR JSON snippet (mirrors organizer slide style):
```json
{
  "resourceType": "Bundle",
  "type": "document",
  "entry": [{
    "resource": {
      "resourceType": "Encounter",
      "status": "finished",
      "class": { "code": "AMB" }
    }
  }]
}
```

### ③ DPDP Act 2023 Compliance
- Consent collection + revocation flow
- Audit trail for all data access
- Data deletion request capability
- Role-based access via Supabase RLS

### ④ 4-Level Triage Escalation
- Level 1: Automated follow-up (no intervention)
- Level 2: Coordinator notification
- Level 3: Doctor priority queue
- Critical: Immediate SOS routing
- Human-in-the-loop at every clinical decision point

## What NOT to include
- Don't list every npm/pip package
- Don't show raw code
- Don't over-explain Supabase basics (judges know it, it's mandatory)
- Don't make the architecture diagram complex — clean horizontal layers only

## Speaker Script
> "Our voice pipeline uses Bhashini — India's government STT/TTS API — for native Hindi, not translated English. Gemini 2.5 Flash runs seven context-aware clinical prompt personas, one per use case. Every call produces structured FHIR R4 bundles aligned with ABDM profiles — OPD notes, prescriptions, immunization records — all with SNOMED and LOINC coding. The entire system is DPDP Act compliant: explicit consent, audit trails, data deletion, and role-based access through Supabase RLS. Triage operates on four escalation levels, and doctors always have the final word."

---

---

# SLIDE 5 — IMPACT & SCALE

## Title

**"From 1 Hospital to 1,000 — Without Hiring"**

## Layout

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│   "From 1 Hospital to 1,000 — Without Hiring"               │
│                                                              │
│   ┌────────────────┐  ┌────────────────┐  ┌──────────────┐  │
│   │    ~Rs 3-5     │  │     6 / 6      │  │  Real-Time   │  │
│   │  cost per      │  │   use cases    │  │  escalation  │  │
│   │  follow-up     │  │   covered      │  │  routing     │  │
│   │                │  │                │  │              │  │
│   │ vs Rs 50-80    │  │ Full problem   │  │ vs 24-48 hr  │  │
│   │ manual call    │  │ statement      │  │ manual       │  │
│   └────────────────┘  └────────────────┘  └──────────────┘  │
│                                                              │
│   SCALABILITY:                                               │
│   • Same platform core scales across districts               │
│     — add patients, not call-center seats                    │
│   • Telephony bridge (SIP/Twilio) extends demo to real       │
│     phone calls without changing triage/data layer           │
│                                                              │
│   WHAT'S NEXT (small, 3 items):                              │
│   → WhatsApp reminders  → Predictive risk  → ABDM sandbox   │
│                                                              │
│   ─────────────────────────────────────────────────────────   │
│                                                              │
│   CLOSING (large, bold):                                     │
│   "Swadhikaar turns follow-up from a                         │
│    staffing problem into a software problem."                │
│                                                              │
│   Dataset: 240 real patient records from health camp data     │
│   Built end-to-end by one developer.                         │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## 3 Impact Metrics (big numbers, top row)

| Metric | Value | Context |
|--------|-------|---------|
| **Cost per follow-up** | ~Rs 3-5 | vs Rs 50-80 for manual call center |
| **Use case coverage** | 6/6 | Complete problem statement coverage |
| **Escalation speed** | Real-time | vs 24-48 hour manual triage delay |

## Scalability (2 bullets)
- Same platform core scales across districts — add patients, not call-center seats
- Telephony bridge (SIP/Twilio) extends browser demo to real phone calls without changing the triage or data layer

## What's Next (3 small forward items)

| Next Step | Description |
|-----------|-------------|
| WhatsApp Integration | Medication reminders + vaccination alerts |
| Predictive Risk Scoring | ML model on call pattern + vitals history |
| ABDM Sandbox | Real ABHA ID linkage + health locker integration |

## Closing Statement (large, bold, bottom)
> **"Swadhikaar turns follow-up from a staffing problem into a software problem."**

## Subtle Flex Line (small, bottom corner)
> Dataset: 240 real patient records from health camp data. Built end-to-end by one developer.

## What NOT to include
- Don't overpromise ("we'll serve all of India" = red flag)
- Don't introduce new concepts — this slide closes, doesn't open
- No "Thank You" text — end on impact, say thank you verbally
- Don't add a Q&A slide — judges will ask questions regardless

## Speaker Script
> "At roughly 3 rupees per follow-up versus 80 for manual outreach, this isn't just better care — it's economically inevitable. We cover all 6 use cases from the problem statement. Escalations route in real time, not after a 48-hour delay. The platform scales by software and workflow design, not by hiring call-center staff. Next: WhatsApp integration, predictive risk scoring from call patterns, and ABDM sandbox integration for real ABHA linkage. Swadhikaar turns patient follow-up from a staffing burden into an intelligent, measurable care system. Thank you."

---

---

# APPENDIX: Tactical Tips

## Screenshots Checklist (capture all before building PPT)

- [ ] Patient dashboard — full view with vitals, SOS, voice widget, consent
- [ ] Patient dashboard — Hindi mode toggled on
- [ ] Doctor dashboard — escalations table with severity colors
- [ ] Doctor dashboard — AI Co-Pilot sheet open (AI Summary tab)
- [ ] Doctor vaccinations page — NIP schedule with Mark Done
- [ ] Admin dashboard — ROI metrics + compliance cards
- [ ] Admin workflows page — all 6 workflow cards visible
- [ ] Voice call in progress — WebRTC widget active

## Q&A Prep (likely judge questions)

### Q: "Why voice, not WhatsApp or SMS?"
> Voice works for low-literacy populations, elderly users, and natural symptom capture. You can't describe chest pain effectively via text. SMS/WhatsApp is additive for reminders, but voice is primary for clinical signal collection.

### Q: "Is this replacing doctors?"
> No. It automates routine outreach and early signal collection. Every clinical decision stays with human care teams. Doctors approve, correct, or reject every AI extraction.

### Q: "How do you handle urgent cases?"
> Four-level triage: automated follow-up, coordinator notification, doctor priority queue, and immediate SOS routing. Each level has different response SLAs.

### Q: "How is this compliant?"
> DPDP Act 2023: explicit consent collection and revocation, audit trails for all data access, data deletion requests, and Supabase RLS for role-based access. FHIR R4 for structured clinical data aligned with ABDM profiles.

### Q: "Can this work beyond browser demo?"
> Yes. Current implementation uses WebRTC via LiveKit. Production path is a telephony bridge (SIP/Twilio) — same voice agent, same triage logic, same data layer. Only the transport changes.

### Q: "What's your moat vs a generic chatbot?"
> Healthcare workflow specificity. Multilingual clinical prompts, structured FHIR extraction, four-level triage automation, three role-based dashboards, and ABDM-aligned outputs — all in one integrated system. A chatbot gives you text. We give you actionable clinical intelligence.

### Q: "How did you build all this solo?"
> Supabase handles auth, database, realtime, and storage — that's the entire backend-as-a-service. LiveKit handles WebRTC complexity. I focused on clinical workflow logic and UI. The right tools let one developer build what would normally take a team.

## Killer Moves That Win Hackathons

1. **Live demo > slides** — 60 seconds of a real voice call → escalation appearing on doctor dashboard is worth more than all 5 slides combined
2. **Show the dataset** — "240 real patient records from health camp data" signals grounded-in-reality, not hypothetical
3. **Strategic name-drops** — Bhashini (India-specific), FHIR R4 (healthcare standards), DPDP Act (compliance maturity), ABDM (ecosystem awareness)
4. **Solo dev flex** — Mention once, casually: "Built end-to-end by one developer in one week." Let judges do the mental math against team sizes around you
5. **Don't read slides** — Know your script, maintain eye contact, speak with conviction. The slides support you, not the other way around

## Common Pitfalls to Avoid

| Pitfall | Why It Hurts | What to Do Instead |
|---------|-------------|-------------------|
| Reading slides word-for-word | Looks unprepared | Know your 45-second script per slide |
| Too much text on slides | Judges stop reading | Max 30-40 words per slide body |
| Showing code | Nobody reads code in 5 minutes | Show architecture diagrams and screenshots |
| Demoing with errors | Kills credibility | Test the full demo flow 3x before presenting |
| Saying "we plan to build X" | Sounds incomplete | Say "we built X, next we'll extend to Y" |
| Apologizing for being solo | Undermines your work | State it as a strength, not a limitation |
| Running over time | Judges penalize | Practice with a timer, aim for 4:30 |
