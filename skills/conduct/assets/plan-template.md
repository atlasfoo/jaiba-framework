---
type: plan
slug: <kebab-case-identifier>          # e.g. collaborative-itineraries
created: <YYYY-MM-DD>
depth: design                          # design | spec (what triage decided)
prd: <.ai/work/PRD.md or empty>        # local PRD, only at spec depth
criteria: []                           # acceptance criteria IDs this plan delivers, e.g. [ITIN-001, ITIN-002]. Empty at design depth.
status: draft                          # draft | approved | executing | validated | summarized
---

# Plan: <Short descriptive title>

## Objective

<2–4 sentences. What this plan delivers and why it matters. At
`design` depth this section carries the whole motivation — the perf
target, the bump's breaking-changes summary, the refactor rationale —
since there is no PRD.>

## Covered criteria

<Only at spec depth. List each acceptance criterion this plan
delivers, by ID and one-line title, so a reviewer can trace
plan → PRD. The criteria's happy/sad paths are the source for this
plan's tests. At design depth, write "None — design depth.">

- `<PREFIX>-NNN` — <one-line criterion title>

## Scope

**In:**
- <Concrete deliverable 1>
- <Concrete deliverable 2>

**Out:**
- <What looks adjacent but is deliberately excluded, with a one-line
  reason>

## Technical approach

<The *how*, in plain prose. Reference the `architecture` and
`convention` concepts for the project's style and conventions; respect
the `sub-unit` concepts' boundaries and name any `internal-contract`
reference concepts touched. Cite specific `reference` concepts for
external integrations. If knowledge skills (TDD, ASP.NET, etc.) are
relevant, cite the patterns they prescribe.

Keep this section explanatory, not instructional — instructions live
in `tasks.md`. The point is for a human reviewer to nod and say "yes,
that's the right shape".>

## Discrepancies vs PRD

<Only fill this if a PRD exists *and* the design deliberately
deviates from it. List each deviation with its rationale. Otherwise
write "None.">

## Sources consulted

- `[<concept file>](../memory/<path-to-concept>.md)` — the constitutive concept(s) consulted, e.g. `[identity/architecture.md](../memory/identity/architecture.md)`
- `[<reference label>](../memory/references/<slug>.md)` — the `reference` concept(s) consulted for external integrations, e.g. `[Stripe](../memory/references/stripe.md)`
- `.ai/work/PRD.md` (if spec depth)
- `.ai/memory/log/<entry>` (prior related work, if any)
- <Knowledge skill name> (if applicable)
- <External docs / web sources, with URLs>

## Plan amendments

<Empty at plan creation. Append a dated bullet whenever the plan is
modified during execution. Format:

- `YYYY-MM-DD` — <what changed and why, one line>
>
