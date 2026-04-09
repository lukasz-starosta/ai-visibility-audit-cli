# AI Visibility Audit by PromptScout

- Domain: example.com
- Status: Needs work
- Checks version: website_scan_v1

## Executive Summary

- Needs work across 3 scanned pages with 2 total findings.
- 1 citation hint was supplied to bias owned-page discovery.
- 1 page needs structured data

## Overall Status

- Pages scanned: 3
- Findings detected: 2
- Issue-level findings: 0
- Warning-level findings: 2
- Good pages: 1

## Priority Findings

- Medium: 1 page needs structured data (https://example.com/compare)
- Low: 1 page may look outdated (https://example.com/about)

## Pages

### Pricing
- URL: https://example.com/pricing
- Status: On track
- Fetch status: ok
- Discovered from: citation
- Page type: pricing
- Word count: 560
- Findings: 0
- Page findings: none

### PromptScout vs Profound
- URL: https://example.com/compare
- Status: Needs work
- Fetch status: ok
- Discovered from: manual
- Page type: comparison
- Word count: 420
- Findings: 1
- Page findings:
  - Medium / Needs work: Comparison page is missing structured data. Evidence: {"path": "/compare"}

### About PromptScout
- URL: https://example.com/about
- Status: Needs work
- Fetch status: ok
- Discovered from: homepage
- Page type: about
- Word count: 280
- Findings: 1
- Page findings:
  - Low / Needs work: About page may look outdated. Evidence: {"last_updated": "2022-03-01"}

## Parity Notes

- Prompt-aware coverage summaries remain richer inside the PromptScout Website tab because the OSS CLI does not have monitored-prompt context by default.
- Website-tab criteria cards are not yet emitted as first-class CLI artifacts; the raw finding model remains canonical here.
- Answer-block, snippet-shape, and evidence-density signals remain outside the deterministic shared v1 contract.

## Compact Summary

Needs work for example.com: 3 scanned pages, 2 findings. Top priority: 1 page needs structured data.
