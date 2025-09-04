from __future__ import annotations

import os
import psycopg
from app.baseline_model import PlayerFeature, simple_heuristic


def main() -> None:
    print("[cron] prematch_pull executed", flush=True)
    dsn = os.getenv("DATABASE_URL")
    if not dsn:
        print("[cron] DATABASE_URL not set, skipping predictions", flush=True)
        return

    try:
        with psycopg.connect(dsn) as conn:
            with conn.cursor() as cur:
                # mark run start
                cur.execute("INSERT INTO job_runs (job_name, status) VALUES (%s, %s) RETURNING id", ("prematch_pull", "started"))
                run_id = cur.fetchone()[0]

                cur.execute("SELECT id, position, team, market_value FROM players")
                rows = cur.fetchall()
                feats = [
                    PlayerFeature(
                        player_id=r[0],
                        position=r[1] or "UNK",
                        team=r[2] or "UNK",
                        market_value=(float(r[3]) if r[3] is not None else None),
                    )
                    for r in rows
                ]

                preds = simple_heuristic(feats)
                for p in preds:
                    cur.execute(
                        """
                        INSERT INTO predictions (player_id, model_name, pred_mean, pred_std)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (player_id, model_name, as_of_date)
                        DO UPDATE SET pred_mean = EXCLUDED.pred_mean, pred_std = EXCLUDED.pred_std
                        """,
                        (p.player_id, "baseline_v1", p.pred_mean, p.pred_std),
                    )
                # mark run done
                cur.execute(
                    "UPDATE job_runs SET status = 'completed', finished_at = NOW(), details = jsonb_build_object('predictions', %s) WHERE id = %s",
                    (len(preds), run_id),
                )
                conn.commit()
        print("[cron] predictions upserted", flush=True)
    except Exception as exc:
        print(f"[cron] prediction job failed: {exc}", flush=True)


if __name__ == "__main__":
    main()