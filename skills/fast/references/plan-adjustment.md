# `fast`: out-of-band changes while a plan is active

When a change request arrives while an approved plan is active in the
selected executive context and the work wasn't contemplated by the plan,
it is **out-of-band**. For filesystem this plan is `.ai/work/plan.md`; for
an external surface, resolve standard binding `v2` (`~/.jaiba/memory/bindings/<sha256(canonical-work-root)>.yaml`, with legacy fallback to `~/.jaiba/memory/<host>/...` when present), exact context, and use the complete
owned executive catalogue and full logical reads under `jaiba-memory-surface` contract version **1.1.0**. What
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

- The selected context's plan exists and is approved/executing, established
  by authoritative reads (filesystem: `.ai/work/plan.md`; external:
  resolved standard binding `v2` at `~/.jaiba/memory/bindings/<sha256(canonical-work-root)>.yaml`
  with legacy fallback to `~/.jaiba/memory/<host>/...` when present, exact context,
  complete executive catalogue, and exact full reads of plan/tasks and relevant
  walkthrough objects under contract `jaiba-memory-surface` **1.1.0**).
- The change triaged `inline` (shared triage).
- The change falls inside or adjacent to the plan's scope. If it's
  unrelated to the plan, treat it as **free-standing** instead — don't
  record it into a plan it doesn't belong to.

For an external surface, do not interpret an unavailable binding, incomplete
catalogue, partial/truncated read, permission failure, ambiguous context or
missing revision/head evidence as an absent plan. Stop plan-dependent work; make
no memory changes and do not route around the selected surface. Before an
approved adjustment is recorded, retain full-read revision and head baseline evidence (`expected-head`) for the
plan, tasks and walkthrough objects to be changed. `fast` is not the
executive writer: after the developer confirms the completed change,
handoff the proposed amendment operations and baseline evidence to `conduct`. Conduct must
establish its single-writer authority/handoff, compare current revisions/heads to
the recorded pre-read revisions/heads, perform the authorized write or patch, then exact-
read and verify complete content, relations and receipt/revision evidence.
If any check or verification fails, stop with no further memory writes and
report the known outcome; never claim an unverified update succeeded.

### Procedure

1. **Execute the change** and bring the Quality Gate green (see
   `SKILL.md` flow). Don't write to work artifacts yet.

2. **Ask the developer to confirm.** Show what changed (a minimal
   diff or a one-line description) and ask whether it's correct before
   you record it. A bare "yes" / "correct" / "confirmed" is enough; silence
   or ambiguity is not. Example:
   > I added the email validation to `InvitationSerializer` and its
   > test passes. Shall I confirm it in the plan (tasks + amendment + walkthrough)?

3. **On confirmation, record the amendment.** Keep edits surgical —
   you're annotating, not rewriting. The filesystem procedure below is for
   its local work artifacts. For an external context, hand off the proposed
   amendment operations and baseline evidence to conduct under the preceding
   revision-check and verification requirements; `fast` does not write
   executive memory directly.

   **Filesystem layout:**
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

   **External memory surface (`MSV-005`):**
   When recording an approved unplanned adjustment to an active plan:
   - **Surfaces with `executive-journal` capability:**
     Emit targeted `patch` operations rather than requesting a monolithic full rewrite:
     - **Task changes:**
       - Adding a task: `add-task{after: "<anchor>", block: "<task-block>"}`. The anchor `after` is an existing task ID (e.g. `T-013`) or heading. The block contains the checked task line with next free `T-NNN` ID.
       - Modifying an existing planned task: `amend-task{id: "<T-NNN>", block: "<modified-block>"}`.
     - **Plan amendments:**
       - Appending to existing section: `append-to-section{heading: "Plan amendments", content: "..."}` with the dated amendment bullet.
       - Inserting the section if absent: `append-section{after: "<anchor-heading>", heading: "Plan amendments", content: "..."}`.
     - **Walkthrough:**
       - `append-entry{content: "<Out-of-band change block>"}`.
   - **Surfaces lacking `patch` (legacy 1.0.x adapters):**
     If the resolved surface lacks `patch`, hand off the full updated object to conduct's single-writer update path with:
     `efficiency-warning: full-update-without-patch`.

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
     to the addition — it designs the phase, appends tasks to `tasks`
     (on `executive-journal` surfaces, using `add-task` ops; on filesystem,
     to `tasks.md`; new `T-NNN` tasks, `depends on:` the appropriate phases), and
     records a dated bullet via `append-to-section{heading: "Plan amendments", content: "..."}`
     (or `append-section{after, heading, content}`) describing
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
