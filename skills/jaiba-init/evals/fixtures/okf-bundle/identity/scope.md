---
type: scope
title: "Scope"
description: "In scope: order domain logic and its REST surface; out of scope: payment processing itself and any client application."
tags: [identity, scope, boundaries]
updated: "2026-06-02"
---

# Scope

- **In scope:**
  - Order domain logic (creation, status transitions, fulfillment)
  - REST API surface (Api layer)
  - Payment capture orchestration via the Payments API (Application layer)
  - Persistence of orders (Infrastructure layer, PostgreSQL)
- **Out of scope:**
  - Payment authorization and settlement itself (owned by the
    upstream Payments API)
  - Any UI or client application (this project is API-only)
- **Cross-cutting packages:**
  - None. Single-project layered solution, not a monorepo.

## Sub-units

If this repository holds more than one deliverable unit — packages in a
monorepo or turborepo, projects in a `.sln`, apps in a workspace — each
unit is its own `sub-unit` concept under `units/`, carrying its
path, its one-line scope, and what it may depend on. That is what lets a
plan target one unit precisely instead of the whole repo.

Single unit — the `units/` directory does not exist.

## Relations

Upstream, downstream and infrastructure relationships are **not
inventoried here**. Each external surface is its own `reference` concept
carrying a `role:` (`upstream` | `downstream` | `infrastructure`); this
section only links the ones that draw a boundary — the surfaces that
explain why something is out of scope, or that this project must not
reimplement.

- [Payments API](../references/payments-api.md) — the boundary this
  project must not reimplement; payment authorization and settlement
  stay there.
- [PostgreSQL](../references/postgresql.md) — infrastructure this
  project operates on for order persistence.

Never copy a reference's details into this list. One line, one link; the
`reference` concept owns the facts.
