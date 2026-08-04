---
type: reference
title: Payments API
description: External payment processor; Orders API calls it via a typed HttpClient to capture payment for orders.
tier: code-scope
kind: external-api
role: upstream
resource: "vendored at `docs/openapi/payments-v2.yaml`"
tags: [payments, external, upstream]
updated: 2026-06-02
---

# Payments API

## What it is

A third-party payment processor. It authorizes and captures payment
for customer orders; the boundary of what it owns (authorization,
settlement) stops there — Orders API never re-implements payment
logic itself.

## How the project uses it

The Infrastructure layer calls it through a typed `HttpClient`
(wrapped since ADR-002 with a Polly retry policy for transient
failures); the Application layer orchestrates the capture as part of
the order-fulfillment flow.

## How to consult it

The contract is vendored in-repo as an OpenAPI document at
`docs/openapi/payments-v2.yaml` — read it there rather than fetching
a live spec.

## Gotchas

Only 5xx/timeout/connection failures are retried (ADR-002); a 4xx from
the Payments API is a genuine rejection and must not be retried.
