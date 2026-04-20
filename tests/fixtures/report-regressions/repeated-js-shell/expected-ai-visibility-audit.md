# AI Visibility Audit by PromptScout

- Domain: example.com
- Status: Action needed
- Checks version: website_scan_v2

## Executive Summary

- Action needed across 4 scanned pages with 1 grouped finding.
- 3 secondary pages look like empty raw HTML shells. This often means important content depends on client-side rendering.

## Overall Status

- Pages scanned: 4
- Grouped findings detected: 1
- Raw findings captured: 12
- Grouped issue-level findings: 1
- Grouped warning-level findings: 0
- Raw issue-level findings: 0
- Raw warning-level findings: 12
- Good pages: 1

## Site Diagnoses

- High / Action needed: 3 secondary pages look like empty raw HTML shells. This often means important content depends on client-side rendering.
  Affected pages: 3
  Sample URLs: https://example.com/service-areas/austin, https://example.com/service-areas/dallas, https://example.com/service-areas/houston

## Priority Findings

- High: 3 secondary pages look like empty raw HTML shells. This often means important content depends on client-side rendering.

## Pages

### Example
- URL: https://example.com
- Status: On track
- Fetch status: ok
- Discovered from: homepage
- Page type: homepage
- Word count: 320
- Findings: 0
- Page findings: none

### https://example.com/service-areas/austin
- URL: https://example.com/service-areas/austin
- Status: Needs work
- Fetch status: ok
- Discovered from: homepage
- Page type: service_area
- Word count: 4
- Findings: 4
- Page findings:
  - Medium / Needs work: Page is missing a title tag. Evidence: {"path": "/service-areas/austin"}
  - Low / Needs work: Page is missing a meta description. Evidence: {"path": "/service-areas/austin"}
  - Medium / Needs work: Page does not contain an H1 heading. Evidence: {"path": "/service-areas/austin"}
  - Medium / Needs work: Page has limited visible text content in the raw HTML response. Evidence: {"word_count": 4}

### https://example.com/service-areas/dallas
- URL: https://example.com/service-areas/dallas
- Status: Needs work
- Fetch status: ok
- Discovered from: homepage
- Page type: service_area
- Word count: 5
- Findings: 4
- Page findings:
  - Medium / Needs work: Page is missing a title tag. Evidence: {"path": "/service-areas/dallas"}
  - Low / Needs work: Page is missing a meta description. Evidence: {"path": "/service-areas/dallas"}
  - Medium / Needs work: Page does not contain an H1 heading. Evidence: {"path": "/service-areas/dallas"}
  - Medium / Needs work: Page has limited visible text content in the raw HTML response. Evidence: {"word_count": 5}

### https://example.com/service-areas/houston
- URL: https://example.com/service-areas/houston
- Status: Needs work
- Fetch status: ok
- Discovered from: homepage
- Page type: service_area
- Word count: 3
- Findings: 4
- Page findings:
  - Medium / Needs work: Page is missing a title tag. Evidence: {"path": "/service-areas/houston"}
  - Low / Needs work: Page is missing a meta description. Evidence: {"path": "/service-areas/houston"}
  - Medium / Needs work: Page does not contain an H1 heading. Evidence: {"path": "/service-areas/houston"}
  - Medium / Needs work: Page has limited visible text content in the raw HTML response. Evidence: {"word_count": 3}

## Parity Notes

- Prompt-aware coverage summaries remain richer inside the PromptScout Website tab because the OSS CLI does not have monitored-prompt context by default.
- Website-tab criteria cards are not yet emitted as first-class CLI artifacts; grouped findings and site-level diagnoses remain the canonical public read model here.
- Answer-block, snippet-shape, and evidence-density signals remain outside the deterministic shared website_scan_v2 contract.

## Compact Summary

Action needed for example.com: 4 scanned pages, 1 grouped finding. Top priority: 3 secondary pages look like empty raw HTML shells. This often means important content depends on client-side rendering.
