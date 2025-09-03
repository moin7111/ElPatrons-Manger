import os
import requests
import psycopg


def main() -> None:
    print("[cron] daily_ingest executed", flush=True)
    dsn = os.getenv("DATABASE_URL")
    if not dsn:
        print("[cron] DATABASE_URL not set, skipping DB write", flush=True)
        return
    try:
        players_url = os.getenv("PLAYERS_SOURCE_URL")
        if players_url:
            print(f"[cron] fetching players from {players_url}", flush=True)
            try:
                resp = requests.get(players_url, timeout=20)
                resp.raise_for_status()
                payload = resp.json()
                players = payload if isinstance(payload, list) else payload.get("players", [])
            except Exception as exc:
                print(f"[cron] fetch failed: {exc}", flush=True)
                players = []
        else:
            players = []

        with psycopg.connect(dsn) as conn:
            with conn.cursor() as cur:
                # Fallback demo row if no players
                if not players:
                    cur.execute(
                        "INSERT INTO players (name, position, team) VALUES (%s,%s,%s) ON CONFLICT DO NOTHING",
                        ("Example Player", "MID", "Demo FC"),
                    )
                else:
                    for p in players:
                        name = p.get("name") or p.get("player") or "Unknown"
                        position = p.get("position") or "UNK"
                        team = p.get("team") or p.get("club") or "Unknown"
                        cur.execute(
                            "INSERT INTO players (name, position, team) VALUES (%s,%s,%s) ON CONFLICT DO NOTHING",
                            (name, position, team),
                        )
                conn.commit()
        print("[cron] ingest completed", flush=True)
    except Exception as exc:
        print(f"[cron] DB write failed: {exc}", flush=True)


if __name__ == "__main__":
    main()