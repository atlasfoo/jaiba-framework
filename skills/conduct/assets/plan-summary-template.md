---
date: <YYYY-MM-DD>                     # archival date
slug: <plan slug>
kind: work-closure
depth: <design | spec>
adr: <ADR-id proposed, or "none">
---

# <Short title: what this work delivered>

> The work-closure entry for `.ai/memory/log/` — drafted in
> `.ai/work/` by `conduct:summarize`, moved by
> `scripts/archive.sh`. **English, always** (long-term memory).
> Concise: one screen. The walkthrough was the narrative; this is the
> record. Follows the log-entry contract owned by `jaiba-init`
> (`log-entry-template.md`): append-only once archived — corrections
> are new entries.

## What happened

<2–4 lines. What the work delivered end to end — the user-visible
behavior or technical capability that now exists.>

## Criteria delivered

<At spec depth: one line per acceptance criterion, flagging
correctives and any waiver. At design depth: "None — design depth;
done = plan scope + gate.">

- `<PREFIX>-NNN` — <title> — delivered
- `<PREFIX>-NNN` — <title> — delivered *(corrective)*

## Phases executed

| # | Theme | Notable result |
|---|---|---|
| 1 | <theme> | <one-line result> |
| 2 | <theme> | <one-line result> |

## Decisions and deviations

<Non-trivial decisions and why; what shipped differently from the
plan/PRD and why; waived gate checks with their documented reason.
If nothing notable: "None.">

## ADR proposals & brain updates

<Either the proposed ADR block(s) (status: Proposed — title, context,
decision, alternatives, consequences) plus any reference-index /
constitution changes worth promoting — or, explicitly: "No ADR
proposed; all decisions were tactical." Enacting them is
`jaiba-init:update-brain`'s job.>

## Pointers

<The trail: commit range / PR, ADR IDs proposed, related prior log
entries. If nothing: "None.">

## Suggested final commit

```
<type(scope): subject>

<optional body — 2–4 lines summarizing the outcome; useful as a
single commit or as the squash target for the chore(wip) phase
commits>
```

## Gate at close

Pass | <waivers and details if not clean>
