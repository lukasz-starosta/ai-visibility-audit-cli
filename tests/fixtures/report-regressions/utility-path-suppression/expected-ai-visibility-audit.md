# AI Visibility Audit by PromptScout

- Domain: example.com
- Status: Needs work
- Checks version: website_scan_v2

## Executive Summary

- Needs work across 4 scanned pages with 1 grouped finding.
- 1 pinned URL was supplied for targeted rechecks.
- Contact page contains multiple H1 headings

## Overall Status

- Pages scanned: 4
- Grouped findings detected: 1
- Raw findings captured: 1
- Grouped issue-level findings: 0
- Grouped warning-level findings: 1
- Raw issue-level findings: 0
- Raw warning-level findings: 1
- Good pages: 3

## Site Diagnoses

- None

## Priority Findings

- Low: Contact page contains multiple H1 headings (https://example.com/en/contact-us)

## Pages

### Contact Us
- URL: https://example.com/en/contact-us
- Status: Needs work
- Fetch status: ok
- Discovered from: manual
- Page type: contact
- Word count: 260
- Findings: 1
- Page findings:
  - Low / Needs work: Contact page contains multiple H1 headings. Evidence: {"count": 2}

### About Us
- URL: https://example.com/about-us
- Status: On track
- Fetch status: ok
- Discovered from: homepage
- Page type: about
- Word count: 340
- Findings: 0
- Page findings: none

### Pricing
- URL: https://example.com/pricing
- Status: On track
- Fetch status: ok
- Discovered from: homepage
- Page type: pricing
- Word count: 310
- Findings: 0
- Page findings: none

### Features
- URL: https://example.com/features
- Status: On track
- Fetch status: ok
- Discovered from: homepage
- Page type: feature
- Word count: 315
- Findings: 0
- Page findings: none

## Parity Notes

- Prompt-aware coverage summaries remain richer inside the PromptScout Website tab because the OSS CLI does not have monitored-prompt context by default.
- Website-tab criteria cards are not yet emitted as first-class CLI artifacts; grouped findings and site-level diagnoses remain the canonical public read model here.
- Answer-block, snippet-shape, and evidence-density signals remain outside the deterministic shared website_scan_v2 contract.

## Compact Summary

Needs work for example.com: 4 scanned pages, 1 grouped finding. Top priority: Contact page contains multiple H1 headings.
