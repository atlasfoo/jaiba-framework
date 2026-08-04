---
type: walkthrough
slug: <kebab-case-slug>                # e.g. collaborative-itineraries
created: <YYYY-MM-DD>
---

# Walkthrough: <plan slug>

> Change-by-change log of the work's execution, written **as you go**
> — one compact entry per completed task, plus a checkpoint block at
> each phase boundary. `.ai/work/` is multisession: this file (with
> the `tasks.md` checkboxes) is how a fresh session reconstructs
> exactly where work stands, even mid-phase.
>
> Keep entries compact — two lines is usually enough. The checkpoint
> block aggregates; the final summary distills. Don't paste diffs.

---

## Phase 1 — <Theme>

<!-- One entry per task, appended as each completes. Format: -->

- `T-NNN` — <what changed, 1–2 lines. Note any decision or trivial
  drift inline.>
- `T-NNN` — <…>

<!-- At the phase boundary, close with the checkpoint block: -->

### Checkpoint — Phase 1     <YYYY-MM-DD>

**Outcome.** <3–6 lines on what the phase delivered.>

**Decisions.**
- <Non-trivial decision and the reasoning. If none: "none".>

**Deviations from plan.**
- <Tasks added (`T-NNN`)/dropped/reworded and why; corrective
  criteria raised; check `plan.md § Plan amendments` reflects it.
  If none: "none".>

**ADR candidates.**
- <Structural decisions `summarize` should consider proposing.
  If nothing: "none".>

**Gate.** Pass | Fail-then-fixed | <details>

---

<!--
Out-of-band change block (written by the `fast` skill when it makes
an unplanned change while this plan is active):

## Out-of-band change (fast)     <YYYY-MM-DD>

**Change.** <what and why it wasn't in the plan>

**Scope touched.** <files / tasks affected; related phase>

**Gate.** Pass | Fail-then-fixed | <details>
-->
