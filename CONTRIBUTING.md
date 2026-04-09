# Contributing

## Boundary rule

This repo does not own the private PromptScout audit engine.

It owns:

- API transport
- CLI UX
- artifact generation
- examples and docs

Do not move or duplicate private PromptScout runtime logic into this repo.

## Local workflow

1. Update the API client, CLI wrapper, or report renderer.
2. Refresh local examples when the public artifact contract changes.
3. Run `uv run --with pytest pytest tests -q`.
