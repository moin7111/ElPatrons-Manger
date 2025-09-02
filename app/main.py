from fastapi import FastAPI
import os

try:
    import psycopg
except Exception:  # psycopg may not be available locally until installed
    psycopg = None

app = FastAPI(title="BLFantasy API")


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.get("/health/db")
async def health_db() -> dict:
    dsn = os.getenv("DATABASE_URL")
    if not dsn:
        return {"status": "degraded", "db": "DATABASE_URL missing"}

    if psycopg is None:
        return {"status": "degraded", "db": "psycopg not installed"}

    try:
        # Render connection strings typically include sslmode.
        with psycopg.connect(dsn, connect_timeout=5) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                cur.fetchone()
        return {"status": "ok", "db": "connected"}
    except Exception as exc:  # noqa: BLE001
        return {"status": "error", "db": str(exc)}