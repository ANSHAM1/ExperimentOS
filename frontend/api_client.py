from __future__ import annotations

from typing import Any

import requests


class APIError(Exception):
    """Raised when the backend is unreachable or returns a hard HTTP error."""


class APIClient:
    def __init__(self, base_url: str, session: requests.Session, timeout: float = 15.0):
        self.base_url = base_url.rstrip("/")
        self.session = session
        self.timeout = timeout

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def _request(self, method: str, path: str, **kwargs) -> requests.Response:
        try:
            return self.session.request(method, self._url(path), timeout=self.timeout, **kwargs)
        except requests.exceptions.RequestException as exc:
            raise APIError(f"Could not reach {self.base_url}{path}: {exc}") from exc

    # ---------------- Auth ----------------

    def login(self, email: str, password: str) -> dict[str, Any]:
        resp = self._request("POST", "/auth/login", json={"email": email, "password": password})
        resp.raise_for_status()
        return resp.json()

    def register(self, email: str, password: str) -> dict[str, Any]:
        resp = self._request("POST", "/auth/register", json={"email": email, "password": password})
        resp.raise_for_status()
        return resp.json()

    def verify_email(self, email: str, otp: str) -> dict[str, Any]:
        resp = self._request("POST", "/auth/verify", json={"email": email, "otp": otp})
        resp.raise_for_status()
        return resp.json()

    def refresh(self) -> dict[str, Any]:
        # session_id + refresh_token cookies ride along automatically.
        resp = self._request("POST", "/auth/refresh")
        resp.raise_for_status()
        return resp.json()

    # ------------- Authenticated -------------

    @staticmethod
    def _auth_headers(access_token: str) -> dict[str, str]:
        return {"Authorization": f"Bearer {access_token}"}

    def submit_experiment(self, access_token: str, prompt: str) -> requests.Response:
        """Returns the raw Response so callers can inspect status codes (401 etc.)."""
        return self._request(
            "POST",
            "/experiment/",
            json={"prompt": prompt},
            headers=self._auth_headers(access_token),
        )

    def get_experiment_status(self, access_token: str, experiment_id: str) -> requests.Response:
        """
        Best-effort status lookup. Not part of the backend today -- see README.
        Expected (suggested) shape: GET /experiment/{id} -> {"status": "pending"|"completed"|"failed", ...}
        Callers must handle 404/405 gracefully since this endpoint may not exist yet.
        """
        return self._request(
            "GET",
            f"/experiment/{experiment_id}",
            headers=self._auth_headers(access_token),
        )
