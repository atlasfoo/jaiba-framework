# `jaiba-init:update-brain:update`

Reconcile an existing brain with reality. End state: the long-term
memory in `.ai/memory/` reflects the project as it now is — proposals
enacted, drift corrected — with every change confirmed by the human and
any remaining gap surfaced.

This mode runs on a project whose brain already exists. It has **two
entry paths**, and a single run may involve either or both:

- **Apply proposals** — `conduct:summarize` *proposed* a decision, an
  external surface, or an identity change; enact it here.
- **Fix drift** — the project evolved (new module, new integration,
  scope shift) and the brain has fallen behind; re-analyze the affected
  slice and update.

Same mode, two on-ramps. Pick the path from the developer's intent; ask
if it's unclear.

The bundle layout, the closed `type:` vocabulary, the per-type
frontmatter and the link convention are **not restated here** —
`references/okf-pattern.md` owns them, and each
`assets/concepts/<name>.md` template is the authority on its own fields.
This file is the *procedure*: what to change, where, and what must never
be touched on the way.

## Preconditions

1. The brain exists with real content. If `.ai/memory/` holds no
   concepts at all, or only bare templates full of `[brackets]`, this is
   `initialize` — stop and switch.
2. For **apply proposals**: there is a concrete proposal to enact — a
   decision drafted by `conduct:summarize`, a named integration, a
   stated scope change. If the developer says "apply the proposed ADR"
   but you can't find it, ask where it is (usually the most recent
   `work-closure` entry in `.ai/memory/log/`).
3. For **fix drift**: a specific contradiction between brain and repo.
   Identify it before editing — don't re-derive the whole brain.

## Which layout you are in

**Resolve the layout first**, per the dual-resolution rule in
`jaiba-contract.md` §1 (do not restate it, apply it). Every rule below
is written twice, once per layout; resolving first is what tells you
which half to follow.

| `.ai/memory/` holds | Layout | Follow |
|---|---|---|
| `index.md` | concept bundle | the **bundle** half of each rule below |
| `constitution.md`, no `index.md` | legacy flat | the **legacy flat** half. This is a supported layout — maintain it in place, and never offer migration unless the developer asks (`references/migrate-mode.md`) |
| both | ambiguous | **Stop and surface it** (contract §1). Never silently pick a half. |
| neither | no brain | Wrong mode — route to `initialize`. |

The two halves are not a transition state. A flat brain maintained by
this mode stays flat and stays correct; converting it is a separate,
human-triggered run of `migrate`.

## The governing rule: propose → confirm → enact

The brain is read-mostly (`AGENTS.md` §2.9). This mode is the exception
that's *allowed* to write — but it still earns each write:

1. **Show the diff in prose.** Before touching a file, tell the developer
   exactly what will change and why (which fact, which concept — or
   which flat section — from what to what).
2. **Confirm.** Wait for explicit approval. A manual human edit to any
   `.ai/` file is itself a final directive (`AGENTS.md` §2.8) — re-read
   and realign if you find one.
3. **Enact, minimally.** Change only what the trigger justifies. Don't
   "tidy" untouched concepts; a noisy memory diff is hard to trust.
   Bump `updated:` on what you changed, and only on what you changed.
4. **Record.** Append a `brain-change` entry to `.ai/memory/log/`
   (shape in `assets/log-entry-template.md`) stating what changed,
   from what to what, and its provenance. The log is append-only —
   never rewrite a prior entry; a correction is a new entry pointing
   at the old one. This is what keeps brain evolution auditable
   without diffing git history. `log/` is identical in both layouts.

**In the bundle, one step joins every enactment: regenerate
`index.md`.** Any concept added, removed or renamed changes the map —
one direct link and one line (that concept's `description:` frontmatter,
verbatim), grouped by `type:`, per `okf-pattern.md`'s index rules. A
concept that exists but is not in the index is invisible to every skill
that resolves through it, and a line pointing at a deleted concept is a
broken-link finding for `jaiba-doctor`. The flat layout has no
equivalent step: its indexes live inside the files themselves.

## Path A — apply proposals

The proposal usually originated upstream and is waiting to be enacted.

### Decisions

**Bundle.** One decision is one file.

- Create `decisions/<NNN>-<slug>.md` from `assets/concepts/decision.md`,
  with `status: accepted` (or `rejected`, if that's the decision),
  `date:` today, and `<slug>` kebab-case from the title.
- **Finding the next `NNN`.** There is no Decision Index table anymore:
  **the directory is the register.** List `decisions/*.md`, take the
  highest numeric prefix, add one, zero-pad to three.
  - **Scan the filenames, never `index.md`.** The index is regenerated
    *from* the concepts and may lag by one run; a number read off a
    stale index collides with a decision that already exists.
  - **A number, once issued, stays issued.** A `rejected`, `deprecated`
    or `superseded` decision keeps its file and its number — none of
    those statuses frees it. The highest prefix present on disk is the
    high-water mark whatever the statuses say.
  - **Never close a gap.** If `003` is absent (a flat log with a hole,
    migrated as-is), the next number is still highest + 1. Filling the
    hole would silently re-point every citation of "ADR-003".
  - **If the filename you computed already exists, your scan was
    wrong.** Re-scan; never overwrite a decision file.
  - `id: ADR-NNN` and the filename's `NNN` are two spellings of the same
    number and must match.
- **Never edit or delete a prior decision.** Superseding is the only
  permitted edit to a decision that has landed, and it touches two
  files: the new one carries `supersedes:`, the old one flips to
  `status: superseded`, gains `superseded-by:` and a bumped `updated:`,
  and **changes nothing else**. Both ends or neither — a one-sided link
  is a broken-link finding. `assets/concepts/decision.md` is the
  authority on this.
- Regenerate `index.md` so the new decision appears in its group.

**Legacy flat.** Append a new entry per `adr-log.md`'s template and flip
its status `Proposed → Accepted` (or `Rejected`); add it to the Decision
Index table at the top with today's date, taking its number from the
table's last row. If this decision supersedes an earlier one, mark the
old entry `Superseded by ADR-XXX` — that is the *only* permitted change
to an existing entry.

### References

**Bundle.** One external surface is one file.

- Create `references/<slug>.md` from `assets/concepts/reference.md`,
  kebab-case slug naming the surface. Fill `tier` (`code-scope` for
  something the running code depends on — infrastructure, external APIs,
  internal cross-component contracts, packages needing context;
  `workflow` for scanners, security audits and non-code sources of
  truth), `kind`, `role` (only meaningful at `tier: code-scope`; `—` on
  workflow tooling), and `resource`. The template owns that vocabulary —
  read it rather than re-deriving it here.
- **There is no section to re-create and nothing to renumber.** The flat
  index numbered its tiers and pruned the empty ones, so the first entry
  of a pruned category meant re-creating a section and renumbering the
  rest. In the bundle a category that doesn't apply simply *has no
  files*, so its first surface is an ordinary file creation — the same
  rule `initialize` follows when it declines to write placeholder
  concepts.
- The consumption point must be the **external** surface (OpenAPI /
  vendored spec / docs URL), grounded in real evidence. Vendored copies
  live under `.ai/vendored/`; `resource:` points at that path. If the
  proposal named an integration but you can't find where it's consumed,
  mark `[MISSING]` and ask — don't invent the path.
- **Removing a reference.** When the enactment is the *removal* of a
  dependency the project dropped, delete the file — again no section to
  prune, no renumbering. Then clear what pointed at it: its line in
  `index.md`, any `## Relations` link in `identity/purpose.md` or
  `identity/scope.md`, and any decision that cited it. The deletion is
  not done until the last inbound link is gone; a dangling link is a
  broken-link finding.
- Regenerate `index.md` on every add, remove or rename.

**Legacy flat.** Add the integration to the correct tier (code-scope
§1–§4 — including internal cross-component contracts in §3 — or workflow
tooling §5). If that tier's section was pruned at `initialize` because it
was empty, re-create it (and renumber) now that it has an entry. The
same grounding rule applies to the consumption point. Removing a
reference deletes its row; if that empties a whole section, prune the
section and renumber.

### Identity changes

Only enact one if it's a genuine identity event: an architecture change,
a scope change, a consumer change, a Quality Gate change.

**Bundle.** Map the fact to the **one** concept that owns it, and touch
only that concept:

| What changed | The concept |
|---|---|
| Name, description, lifecycle status | `identity/project.md` |
| Architectural style, language, framework, persistence, key packages | `identity/architecture.md` |
| Business objective, position in the bigger picture | `identity/purpose.md` |
| In scope, out of scope, cross-cutting packages | `identity/scope.md` |
| A deliverable unit added, removed or re-scoped | `identity/units/<slug>.md` |
| Verification commands or gate thresholds | `identity/quality-gate.md` |
| Planning conventions, or where style is configured | `identity/conventions.md` |

**A consumer change is not an identity edit.** Upstream, downstream and
infrastructure partners are **not inventoried inside identity
concepts** — each is its own `reference` concept carrying `role:`, and
re-creating that inventory is the single duplication the bundle exists
to remove (`okf-pattern.md`, "One deliberate improvement"). So a new
consumer is a new `references/<slug>.md` with `role: downstream`, by the
rules above; a departed one is that file's removal. Touch
`identity/purpose.md` or `identity/scope.md` **only** if the change also
moves why the project exists or where its boundary runs — and then only
to add or drop **one line, one link** in their `## Relations`. Never
copy the surface's details into either.

**Legacy flat.** Apply the change to the matching section of
`constitution.md` (§2 how, §3 why, §4 with whom, §5 scope, §6 Quality
Gate) and leave the rest untouched. §4 keeps its inventory here — that
duplication is part of the flat layout and is not a defect to fix
in place.

## Path B — fix drift

Triggered manually ("the brain is stale", "reconcile memory with the
code") or by another skill noticing a contradiction (`AGENTS.md` §5).

1. **Scope the drift.** Name the specific contradiction: which concept
   (or flat section), which fact, repo-says-X vs brain-says-Y. Read the
   slice of the repo that proves it (the manifest for a stack change,
   the new module's code, the CI file for a new scanner).
2. **Map it to the right concept.**

   **Bundle:**

   | The drift | Goes to |
   |---|---|
   | Stack / architecture | `identity/architecture.md` |
   | What the project does or deliberately doesn't | `identity/scope.md` — plus `identity/units/<slug>.md` if one unit's boundary moved |
   | Business objective or position | `identity/purpose.md` |
   | Consumers — a new downstream, or one that went away | the surface's own `references/<slug>.md` (`role: downstream`), **not** an identity concept. Re-link `purpose.md` / `scope.md` only if the boundary itself moved |
   | Quality Gate commands or thresholds | `identity/quality-gate.md` |
   | A new external integration or verification tool | a new `references/<slug>.md`, by Path A's reference rules |
   | A structural decision behind the change | propose a decision, then enact it via Path A |

   **Legacy flat:** stack / scope / consumers / Quality Gate →
   `constitution.md` (§2 / §5 / §4 / §6); a new external integration or
   verification tool → `reference-index.md`; the decision behind the
   change → `adr-log.md`, via Path A.

   Note in either layout: drift discovered in code often *implies* a
   decision was made outside the framework. Record it forward as a new
   decision dated today — never back-date it, and never write one to
   retroactively justify a pattern already in the code
   (`assets/concepts/decision.md`).
3. **Apply minimally**, propose → confirm → enact as above — and in the
   bundle, regenerate `index.md` if the set of concepts changed.

> Not every divergence is a brain change. If the *repo* is wrong (a bug),
> the fix belongs in `conduct`/`fast`, not in memory. Only update the
> brain when the *brain* is what's behind.

## Closing

End every `update` run with a short report:

1. **What changed** — concept by concept in the bundle, file by file in
   the flat layout (and what you deliberately left untouched, if the
   developer might expect a change there). Say explicitly if `index.md`
   was regenerated.
2. **What's outstanding** — any `[MISSING]` / `[NEEDS CLARIFICATION]`
   introduced or still present, grouped by the concept that carries it.
   Mandatory (`AGENTS.md` §5.4).
3. **Provenance** — if this enacted an upstream proposal, name its source
   (the work-closure log entry or the plan it came from) so the trail
   stays followable.

## Common failure modes

- **Enacting without confirming.** The write permission is conditional on
  a shown diff and an approval. Don't fast-path it.
- **Writing before resolving the layout.** Editing `constitution.md` in a
  bundle repo, or creating `identity/` concepts next to a live flat
  brain, manufactures the ambiguous state the contract tells every skill
  to stop on.
- **Editing or deleting a prior decision.** Append and supersede; never
  rewrite history.
- **Reusing an `NNN`** because the decision holding it was rejected,
  deprecated or superseded — or **closing a gap** in the series. Numbers
  are issued once, and every citation of one must keep resolving.
- **Taking the next `NNN` from `index.md`** instead of from the
  `decisions/` directory. The directory is the register; the index is a
  regenerated map that may lag.
- **Leaving `index.md` stale** after adding, removing or renaming a
  concept — or fattening it with a summary of what changed.
- **Deleting a reference and leaving inbound links dangling** in
  `index.md`, in `purpose.md` / `scope.md`'s `## Relations`, or in a
  decision that cited it.
- **Over-editing.** Touching concepts the trigger didn't justify makes
  the memory diff untrustworthy. Change the minimum.
- **Treating a code bug as drift.** If the repo is wrong, that's a
  `conduct`/`fast` fix, not a brain update.
- **Inventing a consumption point** for a proposed integration instead of
  grounding it or marking `[MISSING]`.
- **Re-inventorying consumers inside `purpose.md` / `scope.md`** instead
  of creating (or removing) the `reference` concept that carries
  `role: downstream`. That duplication is exactly what the bundle
  removed.
- **Touching an identity concept — or `constitution.md` — for a
  non-identity change.**
- **Finishing without surfacing remaining gaps.**
</content>
</invoke>
