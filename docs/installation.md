# Installation

## Requirements

- Python 3.11 or newer
- `uv` recommended for installation and local development

## Install the CLI

Recommended:

```bash
uv tool install .
```

Alternative:

```bash
python -m pip install .
```

## Configure an audit API target

The CLI can call either:

- a hosted audit API
- a local compatible development API

Supported env vars:

- `AI_VISIBILITY_AUDIT_API_URL`
- `AI_VISIBILITY_AUDIT_API_KEY`
- `AI_VISIBILITY_AUDIT_BRAND_ID` optional

Fallbacks kept for current PromptScout maintainer workflows:

- `PROMPT_SUGGESTION_API_URL`
- `PROMPT_SUGGESTION_API_KEY`
- `PROMPT_SUGGESTION_BRAND_ID` optional

Example:

```bash
export AI_VISIBILITY_AUDIT_API_URL=http://localhost:8081
export AI_VISIBILITY_AUDIT_API_KEY=local-dev-key
```

## Live audit mode

```bash
ai-visibility-audit --domain promptscout.app --output-dir ./out
```

## Example-only mode

Use this when you want to review the renderer without calling any API:

```bash
ai-visibility-audit \
  --input-file examples/sample-request.json \
  --response-file examples/sample-scan-response.json \
  --output-dir examples/generated
```

## Contributor setup

Install the development group on demand when running tests:

```bash
uv run --group dev pytest tests -q
```
