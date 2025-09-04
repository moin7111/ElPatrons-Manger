from __future__ import annotations

import os
import re
from typing import Iterable, List, Tuple

import psycopg
import requests


KEYWORDS_INJURED = [
	"verletzt",
	"injured",
	"muscle",
	"hamstring",
	"bänderriss",
	"kreuzband",
	"fällt aus",
]
KEYWORDS_DOUBTFUL = ["fraglich", "doubtful", "angeschlagen", "questionable"]


def classify_status(text: str) -> Tuple[str, str]:
	l = text.lower()
	if any(k in l for k in KEYWORDS_INJURED):
		return ("injured", text)
	if any(k in l for k in KEYWORDS_DOUBTFUL):
		return ("doubtful", text)
	return ("ok", text)


def load_feeds() -> List[str]:
	feeds_env = os.getenv("NEWS_FEEDS", "")
	feeds = [f.strip() for f in feeds_env.split(",") if f.strip()]
	return feeds


def fetch_feed_items(url: str) -> List[Tuple[str, str]]:
	# Minimal generic fetch: expect JSON array of objects with 'title' or 'summary'
	# For RSS, consider feedparser; here we keep it dependency-light.
	try:
		resp = requests.get(url, timeout=15)
		resp.raise_for_status()
		data = resp.json()
		items = []
		for it in data if isinstance(data, list) else data.get("items", []):
			title = it.get("title") or ""
			summary = it.get("summary") or it.get("description") or ""
			items.append((title, summary))
		return items
	except Exception:
		return []


def find_player_ids(conn: psycopg.Connection, text: str) -> List[int]:
	# naive name matching by full token; improve later with fuzzy matching
	with conn.cursor() as cur:
		cur.execute("SELECT id, name FROM players")
		rows = cur.fetchall()
	ids: List[int] = []
	for pid, name in rows:
		if not name:
			continue
		pattern = r"\b" + re.escape(name.lower()) + r"\b"
		if re.search(pattern, text.lower()):
			ids.append(pid)
	return ids


def main() -> None:
	feeds = load_feeds()
	if not feeds:
		print("[news] no NEWS_FEEDS configured", flush=True)
		return

	dsn = os.getenv("DATABASE_URL")
	if not dsn:
		print("[news] DATABASE_URL missing", flush=True)
		return

	with psycopg.connect(dsn) as conn:
		for url in feeds:
			items = fetch_feed_items(url)
			for title, summary in items:
				status, note = classify_status(" ".join([title or "", summary or ""]))
				if status == "ok":
					continue
				player_ids = find_player_ids(conn, f"{title} {summary}")
				with conn.cursor() as cur:
					for pid in player_ids:
						cur.execute(
							"INSERT INTO injuries (player_id, status, note, source, active) VALUES (%s,%s,%s,%s,TRUE)",
							(pid, status, note[:500], url),
						)
					conn.commit()
	print("[news] ingest completed", flush=True)


if __name__ == "__main__":
	main()

