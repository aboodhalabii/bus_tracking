#!/usr/bin/env bash
set -euo pipefail

if [ -z "${VIRTUAL_ENV:-}" ]; then
  if [ -f .venv/bin/activate ]; then
    # shellcheck disable=SC1091
    source .venv/bin/activate
  else
    echo "No virtualenv detected. Create one with: python3 -m venv .venv" >&2
  fi
fi

echo "Starting uvicorn on http://127.0.0.1:8000"
exec uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
