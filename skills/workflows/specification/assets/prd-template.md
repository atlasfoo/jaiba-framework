---
slug: <kebab-case-spec-slug>           # e.g. collaborative-itineraries
created: <YYYY-MM-DD>
status: draft                          # draft | approved | in-progress | completed | archived
prefix: <SHORT-UPPERCASE>              # story-ID prefix, unique across specs — e.g. ITIN
source: manual                         # manual | file | ticket
source-ref: <path-or-ticket-id-or-empty>
---

# PRD: <Requirement title>

> Product Requirements Document. Concise by design — one to two screens.
> It states the *what* and the *why*. The *how* (design, schema,
> libraries, phases) belongs to `planning`, not here.

## Problem & context

<The *why*. What can users not do today? What pain or opportunity does
this address? Ground it in reality — reference the current behavior of
the system, not a hypothetical one. 2–5 sentences.>

## Goals / Non-goals

**Goals:**
- <What success looks like, business-level. 2–4 bullets.>

**Non-goals:**
- <What this requirement explicitly does NOT attempt — the adjacent
  things a reader might assume are included but aren't.>

## Users

<The actors involved and, briefly, what each needs. One line each.>

- <Role A> — <what they need>
- <Role B> — <what they need>

## Proposed solution

<The agreed shape, high level. Enough for a reviewer to picture it and
nod. Cite the existing integration or pattern it reuses
(`reference-index.md`) rather than inventing a new one. Not a design
doc — no schemas, no sequence diagrams.>

## Scope

**In:**
- <Concrete capability 1>
- <Concrete capability 2>

**Out:**
- <What looks adjacent but is deliberately excluded, with a one-line
  reason. Mirrors the Non-goals at the feature level.>

## Assumptions & constraints

- <Assumptions the spec relies on — including ones the code imposes
  (existing models, current auth, etc.).>
- <Constraints — performance, security, compliance, platform.>

## Dependencies

- <External integration or package, cited from
  `.ai/memory/reference-index.md`. If the requirement implies a NEW
  integration not yet indexed, flag it here as "NEW — to be added" so
  it surfaces for `update-brain`.>

## Success metrics

- <How you'd know it worked. Prefer something observable over a
  feeling. "X% of trips have ≥2 collaborators within 30 days.">

## Open questions

<MUST be empty at approval. If anything is here, `define` is not
finished — resolve it via the questionnaire and move the answer into
the relevant section above. Delete this heading's contents before
setting status: approved.>
