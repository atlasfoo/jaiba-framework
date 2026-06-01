# `planning:cleanup`

Archive the plan summary into long-term memory and empty
`.ai/session/`. This mode is destructive — confirm with the
developer before running the script.

## Preconditions

Stop if any of these is not true:

1. A summary file `<slug>-summary.md` exists in `.ai/session/`.
2. The developer has had the chance to review the summary (don't
   chain `summarize` and `cleanup` in one turn).
3. The Quality Gate is green (so cleanup doesn't bury an unresolved
   problem).

## Flow

1. **Read the summary.** Confirm it exists and the slug matches
   `plan.md`'s frontmatter.
2. **Confirm intent.** Ask the developer for explicit confirmation,
   e.g. *"I am going to archive the summary and empty `.ai/session/`.
   Shall I proceed?"*. A bare "yes" is enough; ambiguity is not.
3. **Run the cleanup script.** Use `scripts/cleanup.sh`. It is the
   one source of truth for the archive layout:
   ```bash
   bash scripts/cleanup.sh <slug>
   ```
   The script:
   - Verifies the summary file exists under `.ai/session/`.
   - Creates `.ai/memory/archive/plans/` if it doesn't exist.
   - Moves the summary to
     `.ai/memory/archive/plans/<YYYY-MM-DD>-<slug>.md` (date from
     `plan.md` frontmatter, or today's date if absent).
   - Removes `plan.md`, `tasks.md`, `walkthrough.md` from
     `.ai/session/`.
   - Prints a summary of what it did.

   **Read the script before running it** — it is short by design,
   precisely so it can serve as documentation of the cleanup
   contract.
4. **Report.** Tell the developer where the archived summary lives
   and that the session is empty, ready for the next plan.

## When *not* to run the script

If any of the following is true, do the operation manually (or stop
and ask):

- The repository's `.ai/` layout differs from JAIBA defaults (some
  projects mount `.ai/` to a sibling repo or symlink it). The script
  assumes the default layout.
- The summary file path contains spaces or unusual characters.
- The developer asked to keep one of the session files for their own
  reasons.

The script is a convenience, not a contract. The contract is:
*"summary lives in `.ai/memory/archive/plans/`, session is empty"*.
Achieve the contract by whatever means the repo allows.

## Worked example (TripNest)

The summary `collaborative-itineraries-base-model-summary.md`
exists. The developer says: *"go ahead, clean it up"*.

Steps:

1. Confirm the file exists.
2. Confirm intent (the developer just said "go ahead" — that's
   confirmation).
3. Run `bash scripts/cleanup.sh collaborative-itineraries-base-model`.
4. Report: archived to
   `.ai/memory/archive/plans/2026-05-26-collaborative-itineraries-base-model.md`,
   session emptied.

## Common failure modes

- **Cleanup without review.** If the developer never saw the
  summary, they can't catch errors. Don't fast-path.
- **Editing the archive after archival.** Archived summaries are
  immutable in spirit — once they live in `.ai/memory/archive/`,
  treat them like `adr-log` entries. If something is wrong, write a
  new addendum next to it instead of rewriting.
- **Cleaning up while another session is mid-flight.** If `git
  status` shows files modified in `.ai/session/` since the summary
  was produced, stop and ask. The developer may have started a new
  plan elsewhere.
