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
    "Website-tab criteria cards are not yet emitted as first-class CLI artifacts; grouped findings and site-level diagnoses remain the canonical public read model here.",
    "Answer-block, snippet-shape, and evidence-density signals remain outside the deterministic shared website_scan_v2 contract.",
]

STATUS_RANK = {
    "issue": 0,
    "warning": 1,
    "unknown": 2,
    "good": 3,
}

SHELL_COMPONENT_FINDING_KEYS = frozenset(
    {
        "missing_title",
        "missing_meta_description",
        "missing_primary_heading",
        "thin_visible_content",
    }
)


@dataclass(frozen=True)
class ArtifactBundle:
    structured: dict[str, Any]
    markdown: str
    summary: str


@dataclass
class GroupedFindingSummary:
    group_key: str
    finding_key: str
    severity: str
    status: str
    message: str
    page_count: int
    sample_urls: list[str]


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


def _summary_count(
    raw_summary: dict[str, Any],
    primary_key: str,
    fallback_key: str,
    fallback_value: int,
) -> int:
    value = raw_summary.get(primary_key)
    if isinstance(value, int):
        return value

    value = raw_summary.get(fallback_key)
    if isinstance(value, int):
        return value

    return fallback_value


def _parse_diagnosis_groups(raw_summary: dict[str, Any]) -> list[dict[str, Any]]:
    groups: list[dict[str, Any]] = []
    for group in raw_summary.get("diagnosis_groups", []):
        if not isinstance(group, dict):
            continue

        diagnosis_id = group.get("id")
        message = group.get("message")
        severity = group.get("severity")
        status = group.get("status")
        sample_urls = [
            item
            for item in group.get("sample_urls", [])
            if isinstance(item, str)
        ]
        page_count = group.get("page_count")

        if not all(
            isinstance(value, str)
            for value in (diagnosis_id, message, severity, status)
        ):
            continue

        if not isinstance(page_count, int):
            page_count = len(sample_urls)

        groups.append(
            {
                "id": diagnosis_id,
                "message": message,
                "severity": severity,
                "status": status,
                "pageCount": page_count,
                "sampleUrls": sample_urls,
            }
        )

    return groups


def _worst_severity(left: str, right: str) -> str:
    return left if SEVERITY_RANK[left] <= SEVERITY_RANK[right] else right


def _worst_status(left: str, right: str) -> str:
    return left if STATUS_RANK[left] <= STATUS_RANK[right] else right


def _page_role(page: dict[str, Any] | None) -> str:
    if not page:
        return "secondary"

    evidence = page.get("evidence")
    if isinstance(evidence, dict) and isinstance(evidence.get("page_role"), str):
        return str(evidence["page_role"])

    return "secondary"


def _format_group_message(
    *,
    finding_key: str,
    page_count: int,
    page_role: str,
    page_type: str,
    discovered_from: str,
    original_message: str,
) -> str:
    if page_count <= 1 or page_role == "core":
        return _trim_period(original_message)

    page_label = (
        "utility pages"
        if page_role == "utility"
        else f"{page_type} pages" if page_type != "other" else "secondary pages"
    )

    messages = {
        "robots_disallow_all": "Search and AI crawlers are blocked from the whole site",
        "ai_bot_access_blocked": "AI crawlers are blocked from part of the site",
        "robots_missing": "robots.txt is missing",
        "sitemap_missing_or_empty": "A sitemap could not be found",
        "page_fetch_failed": (
            f"{page_count} {page_label} could not be fetched from {discovered_from} discovery."
        ),
        "missing_title": f"{page_count} {page_label} are missing title tags.",
        "missing_meta_description": (
            f"{page_count} {page_label} are missing meta descriptions."
        ),
        "missing_primary_heading": (
            f"{page_count} {page_label} do not contain an H1 heading."
        ),
        "multiple_primary_headings": (
            f"{page_count} {page_label} contain multiple H1 headings."
        ),
        "thin_visible_content": (
            f"{page_count} {page_label} have very little visible raw HTML content."
        ),
        "missing_schema_markup": (
            f"{page_count} {page_label} have no detectable JSON-LD schema markup."
        ),
        "cross_domain_canonical": (
            f"{page_count} {page_label} point canonical URLs to another domain."
        ),
        "stale_content_signal": f"{page_count} {page_label} may look outdated.",
    }
    return messages.get(finding_key, _trim_period(original_message))


def _group_findings(
    pages: list[dict[str, Any]],
    findings: list[dict[str, Any]],
    diagnosis_groups: list[dict[str, Any]],
) -> list[GroupedFindingSummary]:
    page_by_url = {page["url"]: page for page in pages}
    diagnosis_page_urls = {
        url
        for group in diagnosis_groups
        for url in group.get("sampleUrls", [])
        if isinstance(url, str)
    }
    groups: dict[str, GroupedFindingSummary] = {}

    for finding in findings:
        page_url = finding.get("page_url")
        finding_key = finding["finding_key"]
        if page_url in diagnosis_page_urls and finding_key in SHELL_COMPONENT_FINDING_KEYS:
            continue

        page = page_by_url.get(page_url or "")
        page_role = _page_role(page)
        page_type = (
            str(page.get("page_type") or "other")
            if page
            else "other"
        )
        discovered_from = (
            str(page.get("discovered_from") or "run")
            if page
            else "run"
        )

        if page_url is None:
            group_key = f"run::{finding_key}"
        elif finding_key == "page_fetch_failed":
            group_key = (
                f"page::{page_url}"
                if page_role == "core"
                else f"page_fetch_failed::{page_role}::{discovered_from}"
            )
        elif page_role == "core":
            group_key = f"{finding_key}::{page_url}"
        else:
            group_key = f"{finding_key}::{page_role}::{page_type}"

        existing = groups.get(group_key)
        if existing:
            existing.page_count += 1
            if page_url and page_url not in existing.sample_urls:
                existing.sample_urls.append(page_url)
            existing.severity = _worst_severity(existing.severity, finding["severity"])
            existing.status = _worst_status(existing.status, finding["status"])
            existing.message = _format_group_message(
                finding_key=finding_key,
                page_count=existing.page_count,
                page_role=page_role,
                page_type=page_type,
                discovered_from=discovered_from,
                original_message=finding["message"],
            )
            continue

        groups[group_key] = GroupedFindingSummary(
            group_key=group_key,
            finding_key=finding_key,
            severity=finding["severity"],
            status=finding["status"],
            message=_format_group_message(
                finding_key=finding_key,
                page_count=1,
                page_role=page_role,
                page_type=page_type,
                discovered_from=discovered_from,
                original_message=finding["message"],
            ),
            page_count=1,
            sample_urls=[page_url] if page_url else [],
        )

    return list(groups.values())


def _build_priority_findings(
    pages: list[dict[str, Any]],
    findings: list[dict[str, Any]],
    diagnosis_groups: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    diagnosis_priority = [
        {
            "findingKey": group["id"],
            "message": group["message"],
            "pageUrl": group["sampleUrls"][0]
            if group["pageCount"] == 1 and group["sampleUrls"]
            else None,
            "severity": group["severity"],
        }
        for group in diagnosis_groups
    ]
    grouped_findings = _group_findings(pages, findings, diagnosis_groups)
    finding_priority = [
        {
            "findingKey": group.finding_key,
            "message": group.message,
            "pageUrl": group.sample_urls[0]
            if group.page_count == 1 and group.sample_urls
            else None,
            "severity": group.severity,
        }
        for group in grouped_findings
    ]

    return sorted(
        diagnosis_priority + finding_priority,
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
    grouped_findings_label = (
        "grouped finding" if summary["findingsCount"] == 1 else "grouped findings"
    )
    lines = [
        (
            f"{STATUS_LABELS[summary['overallStatus']]} across "
            f"{summary['pagesScanned']} scanned pages with "
            f"{summary['findingsCount']} {grouped_findings_label}."
        )
    ]

    if request.citation_urls:
        lines.append(
            f"{len(request.citation_urls)} citation hint{'s' if len(request.citation_urls) != 1 else ''} {'was' if len(request.citation_urls) == 1 else 'were'} supplied to bias owned-page discovery."
        )
    if request.pinned_urls:
        lines.append(
            f"{len(request.pinned_urls)} pinned URL{'s' if len(request.pinned_urls) != 1 else ''} {'was' if len(request.pinned_urls) == 1 else 'were'} supplied for targeted rechecks."
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
    diagnosis_groups = _parse_diagnosis_groups(raw_summary)
    priority_findings = _build_priority_findings(pages, findings, diagnosis_groups)
    grouped_pages = _group_findings_by_page(pages, findings)
    grouped_counts = {
        "findings": _summary_count(
            raw_summary,
            "grouped_findings_count",
            "findings_count",
            len(priority_findings),
        ),
        "issues": _summary_count(
            raw_summary,
            "grouped_issue_count",
            "issue_count",
            0,
        ),
        "warnings": _summary_count(
            raw_summary,
            "grouped_warning_count",
            "warning_count",
            0,
        ),
    }
    raw_counts = {
        "findings": _summary_count(
            raw_summary,
            "raw_findings_count",
            "findings_count",
            len(findings),
        ),
        "issues": _summary_count(
            raw_summary,
            "raw_issue_count",
            "issue_count",
            0,
        ),
        "warnings": _summary_count(
            raw_summary,
            "raw_warning_count",
            "warning_count",
            0,
        ),
    }

    summary = {
        "overallStatus": raw_summary["overall_status"],
        "statusLabel": STATUS_LABELS[raw_summary["overall_status"]],
        "pagesScanned": raw_summary.get("pages_scanned", len(pages)),
        "findingsCount": grouped_counts["findings"],
        "issueCount": grouped_counts["issues"],
        "warningCount": grouped_counts["warnings"],
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
        "groupedCounts": grouped_counts,
        "rawCounts": raw_counts,
        "executiveSummary": executive_summary,
        "priorityFindings": priority_findings,
        "diagnosisGroups": diagnosis_groups,
        "pages": grouped_pages,
        "findings": findings,
        "websiteAudit": scan_response.get("website_audit"),
        "parityGapNotes": PARITY_GAP_NOTES,
    }

    compact_summary_parts = [
        (
            f"{summary['statusLabel']} for {request.domain}: "
            f"{summary['pagesScanned']} scanned pages, "
            f"{summary['findingsCount']} grouped finding{'s' if summary['findingsCount'] != 1 else ''}"
        )
    ]
    if priority_findings:
        compact_summary_parts.append(
            f"Top priority: {_trim_period(priority_findings[0]['message'])}"
        )

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
        f"- Grouped findings detected: {grouped_counts['findings']}",
        f"- Raw findings captured: {raw_counts['findings']}",
        f"- Grouped issue-level findings: {grouped_counts['issues']}",
        f"- Grouped warning-level findings: {grouped_counts['warnings']}",
        f"- Raw issue-level findings: {raw_counts['issues']}",
        f"- Raw warning-level findings: {raw_counts['warnings']}",
        f"- Good pages: {summary['goodCount']}",
    ]

    if summary["errors"]:
        markdown_lines.append(f"- Errors: {'; '.join(summary['errors'])}")

    markdown_lines.extend(["", "## Site Diagnoses", ""])
    if diagnosis_groups:
        for diagnosis in diagnosis_groups:
            markdown_lines.append(
                f"- {SEVERITY_LABELS[diagnosis['severity']]} / {STATUS_LABELS[diagnosis['status']]}: {diagnosis['message']}"
            )
            markdown_lines.append(
                f"  Affected pages: {diagnosis['pageCount']}"
            )
            markdown_lines.append(
                "  Sample URLs: "
                + (
                    ", ".join(diagnosis["sampleUrls"])
                    if diagnosis["sampleUrls"]
                    else "none"
                )
            )
    else:
        markdown_lines.append("- None")

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
