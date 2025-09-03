import os
from pathlib import Path
import psycopg


def get_connection_dsn() -> str:
	dsn = os.getenv("DATABASE_URL")
	if not dsn:
		raise RuntimeError("DATABASE_URL is not set")
	return dsn


def ensure_migrations_table(conn: psycopg.Connection) -> None:
	with conn.cursor() as cur:
		cur.execute(
			"""
			CREATE TABLE IF NOT EXISTS schema_migrations (
				id SERIAL PRIMARY KEY,
				filename TEXT NOT NULL UNIQUE,
				applied_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
			);
			"""
		)
		conn.commit()


def get_applied_filenames(conn: psycopg.Connection) -> set[str]:
	with conn.cursor() as cur:
		try:
			cur.execute("SELECT filename FROM schema_migrations")
			rows = cur.fetchall()
			return {r[0] for r in rows}
		except Exception:
			return set()


def apply_migration_file(conn: psycopg.Connection, file_path: Path) -> None:
	sql = file_path.read_text(encoding="utf-8")
	with conn.cursor() as cur:
		cur.execute(sql)
		cur.execute(
			"INSERT INTO schema_migrations (filename) VALUES (%s) ON CONFLICT DO NOTHING",
			(file_path.name,),
		)
		conn.commit()


def main() -> None:
	migrations_dir = Path(__file__).parent / "migrations"
	files = sorted([p for p in migrations_dir.glob("*.sql")])
	if not files:
		print("No migrations to apply.")
		return

	dsn = get_connection_dsn()
	with psycopg.connect(dsn) as conn:
		ensure_migrations_table(conn)
		applied = get_applied_filenames(conn)
		for fp in files:
			if fp.name in applied:
				continue
			print(f"Applying migration: {fp.name}")
			apply_migration_file(conn, fp)
	print("Migrations completed.")


if __name__ == "__main__":
	main()

