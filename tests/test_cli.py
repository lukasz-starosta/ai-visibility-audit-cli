from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import AsyncMock, patch

from ai_visibility_audit.checks import CHECKS_VERSION
from ai_visibility_audit.cli import main

FIXTURE_ROOT = Path(__file__).parent / "fixtures" / "artifact-contract"


def test_cli_writes_expected_files(tmp_path: Path) -> None:
    response = {
        "brand_id": "ai-visibility-audit-oss",
        "checks_version": "website_scan_v2",
        "summary": {
            "base_url": "https://example.com",
            "overall_status": "good",
            "overall_score": 97,
            "pages_scanned": 1,
            "findings_count": 0,
            "issue_count": 0,
            "warning_count": 0,
            "good_count": 1,
            "raw_findings_count": 0,
            "raw_issue_count": 0,
            "raw_warning_count": 0,
            "grouped_findings_count": 0,
            "grouped_issue_count": 0,
            "grouped_warning_count": 0,
            "diagnosis_groups": [],
            "errors": [],
        },
        "pages": [
            {
                "url": "https://example.com",
                "canonical_url": None,
                "discovered_from": "homepage",
                "fetch_status": "ok",
                "status": "good",
                "http_status": 200,
                "page_type": "homepage",
                "title": "Example",
                "meta_description": "Example site",
                "word_count": 300,
                "heading_summary": {},
                "schema_summary": {},
                "freshness_date": None,
                "freshness_confidence": None,
                "evidence": {},
            }
        ],
        "findings": [],
        "website_audit": None,
    }
    request_file = tmp_path / "request.json"
    response_file = tmp_path / "response.json"
    output_dir = tmp_path / "artifacts"

    request_file.write_text(
        json.dumps(
            {
                "domain": "example.com",
                "page_limit": 5,
                "citation_urls": [],
                "pinned_urls": [],
            }
        )
    )
    response_file.write_text(json.dumps(response))

    exit_code = main(
        [
            "--input-file",
            str(request_file),
            "--response-file",
            str(response_file),
            "--output-dir",
            str(output_dir),
        ]
    )

    assert exit_code == 0
    assert (output_dir / "ai-visibility-audit.json").exists()
    assert (output_dir / "ai-visibility-audit.md").exists()
    assert (output_dir / "ai-visibility-audit.txt").exists()


def test_cli_can_print_the_check_catalog(capsys) -> None:
    exit_code = main(["--show-checks", "--stdout-format", "json"])
    captured = capsys.readouterr()

    assert exit_code == 0
    payload = json.loads(captured.out)
    assert payload["checksVersion"] == CHECKS_VERSION
    assert len(payload["checks"]) == 13


def test_cli_can_run_live_mode_from_env(tmp_path: Path, monkeypatch) -> None:
    output_dir = tmp_path / "artifacts"
    live_response = {
        "brand_id": "live-brand",
        "checks_version": "website_scan_v2",
        "summary": {
            "base_url": "https://example.com",
            "overall_status": "warning",
            "overall_score": 92,
            "pages_scanned": 1,
            "findings_count": 1,
            "issue_count": 0,
            "warning_count": 1,
            "good_count": 0,
            "raw_findings_count": 1,
            "raw_issue_count": 0,
            "raw_warning_count": 1,
            "grouped_findings_count": 1,
            "grouped_issue_count": 0,
            "grouped_warning_count": 1,
            "diagnosis_groups": [],
            "errors": [],
        },
        "pages": [
            {
                "url": "https://example.com",
                "canonical_url": None,
                "discovered_from": "homepage",
                "fetch_status": "ok",
                "status": "warning",
                "http_status": 200,
                "page_type": "homepage",
                "title": "Example",
                "meta_description": "Example site",
                "word_count": 300,
                "heading_summary": {},
                "schema_summary": {},
                "freshness_date": None,
                "freshness_confidence": None,
                "evidence": {},
            }
        ],
        "findings": [
            {
                "finding_key": "missing_schema_markup",
                "severity": "medium",
                "status": "warning",
                "message": "Page is missing structured data markup.",
                "page_url": "https://example.com",
                "evidence": {},
            }
        ],
        "website_audit": None,
    }

    monkeypatch.setenv("PROMPT_SUGGESTION_API_URL", "https://prompt-api.example.com")
    monkeypatch.setenv("PROMPT_SUGGESTION_API_KEY", "test-key")

    with patch(
        "ai_visibility_audit.cli.request_live_scan",
        AsyncMock(return_value=live_response),
    ) as request_live_scan:
        exit_code = main(
            [
                "--domain",
                "example.com",
                "--output-dir",
                str(output_dir),
            ]
        )

    assert exit_code == 0
    request_live_scan.assert_awaited_once()
    assert (output_dir / "ai-visibility-audit.json").exists()


def test_cli_replay_matches_golden_artifacts(tmp_path: Path) -> None:
    output_dir = tmp_path / "artifacts"

    exit_code = main(
        [
            "--input-file",
            "examples/sample-request.json",
            "--response-file",
            "examples/sample-scan-response.json",
            "--output-dir",
            str(output_dir),
        ]
    )

    assert exit_code == 0
    assert json.loads((output_dir / "ai-visibility-audit.json").read_text()) == json.loads(
        (FIXTURE_ROOT / "expected-ai-visibility-audit.json").read_text()
    )
    assert (output_dir / "ai-visibility-audit.md").read_text() == (
        FIXTURE_ROOT / "expected-ai-visibility-audit.md"
    ).read_text()
    assert (output_dir / "ai-visibility-audit.txt").read_text() == (
        FIXTURE_ROOT / "expected-ai-visibility-audit.txt"
    ).read_text()
