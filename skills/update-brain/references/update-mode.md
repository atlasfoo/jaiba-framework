# `update-brain:update`

Reconcile an existing brain with reality. End state: the long-term
artifacts in `.ai/memory/` reflect the project as it now is — proposals
enacted, drift corrected — with every change confirmed by the human and
any remaining gap surfaced.

This mode runs on a project whose brain already exists. It has **two
entry paths**, and a single run may involve either or both:

- **Apply proposals** — `planning:summarize` or `specification:archive`
  *proposed* ADRs, reference-index entries, or constitution changes;
  enact them here.
- **Fix drift** — the project evolved (new module, new integration,
  scope shift) and the brain has fallen behind; re-analyze the affected
  slice and update.

Think of `specification:define`'s "new spec vs amend active spec" split:
same mode, two on-ramps. Pick the path from the developer's intent; ask
if it's unclear.

## Preconditions

1. The brain exists with real content. If `.ai/memory/*.md` are absent or
   bare templates, this is `initialize` — stop and switch.
2. For **apply proposals**: there is a concrete proposal to enact — an
   ADR drafted by `planning:summarize` / `specification:archive`, a named
   integration, a stated scope change. If the developer says "apply the
   proposed ADR" but you can't find it, ask where it is (usually the last
   plan summary in `.ai/memory/archive/plans/` or the spec archive).
3. For **fix drift**: a specific contradiction between brain and repo.
   Identify it before editing — don't re-derive the whole brain.

## The governing rule: propose → confirm → enact

The brain is read-mostly (`AGENTS.md` §2.9). This mode is the exception
that's *allowed* to write — but it still earns each write:

1. **Show the diff in prose.** Before touching a file, tell the developer
   exactly what will change and why (which fact, which section, from what
   to what).
2. **Confirm.** Wait for explicit approval. A manual human edit to any
   `.ai/` file is itself a final directive (`AGENTS.md` §2.8) — re-read
   and realign if you find one.
3. **Enact, minimally.** Change only what the trigger justifies. Don't
   "tidy" untouched sections; a noisy memory diff is hard to trust.

## Path A — apply proposals

The proposal usually originated upstream and is waiting to be enacted.

### ADRs

- Append a new entry per `adr-log.md`'s template, and flip its status
  `Proposed → Accepted` (or `Rejected`, if that's the decision).
- Add it to the Decision Index table at the top with today's date.
- **Never edit or delete a prior ADR.** If this decision supersedes an
  earlier one, mark the old entry `Superseded by ADR-XXX` — that is the
  *only* permitted change to an existing entry.

### Reference-index entries

- Add the integration to the correct tier (code-scope §1–§3 or workflow
  tooling §4). If that tier's section was pruned at `initialize` because
  it was empty, re-create it (and renumber) now that it has an entry.
- The consumption point must be the **external** surface (OpenAPI /
  vendored spec / docs URL), grounded in real evidence. Vendored copies
  live under `.ai/vendored/`. If the proposal named an integration but
  you can't find where it's consumed, mark `[MISSING]` and ask — don't
  invent the path.
- **Removing a reference.** When a drift fix is the *removal* of a
  dependency the project dropped, delete its row; if that empties a whole
  section, prune the section and renumber — same rule as `initialize`.

### Constitution changes

- Only enact a constitution change if it's a genuine identity event: new
  upstream/downstream, consumer change, Quality Gate change, scope
  change. Apply it to the matching section (§3/§4/§5/§6) and leave the
  rest untouched.

## Path B — fix drift

Triggered manually ("the constitution is stale", "reconcile memory with
the code") or by another skill noticing a contradiction (`AGENTS.md` §5).

1. **Scope the drift.** Name the specific contradiction: which file,
   which fact, repo-says-X vs brain-says-Y. Read the slice of the repo
   that proves it (the manifest for a stack change, the new module's
   code, the CI file for a new scanner).
2. **Map it to the right artifact** using the per-file rules:
   - Stack / scope / consumers / Quality Gate → `constitution.md`.
   - A new external integration or verification tool → `reference-index.md`.
   - A structural decision behind the change → propose an ADR (then enact
     it via Path A, with confirmation). Note: drift discovered in code
     often *implies* a decision was made outside the framework; record it
     forward as a new ADR, don't back-date it.
3. **Apply minimally**, propose → confirm → enact as above.

> Not every divergence is a brain change. If the *repo* is wrong (a bug),
> the fix belongs in `planning`/`fast`, not in memory. Only update the
> brain when the *brain* is what's behind.

## Closing

End every `update` run with a short report:

1. **What changed**, file by file (and what you deliberately left
   untouched, if the developer might expect a change there).
2. **What's outstanding** — any `[MISSING]` / `[NEEDS CLARIFICATION]`
   introduced or still present, grouped by file. Mandatory
   (`AGENTS.md` §5.4).
3. **Provenance** — if this enacted an upstream proposal, name its source
   (the plan summary or spec archive) so the trail stays followable.

## Common failure modes

- **Enacting without confirming.** The write permission is conditional on
  a shown diff and an approval. Don't fast-path it.
- **Editing or deleting a prior ADR.** Append and supersede; never
  rewrite history.
- **Over-editing.** Touching sections the trigger didn't justify makes
  the memory diff untrustworthy. Change the minimum.
- **Treating a code bug as drift.** If the repo is wrong, that's a
  `planning`/`fast` fix, not a brain update.
- **Inventing a consumption point** for a proposed integration instead of
  grounding it or marking `[MISSING]`.
- **Touching the constitution for a non-identity change.**
- **Finishing without surfacing remaining gaps.**
