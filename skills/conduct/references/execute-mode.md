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

Two execution paths, same rules and same outputs. If the host agent
supports subagents and the JAIBA executor battery is installed, prefer
**delegated execution in waves** (next section). Otherwise — or when
the pre-invocation check says otherwise — run this **sequential path**
yourself:

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
check` — battery installed, every needed executor's `requires:` tools
present per `.atl/tool-layout.md`. Any gap ⇒ surface it now and fall
back to the sequential path (or a partial one: an available tier can
still take its tasks). Never discover a gap mid-wave.

1. **Build the wave.** From the active phase's unchecked tasks, take
   every task whose `depends-on` IDs are all checked. That set is the
   candidate wave.
2. **Partition by files.** Infer each candidate's file footprint from
   its statement and the plan. Tasks whose footprints might overlap
   don't share a wave — keep the first, defer the rest. When in doubt,
   serialize (`subagents.md § Concurrency policy`).
3. **Fan out, capped at 3 in flight.** Dispatch each task to the
   executor tier its `load` names (`subagents.md § load → executor
   tier`), each with the three-part envelope: the task verbatim,
   minimal context, the Phase gate commands. A wave wider than the cap
   runs in batches.
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

**Fallback is sequential, not optional.** No subagent support, no
battery, or a declined tool install ⇒ the sequential path above, in
dependency order. Same rules, same walkthrough, same gate — delegation
changes throughput, never the contract.

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

1. Preflight: git clean, no prior phases, Phase 1 active.
2. T-001 (failing test) → confirm it fails for the right reason →
   walkthrough entry: `T-001 — collaborator model test red, as
   expected`.
3. T-002 (model) → test green → entry logged. T-003 (migration) →
   entry. T-004, T-005 → entries (T-005 notes the decision to map
   guardian perms per role via choices, matching the plan).
4. Phase gate green. Checkboxes flipped as each task landed.
5. Phase-checkpoint block appended; suggest `chore(wip): itinerary
   collaborator domain model`; pause.

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
