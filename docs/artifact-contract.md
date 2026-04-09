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
- `executiveSummary`
- `priorityFindings`
- `pages`
- `findings`
- `websiteAudit`
- `parityGapNotes`

## Fixture coverage

The repo ships a checked-in request/response pair in `examples/` and golden
expected outputs in `tests/fixtures/artifact-contract/`. Those fixtures protect
the contract against accidental renderer regressions.
