# Tasks: <plan slug>

## Gate Commands

<!-- Populated by conduct:tasks from constitution.md §6. Do not edit manually. -->

**Phase gate** (run at each phase close):
- `<affected tests command>`
- `<lint command>`
- `<typecheck command>`
- `<format check command>`

**Plan gate** (run once in `conduct:validate`):
- `<full test suite command>`
- `<coverage command>`
- `<build command>`
- `<security scan command>` *(omit if not configured)*

---

> Task rules:
> - IDs are `T-NNN`, incrementing, **never reused or renumbered**.
> - `depends-on` lists task IDs (or `none`) — a graph, not a chapter
>   order. Tasks with no path between them are independent; `execute`
>   may run them in parallel if they don't share files.
> - `load` is cognitive load (`high` = design judgment / multi-file,
>   `medium` = bounded implementation, `low` = mechanical) — it picks
>   the executor tier on delegation.
> - `covers` maps the task to acceptance criteria IDs from the PRD
>   schema (`—` at design depth). Every criterion must be covered by
>   at least one task.
> - Phases are **multisession checkpoints**: architectural cohesion,
>   reversible/buildable at close, gate green, safe `chore(wip)`
>   commit point. A phase cannot start until `depends on:` phases are
>   fully checked.
> - If TDD is enabled, every implementation task is preceded by a
>   failing-test task in the same phase.

---

## Phase 1 — <Theme>

- **Depends on:** none
- **Reversible:** yes
- **Suggested commit:** `chore(wip): <short phase summary>`

- [ ] **T-001** — <task, concrete and imperative>
  `load: <high|medium|low>` · `depends-on: none` · `covers: <PREFIX>-NNN`
- [ ] **T-002** — <task>
  `load: <high|medium|low>` · `depends-on: [T-001]` · `covers: <PREFIX>-NNN`

---

## Phase 2 — <Theme>

- **Depends on:** Phase 1
- **Reversible:** yes
- **Suggested commit:** `chore(wip): <short phase summary>`

- [ ] **T-003** — <task>
  `load: <high|medium|low>` · `depends-on: [T-002]` · `covers: —`
- [ ] **T-004** — <task independent of T-003 — may run in parallel>
  `load: <high|medium|low>` · `depends-on: [T-002]` · `covers: —`

---

<!--
TDD-enabled worked example (delete when filling the template):

## Phase 1 — Domain model
- **Depends on:** none
- **Reversible:** yes
- **Suggested commit:** `chore(wip): itinerary collaborator domain model`

- [ ] **T-001** — Write failing test for `ItineraryCollaborator` creation and role validation
  `load: medium` · `depends-on: none` · `covers: ITIN-001`
- [ ] **T-002** — Implement `ItineraryCollaborator` model (FK to `Itinerary` and `User`, `role` CharField with choices)
  `load: medium` · `depends-on: [T-001]` · `covers: ITIN-001`
- [ ] **T-003** — Add migration for `ItineraryCollaborator`
  `load: low` · `depends-on: [T-002]` · `covers: ITIN-001`
- [ ] **T-004** — Write failing test for object-level permission lookup per role
  `load: medium` · `depends-on: none` · `covers: ITIN-002, ITIN-003`
- [ ] **T-005** — Wire django-guardian permissions (view/change/delete) per role
  `load: high` · `depends-on: [T-002, T-004]` · `covers: ITIN-002, ITIN-003`

T-001/T-004 share no edge and no files → parallelizable wave.
-->
