AAU Bus Tracking API
====================

Quickstart (development)
------------------------

1. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. (Optional) set a JWT secret for tokens (if you want custom secret):

```bash
export JWT_SECRET="a-strong-secret"
```

4. Start the server:

```bash
./scripts/run.sh
```

5. Open API docs: http://127.0.0.1:8000/docs

Notes
-----
- The app uses a SQLite fallback if `DATABASE_URL` is not set.
- Auth is currently implemented using JWTs issued by the `/auth/login` endpoint. For production you should integrate Supabase Auth or JWKS-based verification.
- Database tables are created automatically at app startup using SQLAlchemy metadata. For production use Alembic migrations.

Next steps you may want me to do:
- Scaffold Alembic migrations.
- Integrate Supabase JWKS verification for RS256 tokens.
- Add WebSocket endpoint for realtime location updates.
