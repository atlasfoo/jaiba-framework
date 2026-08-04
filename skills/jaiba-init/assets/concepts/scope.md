---
type: scope                                       # mandatory — exact value, never change
title: "Scope"                                    # recommended — human-readable name
description: "[one line: what belongs inside this project and what does not]" # recommended — this is what index.md shows
tags: [identity, scope, boundaries]               # recommended — list, for grouping and search
updated: "[YYYY-MM-DD]"                           # recommended — last substantive change
---

# Scope

> **For repository maintainers:** replace every bracketed placeholder
> (`[like this]`) with real project values. "Out of scope" is the half
> that earns this file its keep — fill it as carefully as the other.

> **Meta-instruction for the agent:** this concept is the authority on
> **the project's boundaries**. Work that falls outside them is surfaced
> to the human before it is planned, never absorbed silently. Why the
> project exists is the `purpose` concept; how it is built is
> `architecture`.

- **In scope:**
  - [e.g., Itinerary domain logic, collaborator management, REST API]
- **Out of scope:**
  - [e.g., Authentication (delegated to an upstream service), payment
    processing (handled by a third party), email delivery]
- **Cross-cutting packages:**
  - [If the project lives in a monorepo or shares packages across
    services, list them here, e.g. `@org/logger`, `@org/ui-components`.
    Otherwise: "None."]

## Sub-units

If this repository holds more than one deliverable unit — packages in a
monorepo or turborepo, projects in a `.sln`, apps in a workspace — each
unit is its own `sub-unit` concept under [`units/`](units/), carrying its
path, its one-line scope, and what it may depend on. That is what lets a
plan target one unit precisely instead of the whole repo.

Single-unit repository: **"Single unit."** — and the `units/` directory
does not exist at all. Do not create it to hold a placeholder.

## Relations

Upstream, downstream and infrastructure relationships are **not
inventoried here**. Each external surface is its own `reference` concept
carrying a `role:` (`upstream` | `downstream` | `infrastructure`); this
section only links the ones that draw a boundary — the surfaces that
explain why something is out of scope, or that this project must not
reimplement.

- [MISSING: links to the `reference` concepts that bound this project,
  e.g. `[Stripe](../references/stripe.md)`]

Never copy a reference's details into this list. One line, one link; the
`reference` concept owns the facts.
