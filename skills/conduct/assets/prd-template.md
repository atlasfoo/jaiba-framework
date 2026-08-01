---
slug: <kebab-case-slug>                # e.g. collaborative-itineraries
created: <YYYY-MM-DD>
status: draft                          # draft | approved | delivered
prefix: <SHORT-UPPERCASE>              # criteria-ID prefix — e.g. ITIN
source: manual                         # manual | file | ticket
source-ref: <path-or-ticket-id-or-empty>
---

# PRD: <Requirement title>

> Product Requirements Document — produced by `conduct:spec`
> (define step) only when triage lands at `spec` depth. Concise by
> design: one to two screens. It states the *what* and the *why*; the
> *how* belongs to the design (`plan.md`). Lives in `.ai/work/` until
> `summarize` archives its essence.

## Problem & context

<The *why*. What can users not do today? Ground it in the current
behavior of the system, not a hypothetical one. 2–5 sentences.>

## Goals / Non-goals

**Goals:**
- <What success looks like, business-level. 2–4 bullets.>

**Non-goals:**
- <What this explicitly does NOT attempt — the adjacent things a
  reader might assume are included but aren't.>

## Users

- <Role A> — <what they need>
- <Role B> — <what they need>

## Proposed solution

<The agreed shape, high level. Cite the existing integration or
pattern it reuses (`reference-index.md`) rather than inventing a new
one. Not a design doc — no schemas, no sequence diagrams.>

## Scope

**In:**
- <Concrete capability 1>

**Out:**
- <Deliberately excluded, with a one-line reason.>

## Assumptions & constraints

- <Assumptions the spec relies on — including ones the code imposes.>
- <Constraints — performance, security, compliance, platform.>

## Dependencies

- <External integration or package, cited from
  `.ai/memory/reference-index.md`. A NEW integration not yet indexed:
  flag as "NEW — to be added" so it surfaces for
  `jaiba-init:update-brain`.>

## Success metrics

- <Something observable over a feeling. "X% of trips have ≥2
  collaborators within 30 days.">

## Acceptance criteria

> The machine contract of this PRD. Rules:
> - IDs are `<PREFIX>-NNN`, incrementing, **never reused or
>   renumbered**. Gaps fine; reshuffling not. Corrective criteria
>   surfaced during execution take the next ID with
>   `corrective: true`.
> - Every criterion is Given/When/Then, with at least one `happy`
>   and normally one or more `sad` paths — a criterion with no sad
>   path is almost always under-specified.
> - Keep this block **well-formed YAML**: `conduct:validate`
>   (and the `verify` subagent) parse it to check delivery criterion
>   by criterion. Prose belongs in the sections above, not here.
> - `status` is flipped to `delivered` by `validate`, never by hand.

```yaml
criteria:
  - id: <PREFIX>-001
    title: <short title>
    story: As a <role>, I want <capability> so that <benefit>.
    happy:
      - given: <precondition>
        when: <action>
        then: <expected outcome>
    sad:
      - given: <error precondition>
        when: <action>
        then: <handled failure>
    status: open            # open | delivered
  - id: <PREFIX>-002
    title: <short title>
    story: As a <role>, I want <capability> so that <benefit>.
    happy:
      - given: <precondition>
        when: <action>
        then: <expected outcome>
    sad:
      - given: <edge precondition>
        when: <action>
        then: <handled edge>
    status: open
```

<!--
Worked example (delete when filling the template):

```yaml
criteria:
  - id: ITIN-001
    title: Invite a collaborator by email
    story: As an owner, I want to invite a collaborator by email so
      that they can help me plan the trip.
    happy:
      - given: I own an itinerary
        when: I invite a valid email with the role "editor"
        then: an invitation is created and the invitee gains editor
          access to that itinerary
    sad:
      - given: the email already collaborates on the itinerary
        when: I invite it again
        then: I get an "already a collaborator" error and no duplicate
          is created
      - given: I am only an editor (not the owner)
        when: I try to invite someone
        then: the action is rejected with a permission error
    status: open
  - id: ITIN-008
    title: Refresh expiring session mid-edit
    story: As a collaborator, I want my session refreshed before it
      expires mid-request so that I'm not silently logged out while
      editing.
    corrective: true        # surfaced during ITIN-005
    happy:
      - given: my session is near expiry
        when: I save an edit
        then: the session is refreshed transparently and the edit
          succeeds
    sad:
      - given: my session is already fully expired
        when: I save an edit
        then: I'm redirected to log in and my unsaved edit is
          preserved locally
    status: open
```
-->

## Open questions

<MUST be empty at approval. If anything is here, the define step is
not finished — resolve via the questionnaire and move the answer into
the relevant section above.>
