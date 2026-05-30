# `planning:define`

Build a new plan from scratch. End state: `.ai/session/plan.md` and
`.ai/session/tasks.md` exist, are coherent with the codebase, and the
developer has explicitly approved them.

This mode runs **only** when no plan is currently active in
`.ai/session/`. If `plan.md` already exists, stop and ask the
developer whether to discard, summarize, or continue the existing
plan — never silently overwrite.

## Inputs

- The developer's prompt describing the work.
- An optional active spec — when the developer references one, or
  when a single spec lives under `.ai/specs/` and the prompt fits it,
  treat its `user-stories.md` as the primary source of scope.
- The codebase itself — the plan must be grounded in what exists,
  not in what the prompt assumes exists.
- The constitution — for stack, Quality Gate, and the TDD mode flag.
- `reference-index.md` — for any external integrations the plan
  touches.

## Flow

1. **Read the universal preconditions** (see `SKILL.md`).
2. **Survey the codebase.** Don't read everything — read what the
   request will plausibly touch: the relevant module / app / layer,
   its tests, its closest neighbors. Tools serve discovery here, not
   bulk content delivery (see `AGENTS.md` §3).
3. **Detect discrepancies.** Compare the prompt and (if present) the
   spec against what the codebase shows:
   - Does the spec assume a model that doesn't exist yet, or
     contradicts an existing one?
   - Does the prompt reference an integration not in
     `reference-index.md`?
   - Are there conventions in the constitution that the prompt
     violates?
   List every discrepancy you find.
4. **Clarify before writing.** For each discrepancy and each open
   question about scope, ask the developer using a structured
   questionnaire (prefer `ask_user_input_v0` if available, otherwise
   chat). One topic per question. Loop until no clarification is
   pending — **never** punt unresolved questions into the artifact.
5. **Decide the TDD posture.** Read the `TDD mode` line from the
   constitution's Planning Conventions section.
   - `enabled` (default) ⇒ structure phases as red → green →
     refactor. Each implementation task is preceded by a failing-test
     task **in the same phase**.
   - `disabled` ⇒ tests are scheduled at the team's discretion;
     typically a dedicated phase.
6. **Decompose into phases.** Group tasks by **architectural
   cohesion**, not by chronology. Each phase must:
   - Have a single, nameable theme (e.g., "Domain model", "API
     layer", "Frontend integration").
   - Leave the codebase in a reversible, buildable, gate-passing
     state when complete (so a `chore(wip)` commit is safe).
   - Declare its dependencies on prior phases in its header.
7. **Write the artifacts.** Use the templates verbatim:
   - `assets/plan-template.md` → `.ai/session/plan.md`
   - `assets/tasks-template.md` → `.ai/session/tasks.md`
   - `assets/walkthrough-template.md` → `.ai/session/walkthrough.md`
     (stub only; gets populated during `execute`)
8. **Stop and ask for approval.** The plan is not active until the
   developer says so explicitly (`"approved"`, `"go ahead"`,
   `"confirmed"`, etc.). Do not transition into `execute`. Do not
   write any source code.

## What goes in `plan.md`

The template (`assets/plan-template.md`) is authoritative. Brief map:

- **Identity:** slug, date, spec reference if any.
- **Objective:** the *what* and *why* in 2-4 sentences.
- **Scope:** in / out. Be explicit about exclusions — what looks
  in-scope but isn't.
- **Technical approach:** the *how*. Cite the constitution,
  `reference-index.md`, knowledge skills, and external docs as
  relevant.
- **Discrepancies vs spec:** only if a spec is active *and* the plan
  deliberately deviates from it. Empty otherwise.
- **Sources consulted:** brain files, knowledge skills, external
  references, web searches. This is how reviewers see what shaped the
  plan.

## What goes in `tasks.md`

The template (`assets/tasks-template.md`) is authoritative. Key rules:

- Phases are numbered (Phase 1, Phase 2, ...). Tasks within a phase
  use checkboxes.
- Each phase header declares: theme, depends-on (list of phase IDs or
  "none"), reversible-yes/no, suggested-commit-message.
- Tasks are imperative and concrete: "Add `ItineraryCollaborator`
  model with FK to `Itinerary` and `User`" — not "Work on the
  collaborator model".
- If TDD is `enabled`, the test task is the first task of each
  implementation pair: `[ ] Write failing test for X`, then
  `[ ] Implement X`, then optionally `[ ] Refactor X`.

## Worked example (TripNest)

The developer says: *"Let's implement the email invitation for
itinerary collaborators."* A spec `collaborative-itineraries`
is active. The codebase already has `Itinerary` and `User` models;
`django-guardian` is configured per `reference-index.md`; there is no
`ItineraryCollaborator` model yet.

Steps in this mode:

1. Read `PRD.md`, `user-stories.md`, the `Itinerary` model and its
   views, `reference-index.md` (django-guardian entry).
2. Detect discrepancies: the spec mentions roles `owner /
   editor / reader`, but the codebase has no permission scheme yet.
   Not a contradiction, a gap. List it.
3. Ask, via questionnaire: "For roles, should we use `CharField` with
   choices or a separate table?" → developer picks `CharField`.
4. Read constitution: TDD `enabled`.
5. Decompose into phases:
   - Phase 1 — Domain model (model + permissions + tests).
   - Phase 2 — Invitation service (email integration + tests).
   - Phase 3 — API endpoint exposure.
   Phase 2 depends on Phase 1; Phase 3 depends on Phase 2.
6. Write plan.md and tasks.md from templates.
7. Stop, ask for approval.

## Common failure modes

- **Writing without surveying.** Plans grounded in assumptions
  produce phantom tasks. Read the code first.
- **Silent over-scoping.** If the prompt seems small but you find
  three hidden subsystems, surface that as a question, not as eight
  extra phases.
- **Stuffing `[NEEDS CLARIFICATION]` into the artifact.** Forbidden.
  Ask in chat.
- **Skipping the approval pause.** `define` ends at "approve?". Not
  at "I wrote the files". The developer's word is the trigger for
  `execute`.
