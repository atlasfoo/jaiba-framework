---
name: planning
description: >-
  Tactical planning workflow inside the JAIBA framework. Use this skill whenever the developer wants to plan a concrete piece of work, advance an existing plan, wrap up a completed plan, or archive its session artifacts. Trigger on any of: explicit calls like "planning define / summarize / cleanup", phrases like "let's plan", "let's build a plan", "next task", "continue the plan", "close this plan", "archive the plan". Also trigger implicitly whenever `.ai/session/plan.md` exists in the repository and the developer's message reads as a continuation cue (e.g. "next", "go", "advance", "keep going", "okay continue"). Covers writing plan.md and tasks.md, executing tasks phase by phase with walkthrough logging, summarizing a finished plan with optional ADR proposal, and cleaning up `.ai/session/` after archival.
version: 1.0.0
author: atlasfoo<iscomejia15@outlook.com>
requires:
  - git
tags:
  - jaiba
  - workflows
  - jaiba-workflows
  - plan-mode
---

# Planning Skill

Tactical workflow for building, executing, summarizing, and archiving
plans within the JAIBA framework. This is the everyday workhorse for
concrete pieces of work that need traceability but don't warrant a
full `specification` cycle.

This skill has **four modes**, each documented in its own reference
file. Read the relevant reference *before* taking action — the
selection table below tells you which one.

## Brain Discovery and Validation

This skill can be installed per-project (`.claude/skills/`,
`.agents/skills/`) or **globally** (e.g. `~/.claude/skills/`), shared
across every repository you work in. Either way, "the brain" means
`.ai/` and `AGENTS.md` at the root of the **project you're currently
in** — where `.git/` lives — never a path relative to this skill's own
installation location.

Before selecting a mode, confirm the project is JAIBA-instrumented:

1. **`AGENTS.md` exists at the project root, is non-empty, and is the
   JAIBA behavioral contract** — it describes the `.ai/` Brain Map and
   the numbered Behavioral Rules. An `AGENTS.md` that exists but is
   unrelated (some other agent-instructions file) doesn't count.
2. **`.ai/memory/constitution.md`, `adr-log.md`, and
   `reference-index.md` exist and hold real content** — not the bare
   `[bracket]` templates.

If either check fails, **stop here** — do not enter any mode or write
to `.ai/session/`. An orphaned plan with no constitution to ground it
helps no one. Tell the developer plainly what's missing and route
them:

- No `.ai/` at all → `jaiba-scaffold` (installs the skeleton, the
  behavioral `AGENTS.md`, and the rest of the skillset).
- `.ai/` exists but `.ai/memory/` is bare templates → `update-brain`
  in `initialize` mode.
- `AGENTS.md` is missing or isn't the JAIBA contract → `jaiba-scaffold`
  (it handles the existing-`AGENTS.md` coexist/replace decision).

## Mode Selection

Decide the mode **before** reading anything else. If the message is
ambiguous, ask the developer instead of guessing.

| Situation | Mode | Read |
|---|---|---|
| Developer asks for a new plan / says "planning define" / there is no `.ai/session/plan.md` and they describe work to do | `define` | `references/define-mode.md` |
| `.ai/session/plan.md` exists, `tasks.md` has unchecked tasks, and the developer's message is a continuation cue (`continue`, `next`, `go`, `advance`, `keep going`, a reply to a pending question) | `execute` *(implicit)* | `references/execute-mode.md` |
| `.ai/session/plan.md` exists, all tasks in `tasks.md` are checked, developer asks to close / wrap up / "planning summarize" | `summarize` | `references/summarize-mode.md` |
| `.ai/session/<slug>-summary.md` exists, developer asks to clean up / archive / "planning cleanup" | `cleanup` | `references/cleanup-mode.md` |
| Anything else, including `.ai/session/plan.md` exists but the message is unrelated to the plan | **Ask.** Don't enter any mode silently. | — |

## Context Loading

Context is loaded per mode — not universally — to minimize token usage.
Read only what your mode requires.

### `define` (full context)
1. **`AGENTS.md`** — behavioral contract.
2. **`.ai/memory/constitution.md`** — Quality Gate (§6), TDD mode (§7), stack and conventions.
3. **`.ai/memory/reference-index.md`** — sections relevant to integrations the plan will touch.
4. **Active spec, if any** — `.ai/specs/<name>/PRD.md` and `user-stories.md`. Identify story IDs
   this plan covers; their acceptance criteria are the source for tests, and `summarize` will
   mark them `[x]` when the plan closes.

### `execute` (session only)
1. **`AGENTS.md`** — behavioral contract.
2. **`.ai/session/plan.md`**, **`tasks.md`**, **`walkthrough.md`** — complete plan context,
   including Phase Gate commands embedded in `tasks.md § Gate Commands`.

> `constitution.md` and `reference-index.md` are **not** re-read during execute.
> Gate commands and TDD posture were copied into `tasks.md` at define time.

### `summarize` (session only)
1. **`AGENTS.md`** — behavioral contract.
2. **`.ai/session/plan.md`**, **`tasks.md`**, **`walkthrough.md`** — plan outcomes and gate commands.

### `cleanup` (no reads required)
Verify the summary file exists, then run the cleanup script.

---

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
