from __future__ import annotations
import os
import json
import time
import asyncio
from typing import Optional, Dict
import httpx
from loguru import logger
from .models import LocatorResult
from .exceptions import (
    Talk2DomError,
    AuthError,
    RateLimitError,
    RemoteError,
    BadRequestError,
)


class Talk2DomClient:
    """
    Minimal client for Talk2Dom API (no local cache).

    Expected API:
      POST {endpoint}/api/v1/locate
      Body: {"instruction","html","url"}
      Return: {"selector_type","selector_value"}
    """

    def __init__(
        self,
        api_key: str = None,
        project_id: str = None,
        timeout_s: float = 30.0,
        retries: int = 2,
        backoff_base: float = 0.5,
        endpoint: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> None:
        self.endpoint = (
            endpoint or os.getenv("T2D_ENDPOINT") or "https://api.talk2dom.itbanque.com"
        ).rstrip("/")
        self.api_key = api_key or os.getenv("T2D_API_KEY")
        self.project_id = project_id or os.getenv("T2D_PROJECT_ID")
        self.timeout_s = timeout_s
        self.retries = retries
        self.backoff_base = backoff_base
        if not self.api_key:
            raise Talk2DomError("Need Talk2Dom API key")
        if not self.project_id:
            raise Talk2DomError("Need Talk2Dom project ID")
        base_headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-Project-ID": self.project_id,
        }
        if headers:
            base_headers.update(headers)
        self.headers = {k: v for k, v in base_headers.items() if v}
        self._client = httpx.Client(timeout=self.timeout_s, headers=self.headers)
        self._aclient = httpx.AsyncClient(timeout=self.timeout_s, headers=self.headers)

    # ---------- sync ----------
    def locate(
        self,
        instruction: str,
        html: str,
        url: str,
        path: str = "/api/v1/inference/locator",
    ) -> LocatorResult:
        payload = {"user_instruction": instruction, "html": html, "url": url}
        data = self._post_with_retry(path, payload)
        logger.info(f"Location response: {data}")
        return LocatorResult(
            action_type=data.get("action_type"),
            action_value=data.get("action_value"),
            selector_type=data.get("selector_type"),
            selector_value=data["selector_value"],
        )

    # ---------- async ----------
    async def alocate(
        self,
        instruction: str,
        html: str,
        url: Optional[str] = None,
        path: str = "/api/v1/inference/locator",
    ) -> LocatorResult:
        payload = {
            "user_instruction": instruction,
            "html": html,
            "url": url or "",
        }
        data = await self._apost_with_retry(path, payload)
        return LocatorResult(
            selector_type=data.get("selector_type"),
            selector_value=data["selector_value"],
        )

    # ---------- internals ----------
    def _post_with_retry(self, path: str, payload: dict) -> dict:
        url = f"{self.endpoint}{path}"
        backoff = self.backoff_base
        for attempt in range(self.retries + 1):
            try:
                resp = self._client.post(url, content=json.dumps(payload))
                if resp.status_code == 401:
                    raise AuthError("Unauthorized (401): invalid API key or project.")
                if resp.status_code == 429:
                    raise RateLimitError("Rate limited (429).")
                if resp.status_code == 400:
                    raise BadRequestError(f"Bad Request (400): {resp.text}")
                if 500 <= resp.status_code < 600:
                    raise RemoteError(f"Server error {resp.status_code}: {resp.text}")
                if resp.status_code >= 300:
                    raise RemoteError(f"HTTP {resp.status_code}: {resp.text}")
                data = resp.json()
                return data.get("result", data)
            except (RateLimitError, RemoteError):
                if attempt < self.retries:
                    time.sleep(backoff)
                    backoff *= 2
                    continue
                raise
            except Exception:
                if attempt < self.retries:
                    time.sleep(backoff)
                    backoff *= 2
                    continue
                raise

    async def _apost_with_retry(self, path: str, payload: dict) -> dict:
        url = f"{self.endpoint}{path}"
        backoff = self.backoff_base
        for attempt in range(self.retries + 1):
            try:
                resp = await self._aclient.post(url, content=json.dumps(payload))
                if resp.status_code == 401:
                    raise AuthError("Unauthorized (401): invalid API key or project.")
                if resp.status_code == 429:
                    raise RateLimitError("Rate limited (429).")
                if resp.status_code == 400:
                    body = await resp.aread()
                    raise BadRequestError(f"Bad Request (400): {body!r}")
                if 500 <= resp.status_code < 600:
                    body = await resp.aread()
                    raise RemoteError(f"Server error {resp.status_code}: {body!r}")
                if resp.status_code >= 300:
                    body = await resp.aread()
                    raise RemoteError(f"HTTP {resp.status_code}: {body!r}")
                data = resp.json()
                return data.get("result", data)
            except (RateLimitError, RemoteError):
                if attempt < self.retries:
                    await asyncio.sleep(backoff)
                    backoff *= 2
                    continue
                raise
            except Exception:
                if attempt < self.retries:
                    await asyncio.sleep(backoff)
                    backoff *= 2
                    continue
                raise
