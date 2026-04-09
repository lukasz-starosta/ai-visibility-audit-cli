# AI Visibility Audit by PromptScout

Deterministic AI visibility audit artifacts for owned websites.

This repository is the official CLI surface and artifact contract for
`AI Visibility Audit by PromptScout`. Today it can call a compatible audit API
or replay saved scan responses locally, which makes it useful for demos, CI,
wrapper development, and contract testing while the standalone audit runner is
opened up in later phases.

## Why this exists

- keep the public audit surface aligned with the PromptScout Website tab
- ship stable JSON, Markdown, and terminal outputs that other wrappers can trust
- make the product usable before broader skill, app, and MCP packaging lands
- document parity gaps instead of silently forking into a different audit rubric

## Current surface

What you get today:

- a CLI that submits owned-domain audit requests to a compatible API
- a replay mode that renders checked-in raw responses with no network calls
- a published baseline check catalog and stable artifact contract
- golden tests that pin the generated JSON, Markdown, and summary outputs

What is still intentionally out of scope in this repo today:

- the standalone public audit runner
- private PromptScout monitoring and customer-only context
- prompt-aware coverage analysis that depends on monitored prompt data

## Install

Recommended with `uv`:

```bash
uv tool install .
```

Plain `pip` also works:

```bash
python -m pip install .
```

## Quick start

Configure a compatible audit API target:

```bash
export AI_VISIBILITY_AUDIT_API_URL=http://localhost:8081
export AI_VISIBILITY_AUDIT_API_KEY=local-dev-key
```

Run a live audit:

```bash
ai-visibility-audit --domain promptscout.app --output-dir ./out
```

Inspect the bundled baseline checks:

```bash
ai-visibility-audit --show-checks
```

Replay the bundled example without making network calls:

```bash
ai-visibility-audit \
  --input-file examples/sample-request.json \
  --response-file examples/sample-scan-response.json \
  --output-dir examples/generated
```

## Outputs

The CLI writes three files:

- `ai-visibility-audit.json`
- `ai-visibility-audit.md`
- `ai-visibility-audit.txt`

The JSON artifact is canonical. The Markdown and text outputs are deterministic
renderings of the same report data.

## Docs

- [docs/installation.md](docs/installation.md): install and environment setup
- [docs/usage.md](docs/usage.md): CLI examples and output modes
- [docs/artifact-contract.md](docs/artifact-contract.md): versioned output contract
- [docs/parity-gap-register.md](docs/parity-gap-register.md): current Website-tab gaps

## Repo layout

- `ai_visibility_audit/`: HTTP client, CLI surface, and artifact renderer
- `docs/`: installation, usage, contract, and parity documentation
- `examples/`: sample request, sample response, and generated example artifacts
- `tests/`: API, CLI, and artifact contract coverage

## Boundary

This repository currently owns the public wrapper surface:

- transport and CLI UX
- report rendering and artifact versioning
- docs, examples, and golden tests

It does not yet own the standalone deterministic audit runtime. That gap is
tracked explicitly in the parity register instead of being hidden behind
marketing language.
