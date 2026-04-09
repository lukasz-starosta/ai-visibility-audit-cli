# Contributing

## Boundary rule

This repo currently does not own the standalone public audit runtime.

It owns:

- API transport
- CLI UX
- artifact generation
- golden artifact fixtures
- examples and docs

Do not move or duplicate private PromptScout runtime logic into this repo
without explicitly changing the boundary and parity docs at the same time.

## Local workflow

1. Update the API client, CLI surface, or report renderer.
2. Update `docs/artifact-contract.md` if the public report shape changes.
3. Update `docs/parity-gap-register.md` if OSS behavior moves relative to the Website tab.
4. Refresh golden fixtures in `tests/fixtures/artifact-contract/` when the contract changes.
5. Run `uv run --group dev pytest tests -q`.
