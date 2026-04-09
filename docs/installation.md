# Installation

## Configure an audit API target

The CLI can call either:

- a hosted PromptScout audit API
- a local `prompt-suggestion-api` process

Supported env vars:

- `AI_VISIBILITY_AUDIT_API_URL`
- `AI_VISIBILITY_AUDIT_API_KEY`
- `AI_VISIBILITY_AUDIT_BRAND_ID` optional

Fallbacks for current internal naming:

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
uv run python -m ai_visibility_audit.cli --domain promptscout.app --output-dir ./out
```

## Example-only mode

Use this when you want to review the renderer without calling any API:

```bash
uv run python -m ai_visibility_audit.cli \
  --input-file examples/sample-request.json \
  --response-file examples/sample-scan-response.json \
  --output-dir examples/generated
```
