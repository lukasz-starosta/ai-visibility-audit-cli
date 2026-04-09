from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any
from urllib.parse import quote

import httpx

from .inputs import AuditRequest

DEFAULT_BRAND_ID = "ai-visibility-audit-cli"
DEFAULT_TIMEOUT_SECONDS = 30.0


def _pick_env(*keys: str) -> str | None:
    for key in keys:
        value = os.environ.get(key)
        if value:
            return value
    return None


@dataclass(frozen=True)
class AuditApiConfig:
    api_url: str
    api_key: str
    brand_id: str
    timeout_seconds: float


def resolve_api_config(
    *,
    api_url: str | None,
    api_key: str | None,
    brand_id: str | None,
    timeout_seconds: float | None = None,
) -> AuditApiConfig:
    resolved_url = api_url or _pick_env(
        "AI_VISIBILITY_AUDIT_API_URL",
        "PROMPT_SUGGESTION_API_URL",
    )
    if not resolved_url:
        raise ValueError(
            "Missing API URL. Set --api-url, AI_VISIBILITY_AUDIT_API_URL, or PROMPT_SUGGESTION_API_URL."
        )

    resolved_key = api_key or _pick_env(
        "AI_VISIBILITY_AUDIT_API_KEY",
        "PROMPT_SUGGESTION_API_KEY",
    )
    if not resolved_key:
        raise ValueError(
            "Missing API key. Set --api-key, AI_VISIBILITY_AUDIT_API_KEY, or PROMPT_SUGGESTION_API_KEY."
        )

    resolved_brand_id = (
        brand_id
        or _pick_env(
            "AI_VISIBILITY_AUDIT_BRAND_ID",
            "PROMPT_SUGGESTION_BRAND_ID",
        )
        or DEFAULT_BRAND_ID
    )
    resolved_timeout = (
        timeout_seconds if timeout_seconds is not None else DEFAULT_TIMEOUT_SECONDS
    )
    if resolved_timeout <= 0:
        raise ValueError("Timeout must be greater than zero seconds.")

    return AuditApiConfig(
        api_url=resolved_url.rstrip("/"),
        api_key=resolved_key,
        brand_id=resolved_brand_id,
        timeout_seconds=resolved_timeout,
    )


async def request_live_scan(
    request: AuditRequest,
    config: AuditApiConfig,
) -> dict[str, Any]:
    endpoint = (
        f"{config.api_url}/v1/brands/{quote(config.brand_id, safe='')}/website-scan"
    )
    headers = {"x-api-key": config.api_key}

    async with httpx.AsyncClient(timeout=config.timeout_seconds) as client:
        response = await client.post(
            endpoint,
            headers=headers,
            json=request.model_dump(mode="json"),
        )

    if response.is_success:
        return response.json()

    detail: str
    try:
        payload = response.json()
    except json.JSONDecodeError:
        detail = response.text.strip() or "unknown error"
    else:
        if isinstance(payload, dict) and "detail" in payload:
            raw_detail = payload["detail"]
            if isinstance(raw_detail, str):
                detail = raw_detail
            else:
                detail = json.dumps(raw_detail, ensure_ascii=True)
        else:
            detail = json.dumps(payload, ensure_ascii=True)

    raise RuntimeError(
        f"Website scan API request failed ({response.status_code}): {detail}"
    )
