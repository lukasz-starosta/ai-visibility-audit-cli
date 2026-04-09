from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import json
from typing import Any

from .inputs import AuditRequest

STATUS_LABELS = {
    "good": "On track",
    "warning": "Needs work",
    "issue": "Action needed",
    "unknown": "Needs scan",
}

SEVERITY_LABELS = {
    "critical": "Critical",
    "high": "High",
    "medium": "Medium",
    "low": "Low",
}

SEVERITY_RANK = {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 3,
}

PARITY_GAP_NOTES = [
    "Prompt-aware coverage summaries remain richer inside the PromptScout Website tab because the OSS CLI does not have monitored-prompt context by default.",
    "Website-tab criteria cards are not yet emitted as first-class CLI artifacts; the raw finding model remains canonical here.",
    "Answer-block, snippet-shape, and evidence-density signals remain outside the deterministic shared v1 contract.",
]


@dataclass(frozen=True)
class ArtifactBundle:
    structured: dict[str, Any]
    markdown: str
    summary: str


def _page_count(count: int) -> str:
    return f"{count} page{'s' if count != 1 else ''}"


def _pages_need(count: int, singular: str, plural: str | None = None) -> str:
    verb = "needs" if count == 1 else "need"
    detail = singular if count == 1 else (plural or singular)
    return f"{_page_count(count)} {verb} {detail}"


def _pages_have(count: int, singular: str, plural: str | None = None) -> str:
    verb = "has" if count == 1 else "have"
    detail = singular if count == 1 else (plural or singular)
    return f"{_page_count(count)} {verb} {detail}"


def _trim_period(value: str) -> str:
    return value.strip().rstrip(".")


def _summarize_finding_group(findings: list[dict[str, Any]]) -> str:
    first_finding = findings[0]
    finding_key = first_finding["finding_key"]
    count = len(findings)

    if finding_key == "robots_disallow_all":
        return "Search and AI crawlers are blocked from the whole site"
    if finding_key == "ai_bot_access_blocked":
        return "AI crawlers are blocked from part of the site"
    if finding_key == "robots_missing":
        return "robots.txt is missing"
    if finding_key == "sitemap_missing_or_empty":
        return "A sitemap could not be found"
    if finding_key == "page_fetch_failed":
        return f"{_page_count(count)} could not be reached during the scan"
    if finding_key == "missing_title":
        return _pages_need(count, "a better page title", "better page titles")
    if finding_key == "missing_meta_description":
        return _pages_need(count, "a meta description", "meta descriptions")
    if finding_key == "missing_primary_heading":
        return _pages_need(count, "a clear main heading")
    if finding_key == "multiple_primary_headings":
        return _pages_have(count, "more than one main heading")
    if finding_key == "thin_visible_content":
        return _pages_need(
            count,
            "more visible content before it can be reused confidently",
            "more visible content before they can be reused confidently",
        )
    if finding_key == "missing_schema_markup":
        return _pages_need(count, "structured data")
    if finding_key == "cross_domain_canonical":
        return _pages_have(
            count,
            "a canonical URL pointing to another domain",
            "canonical URLs pointing to another domain",
        )
    if finding_key == "stale_content_signal":
        return f"{_page_count(count)} may look outdated"

    return _trim_period(first_finding["message"])


def _build_priority_findings(findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for finding in findings:
        grouped[finding["finding_key"]].append(finding)

    priority_findings: list[dict[str, Any]] = []
    for group in grouped.values():
        first = group[0]
        worst_severity = sorted(
            (finding["severity"] for finding in group),
            key=lambda severity: SEVERITY_RANK[severity],
        )[0]
        priority_findings.append(
            {
                "findingKey": first["finding_key"],
                "message": _summarize_finding_group(group),
                "pageUrl": first.get("page_url") if len(group) == 1 else None,
                "severity": worst_severity,
            }
        )

    return sorted(
        priority_findings,
        key=lambda item: SEVERITY_RANK[item["severity"]],
    )[:3]


def _group_findings_by_page(
    pages: list[dict[str, Any]],
    findings: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    findings_by_page: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for finding in findings:
        page_url = finding.get("page_url")
        if page_url:
            findings_by_page[page_url].append(finding)

    grouped_pages: list[dict[str, Any]] = []
    for page in pages:
        grouped_pages.append(
            {
                **page,
                "findings": findings_by_page.get(page["url"], []),
            }
        )

    return grouped_pages


def _build_executive_summary(
    request: AuditRequest,
    summary: dict[str, Any],
    priority_findings: list[dict[str, Any]],
) -> list[str]:
    lines = [
        (
            f"{STATUS_LABELS[summary['overallStatus']]} across "
            f"{summary['pagesScanned']} scanned pages with "
            f"{summary['findingsCount']} total findings."
        )
    ]

    if request.citation_urls:
        lines.append(
            f"{len(request.citation_urls)} citation hint{'s' if len(request.citation_urls) != 1 else ''} {'was' if len(request.citation_urls) == 1 else 'were'} supplied to bias owned-page discovery."
        )

    if priority_findings:
        lines.append(priority_findings[0]["message"])
    else:
        lines.append("No high-priority findings were detected in this run.")

    return lines


def build_artifacts(
    request: AuditRequest,
    scan_response: dict[str, Any],
) -> ArtifactBundle:
    raw_summary = scan_response["summary"]
    findings = scan_response.get("findings", [])
    pages = scan_response.get("pages", [])
    priority_findings = _build_priority_findings(findings)
    grouped_pages = _group_findings_by_page(pages, findings)

    summary = {
        "overallStatus": raw_summary["overall_status"],
        "statusLabel": STATUS_LABELS[raw_summary["overall_status"]],
        "pagesScanned": raw_summary.get("pages_scanned", len(pages)),
        "findingsCount": raw_summary.get("findings_count", len(findings)),
        "issueCount": raw_summary.get("issue_count", 0),
        "warningCount": raw_summary.get("warning_count", 0),
        "goodCount": raw_summary.get("good_count", 0),
        "errors": raw_summary.get("errors", []),
    }
    executive_summary = _build_executive_summary(request, summary, priority_findings)

    structured = {
        "artifactVersion": 1,
        "generatedFrom": "ai_visibility_audit_cli",
        "checksVersion": scan_response["checks_version"],
        "input": request.model_dump(mode="json"),
        "sourceSummary": raw_summary,
        "summary": summary,
        "executiveSummary": executive_summary,
        "priorityFindings": priority_findings,
        "pages": grouped_pages,
        "findings": findings,
        "websiteAudit": scan_response.get("website_audit"),
        "parityGapNotes": PARITY_GAP_NOTES,
    }

    compact_summary_parts = [
        (
            f"{summary['statusLabel']} for {request.domain}: "
            f"{summary['pagesScanned']} scanned pages, "
            f"{summary['findingsCount']} findings"
        )
    ]
    if priority_findings:
        compact_summary_parts.append(f"Top priority: {priority_findings[0]['message']}")

    markdown_lines = [
        "# AI Visibility Audit by PromptScout",
        "",
        f"- Domain: {request.domain}",
        f"- Status: {summary['statusLabel']}",
        f"- Checks version: {scan_response['checks_version']}",
        "",
        "## Executive Summary",
        "",
        *[f"- {line}" for line in executive_summary],
        "",
        "## Overall Status",
        "",
        f"- Pages scanned: {summary['pagesScanned']}",
        f"- Findings detected: {summary['findingsCount']}",
        f"- Issue-level findings: {summary['issueCount']}",
        f"- Warning-level findings: {summary['warningCount']}",
        f"- Good pages: {summary['goodCount']}",
    ]

    if summary["errors"]:
        markdown_lines.append(f"- Errors: {'; '.join(summary['errors'])}")

    markdown_lines.extend(["", "## Priority Findings", ""])
    if priority_findings:
        for finding in priority_findings:
            page_label = f" ({finding['pageUrl']})" if finding["pageUrl"] else ""
            markdown_lines.append(
                f"- {SEVERITY_LABELS[finding['severity']]}: {finding['message']}{page_label}"
            )
    else:
        markdown_lines.append("- No high-priority findings were detected.")

    markdown_lines.extend(["", "## Pages", ""])
    for page in grouped_pages:
        markdown_lines.append(f"### {page.get('title') or page['url']}")
        markdown_lines.append(f"- URL: {page['url']}")
        markdown_lines.append(f"- Status: {STATUS_LABELS[page['status']]}")
        markdown_lines.append(f"- Fetch status: {page['fetch_status']}")
        markdown_lines.append(f"- Discovered from: {page['discovered_from']}")
        markdown_lines.append(f"- Page type: {page.get('page_type') or 'unknown'}")
        if page.get("canonical_url"):
            markdown_lines.append(f"- Canonical URL: {page['canonical_url']}")
        if page.get("word_count") is not None:
            markdown_lines.append(f"- Word count: {page['word_count']}")

        page_findings = page.get("findings", [])
        markdown_lines.append(f"- Findings: {len(page_findings)}")
        if not page_findings:
            markdown_lines.append("- Page findings: none")
            markdown_lines.append("")
            continue

        markdown_lines.append("- Page findings:")
        for finding in page_findings:
            evidence = finding.get("evidence") or {}
            evidence_text = json.dumps(evidence, sort_keys=True)
            markdown_lines.append(
                f"  - {SEVERITY_LABELS[finding['severity']]} / {STATUS_LABELS[finding['status']]}: {_trim_period(finding['message'])}. Evidence: {evidence_text}"
            )
        markdown_lines.append("")

    markdown_lines.extend(["## Parity Notes", ""])
    markdown_lines.extend([f"- {note}" for note in PARITY_GAP_NOTES])
    markdown_lines.extend(["", "## Compact Summary", "", ". ".join(compact_summary_parts) + "."])

    return ArtifactBundle(
        structured=structured,
        markdown="\n".join(markdown_lines).strip(),
        summary=". ".join(compact_summary_parts) + ".",
    )
