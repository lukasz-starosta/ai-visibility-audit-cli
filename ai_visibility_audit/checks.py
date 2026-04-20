from __future__ import annotations

from dataclasses import asdict, dataclass


CHECKS_VERSION = "website_scan_v2"


@dataclass(frozen=True)
class CheckDefinition:
    key: str
    title: str
    area: str
    severity: str
    description: str


BASELINE_CHECKS: tuple[CheckDefinition, ...] = (
    CheckDefinition(
        key="robots_disallow_all",
        title="All crawlers blocked",
        area="crawl access",
        severity="critical",
        description="robots.txt blocks all crawling across the whole site.",
    ),
    CheckDefinition(
        key="ai_bot_access_blocked",
        title="AI crawlers blocked",
        area="crawl access",
        severity="high",
        description="robots.txt blocks one or more major AI crawlers.",
    ),
    CheckDefinition(
        key="robots_missing",
        title="robots.txt missing",
        area="crawl access",
        severity="medium",
        description="robots.txt could not be found on the owned domain.",
    ),
    CheckDefinition(
        key="sitemap_missing_or_empty",
        title="Sitemap missing or empty",
        area="discovery",
        severity="high",
        description="No sitemap URLs were discovered for the site.",
    ),
    CheckDefinition(
        key="page_fetch_failed",
        title="Page fetch failed",
        area="reachability",
        severity="high",
        description="A scanned page could not be reached or timed out.",
    ),
    CheckDefinition(
        key="missing_title",
        title="Title missing",
        area="page structure",
        severity="medium",
        description="A scanned page is missing a usable title element.",
    ),
    CheckDefinition(
        key="missing_meta_description",
        title="Meta description missing",
        area="page structure",
        severity="low",
        description="A scanned page is missing a meta description.",
    ),
    CheckDefinition(
        key="missing_primary_heading",
        title="Primary heading missing",
        area="page structure",
        severity="medium",
        description="A scanned page is missing a clear primary heading.",
    ),
    CheckDefinition(
        key="multiple_primary_headings",
        title="Multiple primary headings",
        area="page structure",
        severity="low",
        description="A scanned page appears to have more than one primary heading.",
    ),
    CheckDefinition(
        key="thin_visible_content",
        title="Thin visible content",
        area="extractability",
        severity="medium",
        description="A scanned page looks too thin to quote or reuse confidently.",
    ),
    CheckDefinition(
        key="missing_schema_markup",
        title="Structured data missing",
        area="schema",
        severity="medium",
        description="A scanned page is missing structured data markup.",
    ),
    CheckDefinition(
        key="cross_domain_canonical",
        title="Cross-domain canonical",
        area="attribution",
        severity="high",
        description="A page points its canonical URL to a different domain.",
    ),
    CheckDefinition(
        key="stale_content_signal",
        title="Stale content signal",
        area="freshness",
        severity="low",
        description="A page appears outdated based on a detected freshness signal.",
    ),
)


def list_checks() -> list[dict[str, str]]:
    return [asdict(check) for check in BASELINE_CHECKS]


def render_check_catalog() -> str:
    lines = [
        "# AI Visibility Audit Baseline Checks",
        "",
        f"- Checks version: {CHECKS_VERSION}",
        f"- Total checks: {len(BASELINE_CHECKS)}",
        "",
    ]

    for check in BASELINE_CHECKS:
        lines.append(
            f"- `{check.key}`: {check.title} ({check.area}, {check.severity})"
        )
        lines.append(f"  {check.description}")

    return "\n".join(lines)
