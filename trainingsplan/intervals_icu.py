"""Minimaler Client für die intervals.icu REST-API (nur Standardbibliothek).

Authentifizierung: HTTP Basic mit Benutzername ``API_KEY`` und dem
persönlichen API-Key als Passwort (intervals.icu > Settings > Developer).
Athleten-ID ``0`` steht für den Athleten, dem der API-Key gehört.
"""

from __future__ import annotations

import base64
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from datetime import date

BASE_URL = "https://intervals.icu/api/v1"


class IntervalsError(RuntimeError):
    pass


class IntervalsClient:
    def __init__(self, api_key: str | None = None, athlete_id: str | None = None,
                 base_url: str = BASE_URL, timeout: float = 30.0):
        self.api_key = api_key or os.environ.get("INTERVALS_API_KEY")
        if not self.api_key:
            raise IntervalsError(
                "Kein API-Key gefunden. Setze INTERVALS_API_KEY "
                "(intervals.icu > Settings > Developer Settings).")
        self.athlete_id = athlete_id or os.environ.get("INTERVALS_ATHLETE_ID", "0")
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        token = base64.b64encode(f"API_KEY:{self.api_key}".encode()).decode()
        self._auth = f"Basic {token}"

    # -- intern -----------------------------------------------------------
    def _request(self, method: str, path: str, params: dict | None = None,
                 body: object | None = None):
        url = f"{self.base_url}{path}"
        if params:
            url += "?" + urllib.parse.urlencode(params)
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("Authorization", self._auth)
        req.add_header("Accept", "application/json")
        if data is not None:
            req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                raw = resp.read()
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode(errors="replace")[:500]
            raise IntervalsError(f"{method} {path} -> HTTP {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise IntervalsError(f"{method} {path} fehlgeschlagen: {exc.reason}") from exc
        return json.loads(raw) if raw else None

    def _athlete(self, suffix: str) -> str:
        return f"/athlete/{self.athlete_id}{suffix}"

    # -- Lesen ------------------------------------------------------------
    def athlete(self) -> dict:
        return self._request("GET", self._athlete(""))

    def wellness(self, oldest: date, newest: date) -> list[dict]:
        """Tägliche Wellness-Daten: ctl, atl, rampRate, restingHR, hrv,
        sleepSecs, sleepScore, readiness, fatigue, soreness, stress, mood …"""
        return self._request("GET", self._athlete("/wellness"),
                             {"oldest": oldest.isoformat(), "newest": newest.isoformat()}) or []

    def activities(self, oldest: date, newest: date) -> list[dict]:
        return self._request("GET", self._athlete("/activities"),
                             {"oldest": oldest.isoformat(), "newest": newest.isoformat()}) or []

    def events(self, oldest: date, newest: date, category: str = "WORKOUT") -> list[dict]:
        return self._request("GET", self._athlete("/events"),
                             {"oldest": oldest.isoformat(), "newest": newest.isoformat(),
                              "category": category}) or []

    # -- Schreiben --------------------------------------------------------
    def upsert_events(self, events: list[dict]) -> list[dict]:
        """Legt geplante Workouts an bzw. aktualisiert sie (Match über external_id)."""
        if not events:
            return []
        return self._request("POST", self._athlete("/events/bulk"),
                             {"upsert": "true"}, events) or []
