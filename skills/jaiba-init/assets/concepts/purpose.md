---
type: purpose                                     # mandatory — exact value, never change
title: "Purpose"                                  # recommended — human-readable name
description: "[one line: the problem this project solves and for whom]" # recommended — this is what index.md shows
tags: [identity, purpose, business]               # recommended — list, for grouping and search
updated: "[YYYY-MM-DD]"                           # recommended — last substantive change
---

# Purpose

> **For repository maintainers:** replace every bracketed placeholder
> (`[like this]`) with real project values. A purpose you cannot state
> from evidence is `[NEEDS CLARIFICATION]` and a question for a human —
> never an invented mission statement.

> **Meta-instruction for the agent:** this concept is the authority on
> **why this project exists** — the business objective it serves and the
> role it plays in whatever larger system it belongs to. Read it before
> judging whether proposed work is worth doing. What the project *builds*
> is the `scope` concept's job, not this one's.

- **Business objective:** [What problem this solves and for whom]
- **Position in the bigger picture:** [If this project is one component
  of a multi-component solution, describe its role and what it enables
  for the rest of the system. Otherwise: "Standalone."]

## Relations

Upstream, downstream and infrastructure relationships are **not
inventoried here**. Each external surface is its own `reference` concept
carrying a `role:` (`upstream` | `downstream` | `infrastructure`) along
with how to consult it; this section only links the ones that explain the
project's *purpose* — who it serves and what it depends on to serve them.

- [MISSING: links to the `reference` concepts that give this project its
  reason to exist, e.g. `[Central Auth](../references/central-auth.md)`]

Never copy a reference's details into this list. One line, one link; the
`reference` concept owns the facts.
