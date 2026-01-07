import os
from typing import Optional

from pathlib import Path

try:
    # optional dotenv support if available in environment
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass


def get_database_url() -> str:
    """Return database URL from env or fallback to a local sqlite file.

    The documentation suggests Supabase/Postgres in production. For local
    development we fall back to sqlite so the app can run without extra
    configuration.
    """
    url = os.getenv("DATABASE_URL")
    if url:
        return url
    db_file = Path(os.getenv("DATABASE_FILE", "./bus_tracking.db")).resolve()
    return f"sqlite:///{db_file}"


def get_supabase_url() -> Optional[str]:
    return os.getenv("SUPABASE_URL")


def get_supabase_key() -> Optional[str]:
    return os.getenv("SUPABASE_KEY")
