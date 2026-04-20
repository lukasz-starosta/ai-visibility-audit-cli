# Artifact Contract

The public value of this repository is the audit artifact contract.

Downstream wrappers such as skills, apps, and future automation surfaces should
treat the generated JSON artifact as canonical and derive any higher-level UI or
summary output from that structure.

## Canonical files

Each run can emit:

- `ai-visibility-audit.json`
- `ai-visibility-audit.md`
- `ai-visibility-audit.txt`

## Contract rules

- `ai-visibility-audit.json` is the canonical machine-readable output.
- `ai-visibility-audit.md` and `ai-visibility-audit.txt` are deterministic
  renderings of the same report data.
- `artifactVersion` tracks the renderer contract.
- `checksVersion` tracks the upstream check catalog used to produce the scan.
- any change to output shape or wording must update the golden fixtures in
  `tests/fixtures/artifact-contract/`

## Current JSON sections

- `artifactVersion`
- `generatedFrom`
- `checksVersion`
- `input`
- `sourceSummary`
- `summary`
- `groupedCounts`
- `rawCounts`
- `executiveSummary`
- `priorityFindings`
- `diagnosisGroups`
- `pages`
- `findings`
- `websiteAudit`
- `parityGapNotes`

## Website Audit v2 semantics

- `checksVersion` should now align to `website_scan_v2`.
- `summary.findingsCount`, `summary.issueCount`, and `summary.warningCount`
  are grouped headline counts, not raw page-level totals.
- `groupedCounts` makes the grouped headline counts explicit for downstream
  wrappers.
- `rawCounts` preserves the uncollapsed page-level totals from the scan engine.
- `diagnosisGroups` carries site-level diagnoses such as
  `likely_js_rendered_raw_html_shell`.
- `findings` remains the raw page-level evidence list and may be larger than the
  grouped headline counts.
- grouped rendering is page-role-aware: core-page failures stay page-specific,
  while repeated secondary or utility-page noise may collapse into one grouped
  priority finding.
- `input.pinned_urls` is part of the shared input contract for targeted
  rescans, even if dashboard UX for focused scans ships separately.

## Fixture coverage

The repo ships a checked-in request/response pair in `examples/` and golden
expected outputs in `tests/fixtures/artifact-contract/`. Those fixtures protect
the contract against accidental renderer regressions.
