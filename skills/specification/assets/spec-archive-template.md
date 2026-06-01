---
slug: <spec slug>
created: <PRD creation date>
archived: <YYYY-MM-DD>
prefix: <story prefix>
stories_delivered: <count>
adr_proposed: <adr-ids-or-none>        # e.g. ADR-007, or "none"
---

# Spec archive: <Requirement title>

> Permanent, English-only record of a delivered requirement. Concise —
> one to two screens. The plan summaries under
> `.ai/memory/archive/plans/` hold the detail of *how* each story was
> built; this is the requirement-level headline. Written in English
> even if the original spec was in another language.

## Outcome

<2–5 lines. What the requirement delivered, end to end — the
user-visible capability or technical change that now exists in the
product.>

## Stories delivered

| ID | Story | Notes |
|---|---|---|
| `<PREFIX>-001` | <one-line story> | <e.g. "as specified" / "corrective"> |
| `<PREFIX>-002` | <one-line story> | |

<If any story was dropped or split out, list it here with the reason.>

## Plans that built it

<The plan summaries (in `.ai/memory/archive/plans/`) that implemented
this spec. Gives a reader the trail to the detailed record.>

- `<YYYY-MM-DD>-<plan-slug>.md` — <one-line scope>
- `<YYYY-MM-DD>-<plan-slug>.md` — <one-line scope>

## Deviations from the PRD

<What shipped differently from the original PRD, and why. Deferred
goals, scope cut or added, corrective stories that appeared during
delivery. If nothing notable, write "None.">

## ADR proposals & brain updates

<Either the proposed ADR block(s) (status: Proposed — title, context,
decision, alternatives, consequences) and any reference-index /
constitution updates worth promoting — or, explicitly: "No ADR
proposed; no brain updates needed." Enacting these is `update-brain`'s
job, not this archive's.>

## Quality gate at close

Pass | <details if not>
