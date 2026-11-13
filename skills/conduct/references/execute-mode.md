# `conduct:execute`

Advance the approved work, one plan-phase at a time, in the resolved
executive context. End state per invocation: one phase fully done,
`tasks` and `walkthrough` updated and verified, the Phase gate green, a
commit message suggested.

This phase is **implicit by default** — the routing rule sends
continuation cues here. Activation conditions:

1. A fully read `plan` exists in the resolved executive context with
   `status: approved` (or later).
2. The context's fully read `tasks` artifact has at least one unchecked
   task.
3. The developer's message is a continuation cue: `continue`, `next`,
   `go`, `proceed`, `keep going`, or a direct answer to the question
   you asked at the previous phase boundary.

Anything else routes per `SKILL.md § Routing rule` — a question is
`ask`'s, an out-of-band change request is `fast`'s. Don't enter
execute for them.

## Preflight checks

Run in order; stop and ask on any failure.

1. **Resolve and `render` the context's executive artifacts.** Catalogue
   the selected context completely; resolve `plan`, `tasks` and
   `walkthrough` by exact logical address and `render` their materialized
   content, revision, and head. Read the entire artifacts, not previews,
   search hits, or summaries. Only in the explicit filesystem branch do
   these names mean `.ai/work/plan.md`, `tasks.md` and `walkthrough.md`.
   An unavailable, partial, truncated, ambiguous or permission-filtered
   result is not absence: stop and surface it; never switch surfaces or
   contexts.
2. **Confirm approval, scope and resume point.** Check the verified plan
   approval, reconcile tasks against its scope, and use walkthrough
   entries together with task checkboxes to resume actual progress across
   sessions. Manual developer edits are final directives; re-align the
   artifacts before continuing. Note the gate commands in the fully read
   `tasks` artifact (`Gate Commands`).
3. **Check `git status`** whenever the selected work root is a Git
   checkout/worktree, regardless of the selected memory surface. A dirty
   worktree means uncommitted work
   from another session or manual edits. Stop and report; suggest
   commit/stash/discard. Proceed only on an explicit "go anyway" —
   or when the dirt is exactly the uncommitted output of this plan's
   previous phase (compare against the walkthrough) and the developer
    has chosen to carry WIP forward. An external workspace with no Git
    root has no Git status to check; this alone is not a failure.
4. **Identify the active phase.** The first phase with any unchecked
   task, provided its `depends on:` phases are fully checked;
   otherwise surface the broken ordering and ask.

> The constitution is **not** re-read here. Gate commands and TDD
> posture were copied into `tasks.md` at the `tasks` phase.

### Executive artifact writes and recovery

Conduct is the only executive writer for this context. Establish
serialized access and retain each object's exact address, materialized
revision, and `expected-head` before mutating it. Do not implicitly
create or upsert `tasks` or `walkthrough`. When `executive-journal` is
realized, task transitions are `patch` ops, O(delta), not a rewrite of
either artifact:

| Transition | Address | Op |
|---|---|---|
| Task truly complete | `tasks` | `check` with those IDs |
| Checkbox set in error, after reconciliation | `tasks` | `uncheck` with those IDs |
| One compact walkthrough entry, or the phase-checkpoint block | `walkthrough` | `append-entry` |

`check` of an already checked ID is a no-op, not a conflict. Only the
checkbox character changes. Preserve unknown metadata and relations.
On `record-store`, one accepted `patch` is one new delta plus that
object's `context-head` slot — not a new base and not a catalogue
rewrite. On `document-tree`, the same ops are a surgical edit of the
document. Before any dependent checkbox or Phase-gate progress, retain
the mutation receipt and `render` the complete intended artifact,
including the resulting head. Acknowledgement without verified readback
is not completion. On conflict, unknown outcome, missing receipt/readback,
or mismatch, stop dependent progress and reconcile by exact `render`
before retrying. Do not append a compensating delta. A `1.0.x` adapter
gets the same ops applied locally, then a complete `update` with
`efficiency-warning: full-update-without-patch`. Filesystem names map to
local paths only in the filesystem branch; elsewhere use logical
addresses, never guessed paths or backend record IDs. These checks do
not alter the existing Phase gate or task authority rules.

At a phase boundary, if `executive-journal.compaction-threshold` is a
known delta count and the active count is strictly greater, `compact`
that object. Exceeding the threshold does not fail the gate. An unknown
threshold does not fire the suggestion. Do not compact inside `check` or
`append-entry`. `1.0.x` has no `compact`; note that and continue.

### Surface outage or uncertain progress

Use the effective `create-memory/references/resolution.md` outage policy.
Offer retry/stop or explicitly confirmed recovery through effective
`jaiba-init/references/surface-migration.md`, never filesystem fallback by
creating `.ai/work/`, changing context, or reconstructing tasks from summaries.
Pause new executor waves and dependent writers; account for already dispatched
children and their actual effects before retry. Include all affected contexts
sharing constitutive data or publication infrastructure in the writer freeze.

Retain the original project/context, task IDs, exact attempted artifact request,
full intended value, pre-read revisions, receipts and child reports. A lost
update acknowledgement may mean the write happened: reconcile that exact request
by complete reads and ownership/revision evidence before retrying it. A new
request ID or unchecked-looking task is not evidence of nonexecution. On return,
re-read the complete context and reconcile actual source changes with the human.

If walkthrough verified but tasks failed (or conversely), preserve both outcomes
and mark the phase pending reconciliation. Do not infer completion from one
artifact, run dependent tasks, record gate approval, suggest phase completion or
start the next phase. A gate command's actual result may be reported as evidence,
but code success, an executor report or a partial memory write does not commit
workflow progress. Resume only after all required artifacts and their consistent
progress have full verified readback under serialized access. Recovery restores
evidence, not plan approval, task completion or validation that never occurred.

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
   save the analysis for decisions that actually need it. Persist it
   with `append-entry`, then `check` that task. This is what makes the
   work auditable mid-flight and resumable mid-phase.
3. **Run the Phase gate after each meaningful change.** If a gate
   command fails, fix it as part of the current task — don't
   accumulate red.
4. **Flip checkboxes only on truly complete tasks.** Half-done is
   unchecked.
5. **At the phase boundary, `append-entry` the phase-checkpoint block**
   to the walkthrough: outcome in 3–6 lines, decisions worth keeping,
   deviations, ADR candidates, gate result. Then apply the compaction
   rule above if the threshold says so.
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
Detected definition files alone do not prove runtime support. When a
needed role is missing, not callable, or misconfigured, alert first naming
the role and concrete blocker before sequential fallback; do not block
the chain, and continue dispatching available tiers. An actual dispatch error
requires review of child state and possible partial writes before safe retry or
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
   report: review it against `git diff`; `append-entry` the task's
   walkthrough entry yourself from the report (task ID, what changed,
   decisions — conduct is the walkthrough's only writer); `check` the
   ID only if truly complete. Closing a wave is one `check` of the
   completed IDs plus one `append-entry` per completed task, not an
   `update` of either object. An executor that reported an
   obstacle gets its task back in the pool — resolve the obstacle
   (or surface it to the developer) before re-dispatching. `uncheck`
   only a box this phase set in error.
5. **Repeat** — new wave from the newly unblocked tasks — until the
   phase has no unchecked tasks.
6. **Close the phase as usual:** run the Phase gate yourself (executor
   runs don't substitute for the phase-close gate), append the
   phase-checkpoint block, suggest the commit, pause.

**Fallback requires evidence.** Inline sequential execution is limited
per role/task to the concrete blockers in `subagents.md § Dispatch and
fallback accounting`. When a needed role is missing, not callable, or
misconfigured, alert first naming the role and concrete blocker before
sequential fallback; do not block the chain. Record dispatched role or
fallback reason beside each task's result. Convenience, task size, and
overlapping files never justify bypassing an available executor. Same
walkthrough and gate apply.

## Mid-phase deviations

- **Trivial drift** (rename, equivalent-library pick, typo fix): do
  it, log it in the task's walkthrough entry.
- **Structural drift** (a task needs a different approach; a new task
  surfaces; a "design"-depth change turns out to alter user-visible
  behavior): stop, surface, ask. On agreement `add-task` new `T-NNN`s
  — never renumber, never `remove-task` — `append-to-section` on the
  plan's amendments heading, and — if the drift is a fix the PRD needs
  to hold — `add-criterion` with the next ID and `corrective: true`.
  Do not `update-criterion` or `remove-criterion` once `status` is not
  `draft`; that fails `conflict`. The walkthrough records the why via
  `append-entry`.

Never silently rewrite the plan. Wanting to is the signal to stop and
ask.

## Worked example (TripNest)

Phase 1 (Domain model), TDD enabled, tasks T-001…T-005 as in the
tasks template's example. Developer: *"continue"*.

1. Preflight: git clean, no prior phases, Phase 1 active; the runtime
   executors are callable and their prerequisites are green.
2. Dispatch T-001 and T-004 concurrently to their matching load
   executors: they are independent tests with disjoint files. Review
   both returned results, `append-entry` each task in the walkthrough, and `check`
   each ID only when complete.
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
- **Letting executors touch `.ai/work/` or emit `patch`.** Reports flow
  up; you `append-entry` and `check` (`subagents.md § Concurrency
  policy`).
- **Rewriting `tasks` or `walkthrough` to flip one box.** `check` and
  `append-entry` are the wave close. A full `update` is the `1.0.x`
  warning path only.
