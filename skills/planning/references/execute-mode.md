# `planning:execute`

Advance an approved plan, one phase at a time. End state per
invocation: one phase fully done, `tasks.md` updated,
`walkthrough.md` appended, the Quality Gate green, a commit message
suggested.

This mode is **implicit by default** — the developer does not type a
slash command. Activation conditions:

1. `.ai/session/plan.md` exists and has been explicitly approved.
2. `.ai/session/tasks.md` has at least one unchecked task.
3. The developer's message is a continuation cue:
   - `continue`, `next`, `go`, `proceed`, `keep going`.
   - A direct answer to a pending question you asked at the end of
     the previous phase.

If the message is anything else (a question, an unrelated request, a
new requirement), **don't enter execute**. Either route to `ask` /
`fast` or ask the developer what they want.

## Preflight checks

Run these in order. Stop and ask on any failure.

1. **Read `plan.md` and `tasks.md`.** Confirm the plan is approved and the
   tasks reflect the same scope. If they diverged (e.g., the developer
   hand-edited the plan), treat the manual edits as final and re-align
   tasks accordingly before doing anything else. Note the Phase Gate
   commands in `tasks.md § Gate Commands` — you will use them after each
   phase.
2. **Read the walkthrough.** It tells you what already happened in
   prior phases of this same plan, including decisions and deviations.
3. **Check `git status`.** A dirty worktree means uncommitted work
   from another session or manual edits. **Stop and report it.**
   Suggest the developer either commit, stash, or discard before
   proceeding. Do not silently overwrite changes. If the developer
   explicitly says "go anyway", proceed.
4. **Identify the next phase.** The next phase is the first one with
   any unchecked task. If a phase depends on prior phases that are
   not fully checked, surface that and ask.

> `constitution.md` and `reference-index.md` are not re-read here.
> Everything needed for execution is in the session files.

## Executing a phase

Operate one phase at a time. Do not start the next phase in the same
turn unless the developer explicitly asks.

1. **Take the first unchecked task in the active phase.** Implement
   it atomically. If you can't complete it as written (missing API,
   surprising state), stop and surface the obstacle — don't
   improvise.
2. **Run the Phase Gate after each meaningful change.** Use the Phase Gate
   commands from `tasks.md § Gate Commands`. If a gate command fails,
   fix it as part of the current task — don't accumulate red.
3. **Update `tasks.md` as you go.** Flip checkboxes only on truly
   complete tasks. Half-done is unchecked.
4. **Append to `walkthrough.md` at the end of the phase**, not after
   every task. Use the format in
   `assets/walkthrough-template.md` (the phase log block). Record:
   - What was done, in 3–6 lines max.
   - Non-trivial decisions made and their reasoning.
   - Any deviation from `plan.md` and `tasks.md`.
   - Anything that suggests a future ADR.
5. **Suggest a commit message.** Default form: `chore(wip): <phase
   name>`. Mention that this is a WIP candidate; the developer
   decides what to do with it. If the developer asks you to run the
   commit, do it. Otherwise leave it as a suggestion.
6. **Pause.** Do not continue into the next phase automatically. The
   developer triggers the next phase with another continuation cue.

## Mid-phase deviations

Two patterns to handle deviations:

- **Trivial drift** (renaming a variable, picking between two
  equivalent libraries, fixing a typo in a comment): just do it,
  note it in the walkthrough.
- **Structural drift** (a task in the plan turns out to require a
  different approach, or a new task surfaces): stop, surface, ask. If
  the developer agrees, update both `tasks.md` (add/remove/reword
  tasks) **and** `plan.md` (a short note in the "Plan amendments"
  section). The walkthrough records the why.

Never silently rewrite the plan. If you find yourself wanting to,
that's the signal to stop and ask.

## Worked example (TripNest)

Plan: itinerary collaborators, Phase 1 (Domain model), TDD enabled.
Tasks remaining:

```
- [ ] Write failing test for ItineraryCollaborator model
- [ ] Implement ItineraryCollaborator model
- [ ] Wire object-level permissions with django-guardian
```

Developer says: *"continue"*.

Steps:

1. `git status` → clean. OK.
2. Last phase done: none. Active phase: Phase 1.
3. Pick first unchecked: "Write failing test...". Write the test,
   confirm it fails for the right reason.
4. Pick next: "Implement...". Make the test pass.
5. Pick next: "Wire object-level permissions...". Implement.
6. Run Phase Gate (affected tests, lint, typecheck, format). Green.
7. Check the three tasks in `tasks.md`.
8. Append to `walkthrough.md` the Phase 1 block, noting the choice
   of `CharField` over a separate roles table (matches the plan,
   nothing new) and that `django-guardian` permissions were applied
   per the documented pattern.
9. Suggest `chore(wip): domain model for itinerary collaborators`.
10. Pause. Wait for the developer.

## Common failure modes

- **Skipping `git status`.** Worktrees aren't always yours alone.
  Other sessions and manual edits exist.
- **Stacking phases in one turn.** Atomicity says one logical change
  at a time. Phase boundaries are review points; respect them.
- **Logging every task in the walkthrough.** It's a phase log, not
  a tick-by-tick diary. Aggregate.
- **Improvising on structural drift.** When the plan stops matching
  reality, stop and amend it. Don't keep coding and hope.
