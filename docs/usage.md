# Usage

## Live scan via API

```bash
uv run python -m ai_visibility_audit.cli \
  --domain promptscout.app \
  --page-limit 25 \
  --citation-url https://promptscout.app/pricing \
  --pinned-url https://promptscout.app/compare \
  --output-dir ./out
```

## Explicit API target override

```bash
uv run python -m ai_visibility_audit.cli \
  --api-url http://localhost:8081 \
  --api-key local-dev-key \
  --brand-id ai-visibility-audit-local \
  --domain promptscout.app \
  --output-dir ./out
```

## Replay checked-in fixtures

```bash
uv run python -m ai_visibility_audit.cli \
  --input-file examples/sample-request.json \
  --response-file examples/sample-scan-response.json \
  --stdout-format markdown
```

## Output modes

Without `--output-dir`, the CLI prints one artifact to stdout:

- `--stdout-format summary`
- `--stdout-format markdown`
- `--stdout-format json`
