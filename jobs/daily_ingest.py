import os
import psycopg


def main() -> None:
    print("[cron] daily_ingest executed", flush=True)
    dsn = os.getenv("DATABASE_URL")
    if not dsn:
        print("[cron] DATABASE_URL not set, skipping DB write", flush=True)
        return
    try:
        with psycopg.connect(dsn) as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO players (name, position, team) VALUES (%s,%s,%s) ON CONFLICT DO NOTHING",
                            ("Example Player", "MID", "Demo FC"))
                conn.commit()
        print("[cron] sample DB write ok", flush=True)
    except Exception as exc:
        print(f"[cron] DB write failed: {exc}", flush=True)


if __name__ == "__main__":
    main()