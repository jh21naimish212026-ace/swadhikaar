# Swadhikaar

Indic Voice AI patient engagement platform built for HackMatrix 2.0 (Jilo Health PS-3).

Swadhikaar combines:
- multilingual voice follow-up calls,
- FastAPI orchestration for LiveKit voice agents,
- Supabase-backed patient workflows and realtime escalations,
- FHIR R4 resource generation with SNOMED/LOINC coding,
- role-based dashboards for patient, coordinator/doctor, and admin teams.

## What this repo contains

```text
swadhikaar/
|- frontend/                # Next.js 16 app (landing, auth, patient/doctor/admin portals)
|- backend/                 # FastAPI APIs, LiveKit worker, ML + FHIR services, seed scripts
|- supabase/migrations/     # Core migration(s)
|- dataset/                 # Hackathon datasets used for seeding/training
|- templates/landing/       # Static landing template assets
|- PLAN.md                  # Detailed product/architecture plan
`- README.md
```

## Current architecture (as implemented)

### Frontend
- Next.js `16.2.1` + React `19.2.4` (App Router)
- Tailwind CSS 4 + shadcn-style UI components
- Supabase client hooks for all dashboard data and mutations
- LiveKit voice widget in patient experience (`frontend/src/components/voice-agent-widget.tsx`)

### Backend
- FastAPI service with routers:
  - `/api/voice` (start/status/end call + token)
  - `/api/fhir` (generate/query/export FHIR bundles + drug mapping)
  - `/api/triage` (rule-based triage + escalation helpers)
  - `/api/patients` (list/detail/vitals/calls)
  - `/api/risk` (ML risk prediction endpoint)
- LiveKit worker (`backend/voice_agent/agent.py`) using Gemini native realtime audio via `livekit-plugins-google`
- scikit-learn risk model (`backend/services/risk_model.py`)
- FHIR resource generator (`backend/services/fhir_service.py`)

### Data layer
- Supabase/Postgres is the source of truth for app state
- Seed scripts populate synthetic patients + vitals + risk + symptoms + consent + demo escalations
- Includes workflow and vaccination tracking concepts (see schema notes below)

## Product capabilities in this repo

- Multilingual health follow-up voice calls (Hindi-first with mixed language support)
- Structured extraction from calls and persistence to `voice_calls`
- Rule-based triage (`LOW/MODERATE/HIGH/CRITICAL`) with escalation creation
- FHIR bundle generation for OPD consultation, diagnostic report, prescription, and health document records
- Drug brand to INN/SNOMED lookup for India-specific names
- Role-specific UI surfaces:
  - Patient: dashboard, records, calls, consent, embedded voice assistant
  - Doctor/Coordinator: priority queue, campaign outcomes, vaccination outreach workflow
  - Admin: operations dashboard, workflows, patient management, consent and reports

## Database schema notes

There are two schema files in this repo:

1. `supabase/migrations/001_initial_schema.sql`
   - Core PS-3 entities (patients, vitals, risk, symptoms, calls, FHIR, escalations, workflows, consents, audit).

2. `backend/migration_full_schema.sql`
   - Expanded schema used by current frontend features, including `doctors`, `newborns`, and `vaccination_schedules`.

If you want all current pages to work, apply the full schema file (or merge missing tables into your migration stack).

## Prerequisites

- Python 3.11+
- Node.js 18+
- Supabase project
- LiveKit Cloud project
- Google AI Studio API key (Gemini)

## Environment variables

### Backend (`backend/.env`)

Use `backend/.env.example` as reference.

```env
# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
SUPABASE_KEY=your-service-role-key

# Frontend origin for CORS
FRONTEND_URL=http://localhost:3000

# LiveKit
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your-livekit-key
LIVEKIT_API_SECRET=your-livekit-secret

# LLM
GOOGLE_API_KEY=your-gemini-key
```

### Frontend (`frontend/.env.local`)

```env
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
NEXT_PUBLIC_BACKEND_URL=
NEXT_PUBLIC_BACKEND_FALLBACK_URL=http://localhost:8000
```

`NEXT_PUBLIC_BACKEND_URL` should be the public backend URL used by deployed clients.
Keep it empty only for local frontend dev.

## Local setup

Open 3-4 terminals.

### 1) Install and run backend API

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
# source venv/bin/activate

pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 2) Run LiveKit voice worker

```bash
cd backend/voice_agent

# Windows
..\venv\Scripts\activate

# macOS/Linux
# source ../venv/bin/activate

python agent.py dev
# or: python agent.py start
```

### 3) Install and run frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000`.

## Deploy frontend to Vercel (backend stays local)

This repo supports deploying only `frontend/` to Vercel while running FastAPI + LiveKit worker locally.

1. Create a public tunnel to your local backend (`http://localhost:8000`) using tools like ngrok or Cloudflare Tunnel.
2. Set Vercel project root to `frontend/`.
3. Add Vercel env vars:
   - `NEXT_PUBLIC_SUPABASE_URL`
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
   - `NEXT_PUBLIC_BACKEND_URL=https://<your-public-backend-tunnel>`
4. In `backend/.env`, set CORS so your deployed frontend can call it:
   - `FRONTEND_URL=https://<your-vercel-domain>`
   - optionally `FRONTEND_URLS=https://<custom-domain>,https://<preview-domain>`
   - optionally `FRONTEND_ORIGIN_REGEX=https://.*\.vercel\.app`
5. Run backend API + voice worker locally and keep tunnel running.

Important: if backend stays on your machine, the app depends on your PC/network being online. Other users can use the deployed frontend only while your local backend and tunnel are up and reachable.

### 4) Seed demo data (recommended)

```bash
cd backend

# activate venv first
python seed_data.py
python seed_escalations.py
```

## Key API endpoints

### Health
- `GET /`
- `GET /health`

### Voice
- `POST /api/voice/start`
- `POST /api/voice/end/{call_id}`
- `GET /api/voice/status/{call_id}`
- `GET /api/voice/token`

### Triage
- `POST /api/triage/assess`
- `POST /api/triage/escalate`
- `GET /api/triage/escalations`
- `POST /api/triage/escalations/{escalation_id}/resolve`

### FHIR
- `POST /api/fhir/generate`
- `POST /api/fhir/generate/diagnostic-report`
- `POST /api/fhir/generate/prescription`
- `GET /api/fhir/resources/{patient_id}`
- `POST /api/fhir/export/{patient_id}`
- `GET /api/fhir/drug-mapping/{brand_name}`

### Patients and risk
- `GET /api/patients/`
- `GET /api/patients/{patient_id}`
- `GET /api/patients/{patient_id}/vitals`
- `GET /api/patients/{patient_id}/calls`
- `POST /api/risk/predict`

## Demo login accounts (frontend)

The login page includes prefilled test credentials:
- `patient@swadhikaar.in` / `patient123`
- `coordinator@swadhikaar.in` / `coordinator123`
- `admin@swadhikaar.in` / `admin123`

## Known implementation notes

- The voice worker currently uses Gemini native audio in LiveKit; a Bhashini plugin exists in the repo but is not the active primary path.
- `frontend/src/hooks/use-supabase.ts` expects expanded tables (`doctors`, `newborns`, `vaccination_schedules`) that are present in `backend/migration_full_schema.sql`.
- Fallback/demo behaviors exist in multiple endpoints when env vars are not configured.

## Learning and Q/A prep checklist

Use this order when preparing for demos/presentations:

1. Explain system flow: Patient voice interaction -> extraction -> triage -> escalation -> dashboard action.
2. Walk through backend contracts (voice, triage, FHIR, risk APIs).
3. Show schema-level mapping to healthcare operations (calls, FHIR, consents, audit).
4. Demo one critical scenario end-to-end using patient + coordinator/admin views.
5. Discuss tradeoffs: browser WebRTC demo now, telephony bridge as production extension.

## Useful docs in this repo

- `PLAN.md` - deep architecture, flow design, judging alignment, and delivery plan
- `backend/.env.example` - backend env template
- `frontend/README.md` - default Next.js scaffold readme (not project-specific)

## License / attribution

Hackathon MVP repository for HackMatrix 2.0 (IIT Patna, Jilo Health PS-3).
