# AI Visibility Audit CLI

Thin CLI wrapper for the internal PromptScout owned-domain audit API.

This repo does not contain the private PromptScout audit engine. Instead, it
calls the deterministic website-scan API that PromptScout already runs
internally and renders shareable artifacts from the API response.

## What it does

- submits one owned-domain audit request to a configured PromptScout audit API
- exposes the current deterministic baseline check catalog from the CLI
- emits machine-readable JSON, human-readable Markdown, and a compact summary
- keeps status semantics aligned with the PromptScout Website tab
- can replay checked-in raw responses without making network calls

## Quick start

Set either the dedicated CLI env vars or the existing PromptScout API vars:

```bash
export AI_VISIBILITY_AUDIT_API_URL=http://localhost:8081
export AI_VISIBILITY_AUDIT_API_KEY=local-dev-key
```

Run the CLI against a hosted or local `prompt-suggestion-api`:

```bash
uv run python -m ai_visibility_audit.cli --domain promptscout.app --output-dir ./out
```

Inspect the bundled baseline checks:

```bash
uv run python -m ai_visibility_audit.cli --show-checks
```

Replay the bundled example without making network calls:

```bash
uv run python -m ai_visibility_audit.cli \
  --input-file examples/sample-request.json \
  --response-file examples/sample-scan-response.json \
  --output-dir examples/generated
```

## Outputs

The CLI writes three artifacts:

- `ai-visibility-audit.json`
- `ai-visibility-audit.md`
- `ai-visibility-audit.txt`

## Repo layout

- `ai_visibility_audit/`: HTTP client, CLI wrapper, and report renderer
- `docs/`: install and usage docs
- `examples/`: sample request and raw API response
- `tests/`: CLI and API client regression coverage

## Boundary

This repo is the public CLI surface only.

- private runtime stays in PromptScout internals
- dependency-free skills should live in the separate skill repo
- this repo owns transport, artifact rendering, docs, and examples
