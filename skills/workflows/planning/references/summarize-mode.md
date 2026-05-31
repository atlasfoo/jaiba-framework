# `planning:summarize`

Close out a finished plan with a concise, archivable record. End
state: `.ai/session/<slug>-summary.md` exists, an ADR entry is
proposed (or explicitly declined), and a final conventional-commit
message is suggested. **The session is not cleaned up yet** — that's
`cleanup`.

## Preconditions

Stop and ask if any of these is not true:

1. `.ai/session/plan.md` exists and is approved.
2. Every task in `.ai/session/tasks.md` is checked.
3. The Quality Gate passes (run the commands from constitution §6 if
   the last run was not in the current session).

If some tasks are unchecked but the developer wants to summarize
anyway, surface the gap. Options to offer:
- Finish the remaining tasks first.
- Move them to a new plan and summarize what is done.
- Drop them and record the drop in the summary.

Never silently summarize an incomplete plan.

## Flow

1. **Read everything.** `plan.md`, `tasks.md`, `walkthrough.md`,
   plus the active spec (`PRD.md` and `user-stories.md`) if any.
2. **Reconcile the spec.** If a spec is active (the plan's `spec:` /
   `stories:` frontmatter, or an active folder under `.ai/specs/`):
   - Mark each story this plan satisfied as `[x]` in
     `user-stories.md`. Don't touch stories the plan didn't address.
   - **Capture out-of-spec work that the PRD needed.** If, during
     execution, the plan did something the spec hadn't foreseen but
     that was necessary for the PRD to hold (typically a bug fix —
     check `walkthrough.md` for out-of-band changes and structural
     drift), that work should exist as a **retroactive corrective
     story** in `user-stories.md`. If it isn't there yet, route to
     `specification:define` to add it (as a corrective `<PREFIX>-NNN`),
     then mark it `[x]`. This keeps the spec the single source of
     truth for everything it took to satisfy the PRD, instead of
     burying necessary fixes in a walkthrough.
3. **Draft the summary** using `assets/plan-summary-template.md`.
   Hard rules:
   - **Be concise.** The summary lives forever in the brain; bloat
     will accumulate over the project's life. Aim for one screen.
   - Record outcomes, not narrative. The walkthrough is the
     narrative; the summary is the *result*.
   - Highlight deviations: what changed vs `plan.md`, why, and
     whether the team should learn something from it.
4. **Evaluate the ADR question.** Look at each non-trivial decision
   in `walkthrough.md` and ask:
   - Is it *structural*? (introducing/removing a major lib,
     changing an architectural pattern, redefining a boundary,
     superseding a prior ADR)
   - Will future work need to know *why*?
   If yes → propose an ADR entry following `adr-log.md`'s template
   meta-instructions. **Propose only.** Never write to `adr-log.md`
   on your own — that belongs to `update-brain` and to the developer.
   If no → say so explicitly in the summary: *"No ADR proposed; all
   decisions were tactical."* (This signal is useful for reviewers.)
5. **Suggest a final commit message.** Use a conventional-commit
   prefix inferred from the plan's nature:
   - `feat:` — new user-visible capability.
   - `fix:` — corrects a bug.
   - `refactor:` — restructures without changing behavior.
   - `perf:` — performance improvement.
   - `chore:` — internal maintenance.
   - `docs:` — documentation only.
   This message is the natural squash target if the developer kept
   `chore(wip)` commits per phase. Don't run the commit yourself
   unless asked.
6. **Hand off.** Tell the developer the summary is ready and that
   the next step, when they're ready, is `planning:cleanup`. Do not
   trigger cleanup automatically.
   - **If this plan closed the last open story in an active spec**
     (every story in `user-stories.md` is now `[x]`), also point the
     developer at `specification:archive` — the spec is fully
     delivered and ready to be closed into long-term memory. Mention
     it; don't trigger it.

## Naming and location

- The summary file is `<slug>-summary.md` in `.ai/session/`. Slug
  comes from `plan.md`'s frontmatter. Cleanup will rename and move
  it.
- Until cleanup runs, the summary coexists with the other session
  files — that's intentional, so the developer can review the
  summary against the source material in one place.

## Worked example (TripNest)

The plan `collaborative-itineraries-base-model` covered three
phases (domain model, invitation service, API endpoints) and is
fully checked. Walkthrough shows one structural decision
(`CharField` + choices for roles, with the explicit deferral of a
roles table to the future).

Steps:

1. Read all session files, plus the active spec.
2. Mark the four `user-stories.md` items this plan covered.
3. Write `collaborative-itineraries-base-model-summary.md`:
   - Outcome: invitation flow operational with role-based perms.
   - Deviations: none vs plan; minor — used `prefetch_related` in
     the collaborator list endpoint for performance, recorded in
     walkthrough.
   - Quality gate: passing.
4. Propose ADR: "Roles as `CharField` choices, not a separate
   table." Status: Proposed. Context, decision, alternatives,
   consequences. This is structural enough — future work touching
   permissions will want to find it.
5. Suggest `feat(itineraries): collaborator invitations with role-based access`.
6. Tell the developer: ready for cleanup when you are.

## Common failure modes

- **Long summaries.** Past two screens is too long. Trim it. The
  walkthrough is the record; the summary is the headline.
- **Proposing ADRs for everything.** ADR fatigue is real. Tactical
  choices belong in walkthrough only. If a decision wouldn't matter
  to someone joining the project in six months, it's not an ADR.
- **Writing to `adr-log.md` directly.** Propose, don't enact.
- **Running cleanup in the same turn.** They're separate modes for a
  reason — the developer should be able to read the summary, possibly
  amend it, before destroying the session.
