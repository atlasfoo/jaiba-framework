---
type: decision
id: ADR-002
title: Retry policy for the Payments API HttpClient
description: Wrap the Payments API HttpClient with a Polly retry policy for transient failures.
status: accepted
date: 2026-06-10
tags: [payments, resilience, infrastructure]
updated: 2026-06-10
---

# ADR-002: Retry policy for the Payments API HttpClient

## Context

The typed HttpClient that calls the Payments API had no resilience
policy: a transient network blip or a Payments API 5xx surfaced
directly as a failed order, even though the underlying payment
attempt often would have succeeded on a retry. This showed up
repeatedly in the on-call rotation as false-positive order failures.

## Decision

Wrap the Payments API typed HttpClient with a Polly retry policy:
three retries with exponential backoff on transient HTTP failures
(5xx, timeouts, connection errors), registered in the Infrastructure
layer's HttpClient configuration. Non-transient failures (4xx) are
not retried and continue to surface immediately.

## Alternatives Considered

- *Leave retries to the caller (Application layer)* — rejected; would
  duplicate the policy across every call site that touches the
  Payments API.
- *Increase the HttpClient timeout instead* — rejected; masks
  transient failures without addressing them and delays legitimate
  error reporting.

## Consequences

- *Positive:* Fewer false-positive order failures caused by transient
  Payments API or network issues.
- *Negative / Risks:* Retries can extend request latency on a genuine
  outage; must be paired with a circuit breaker if the Payments API
  degrades for a sustained period (not yet implemented).
- *Follow-ups:* Evaluate adding a circuit breaker if repeated extended
  outages are observed.
