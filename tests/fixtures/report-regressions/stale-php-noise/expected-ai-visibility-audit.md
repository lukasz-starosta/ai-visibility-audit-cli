# AI Visibility Audit by PromptScout

- Domain: example.com
- Status: Needs work
- Checks version: website_scan_v2

## Executive Summary

- Needs work across 7 scanned pages with 1 grouped finding.
- 4 secondary pages could not be fetched from homepage discovery.

## Overall Status

- Pages scanned: 7
- Grouped findings detected: 1
- Raw findings captured: 4
- Grouped issue-level findings: 0
- Grouped warning-level findings: 1
- Raw issue-level findings: 0
- Raw warning-level findings: 4
- Good pages: 3

## Site Diagnoses

- None

## Priority Findings

- Medium: 4 secondary pages could not be fetched from homepage discovery.

## Pages

### Pricing
- URL: https://example.com/pricing
- Status: On track
- Fetch status: ok
- Discovered from: homepage
- Page type: pricing
- Word count: 320
- Findings: 0
- Page findings: none

### Features
- URL: https://example.com/features
- Status: On track
- Fetch status: ok
- Discovered from: homepage
- Page type: feature
- Word count: 300
- Findings: 0
- Page findings: none

### Docs
- URL: https://example.com/docs
- Status: On track
- Fetch status: ok
- Discovered from: homepage
- Page type: docs
- Word count: 420
- Findings: 0
- Page findings: none

### https://example.com/about.php
- URL: https://example.com/about.php
- Status: Needs work
- Fetch status: not_found
- Discovered from: homepage
- Page type: other
- Findings: 1
- Page findings:
  - Medium / Needs work: Page could not be fetched during the scan. Evidence: {"http_status": 404}

### https://example.com/blog.php
- URL: https://example.com/blog.php
- Status: Needs work
- Fetch status: not_found
- Discovered from: homepage
- Page type: other
- Findings: 1
- Page findings:
  - Medium / Needs work: Page could not be fetched during the scan. Evidence: {"http_status": 404}

### https://example.com/contacts.php
- URL: https://example.com/contacts.php
- Status: Needs work
- Fetch status: not_found
- Discovered from: homepage
- Page type: other
- Findings: 1
- Page findings:
  - Medium / Needs work: Page could not be fetched during the scan. Evidence: {"http_status": 404}

### https://example.com/wishlist.php
- URL: https://example.com/wishlist.php
- Status: Needs work
- Fetch status: not_found
- Discovered from: homepage
- Page type: other
- Findings: 1
- Page findings:
  - Medium / Needs work: Page could not be fetched during the scan. Evidence: {"http_status": 404}

## Parity Notes

- Prompt-aware coverage summaries remain richer inside the PromptScout Website tab because the OSS CLI does not have monitored-prompt context by default.
- Website-tab criteria cards are not yet emitted as first-class CLI artifacts; grouped findings and site-level diagnoses remain the canonical public read model here.
- Answer-block, snippet-shape, and evidence-density signals remain outside the deterministic shared website_scan_v2 contract.

## Compact Summary

Needs work for example.com: 7 scanned pages, 1 grouped finding. Top priority: 4 secondary pages could not be fetched from homepage discovery.
