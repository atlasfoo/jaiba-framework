# `fast`: out-of-band changes while a plan is active

When a change request arrives while `.ai/work/plan.md` is active and
the work wasn't contemplated by the plan, it is **out-of-band**. What
happens next depends on the size the shared triage measured
(`conduct/references/triage.md`, consumed with default/floor
`inline`):

- **`inline` — a contained adjustment.** `fast` executes it and, after
  the developer confirms, records it into the work artifacts. This is
  the bulk of this reference.
- **`design` or deeper — a big out-of-band change.** `fast` does
  **not** execute. It surfaces the size and offers exactly two exits:
  fold the work into the active plan as a new phase, or
  park-and-replan. See "The big out-of-band change" below.

Either way, one prohibition is absolute: **never create a second plan
silently.** `.ai/work/` holds one plan; anything that would need
another one goes through the developer, in the open.

---

## Case 1 — contained adjustment (`inline`)

The change has to be reflected in the work artifacts — otherwise the
plan, the tasks, and the walkthrough drift behind what the code
actually does, and the next `conduct` `execute` or `summarize`
phase works from a stale picture.

The governing rule: **execute first, confirm, then record.** You do
not write to the work artifacts until the developer confirms the
change is correct. This is what keeps an *approved* plan from silently
expanding — the human stays in the loop on every scope change
(`AGENTS.md` §2.4, §2.8).

### Preconditions

- `.ai/work/plan.md` exists and is approved/executing.
- The change triaged `inline` (shared triage).
- The change falls inside or adjacent to the plan's scope. If it's
  unrelated to the plan, treat it as **free-standing** instead — don't
  record it into a plan it doesn't belong to.

### Procedure

1. **Execute the change** and bring the Quality Gate green (see
   `SKILL.md` flow). Don't write to work artifacts yet.

2. **Ask the developer to confirm.** Show what changed (a minimal
   diff or a one-line description) and ask whether it's correct before
   you record it. A bare "yes" / "correct" / "confirmed" is enough; silence
   or ambiguity is not. Example:
   > I added the email validation to `InvitationSerializer` and its
   > test passes. Shall I confirm it in the plan (tasks + amendment + walkthrough)?

3. **On confirmation, update the three artifacts.** Keep edits
   surgical — you're annotating, not rewriting.

   - **`tasks.md`** — append the new task to the phase it belongs to,
     already checked, with the next free `T-NNN` ID (never renumber
     existing tasks) and tagged so it's traceable as an out-of-band
     add:
     ```markdown
     - [x] **T-014** — Validate email format in `InvitationSerializer` *(fast, out-of-band, 2026-05-29)*
       `load: low` · `depends-on: none` · `covers: —`
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
     understands a change appeared outside the phase flow. The
     conduct's walkthrough template ships the **Out-of-band
     change (fast)** block — use it (or append a short block in the
     same spirit):
     ```markdown
     ## Out-of-band change (fast)     2026-05-29
     **Change.** Added email-format validation to `InvitationSerializer`;
     requested mid-phase, not in the original plan.
     **Scope touched.** `serializers.py`, `test_invitation.py`; new task
     T-014 under Phase 2.
     **Gate.** Pass.
     ```

4. **Suggest a commit.** A `fast` adjustment mid-plan usually folds
   into the current phase's WIP commit. Suggest either amending the
   phase's `chore(wip): <phase>` or a standalone message — let the
   developer decide. Don't run git unless asked.

5. **Hand control back.** The adjustment is recorded; the plan is once
   again in sync. The developer resumes the plan with a normal
   continuation cue ("continue", "next"), which routes to the
   conduct's `execute` phase — `fast` does not advance the plan
   itself.

### If the developer says the change is wrong

Don't record anything. Offer to revert or correct the change. The
work artifacts must only ever reflect changes the developer has
accepted — an un-recorded change is recoverable; a recorded wrong one
pollutes the brain.

---

## Case 2 — the big out-of-band change (`design`+)

Mid-plan, the developer asks for something that triages past `inline`
— a breaking dependency upgrade, a contract change, work that needs
its own phases. `fast` must not execute it, and it must not quietly
spin up a parallel plan around it. Instead:

1. **Don't touch the code.** Leave the worktree exactly as the
   in-progress phase left it.

2. **Surface the size with evidence.** Name what triage found — file
   count, contracts hit, migration implied — and say plainly that
   this exceeds an out-of-band adjustment while a plan is active.

3. **Offer exactly two exits** (closed options; the developer
   chooses):

   - **Fold it into the active plan as a new phase.** The work joins
     the plan explicitly: hand off to the `conduct` chain scoped
     to the addition — it designs the phase, appends it to `tasks.md`
     (new `T-NNN` tasks, `depends on:` the appropriate phases), and
     records a dated bullet in `plan.md § Plan amendments` describing
     the scope extension. The developer approves the amended design
     before any of it executes. Choose this when the new work shares
     the plan's subject and can ride its checkpoints.

   - **Park-and-replan.** The active plan pauses at its last
     reversible checkpoint: note the park (and why) in
     `walkthrough.md` and as a dated bullet in `plan.md § Plan
     amendments`, then enter the `conduct` chain to re-plan with
     both the parked remainder and the new work in view. The chain's
     `spec` phase already guards this boundary — it will never
     silently overwrite an active `plan.md`; superseding or absorbing
     the parked plan is an explicit, developer-approved outcome.
     Choose this when the new work invalidates the plan's assumptions
     or outranks it in urgency.

4. **Whatever the choice, it happens in the open.** Both exits go
   through conduct's approval gates. If the developer
   declines both, the request simply waits — that's a valid outcome;
   record nothing.

### What not to do

- **Don't execute "just the first bit" of a big change.** A
  half-applied breaking change mid-plan is the worst state to be in.
- **Don't create or draft a second plan on your own.** Not as a
  "sketch", not in a scratch file, not by overwriting `plan.md`.
- **Don't downgrade the triage to make the change fit.** If the
  evidence says `design`, the answer is the fork above — not a
  generously re-measured `inline`.

---

## What not to do (both cases)

- **Don't record before confirmation.** The confirmation is the gate.
- **Don't rewrite the plan's Objective/Scope** to absorb a change.
  Amendments are append-only annotations; structural scope changes go
  through the fold-as-phase or park-and-replan fork, under the
  conduct's approval gates.
- **Don't record a free-standing change into a plan.** If it doesn't
  belong to the active plan, it gets no work entry.
