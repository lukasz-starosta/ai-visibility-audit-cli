# Website Tab Parity Gap Register

This repo tracks gaps between the public `AI Visibility Audit by PromptScout`
surface and the PromptScout Website tab instead of silently drifting into a new
audit product.

## Current stage

The current public package ships:

- the CLI
- the artifact contract
- replayable example fixtures
- golden regression tests
- grouped-diagnosis Website Audit v2 summary semantics

The standalone public audit runner is not yet extracted into this repository.

## Known gaps

- The standalone deterministic audit runtime remains private today.
- Website-tab criteria cards are not yet emitted as first-class CLI artifacts.
- Prompt-aware coverage outputs remain richer in PromptScout because the OSS
  surface does not have monitored-prompt context by default.
- Answer-block, snippet-shape, and evidence-density signals remain outside the
  deterministic shared `website_scan_v2` contract.
- Numeric score handling is passed through in `sourceSummary`, but the public
  surface still treats coarse status as the headline signal.

## Change policy

- If the OSS surface adds a capability ahead of the Website tab, document it
  here in the same change.
- If the artifact contract changes, update `docs/artifact-contract.md` and the
  golden fixtures together.
