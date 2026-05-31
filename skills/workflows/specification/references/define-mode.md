# `specification:define`

Turn a clear requirement into the two durable artifacts. End state:
`.ai/specs/<spec-slug>/PRD.md` and `user-stories.md` exist, are
grounded in the codebase, and the developer has **explicitly
approved** them.

`define` also handles **amending an active spec** — adding stories
(including retroactive corrective ones) or revising the PRD — not just
creating a new one. Detect which case applies before writing.

This mode does **not** write source code. It produces the contract;
`planning` implements it.

## Inputs

- The requirement — from chat, a referenced file, or a tracker ticket
  surfaced by a knowledge skill (see `SKILL.md` "Inputs").
- The landed understanding from a `brainstorm` in this same
  conversation, if there was one.
- The codebase, the brain (constitution, reference-index, adr-log),
  and the change history — per the universal preconditions.

## New spec vs. amend active spec

1. **Derive the spec slug** from the requirement (kebab-case).
2. **Check `.ai/specs/`** for a folder with that slug or an obvious
   overlap.
   - **No match** → new spec. Create `.ai/specs/<spec-slug>/`.
   - **Match / strong overlap** → don't silently create a duplicate.
     Ask the developer whether to (a) amend the existing spec
     (add/revise stories, update the PRD), or (b) create a distinct
     spec with a different slug. Amending is usually right when the
     new work serves the same PRD.

For an **amendment**, read the existing `PRD.md` and `user-stories.md`
first; preserve existing story IDs (never renumber), continue the
numbering from the highest existing one, and touch only what the
change requires.

## Flow

1. **Read the universal preconditions** (see `SKILL.md`).
2. **Survey the code the requirement touches.** Not everything — the
   modules, models, and endpoints the stories will plausibly involve,
   plus their tests. The PRD's "what exists today" must be true.
3. **Detect gaps and contradictions.** Compare the requirement against
   reality:
   - Does it assume a model, endpoint, or integration that doesn't
     exist? (a *gap* — fine, name it)
   - Does it contradict an existing model, a standing ADR, or the
     constitution's scope? (a *contradiction* — a headline question)
   - Does it overlap a sibling spec?
   List every one.
4. **Clarify before writing — questionnaire mode.** For each gap,
   contradiction, and open scope question, ask the developer (see
   `SKILL.md` "Asking the Human"). One topic per question; closed
   options where the answer space is closed. **Loop until nothing is
   pending.** Never emit `[NEEDS CLARIFICATION]` into the artifacts —
   the PRD is the answer, not the question list.
5. **Choose the story prefix.** Propose a short UPPERCASE token
   (≈3–6 chars) for story IDs, derived from the spec name, and confirm
   it with the developer. It must be unique across existing specs
   (check their PRDs' `prefix:` fields). Record it in `PRD.md`
   frontmatter. (Skip on amendment — reuse the spec's existing
   prefix.)
6. **Write `PRD.md`** from `assets/prd-template.md`. Keep it to one or
   two screens — concise enough that both the developer and the agent
   can hold it in their head. The PRD carries the *what* and *why*;
   the *how* is `planning`'s job, so resist drifting into
   implementation detail.
7. **Write `user-stories.md`** from `assets/user-stories-template.md`.
   This is the heart of the spec — see "Writing good user stories"
   below.
8. **Stop and ask for approval.** The spec is a draft until the
   developer says otherwise (`"approved"`, `"go ahead"`,
   `"looks good"`). Set `status: approved` in the PRD frontmatter only
   then. Do not transition into `planning`. Do not write source code.

## What goes in `PRD.md`

`assets/prd-template.md` is authoritative. Brief map:

- **Frontmatter:** `slug`, `created`, `status`, `prefix`, `source`
  (manual / file / ticket), `source-ref`.
- **Problem & context** — the *why*. What can't users do today; what
  pain or opportunity this addresses.
- **Goals / Non-goals** — what success means, and what is explicitly
  not being attempted.
- **Users** — the actors involved.
- **Proposed solution** — high level, the shape agreed in brainstorm.
  Not a design doc.
- **Scope (in / out)** — be explicit about exclusions.
- **Assumptions & constraints** — including the ones the code imposes.
- **Dependencies** — cite `reference-index.md` entries; flag any new
  integration the requirement implies (surface it, don't assume it).
- **Success metrics** — how you'd know it worked.
- **Open questions** — must be **empty at approval**. If it isn't, you
  haven't finished clarifying.

## Writing good user stories

Each story is a **deliverable increment** — a clear unit of value a
`planning` plan can implement and verify on its own. For a frontend
that usually means a screen; for a backend, an endpoint; it can also be
an improvement to an existing capability or a bug fix. If a "story"
can't be delivered and demonstrated on its own, it's either a task
(too small — belongs in a plan) or an epic (too big — split it).

Each story has:

- **ID** — `<PREFIX>-NNN`, incrementing, never reused.
- **Status checkbox** — `[ ]` open, `[x]` closed. `planning:summarize`
  flips these as plans land.
- **The story sentence** — "As a `<role>`, I want `<capability>` so
  that `<benefit>`." The *so that* is not decoration; a story whose
  benefit you can't state is a story whose value is in doubt.
- **Acceptance criteria**, split into **Happy path** and **Sad
  paths**, written as **Given / When / Then**. This format is chosen
  deliberately: it is the direct input to business design *and* to the
  integration tests. Under TDD, these become the test cases a
  `planning` plan writes first — so vague criteria produce vague tests.
  - *Happy path*: the primary success scenario(s).
  - *Sad paths*: the failure and edge scenarios — invalid input,
    missing permission, conflicting state, absent dependency. A story
    with no sad paths is almost always under-specified.

**Ordering carries the dependencies.** For now, the *order* of stories
expresses their natural sequence — earlier stories are foundations for
later ones. There are intentionally no per-story priority or
dependency fields yet; keep the list ordered so the sequence reads
correctly top to bottom.

### Retroactive corrective stories (amendment case)

When `planning` (or `fast`) discovers that delivering the spec requires
work the spec didn't foresee — most often a bug that must be fixed for
the PRD to actually hold — that work becomes a **new story here**,
appended with the next ID. Frame it as the correction it is:

> `OAUTH-014` — As a user, I want the session token to be refreshed
> before it expires mid-request, so that I'm not silently logged out
> while editing. *(Corrective — surfaced during OAUTH-009.)*

This keeps `user-stories.md` the single source of truth for everything
it took to satisfy the PRD, instead of letting necessary fixes vanish
into a plan's walkthrough. The plan that does the fix then references
this story like any other.

## Worked example (TripNest)

Continuing the brainstorm: invitation-based async collaboration on
itineraries, roles owner/editor/reader, last-write-wins, reusing
`django-guardian`.

Steps in this mode:

1. Preconditions read. `django-guardian` confirmed in
   `reference-index.md`.
2. Survey: `Itinerary` model exists — but uses `created_by`, not
   `owner`. No collaborator model yet. No invitation flow.
3. Gaps/contradictions: the role "owner" maps to the existing
   `created_by` (naming mismatch — clarify); no permission scheme
   wired yet (gap, not contradiction).
4. Clarify: *"The spec says 'owner'; the model field is `created_by`.
   Keep `created_by` as the owner, or rename?"* → developer keeps
   `created_by`, owner is a role concept. One question, resolved.
5. Prefix: propose `ITIN`, confirm unique. Record in PRD frontmatter.
6. Write `PRD.md`: problem (no in-app co-planning), users (owner,
   editor, reader), solution (invitations + django-guardian roles),
   scope out (real-time, conflict merge), dependencies
   (`django-guardian`), success metric (X% of trips with ≥2
   collaborators).
7. Write `user-stories.md`, e.g.:
   - `ITIN-001` — As an owner, I want to invite a collaborator by
     email so they can help plan.
     - *Happy:* Given I own an itinerary, When I invite a valid email,
       Then an invitation is created and the invitee gains the chosen
       role.
     - *Sad:* Given the email is already a collaborator, When I invite
       it again, Then I get a "already invited" error and no duplicate
       is created.
   - `ITIN-002` — As an editor, I want to add an activity to a day…
   - `ITIN-003` — As a reader, I want to view but not modify…
8. Stop, ask for approval.

## Common failure modes

- **Writing without surveying.** A PRD that misstates what exists
  today poisons every plan built from it.
- **Stories that aren't deliverable.** "Set up the database" is a
  task; "Refactor the whole booking flow" is an epic. A story is one
  demonstrable increment.
- **Happy-path-only stories.** No sad paths means no failure tests
  means brittle delivery. Push for the edges.
- **Drifting into design.** The PRD says *what* and *why*. Sequence
  diagrams, schema choices, and library decisions are `planning`'s
  territory.
- **Renumbering stories.** IDs are permanent references. Amending a
  spec continues the count; it never reshuffles existing IDs.
- **Skipping the approval pause.** `define` ends at "approved", not at
  "files written".
