---
type: log-entry
date: 2026-06-10
slug: payments-retry-policy-adr
kind: brain-change
adr: ADR-002
---

# Recorded ADR-002: retry policy for the Payments API HttpClient

## What happened

`adr-log.md` gained ADR-002 (status: Accepted) — a Polly retry policy
(three retries, exponential backoff) wrapping the typed HttpClient
that calls the Payments API, covering transient 5xx/timeout/connection
failures. The Decision Index table was updated to list it.

## Decisions and deviations

None. This formalizes a decision the team had already agreed to
implement; no alternative constitution or reference-index sections
needed a change.

## Pointers

- ADR-002 (`adr-log.md`)
- None: no PR/commit range recorded for this fixture entry.
