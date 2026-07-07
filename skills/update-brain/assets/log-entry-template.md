# Memory Log Entry

> **Meta-instruction for the agent:**
>
> `.ai/memory/log/` is the project's **append-only chronological
> record**. One file per entry, named `<YYYY-MM-DD>-<slug>.md`. Two
> kinds of entries share this template:
>
> - **`work-closure`** — the distilled essence of a finished piece of
>   work, written when conduct's `summarize` step archives
>   the executive memory (`.ai/work/`) before clearing it. The
>   walkthrough was the narrative; this is the record.
> - **`brain-change`** — a changelog note appended by `update-brain`
>   whenever it enacts a change to the constitutive memory
>   (constitution, adr-log, reference-index): what changed, from what
>   to what, and why.
>
> **Append-only discipline.** Entries are never rewritten, renamed, or
> deleted — a correction is a *new* entry that references the old one.
> The log's value is that it can be trusted as history; the moment an
> entry can be edited after the fact, it can't.
>
> **The log is not the ADR log.** `adr-log.md` is *curated* memory —
> the decisions currently in force, superseded explicitly, always
> readable as "how things are and why". The log is *chronological*
> memory — what happened, in order. A decision lives in `adr-log.md`;
> the closure of the work that produced it lives here, pointing at the
> ADR by ID.

---

```markdown
---
date: <YYYY-MM-DD>
slug: <kebab-case-slug>
kind: work-closure | brain-change
adr: <ADR-NNN proposed or enacted by this entry, or "none">
---

# <Short title: what closed or what changed>

## What happened

<2–4 lines. For work-closure: what the work delivered end to end —
the user-visible behavior or technical capability that now exists.
For brain-change: which constitutive file(s) changed, from what to
what, and the trigger (proposal enacted / drift fixed).>

## Decisions and deviations

<Non-trivial decisions made and why; deviations from the original
plan or proposal. For brain-change: the provenance of the change
(which plan summary or spec proposed it). If nothing notable: "None.">

## Pointers

<Links that keep the trail followable: the ADR ID this entry relates
to, the commit range or PR, acceptance criteria IDs covered
(<PREFIX>-NNN), a superseded log entry being corrected. If nothing:
"None.">
```
