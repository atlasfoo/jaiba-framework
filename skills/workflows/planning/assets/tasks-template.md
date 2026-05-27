# Tasks: <plan slug>

> Phase rules:
> - Phases have **architectural cohesion**, not chronological grouping.
> - Each phase leaves the codebase **reversible and buildable** — a
>   safe point for a `chore(wip)` commit.
> - Dependencies are declared in the header (`depends on: ...`). A
>   phase cannot start until its dependencies are fully checked.
> - If TDD is enabled in `constitution.md`, every implementation
>   task is preceded by a failing-test task within the same phase.

---

## Phase 1 — <Theme>

- **Depends on:** none
- **Reversible:** yes
- **Suggested commit:** `chore(wip): <short phase summary>`

- [ ] <Task 1 — concrete and imperative>
- [ ] <Task 2>
- [ ] <Task 3>

---

## Phase 2 — <Theme>

- **Depends on:** Phase 1
- **Reversible:** yes
- **Suggested commit:** `chore(wip): <short phase summary>`

- [ ] <Task 1>
- [ ] <Task 2>

---

## Phase 3 — <Theme>

- **Depends on:** Phase 2
- **Reversible:** yes
- **Suggested commit:** `chore(wip): <short phase summary>`

- [ ] <Task 1>

---

<!--
TDD-enabled example (delete this block when filling the template):

## Phase 1 — Domain model
- **Depends on:** none
- **Reversible:** yes
- **Suggested commit:** `chore(wip): itinerary collaborator domain model`

- [ ] Write failing test for `ItineraryCollaborator` model creation and role validation
- [ ] Implement `ItineraryCollaborator` model with FK to `Itinerary` and `User`, `role` CharField with choices
- [ ] Add migration for `ItineraryCollaborator`
- [ ] Write failing test for object-level permission lookup per role
- [ ] Wire `django-guardian` permissions (view/change/delete) per role
-->
