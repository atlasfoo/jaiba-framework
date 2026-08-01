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
3. **Evaluate the ADR question.** For each non-trivial decision in
   the walkthrough's checkpoint blocks: is it structural? Will future
   work need the *why*? If yes, include the proposed ADR block
   (status: Proposed) in the summary — **propose only**; enacting is
   `jaiba-init:update-brain`'s right. If no: state "No ADR proposed; all
   decisions were tactical." Same for reference-index entries (a NEW
   integration the work introduced) and constitution changes (scope /
   gate / sub-unit shifts) worth promoting.
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
   deviations (none structural), proposed ADR "Roles as CharField
   choices, not a separate table", suggested commit
   `feat(itineraries): collaborator invitations with role-based
   access`.
2. Present; developer: *"go ahead"*.
3. `bash scripts/archive.sh collaborative-itineraries` → entry at
   `.ai/memory/log/2026-07-03-collaborative-itineraries.md`, work
   cleaned.
4. Report + point at `jaiba-init:update-brain` for the proposed ADR.

## Common failure modes

- **Archiving unseen.** The single-step design removes ceremony, not
  the human's read. Present first, always.
- **A non-English log entry.** `.ai/memory/` is English-only; the
  work artifacts' language doesn't carry over.
- **Long summaries.** Past one screen you're duplicating the
  walkthrough. Distill.
- **ADR fatigue.** Tactical choices stay in the log entry. If it
  wouldn't matter to someone joining in six months, it's not an ADR.
- **Writing to `adr-log.md` or the constitution directly.** Propose;
  `jaiba-init:update-brain` enacts.
- **Editing an archived entry later.** `.ai/memory/log/` is
  append-only — corrections are new entries referencing the old one.
