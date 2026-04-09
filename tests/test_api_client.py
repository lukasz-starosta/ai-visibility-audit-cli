from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, Mock, patch

import pytest

from ai_visibility_audit.api_client import (
    DEFAULT_BRAND_ID,
    AuditApiConfig,
    request_live_scan,
    resolve_api_config,
)
from ai_visibility_audit.inputs import AuditRequest


def test_resolve_api_config_uses_primary_and_fallback_envs(monkeypatch) -> None:
    monkeypatch.setenv("PROMPT_SUGGESTION_API_URL", "https://prompt-api.example.com")
    monkeypatch.setenv("PROMPT_SUGGESTION_API_KEY", "test-key")

    config = resolve_api_config(
        api_url=None,
        api_key=None,
        brand_id=None,
        timeout_seconds=45.0,
    )

    assert config == AuditApiConfig(
        api_url="https://prompt-api.example.com",
        api_key="test-key",
        brand_id=DEFAULT_BRAND_ID,
        timeout_seconds=45.0,
    )


def test_resolve_api_config_prefers_explicit_values(monkeypatch) -> None:
    monkeypatch.setenv("AI_VISIBILITY_AUDIT_API_URL", "https://ignored.example.com")
    monkeypatch.setenv("AI_VISIBILITY_AUDIT_API_KEY", "ignored-key")
    monkeypatch.setenv("AI_VISIBILITY_AUDIT_BRAND_ID", "ignored-brand")

    config = resolve_api_config(
        api_url="https://audit.example.com/",
        api_key="direct-key",
        brand_id="direct-brand",
        timeout_seconds=12.0,
    )

    assert config == AuditApiConfig(
        api_url="https://audit.example.com",
        api_key="direct-key",
        brand_id="direct-brand",
        timeout_seconds=12.0,
    )


def test_resolve_api_config_errors_when_api_url_missing(monkeypatch) -> None:
    monkeypatch.delenv("AI_VISIBILITY_AUDIT_API_URL", raising=False)
    monkeypatch.delenv("PROMPT_SUGGESTION_API_URL", raising=False)
    monkeypatch.setenv("PROMPT_SUGGESTION_API_KEY", "test-key")

    with pytest.raises(ValueError, match="Missing API URL"):
        resolve_api_config(
            api_url=None,
            api_key=None,
            brand_id=None,
            timeout_seconds=30.0,
        )


def test_request_live_scan_calls_configured_endpoint() -> None:
    config = AuditApiConfig(
        api_url="https://prompt-api.example.com",
        api_key="test-key",
        brand_id="brand 1",
        timeout_seconds=15.0,
    )
    request = AuditRequest(domain="example.com", page_limit=5)
    response = Mock()
    response.is_success = True
    response.json.return_value = {"brand_id": "brand 1", "ok": True}
    post = AsyncMock(return_value=response)

    with patch("ai_visibility_audit.api_client.httpx.AsyncClient.post", post):
        payload = asyncio.run(request_live_scan(request, config))

    assert payload == {"brand_id": "brand 1", "ok": True}
    post.assert_awaited_once()
    _, kwargs = post.await_args
    assert kwargs["headers"] == {"x-api-key": "test-key"}
    assert kwargs["json"] == {
        "domain": "example.com",
        "page_limit": 5,
        "citation_urls": [],
        "pinned_urls": [],
    }


def test_request_live_scan_surfaces_api_errors() -> None:
    config = AuditApiConfig(
        api_url="https://prompt-api.example.com",
        api_key="test-key",
        brand_id=DEFAULT_BRAND_ID,
        timeout_seconds=15.0,
    )
    request = AuditRequest(domain="example.com")
    response = Mock()
    response.is_success = False
    response.status_code = 401
    response.json.return_value = {"detail": "Unauthorized"}
    post = AsyncMock(return_value=response)

    with (
        patch("ai_visibility_audit.api_client.httpx.AsyncClient.post", post),
        pytest.raises(RuntimeError, match="401"),
    ):
        asyncio.run(request_live_scan(request, config))
