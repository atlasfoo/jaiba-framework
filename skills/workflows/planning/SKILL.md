---
name: planning
description: Tactical planning workflow inside the JAIBA framework. Use this skill whenever the developer wants to plan a concrete piece of work, advance an existing plan, wrap up a completed plan, or archive its session artifacts. Trigger on any of: explicit calls like "planning define / summarize / cleanup", phrases like "vamos a planear", "armemos un plan", "siguiente tarea", "continúa con el plan", "cierra este plan", "archiva el plan". Also trigger implicitly whenever `.ai/session/plan.md` exists in the repository and the developer's message reads as a continuation cue (e.g. "sigue", "avanza", "next", "go", "okay continúa"). Covers writing plan.md and tasks.md, executing tasks phase by phase with walkthrough logging, summarizing a finished plan with optional ADR proposal, and cleaning up `.ai/session/` after archival.
---

# Planning Skill

Tactical workflow for building, executing, summarizing, and archiving
plans within the JAIBA framework. This is the everyday workhorse for
concrete pieces of work that need traceability but don't warrant a
full `specification` cycle.

This skill has **four modes**, each documented in its own reference
file. Read the relevant reference *before* taking action — the
selection table below tells you which one.

## Mode Selection

Decide the mode **before** reading anything else. If the message is
ambiguous, ask the developer instead of guessing.

| Situation | Mode | Read |
|---|---|---|
| Developer asks for a new plan / says "planning define" / there is no `.ai/session/plan.md` and they describe work to do | `define` | `references/define-mode.md` |
| `.ai/session/plan.md` exists, `tasks.md` has unchecked tasks, and the developer's message is a continuation cue (`continúa`, `sigue`, `avanza`, `siguiente`, `next`, `go`, a reply to a pending question) | `execute` *(implicit)* | `references/execute-mode.md` |
| `.ai/session/plan.md` exists, all tasks in `tasks.md` are checked, developer asks to close / wrap up / "planning summarize" | `summarize` | `references/summarize-mode.md` |
| `.ai/session/<slug>-summary.md` exists, developer asks to clean up / archive / "planning cleanup" | `cleanup` | `references/cleanup-mode.md` |
| Anything else, including `.ai/session/plan.md` exists but the message is unrelated to the plan | **Ask.** Don't enter any mode silently. | — |

## Universal Preconditions

Before entering any mode, do these reads. Stop and surface the gap if
any file is missing or contradicts the request.

1. **`AGENTS.md`** — your behavioral contract. Always.
2. **`.ai/memory/constitution.md`** — authoritative on project facts.
   In particular look for:
   - The Quality Gate section.
   - The Planning Conventions section — especially the **TDD mode**
     line (`enabled` / `disabled`). Default is `enabled` if absent.
3. **`.ai/memory/reference-index.md`** — read sections relevant to the
   integrations the plan will touch. Do not invent integrations.
4. **Active spec, if any** — if the developer references a spec or one
   is implied, read `.ai/specs/<name>/PRD.md` and `user-stories.md`.

If any of these reads reveals a conflict between the developer's
request and recorded project facts, **flag it before producing
artifacts**. See "Discrepancy handling" below.

## Artifacts at a Glance

| File | Produced by | Lives until |
|---|---|---|
| `.ai/session/plan.md` | `define` | `cleanup` |
| `.ai/session/tasks.md` | `define`, updated by `execute` | `cleanup` |
| `.ai/session/walkthrough.md` | stub by `define`, appended by `execute` | `cleanup` |
| `.ai/session/<slug>-summary.md` | `summarize` | moved on `cleanup` |
| `.ai/memory/archive/plans/<YYYY-MM-DD>-<slug>.md` | `cleanup` | permanent |

Templates for every artifact live in `assets/`. **Use them
verbatim** — the structure is what makes the framework consistent
across plans and sessions.

| Asset | When |
|---|---|
| `assets/plan-template.md` | `define` |
| `assets/tasks-template.md` | `define` |
| `assets/walkthrough-template.md` | `define` (stub) |
| `assets/plan-summary-template.md` | `summarize` |

## Discrepancy Handling

When the request, the spec, or the documented brain disagrees with
what the codebase actually shows:

1. **Ask first, write second.** Use a structured questionnaire (e.g.
   `ask_user_input_v0` when available, otherwise inline chat
   questions). Do not emit `[NEEDS CLARIFICATION]` blocks into the
   final artifact — the artifact is the answer, not a list of pending
   doubts.
2. **Record only the discrepancies that survived clarification.** If
   after asking, the plan still deviates from an *approved* spec, the
   plan must contain a "Discrepancies vs spec" section (the template
   has it). Trivial deviations (renaming a field, choosing between
   equivalent libraries) belong in `walkthrough.md`, not in this
   section.

## Git Interaction Policy

JAIBA does not prescribe a versioning strategy. Within this skill:

- **At the end of every executed phase**, suggest a short message
  like `chore(wip): <phase name>` and let the developer decide whether
  to commit, stash, or carry on. Do not run `git commit` on your own
  initiative.
- **At the end of `summarize`**, propose a conventional-commit
  message (`feat`, `fix`, `refactor`, `perf`, `chore`, etc.) inferred
  from the plan's purpose, useful both for a single commit and for a
  squash of the phase-wise WIP commits.
- **If the developer asks you to run a git command** (`git status`,
  `git add`, `git commit`, `git push`, `git stash`, etc.) — do it.
  The "no autonomous commits" rule in `AGENTS.md` means "don't act
  without being asked", not "refuse git access".

## Asking the Human

When a mode says "ask the developer", prefer a structured
questionnaire over a wall of prose questions. Concrete rules:

- One topic per question. Don't bundle "which library and which DB
  and which auth scheme" into one prompt.
- Provide 2–4 mutually exclusive options when the answer space is
  closed (e.g. TDD on/off, library A/B/C).
- For open-ended questions (rationale, constraints), use plain chat.
- Never proceed past `define` while clarification questions remain.

## Hand-off Between Modes

The modes form a chain, not a cycle, within a single plan:

```
define  ──→  execute  ──→  summarize  ──→  cleanup
            (loops phase
             by phase)
```

- `define` ends when the developer explicitly approves the plan. No
  approval ⇒ no `execute`.
- `execute` runs **one phase at a time**, with a pause for human
  review at every phase boundary. Phases are not chained
  automatically.
- `summarize` requires all tasks checked. If something is unchecked,
  ask the developer whether to drop it, defer it, or finish it first.
- `cleanup` requires a summary file in `.ai/session/`. It is
  destructive — confirm before running the script.

When in doubt about which step is next, re-read the relevant mode
reference rather than improvising.
