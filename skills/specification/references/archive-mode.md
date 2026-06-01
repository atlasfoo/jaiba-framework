# `specification:archive`

Close a fully-delivered spec into long-term memory. End state: a
concise archive document lives at
`.ai/memory/archive/specs/<YYYY-MM-DD>-<spec-slug>.md`, any ADRs or
brain updates worth keeping are *proposed* (not written), and the
active spec folder `.ai/specs/<spec-slug>/` is **removed**.

This is a **single mode with a confirmation gate** — not a two-step
draft-then-destroy like `planning:summarize`/`cleanup`. The reason for
the difference: a plan summary coexists with live session files the
developer needs to review side by side, so planning splits the steps.
A spec archive is one self-contained document; the developer reviews it
inline, confirms, and the folder is gone. The confirmation gate is what
keeps the removal safe.

Archiving is **destructive** (it deletes the spec folder). Confirm
explicitly before the removal step.

## Preconditions

Stop and ask if any of these is not true:

1. An active spec exists at `.ai/specs/<spec-slug>/` with `PRD.md` and
   `user-stories.md`.
2. **Every** user story in `user-stories.md` is checked `[x]`. If some
   are open, the spec isn't done — surface the open ones and offer:
   - Finish them first (via `planning`).
   - Drop them, recording the drop in the archive's "Deviations".
   - Split them into a follow-up spec and archive only what shipped.
   Never silently archive an incomplete spec.
3. The Quality Gate is green (the delivered work should be in a
   healthy state at the moment it's frozen into memory).

## Flow

1. **Read everything.** `PRD.md`, `user-stories.md`, and the
   closed-plan summaries in `.ai/memory/archive/plans/` that reference
   this spec (they are the detailed record of *how* each story was
   delivered, and the source for ADR candidates).
2. **Draft the archive document** from
   `assets/spec-archive-template.md`, written to
   `.ai/specs/<spec-slug>/archive.md` (the script picks it up from
   there). Hard rules:
   - **Write it in English.** The archive lives in `.ai/memory/`,
     which is English-only (`AGENTS.md` §3.5) — even when the PRD and
     stories were written in another language. Translate the essence;
     don't paste the original.
   - **Be concise.** This is a permanent record, read for orientation
     years later — aim for one to two screens. The detail lives in the
     plan summaries; this is the distilled headline of the whole
     requirement.
   - Record **outcomes**, not narrative: what the requirement
     delivered, which stories shipped, which plans built them, and
     what deviated from the original PRD.
3. **Show it to the developer for review.** Present the draft
   (`.ai/specs/<spec-slug>/archive.md`) so they can catch errors
   *before* the folder is destroyed.
4. **Evaluate ADRs and knowledge to promote.** Across the whole spec,
   look for:
   - **Structural decisions** worth an ADR (a new pattern, a major
     library, a boundary redefined). Propose them following
     `adr-log.md`'s template — **propose only**, never write to
     `adr-log.md` (that's `update-brain`).
   - **New integrations** that should land in `reference-index.md`.
   - **Scope or identity shifts** that should update `constitution.md`.
   If none, say so explicitly in the archive ("No ADR proposed; no
   brain updates needed"). This signal is useful to reviewers.
5. **Confirm intent.** Ask for explicit confirmation before the
   destructive step, e.g. *"I'll archive the spec to
   `.ai/memory/archive/specs/<date>-<slug>.md` and remove
   `.ai/specs/<slug>/`. Proceed?"*. A bare "yes" is enough; ambiguity
   is not.
6. **Archive and remove.** Use `scripts/archive.sh` — it is the single
   source of truth for the archive layout:
   ```bash
   bash scripts/archive.sh <spec-slug>
   ```
   The script (read it before running — it's short by design):
   - Verifies `.ai/specs/<spec-slug>/` and the drafted
     `archive.md` exist, and refuses if any story is still unchecked.
   - Creates `.ai/memory/archive/specs/` if needed.
   - Moves the draft to
     `.ai/memory/archive/specs/<YYYY-MM-DD>-<spec-slug>.md` (today's
     date — the *archival* date, matching how `planning` dates its
     plan archives).
   - Removes the `.ai/specs/<spec-slug>/` folder.
   - Prints what it did.
7. **Hand off to `update-brain`.** If you proposed ADRs, integrations,
   or constitution changes, tell the developer the next step is
   `update-brain` to apply them. Don't apply them yourself.

## When *not* to run the script

Do the operation manually (or stop and ask) if:

- The repo's `.ai/` layout differs from JAIBA defaults (symlinked or
  mounted elsewhere) — the script assumes the default layout.
- The spec slug contains spaces or unusual characters.
- The developer wants to keep the spec folder for their own reasons.

The script is a convenience, not the contract. The contract is:
*"the archive doc lives in `.ai/memory/archive/specs/`, the active spec
folder is gone."* Achieve it however the repo allows.

## Naming

- Archive file: `<YYYY-MM-DD>-<spec-slug>.md` (archival date, not the
  PRD creation date — matches how `planning` dates its plan archives).
- The folder is `.ai/memory/archive/specs/`, sibling to
  `.ai/memory/archive/plans/`.

## Worked example (TripNest)

The spec `collaborative-itineraries` (prefix `ITIN`) has all stories
`[x]`; three plans built it, each summarized under
`.ai/memory/archive/plans/`. The developer says: *"let's archive this
spec."*

Steps:

1. Read PRD, stories, the three plan summaries.
2. Draft `collaborative-itineraries` archive (in English): outcome
   (in-app invitation-based collaboration with roles, live), stories
   shipped (ITIN-001…ITIN-009, incl. one corrective ITIN-008),
   plans that built it, deviations (last-write-wins kept; real-time
   deferred as planned).
3. Show the draft. Developer reads, approves.
4. Propose one ADR: "Object permissions via django-guardian for
   itinerary roles" — structural, future permission work will want it.
   No constitution change.
5. Confirm: *"Archive and remove the spec folder?"* → "yes".
6. `bash scripts/archive.sh collaborative-itineraries` →
   `.ai/memory/archive/specs/2026-05-30-collaborative-itineraries.md`,
   folder removed.
7. Hand off: *"One ADR proposed — run `update-brain` to record it in
   `adr-log.md` when you're ready."*

## Common failure modes

- **Archiving with open stories.** Unchecked `[ ]` means not done.
  Surface them; offer finish / drop / split. Don't bury open work.
- **A non-English archive in `.ai/memory/`.** The long-term brain is
  English-only. Translate.
- **Destroying before review.** The confirmation gate exists so the
  developer can catch an error before the folder is gone. Don't
  fast-path it.
- **Writing to `adr-log.md` directly.** Propose; let `update-brain`
  enact.
- **Bloated archives.** Past two screens is too long. The plan
  summaries hold the detail; this is the requirement-level headline.
