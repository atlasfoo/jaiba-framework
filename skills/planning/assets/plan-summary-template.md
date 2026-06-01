---
slug: <plan slug>
created: <plan creation date>
archived: <YYYY-MM-DD>
spec: <spec-name-or-empty>
adr_proposed: <adr-id-or-none>         # e.g. ADR-005, or "none"
---

# Plan summary: <Title>

> Concise, archivable. One screen, no more. The walkthrough was the
> narrative; this is the record.

## Outcome

<2–4 lines. What the plan delivered, end to end. Mention the user-
visible behavior or technical capability that now exists.>

## Spec coverage

<If a spec was active, list the user stories closed by this plan.
Empty otherwise.>

- `<story-1>` — closed
- `<story-2>` — closed

## Phases executed

| # | Theme | Notable result |
|---|---|---|
| 1 | <theme> | <one-line result> |
| 2 | <theme> | <one-line result> |
| 3 | <theme> | <one-line result> |

## Deviations and corrections

<What changed between the original plan and what actually shipped.
Why. If a phase was added, removed, or substantially reworked, say
so here. If nothing notable, write "None.">

## ADR proposal

<Either the proposed ADR block (status: Proposed, title, context,
decision, alternatives, consequences) — or, explicitly: "No ADR
proposed; all decisions were tactical.">

## Suggested final commit

```
<type(scope): subject>

<optional body — 2–4 lines summarizing the plan's outcome, useful
both as a single commit message or as the squash target for the
`chore(wip)` phase commits>
```

## Quality gate at close

Pass | <details if not>
