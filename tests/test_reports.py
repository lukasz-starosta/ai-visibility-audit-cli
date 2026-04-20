from __future__ import annotations

import json
from pathlib import Path

import pytest

from ai_visibility_audit.inputs import AuditRequest
from ai_visibility_audit.reports import build_artifacts

FIXTURE_ROOT = Path(__file__).parent / "fixtures" / "report-regressions"


@pytest.mark.parametrize(
    "case_name",
    [
        "repeated-js-shell",
        "stale-php-noise",
        "utility-path-suppression",
    ],
)
def test_report_regressions(case_name: str) -> None:
    case_root = FIXTURE_ROOT / case_name
    request = AuditRequest.model_validate_json((case_root / "request.json").read_text())
    response = json.loads((case_root / "response.json").read_text())

    artifacts = build_artifacts(request, response)

    assert artifacts.structured == json.loads(
        (case_root / "expected-ai-visibility-audit.json").read_text()
    )
    assert artifacts.markdown == (
        case_root / "expected-ai-visibility-audit.md"
    ).read_text().rstrip("\n")
    assert artifacts.summary == (
        case_root / "expected-ai-visibility-audit.txt"
    ).read_text().strip()
