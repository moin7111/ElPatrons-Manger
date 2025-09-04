from fastapi import FastAPI
import os
from typing import List, Optional

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


# Optional private connector endpoints (guarded via env toggle)
try:
    from app.private_connector import build_connector_from_env
except Exception:
    build_connector_from_env = None


@app.get("/me/overview")
async def me_overview() -> dict:
    if not os.getenv("BLF_CONNECTOR_ENABLED") or build_connector_from_env is None:
        return {"enabled": False}
    try:
        conn = build_connector_from_env()
        data = conn.get_overview()
        return {"enabled": True, "data": data}
    except Exception as exc:
        return {"enabled": True, "error": str(exc)}


@app.get("/me/squad")
async def me_squad() -> dict:
    if not os.getenv("BLF_CONNECTOR_ENABLED") or build_connector_from_env is None:
        return {"enabled": False}
    try:
        conn = build_connector_from_env()
        data = conn.get_squad()
        return {"enabled": True, "data": data}
    except Exception as exc:
        return {"enabled": True, "error": str(exc)}


@app.get("/players")
async def list_players(limit: int = 100, offset: int = 0) -> dict:
    dsn = os.getenv("DATABASE_URL")
    if not dsn or psycopg is None:
        return {"players": []}
    rows: List[tuple] = []
    with psycopg.connect(dsn) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, name, position, team, market_value FROM players ORDER BY id LIMIT %s OFFSET %s",
                (limit, offset),
            )
            rows = cur.fetchall()
    players = [
        {
            "id": r[0],
            "name": r[1],
            "position": r[2],
            "team": r[3],
            "market_value": float(r[4]) if r[4] is not None else None,
        }
        for r in rows
    ]
    return {"players": players, "limit": limit, "offset": offset}


@app.get("/predictions/latest")
async def predictions_latest(limit: int = 100, offset: int = 0, model: Optional[str] = None) -> dict:
    dsn = os.getenv("DATABASE_URL")
    if not dsn or psycopg is None:
        return {"predictions": []}
    query = """
        SELECT p.player_id, p.model_name, p.pred_mean, p.pred_std
        FROM predictions_latest p
        WHERE (%s IS NULL OR p.model_name = %s)
        ORDER BY p.player_id
        LIMIT %s OFFSET %s
    """
    rows: List[tuple]
    with psycopg.connect(dsn) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (model, model, limit, offset))
            rows = cur.fetchall()
    preds = [
        {
            "player_id": r[0],
            "model_name": r[1],
            "pred_mean": float(r[2]),
            "pred_std": float(r[3]) if r[3] is not None else None,
        }
        for r in rows
    ]
    return {"predictions": preds, "limit": limit, "offset": offset, "model": model}


@app.get("/predict_team")
async def predict_team(size: int = 11, model: str = "baseline_v1") -> dict:
    """Very simple team selection: top N by prediction."""
    dsn = os.getenv("DATABASE_URL")
    if not dsn or psycopg is None:
        return {"team": [], "size": size, "model": model}
    query = """
        SELECT p.player_id, p.pred_mean
        FROM predictions_latest p
        WHERE p.model_name = %s
        ORDER BY p.pred_mean DESC
        LIMIT %s
    """
    with psycopg.connect(dsn) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (model, size))
            rows = cur.fetchall()
    team = [
        {"player_id": r[0], "pred_mean": float(r[1])}
        for r in rows
    ]
    return {"team": team, "size": size, "model": model}