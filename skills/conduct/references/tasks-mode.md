# `conduct:tasks`

Decompose the approved design into an executable work graph. End
state: `.ai/work/tasks.md` exists (from `assets/tasks-template.md`),
`.ai/work/walkthrough.md` exists as a stub (from
`assets/walkthrough-template.md`), and `execute` can start.

## Preconditions

- `.ai/work/plan.md` exists with `status: approved`. No approved plan
  ⇒ back to `spec`. Never generate tasks for a draft.
- `constitution.md` is readable — this is the phase that copies gate
  commands and TDD posture into `tasks.md`, so `execute` never needs
  the constitution again.

## What a task is

A task is one atomic, imperative, delegable unit: "Add
`ItineraryCollaborator` model with FK to `Itinerary` and `User`" —
not "work on the collaborator model". Each task carries:

- **ID** — `T-NNN`, incrementing, never reused. Stable references for
  `depends-on`, the walkthrough, and (later) subagent delegation.
- **`depends-on`** — the task IDs that must be complete first, or
  `none`. This is a *graph*, not a chapter order: two tasks with no
  path between them are independent by declaration, which is what
  lets `execute` parallelize safely. Only declare real dependencies —
  an inflated chain serializes everything.
- **`load`** — `high | medium | low`, the cognitive load of the task:
  - `high` — design judgment, multi-file changes, ambiguity to
    resolve while working.
  - `medium` — a bounded implementation with a clear contract.
  - `low` — mechanical/repetitive work (renames, boilerplate, config
    echoes).
  Label honestly by *judgment required*, not by effort or prestige —
  the label maps one-to-one onto the executor battery when `execute`
  delegates (`references/subagents.md § load → executor tier`), so a
  dishonest label sends the task to the wrong tier. When genuinely in
  doubt between two labels, take the higher one.
- **`covers`** — the acceptance criteria IDs (`<PREFIX>-NNN`) this
  task contributes to, when a PRD exists; `—` otherwise. Every
  criterion in the PRD schema must be covered by at least one task —
  an uncovered criterion is undeliverable by construction; surface it
  and fix the decomposition before asking for anything else.

## Phases: multisession checkpoints

Group tasks into phases by **architectural cohesion**, not
chronology. Each phase:

- Has a single nameable theme, declares `depends on:` prior phases,
  and leaves the codebase reversible, buildable, and gate-passing —
  a safe `chore(wip)` commit point.
- Is the unit of human review and the unit of session recovery:
  `.ai/work/` is gitignored and multisession, so a fresh session
  resumes from the first phase with unchecked tasks.
- Ends with the **Phase gate** (commands in `tasks.md § Gate
  Commands`).

## Flow

1. **Read `plan.md`** (and `PRD.md` if present).
2. **Read constitution §6 and §7**; copy the Phase Gate and Plan Gate
   commands **verbatim** into `tasks.md § Gate Commands` (the actual
   CLI commands, not descriptions), and note the TDD posture.
3. **Decompose.** TDD `enabled` ⇒ red → green → refactor: every
   implementation task is preceded by a failing-test task in the same
   phase, and the tests come straight from the PRD's happy/sad
   criteria — they're already written, in prose, in the schema. TDD
   `disabled` ⇒ tests scheduled at the team's discretion; criteria
   still define "done".
4. **Wire the graph.** Assign IDs in reading order, declare
   `depends-on` per task, label `load`, map `covers`. Check every
   criterion is covered.
5. **Write `tasks.md`** from the template; **write the walkthrough
   stub** from its template.
6. **Show the graph summary** (phases, task count, any long
   dependency chains) and confirm the developer is ready to execute.
   This is a light confirmation, not a second approval gate — the
   design was already approved; this just hands the wheel over.

## Common failure modes

- **Tasks without IDs, or renumbered IDs.** Everything downstream
  references `T-NNN`; treat IDs as permanent.
- **A linear `depends-on` chain by reflex.** If T-007 doesn't truly
  need T-006, don't say it does — false edges destroy parallelism.
- **`load: high` on everything.** If every task needs the top tier,
  the labels carry no information. Mechanical work is `low`; say so.
- **Uncovered criteria.** A PRD criterion no task covers will fail
  `validate` at the end — catch it here where it's cheap.
- **Regenerating tasks for an amended plan from scratch.** Amend the
  graph: keep completed task IDs, append new ones, adjust edges.
