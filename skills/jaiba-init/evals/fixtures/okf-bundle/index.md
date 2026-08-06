---
type: index
title: "Orders API — memory index"
description: "Entry point to Orders API's constitutive memory."
tags: [index]
updated: "2026-06-10"
---

# Orders API — Memory Index

> **Meta-instruction for the agent:** this file is the **only** entry
> point to `.ai/memory/`. It is a map, never a summary — one link and one
> line per concept, linking **directly** to that concept. Resolving one
> fact must cost reading this file plus *one* concept file; never route a
> reader through another concept on the way. Regenerate this index
> whenever a concept is added, removed or renamed — a stale index is a
> broken-link finding from `jaiba-doctor`.

Each line below is a concept's `description:` frontmatter, verbatim.
Groups are named by the concept `type:` they hold.

## `project`

- [project.md](identity/project.md) — ASP.NET Core 8 Web API that owns the order lifecycle for the e-commerce platform, from creation through fulfillment.

## `architecture`

- [architecture.md](identity/architecture.md) — Layered ASP.NET Core 8 Web API (Api/Application/Domain/Infrastructure) persisting to PostgreSQL via EF Core.

## `purpose`

- [purpose.md](identity/purpose.md) — Order-management backend for the e-commerce platform; creates and fulfills orders, delegating payment capture to the Payments API.

## `scope`

- [scope.md](identity/scope.md) — In scope: order domain logic and its REST surface; out of scope: payment processing itself and any client application.

## `quality-gate`

- [quality-gate.md](identity/quality-gate.md) — Phase gate runs `dotnet test`; plan gate adds the `snyk test` security scan — both sourced from `.github/workflows/ci.yml`.

## `convention`

- [conventions.md](identity/conventions.md) — Planning follows JAIBA defaults (TDD enabled, phase-cohesive plans); code style is delegated to the project's own lint/format config.

## `decision`

One file per ADR, named `<NNN>-<slug>.md` so the directory sorts in
decision order. Superseded decisions stay listed — the link tells the
story.

- [ADR-001 — Adoption of the JAIBA brain structure](decisions/001-adoption-of-jaiba-brain.md) — The project keeps agent-facing memory in .ai/ under the JAIBA framework.
- [ADR-002 — Retry policy for the Payments API HttpClient](decisions/002-payments-api-retry-policy.md) — Wrap the Payments API HttpClient with a Polly retry policy for transient failures.

## `reference`

One file per external surface.

- [Payments API](references/payments-api.md) — External payment processor; Orders API calls it via a typed HttpClient to capture payment for orders.
- [PostgreSQL](references/postgresql.md) — Primary datastore for orders, accessed via Entity Framework Core.
- [Snyk](references/snyk.md) — Dependency vulnerability scan, run as a step in `.github/workflows/ci.yml`.

## `log-entry`

Indexed **as a group, never per entry**: [`log/`](log/) holds one
append-only file per dated record, named `<YYYY-MM-DD>-<slug>.md`. The
filename convention carries the ordering, and the directory grows without
bound — listing entries here would fatten the index until reading it
costs as much as reading the memory it maps.
