# `conduct:summarize`

Close the work in **one step**: distill the essence, show it to the
human, propose what the brain should learn, then — on one explicit
confirmation — archive to `.ai/memory/log/` and clean `.ai/work/`.
End state: `.ai/memory/log/<YYYY-MM-DD>-<slug>.md` exists, ADR/brain
proposals are on the table for `jaiba-init:update-brain`, a final
conventional-commit message is suggested, and `.ai/work/` is empty.

There is deliberately **one confirmation, not two ceremonies**: the
summary is presented and the developer's single "go ahead" both
accepts it and authorizes the archive. What is *not* negotiable is
that the human reads the summary before the executive memory is
destroyed — never chain draft-and-archive in one breath without
showing it.

## Preconditions

1. `validate` has passed (gate green; criteria delivered or waivers
   documented). If validate hasn't run, run it first — summarize
   never substitutes for it.
2. `.ai/work/plan.md` exists; tasks are checked.

## Flow

1. **Read everything in `.ai/work/`** — plan, tasks, walkthrough, PRD
   if present.
2. **Draft the summary** as `.ai/work/<slug>-summary.md` from
   `assets/plan-summary-template.md`. Hard rules:
   - **English, always** — it becomes a long-term memory artifact,
     even when the session (and the work artifacts) were in another
     language. Translate the essence.
   - **Concise** — one screen. The walkthrough was the narrative;
     this is the record. Outcomes, not play-by-play.
   - Record criteria delivered (with corrective ones flagged),
     deviations vs the plan/PRD and why, and any waived checks.
   - **Carry citations over as links, not prose.** A brain concept the
     work consulted or touched is cited the same way the plan cited it
     — a file-relative markdown link, resolved from the entry's home
     in `.ai/memory/log/` (so `../identity/quality-gate.md`,
     `../references/stripe.md`, `../decisions/004-event-bus.md` in a
     bundle; `../constitution.md`, `../reference-index.md` in the
     legacy flat layout). Never a section number. A citation that does
     not resolve is surfaced to the human, never archived silently —
     `spec-mode.md § A citation that doesn't resolve is surfaced,
     never emitted` governs here too, and this is the last chance to
     catch it before the executive memory is destroyed.
3. **Evaluate the brain-change question.** For each non-trivial
   decision in the walkthrough's checkpoint blocks: is it structural?
   Will future work need the *why*? If yes, include the proposed
   `decision` concept (status: Proposed) in the summary — **propose
   only**; enacting is `jaiba-init:update-brain`'s right. If no: state
   "No ADR proposed; all decisions were tactical." Same for a new
   `reference` concept (an integration the work introduced that the
   brain doesn't carry yet) and for changes to the `scope`,
   `quality-gate` or `sub-unit` concepts worth promoting. Name what
   the proposal *is* by `type:`; where it will land is
   `update-brain`'s call, and it differs by layout (a `decision` file
   in a bundle, an `adr-log.md` entry in the legacy flat layout).
   Proposed text that cites an existing concept cites it as a link,
   under the same rule as step 2.
4. **Suggest the final commit message.** Conventional-commit type
   inferred from the work (`feat` / `fix` / `refactor` / `perf` /
   `chore` / `docs`) — the natural squash target for the phase-wise
   `chore(wip)` commits. Don't run git unasked.
5. **Present and confirm.** Show the summary (or its essence) and ask
   one clear question: *"This will be archived to `.ai/memory/log/`
   and `.ai/work/` will be cleaned. Proceed?"* Amendments welcome —
   apply, re-show, re-ask.
6. **Archive.** On the yes, run:
   ```bash
   bash scripts/archive.sh <slug>
   ```
   The script is the source of truth for the layout: it verifies the
   summary exists and no task is left unchecked, moves it to
   `.ai/memory/log/<YYYY-MM-DD>-<slug>.md` (date from `plan.md`'s
   `created:`, else today), removes `plan.md` / `tasks.md` /
   `walkthrough.md` / `PRD.md` from `.ai/work/`, and aborts on
   unexpected files so the developer decides about them. **Read the
   script before running it** — it is short by design.
7. **Report and hand off.** Where the log entry lives; that
   `.ai/work/` is ready for the next piece of work; and — if ADRs or
   brain changes were proposed — that `jaiba-init:update-brain` is the
   next stop to enact them.

## When *not* to run the script

Do the operation manually (or stop and ask) if the repo's `.ai/`
layout is non-default (mounted/symlinked), the slug contains unusual
characters, or the developer asked to keep one of the work files.
The script is a convenience; the contract is *"essence lives in
`.ai/memory/log/`, `.ai/work/` is empty"* — achieve it however the
repo allows.

## Worked example (TripNest)

Plan `collaborative-itineraries` validated: gate green, ITIN-001…003
delivered (ITIN-008 corrective, also delivered).

1. Draft `collaborative-itineraries-summary.md`: outcome (invitation
   flow with role-based perms), 4 criteria delivered (1 corrective),
   deviations (none structural), consulted concepts cited as links
   (`[django-guardian](../references/django-guardian.md)`), proposed
   `decision` "Roles as CharField choices, not a separate table",
   suggested commit
   `feat(itineraries): collaborator invitations with role-based
   access`.
2. Present; developer: *"go ahead"*.
3. `bash scripts/archive.sh collaborative-itineraries` → entry at
   `.ai/memory/log/2026-07-03-collaborative-itineraries.md`, work
   cleaned.
4. Report + point at `jaiba-init:update-brain` for the proposed
   `decision`.

## Common failure modes

- **Archiving unseen.** The single-step design removes ceremony, not
  the human's read. Present first, always.
- **A non-English log entry.** `.ai/memory/` is English-only; the
  work artifacts' language doesn't carry over.
- **Long summaries.** Past one screen you're duplicating the
  walkthrough. Distill.
- **ADR fatigue.** Tactical choices stay in the log entry. If it
  wouldn't matter to someone joining in six months, it's not an ADR.
- **Writing a `decision`, `scope` or `quality-gate` concept
  directly** — under any layout, flat file or bundle. Propose;
  `jaiba-init:update-brain` enacts. The `log/` append is the only
  carve-out.
- **Archiving a dead citation.** `.ai/work/` is about to be deleted;
  a link into the brain that doesn't resolve becomes unfixable the
  moment the plan is gone. Surface it while the evidence still
  exists.
- **Editing an archived entry later.** `.ai/memory/log/` is
  append-only — corrections are new entries referencing the old one.
