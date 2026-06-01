# `fast`: recording a plan adjustment

When a `fast` change is an unplanned adjustment to an **active** plan,
the change has to be reflected in the session artifacts — otherwise
the plan, the tasks, and the walkthrough drift behind what the code
actually does, and the next `planning:execute` or `planning:summarize`
works from a stale picture.

The governing rule: **execute first, confirm, then record.** You do
not write to the session artifacts until the developer confirms the
change is correct. This is what keeps an *approved* plan from silently
expanding — the human stays in the loop on every scope change
(`AGENTS.md` §2.4, §2.8).

## Preconditions

- `.ai/session/plan.md` exists and is approved/executing.
- The change passed triage as `fast`-eligible
  (`references/complexity-triage.md`).
- The change falls inside or adjacent to the plan's scope. If it's
  unrelated to the plan, treat it as **free-standing** instead — don't
  record it into a plan it doesn't belong to.

## Procedure

1. **Execute the change** and bring the Quality Gate green (see
   `SKILL.md` flow). Don't write to session artifacts yet.

2. **Ask the developer to confirm.** Show what changed (a minimal
   diff or a one-line description) and ask whether it's correct before
   you record it. A bare "yes" / "correct" / "confirmed" is enough; silence
   or ambiguity is not. Example:
   > I added the email validation to `InvitationSerializer` and its
   > test passes. Shall I confirm it in the plan (tasks + amendment + walkthrough)?

3. **On confirmation, update the three artifacts.** Keep edits
   surgical — you're annotating, not rewriting.

   - **`tasks.md`** — append the new task to the phase it belongs to,
     already checked, tagged so it's traceable as an out-of-band add:
     ```markdown
     - [x] Validate email format in `InvitationSerializer` (fast, 2026-05-29)
     ```
     If the adjustment instead *modified* a planned task, reword that
     task in place and note the change in the walkthrough.

   - **`plan.md`** — add a dated bullet to the existing **Plan
     amendments** section (the template already provides it):
     ```markdown
     - `2026-05-29` — Added email-format validation to the invitation
       endpoint (fast); not in the original scope, requested mid-phase.
     ```

   - **`walkthrough.md`** — record the *why* so a later reader
     understands a change appeared outside the phase flow. If the
     planning walkthrough template ships the optional **Out-of-band
     change (fast)** block, use it; otherwise append a short block in
     the same spirit:
     ```markdown
     ## Out-of-band change (fast)     2026-05-29
     **Change.** Added email-format validation to `InvitationSerializer`;
     requested mid-phase, not in the original plan.
     **Scope touched.** `serializers.py`, `test_invitation.py`; new task
     under Phase 2.
     **Quality gate.** Pass.
     ```

4. **Suggest a commit.** A `fast` adjustment mid-plan usually folds
   into the current phase's WIP commit. Suggest either amending the
   phase's `chore(wip): <phase>` or a standalone message — let the
   developer decide. Don't run git unless asked.

5. **Hand control back.** The adjustment is recorded; the plan is once
   again in sync. The developer resumes the plan with a normal
   `planning:execute` continuation cue when ready — `fast` does not
   advance the plan itself.

## If the developer says the change is wrong

Don't record anything. Offer to revert or correct the change. The
session artifacts must only ever reflect changes the developer has
accepted — an un-recorded change is recoverable; a recorded wrong one
pollutes the brain.

## What not to do

- **Don't record before confirmation.** The confirmation is the gate.
- **Don't rewrite the plan's Objective/Scope** to absorb the change.
  Amendments are append-only annotations; structural scope changes are
  `planning` work, not `fast`.
- **Don't record a free-standing change into a plan.** If it doesn't
  belong to the active plan, it gets no session entry.
