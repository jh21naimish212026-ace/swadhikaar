"""
Swadhikaar - FastAPI Backend
Voice AI Engine + FHIR Mapping Server

This server handles:
- LiveKit voice agent orchestration
- FHIR R4 resource generation (ABDM profiles)
- Triage/escalation logic
- Supabase integration for data persistence

NOTE: Supabase is the primary backend (mandatory).
FastAPI exists ONLY because LiveKit Agents SDK requires Python runtime.
"""

import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import voice, fhir, triage, patients
from services.risk_router import router as risk_router

load_dotenv()


def _parse_csv_env(var_name: str) -> list[str]:
    raw = os.getenv(var_name, "")
    return [item.strip() for item in raw.split(",") if item.strip()]


cors_origins = [
    "http://localhost:3000",
    "http://localhost:3001",
]

frontend_url = os.getenv("FRONTEND_URL", "").strip()
if frontend_url:
    cors_origins.append(frontend_url)

cors_origins.extend(_parse_csv_env("FRONTEND_URLS"))

seen = set()
cors_origins = [
    origin for origin in cors_origins if not (origin in seen or seen.add(origin))
]

app = FastAPI(
    title="Swadhikaar Voice AI Engine",
    description="Indic Voice AI Patient Engagement Platform - PS-3",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_origin_regex=os.getenv("FRONTEND_ORIGIN_REGEX") or None,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "service": "Swadhikaar Voice AI Engine",
        "status": "running",
        "version": "1.0.0",
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}


app.include_router(voice.router)
app.include_router(fhir.router)
app.include_router(triage.router)
app.include_router(patients.router)
app.include_router(risk_router)
