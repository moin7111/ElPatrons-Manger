"""
BLFantasy Pythonista Thin Client (with retries & longer timeout)

Usage on iPad (Pythonista):
1) Set API_BASE to your Render public URL
2) Optionally set API_KEY if your API requires auth
3) Run: this will call /health and /health/db with retries
"""

import json
import sys
import time
from typing import Any, Dict, Optional

try:
	import requests
except Exception:
	print("requests nicht verfügbar. Bitte Pythonista updaten.")
	raise

# --- Configuration ---
API_BASE = "https://blfantasy-api.onrender.com"  # <-- deine Render-URL hier eintragen
API_KEY: Optional[str] = "c36406e12f8357f0959aacf5ffea35ec"  # z.B. "xyz..." falls nötig

TIMEOUT_SEC = 60
MAX_RETRIES = 3
RETRY_SLEEP = 5  # seconds; increases linearly per attempt


def pretty(obj: Any) -> str:
	try:
		return json.dumps(obj, indent=2, ensure_ascii=False)
	except Exception:
		return str(obj)


def get_with_retry(session: requests.Session, url: str) -> requests.Response:
	last_err: Optional[Exception] = None
	for attempt in range(1, MAX_RETRIES + 1):
		try:
			return session.get(url, timeout=TIMEOUT_SEC)
		except requests.RequestException as exc:
			last_err = exc
			if attempt < MAX_RETRIES:
				sleep_for = RETRY_SLEEP * attempt
				print(f"Warnung: GET fehlgeschlagen, retry {attempt}/{MAX_RETRIES-1} in {sleep_for}s...")
				time.sleep(sleep_for)
	if last_err is not None:
		raise last_err
	# Fallback (sollte nie erreicht werden)
	raise RuntimeError("Unreachable: get_with_retry exhausted without exception")


class APIClient:
	def __init__(self, base_url: str, api_key: Optional[str] = None) -> None:
		self.base_url = base_url.rstrip("/")
		self.session = requests.Session()
		headers = {
			"Accept": "application/json",
			"User-Agent": "BLFantasy-iOS-Tester/1.1",
		}
		if api_key:
			# Falls du Header-Auth nutzt, einen davon aktivieren:
			headers["Authorization"] = f"Bearer {api_key}"
			# headers["X-API-Key"] = api_key
		self.session.headers.update(headers)

	def get(self, path: str) -> Dict[str, Any]:
		url = f"{self.base_url}{path}"
		try:
			resp = get_with_retry(self.session, url)
			data: Any
			try:
				data = resp.json()
			except Exception:
				data = {"raw": resp.text}
			return {"status_code": resp.status_code, "data": data}
		except requests.RequestException as exc:
			return {"status_code": None, "error": str(exc), "url": url}


# --- Tests ---

def test_health(api: APIClient) -> None:
	print("GET /health ...")
	res = api.get("/health")
	print(pretty(res))
	ok = res.get("status_code") == 200 and res.get("data", {}).get("status") == "ok"
	print(f"Ergebnis /health: {'OK' if ok else 'FEHLER'}\n")


def test_health_db(api: APIClient) -> None:
	print("GET /health/db ...")
	res = api.get("/health/db")
	print(pretty(res))
	status = res.get("data", {}).get("status")
	# Erwartet: "ok" wenn DB verbunden; "degraded" falls DATABASE_URL fehlt
	ok = status in {"ok", "degraded"}
	print(f"Ergebnis /health/db: {'OK' if ok else 'FEHLER'}\n")


def main() -> None:
	if not API_BASE.startswith("http"):
		print("Bitte API_BASE mit deiner Render-URL setzen (https://...).")
		sys.exit(1)

	api = APIClient(API_BASE, API_KEY)
	print(f"Teste gegen: {API_BASE}\n")

	# Optionales Aufwecken (kann Cold Starts abfangen)
	try:
		_ = get_with_retry(api.session, f"{api.base_url}/health")
	except Exception:
		pass

	test_health(api)
	time.sleep(0.3)
	test_health_db(api)

	print("Fertig. Falls Fehler auftreten:")
	print("- Prüfe, ob der Service in Render läuft")
	print("- Sieh dir /logs im Render-Dashboard an")
	print("- Setze ggf. DATABASE_URL und API_KEY als Secrets in Render")


if __name__ == "__main__":
	main()
