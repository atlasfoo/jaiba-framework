---
slug: <kebab-case-identifier>          # e.g. itinerarios-colaborativos-modelo-base
created: <YYYY-MM-DD>
spec: <spec-name-or-empty>             # path under .ai/specs/, or leave empty
stories: []                            # story IDs this plan covers, e.g. [ITIN-001, ITIN-002]. Empty if no active spec.
status: draft                          # draft | approved | executing | summarized | archived
---

# Plan: <Short descriptive title>

## Objective

<2–4 sentences. What this plan delivers and why it matters. Tie it
to a business or technical outcome — never just "do X".>

## Covered stories

<Only if a spec is active. List each story this plan implements, by ID
and one-line title, so a reviewer can trace plan → spec. The story's
acceptance criteria (happy/sad paths) are the source for this plan's
tests. If no spec is active, write "None — standalone plan.">

- `<PREFIX>-NNN` — <one-line story title>

## Scope

**In:**
- <Concrete deliverable 1>
- <Concrete deliverable 2>

**Out:**
- <What looks adjacent but is deliberately excluded, with a one-line
  reason>

## Technical approach

<The *how*, in plain prose. Reference the architectural style and
conventions from `constitution.md`. Cite specific entries in
`reference-index.md` for any external integration. If knowledge
skills (TDD, ASP.NET, etc.) are relevant, cite the patterns they
prescribe.

Keep this section explanatory, not instructional — instructions live
in `tasks.md`. The point here is for a human reviewer to nod and say
"yes, that's the right shape".>

## Discrepancies vs spec

<Only fill this in if a spec is active *and* the plan deviates from
it. List each deviation with its rationale. If empty, write
"None.">

## Sources consulted

- `.ai/memory/constitution.md` § <section>
- `.ai/memory/reference-index.md` § <section>
- `.ai/specs/<name>/PRD.md` (if applicable)
- <Knowledge skill name> (if applicable)
- <External docs / web sources, with URLs>

## Plan amendments

<Empty at plan creation. Append a dated bullet whenever the plan is
modified during execution. Format:

- `YYYY-MM-DD` — <what changed and why, one line>
>
