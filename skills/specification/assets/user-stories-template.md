# User stories: <spec slug>

> Story rules:
> - Each story is a **deliverable increment** — one screen, one
>   endpoint, one clear improvement, or one fix. Demonstrable on its
>   own. Not a task (too small) and not an epic (too big).
> - IDs are `<PREFIX>-NNN`, incrementing, **never reused or
>   renumbered**. Gaps are fine; reshuffling is not.
> - Acceptance criteria are **Given / When / Then**, split into Happy
>   path and Sad paths. They are the input to business design and to
>   the integration tests — under TDD, a `planning` plan writes these
>   as tests *first*.
> - **Order = dependency.** Earlier stories are foundations for later
>   ones. There are deliberately no priority/dependency fields yet —
>   keep the list ordered so the sequence reads correctly top to
>   bottom.
> - `planning:summarize` flips `[ ]` → `[x]` as plans deliver stories.

---

## `<PREFIX>-001` — <short title>

`[ ]` As a **<role>**, I want **<capability>** so that **<benefit>**.

**Happy path**
- Given <precondition>, When <action>, Then <expected outcome>.

**Sad paths**
- Given <error precondition>, When <action>, Then <handled failure>.
- Given <edge precondition>, When <action>, Then <handled edge>.

---

## `<PREFIX>-002` — <short title>

`[ ]` As a **<role>**, I want **<capability>** so that **<benefit>**.

**Happy path**
- Given …, When …, Then …

**Sad paths**
- Given …, When …, Then …

---

<!--
Worked example (delete when filling the template):

## `ITIN-001` — Invite a collaborator by email

`[x]` As an owner, I want to invite a collaborator by email so that they
can help me plan the trip.

**Happy path**
- Given I own an itinerary, When I invite a valid email with the role
  "editor", Then an invitation is created and the invitee gains editor
  access to that itinerary.

**Sad paths**
- Given the email already collaborates on the itinerary, When I invite
  it again, Then I get an "already a collaborator" error and no
  duplicate invitation is created.
- Given I am only an editor (not the owner), When I try to invite
  someone, Then the action is rejected with a permission error.

## `ITIN-008` — Refresh expiring session mid-edit   (corrective)

`[x]` As a collaborator, I want my session refreshed before it expires
mid-request so that I'm not silently logged out while editing.
*(Corrective — surfaced during ITIN-005.)*

**Happy path**
- Given my session is near expiry, When I save an edit, Then the
  session is refreshed transparently and the edit succeeds.

**Sad paths**
- Given my session is already fully expired, When I save an edit, Then
  I'm redirected to log in and my unsaved edit is preserved locally.
-->
