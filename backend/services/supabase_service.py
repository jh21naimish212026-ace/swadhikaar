"""Shared Supabase client for FastAPI routers."""

import os
from typing import Optional

from supabase import Client, create_client


def get_supabase_client() -> Optional[Client]:
    """Return a Supabase client when env vars are available."""
    url = os.getenv("SUPABASE_URL", "")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "") or os.getenv("SUPABASE_KEY", "")
    if not url or not key:
        return None

    try:
        return create_client(url, key)
    except Exception:
        return None
