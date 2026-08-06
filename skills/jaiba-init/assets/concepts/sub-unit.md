---
type: sub-unit                                    # mandatory — exact value, never change
title: "[unit-slug]"                              # recommended — human-readable name
description: "[one line: what this unit is and what it owns]" # recommended — this is what index.md shows
tags: [identity, sub-unit]                        # recommended — list, for grouping and search
updated: "[YYYY-MM-DD]"                           # recommended — last substantive change
path: "[packages/api]"                            # repo-relative path of this unit
depends-on:                                       # links to sibling sub-unit concepts; [] if none
  - "[shared](shared.md)"
---

# [unit-slug]

> **For repository maintainers:** one file per deliverable unit, named
> `identity/units/<slug>.md` with a kebab-case slug matching the unit.
> Replace every bracketed placeholder (`[like this]`) with real values;
> `path` is read from the repository, never guessed.

> **Meta-instruction for the agent:** this concept is the authority on
> **one deliverable unit** — where it lives, what it owns, and which
> siblings it may depend on. `depends-on` is a boundary, not a
> description: a change that makes this unit reach beyond it is a scope
> violation to surface, not to implement. The repository-wide boundary is
> the `scope` concept.

> This concept type exists **only** in repositories holding more than one
> deliverable unit — packages in a monorepo or turborepo, projects in a
> `.sln`, apps in a workspace. A single-unit repository has no
> `identity/units/` directory at all; do not create one for a placeholder.

- **Path:** [`packages/api`]
- **Scope (one line):** [e.g., REST backend; owns persistence]
- **May depend on:** the sibling units linked in `depends-on` above, and
  nothing else internal. [If this unit depends on no sibling, `depends-on`
  is `[]` and this line reads "nothing internal".]

Contracts *between* units — event schemas, internal APIs — are external
surfaces from each unit's point of view. Record each as its own
`reference` concept and link it here; do not describe it inline.

- [MISSING: links to the `reference` concepts for this unit's cross-unit
  contracts, e.g. `[Order events](../../references/order-events.md)`]
