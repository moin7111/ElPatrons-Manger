from __future__ import annotations

import os
from typing import Optional

import requests


class BLFantasyConnector:
	"""Private read-only connector using a session cookie/token stored in env.

	This is illustrative; adjust endpoint URLs and headers to match the real app's network calls,
	and keep usage within TOS. Do not commit secrets; pass them via environment variables.
	"""

	def __init__(self, base_url: str, session_cookie: Optional[str]) -> None:
		self.base_url = base_url.rstrip("/")
		self.session = requests.Session()
		headers = {"User-Agent": "BLFantasy-Connector/1.0"}
		self.session.headers.update(headers)
		if session_cookie:
			self.session.headers["Cookie"] = session_cookie

	def get_overview(self) -> dict:
		# Placeholder path; replace with actual
		url = f"{self.base_url}/api/me/overview"
		resp = self.session.get(url, timeout=20)
		resp.raise_for_status()
		return resp.json()

	def get_squad(self) -> dict:
		url = f"{self.base_url}/api/me/squad"
		resp = self.session.get(url, timeout=20)
		resp.raise_for_status()
		return resp.json()

	def get_prices(self) -> dict:
		url = f"{self.base_url}/api/prices"
		resp = self.session.get(url, timeout=20)
		resp.raise_for_status()
		return resp.json()


def build_connector_from_env() -> BLFantasyConnector:
	base = os.getenv("BLF_BASE_URL", "https://fantasy.bundesliga.com")
	cookie = os.getenv("BLF_SESSION")  # e.g., "session=abc123; Path=/; ..."
	return BLFantasyConnector(base, cookie)

