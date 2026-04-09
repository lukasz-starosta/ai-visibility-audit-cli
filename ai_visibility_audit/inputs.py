from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class AuditRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    domain: str = Field(description="Owned domain to audit, e.g. promptscout.app")
    page_limit: int = Field(default=10, ge=1, le=50)
    citation_urls: list[str] = Field(default_factory=list)
    pinned_urls: list[str] = Field(default_factory=list)
