# `conduct:execute`

Advance the approved work, one plan-phase at a time. End state per
invocation: one phase fully done, `tasks.md` updated, the walkthrough
carrying one entry per change, the Phase gate green, a commit message
suggested.

This phase is **implicit by default** — the routing rule sends
continuation cues here. Activation conditions:

1. `.ai/work/plan.md` exists with `status: approved` (or later).
2. `.ai/work/tasks.md` has at least one unchecked task.
3. The developer's message is a continuation cue: `continue`, `next`,
   `go`, `proceed`, `keep going`, or a direct answer to the question
   you asked at the previous phase boundary.

Anything else routes per `SKILL.md § Routing rule` — a question is
`ask`'s, an out-of-band change request is `fast`'s. Don't enter
execute for them.

## Preflight checks

Run in order; stop and ask on any failure.

1. **Read `plan.md` and `tasks.md`.** Confirm approval and that tasks
   still reflect the plan's scope. Manual developer edits to either
   are final directives — re-align the other file to match before
   doing anything else. Note the gate commands in
   `tasks.md § Gate Commands`.
2. **Read `walkthrough.md`.** It is the memory of prior phases *and
   prior sessions* — `.ai/work/` is multisession, and the walkthrough
   plus the checkboxes are how a fresh session reconstructs where
   work stands without re-deriving it.
3. **Check `git status`.** A dirty worktree means uncommitted work
   from another session or manual edits. Stop and report; suggest
   commit/stash/discard. Proceed only on an explicit "go anyway" —
   or when the dirt is exactly the uncommitted output of this plan's
   previous phase (compare against the walkthrough) and the developer
   has chosen to carry WIP forward.
4. **Identify the active phase.** The first phase with any unchecked
   task, provided its `depends on:` phases are fully checked;
   otherwise surface the broken ordering and ask.

> The constitution is **not** re-read here. Gate commands and TDD
> posture were copied into `tasks.md` at the `tasks` phase.

## Executing a phase

One plan-phase per invocation. Do not start the next phase in the
same turn unless the developer explicitly asks.

**Dispatch every task to its load-matched executor** when the current
host permits it, that role is callable, and prerequisites are verified
(`references/subagents.md`). Use delegated waves below even for a single
runnable task. File overlap means sequential executor calls. Use this
**inline sequential path only for affected tasks with a named actual
blocker**, recorded in the walkthrough; keep delegating unaffected tasks:

1. **Pick the next runnable task** — unchecked, with every
   `depends-on` ID checked. Implement it atomically. If it can't be
   completed as written (missing API, surprising state), stop and
   surface the obstacle — don't improvise.
2. **Log the change in `walkthrough.md` as you complete each task** —
   the walkthrough is built **change by change**, not reconstructed
   at the end. One compact entry per task (see the template): task
   ID, what changed, any decision taken. Two lines is usually enough;
   save the analysis for decisions that actually need it. This is
   what makes the work auditable mid-flight and resumable
   mid-phase.
3. **Run the Phase gate after each meaningful change.** If a gate
   command fails, fix it as part of the current task — don't
   accumulate red.
4. **Flip checkboxes only on truly complete tasks.** Half-done is
   unchecked.
5. **At the phase boundary, append the phase-checkpoint block** to
   the walkthrough: outcome in 3–6 lines, decisions worth keeping,
   deviations, ADR candidates, gate result.
6. **Suggest a commit** — default `chore(wip): <phase name>` (the
   phase header carries a suggestion). The developer decides; run git
   only if asked.
7. **Pause.** The next phase starts on the next continuation cue.

## Delegating to executors (waves)

The parallel path. Full contract — envelope, `requires:` convention,
toolchain check, concurrency policy — in `references/subagents.md`;
this section is the wave mechanics.

**Preflight for delegation** (on top of the phase preflight): run the
pre-invocation check from `subagents.md § Pre-invocation toolchain
check` — host permission, exposed/callable roles, and verified tools.
Detected definition files alone do not prove runtime support. Surface
any gap with its role/task and record the reason for affected inline work;
continue dispatching available tiers. An actual dispatch error requires
review of child state and possible partial writes before safe retry or
fallback (`subagents.md § Dispatch and fallback accounting`).

1. **Build the wave.** From the active phase's unchecked tasks, take
   every task whose `depends-on` IDs are all checked. That set is the
   candidate wave.
2. **Partition by files.** Infer each candidate's file footprint from
   its statement and the plan. Tasks whose footprints might overlap
   don't share a wave — keep the first, defer the rest. When in doubt,
   serialize (`subagents.md § Concurrency policy`).
3. **Fan out, capped at min(3, available host child slots).** Dispatch
   each task to the executor tier its `load` names (`subagents.md § load
   → executor tier`), with the task verbatim, minimal context, and Phase
   gate commands. Name its owned files and other workers' ownership;
   require accommodation of concurrent edits without reverting them.
   Launch each independent batch before awaiting any result. Larger
   waves run in batches; overlap and a one-slot host serialize through
   executors. Dispatch a one-task wave too.
4. **Reintegrate every result before the next wave.** Per returned
   report: review it against `git diff`; write the task's walkthrough
   entry yourself from the report (task ID, what changed, decisions —
   conduct is the walkthrough's only writer); flip the
   checkbox only if truly complete. An executor that reported an
   obstacle gets its task back in the pool — resolve the obstacle
   (or surface it to the developer) before re-dispatching.
5. **Repeat** — new wave from the newly unblocked tasks — until the
   phase has no unchecked tasks.
6. **Close the phase as usual:** run the Phase gate yourself (executor
   runs don't substitute for the phase-close gate), append the
   phase-checkpoint block, suggest the commit, pause.

**Fallback requires evidence.** Inline sequential execution is limited
per role/task to the concrete blockers in `subagents.md § Dispatch and
fallback accounting`. Record dispatched role or fallback reason beside
each task's result. Convenience, task size, and overlapping files never
justify bypassing an available executor. Same walkthrough and gate apply.

## Mid-phase deviations

- **Trivial drift** (rename, equivalent-library pick, typo fix): do
  it, log it in the task's walkthrough entry.
- **Structural drift** (a task needs a different approach; a new task
  surfaces; a "design"-depth change turns out to alter user-visible
  behavior): stop, surface, ask. On agreement update `tasks.md`
  (append new `T-NNN`s — never renumber), `plan.md § Plan
  amendments`, and — if the drift is a fix the PRD needs to hold — a
  **corrective criterion** in the PRD schema. The walkthrough records
  the why.

Never silently rewrite the plan. Wanting to is the signal to stop and
ask.

## Worked example (TripNest)

Phase 1 (Domain model), TDD enabled, tasks T-001…T-005 as in the
tasks template's example. Developer: *"continue"*.

1. Preflight: git clean, no prior phases, Phase 1 active; the runtime
   executors are callable and their prerequisites are green.
2. Dispatch T-001 and T-004 concurrently to their matching load
   executors: they are independent tests with disjoint files. Review
   both returned results, log each task in the walkthrough, and flip
   each checkbox only when complete.
3. Dispatch T-002 to its matching load executor once T-001 is checked.
   After reviewing it, T-003 and T-005 are runnable (T-004 is already
   checked): dispatch them concurrently if their file footprints are
   disjoint, otherwise serialize them through their matching load
   executors. Review and log each result, then update its checkbox.
4. Run the Phase gate after the work is integrated and all results are
   reviewed. Append the phase-checkpoint block; suggest
   `chore(wip): itinerary collaborator domain model`; pause.

## Common failure modes

- **Skipping `git status`.** Worktrees aren't always yours alone.
- **Stacking plan phases in one turn.** Boundaries are review points;
  respect them.
- **Reconstructing the walkthrough at the phase boundary.** Change by
  change means *as you go* — a session that dies mid-phase should
  leave a walkthrough that says exactly how far it got.
- **A diary instead of a log.** One compact entry per change; the
  checkpoint block aggregates. Don't paste diffs into the
  walkthrough.
- **Improvising on structural drift.** When the plan stops matching
  reality, stop and amend it. Don't keep coding and hope.
- **Fanning out without the pre-invocation check**, or launching the
  next wave before every result of the current one is reviewed,
  logged, and checked off. Waves are sequential; only their insides
  are parallel.
- **Letting executors touch `.ai/work/`.** Reports flow up; you write
  the walkthrough and flip the boxes (`subagents.md § Concurrency
  policy`).
