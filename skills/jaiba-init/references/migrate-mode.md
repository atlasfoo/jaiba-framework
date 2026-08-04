# `jaiba-init:update-brain:migrate`

Convert a populated **flat** brain into the **concept bundle**. End
state: `.ai/memory/` holds `index.md` plus one file per concept, every
fact carried over from `constitution.md`, `adr-log.md` and
`reference-index.md` without loss and without invention; the three flat
originals are backed up and still in place; a `brain-change` entry
records the conversion.

This mode is **optional and human-triggered**. The flat layout is a
supported layout (`jaiba-contract.md` §1) — a project may stay on it
forever. Never offer migration to a working flat brain that nobody asked
about; run this only when the developer explicitly asks for it.

Migration is a **translation, not a re-survey.** The evidence sweep
belongs to `initialize`; drift correction belongs to `update`. Here the
flat files are the only source: what they say is what the bundle says,
and what they don't say stays unsaid.

The bundle layout, the closed `type:` vocabulary, the per-type
frontmatter and the link convention are **not restated here** —
`references/okf-pattern.md` owns them, and each
`assets/concepts/<name>.md` template is the authority on its own fields.
This file is the *procedure*: what maps to what, in what order, and what
must never be resolved along the way.

## Preconditions

1. **`.ai/memory/index.md` must not exist.** Check this **first**,
   before reading anything else and before writing anything at all. If
   it exists, the brain is already a bundle (or a prior migration ran):
   **stop without writing a single byte**, say so plainly, and route the
   developer to `update` for maintenance. Never merge into an existing
   bundle, never overwrite it, never "top it up" — a second migration
   pass over a migrated brain duplicates concepts and destroys the
   provenance of the first.
2. **The flat brain exists and carries real content.** `constitution.md`
   present with real prose. If the flat files are absent, or are
   untouched templates full of `[brackets]`, there is nothing to
   translate: this is `initialize` — stop and switch.
3. **The developer asked for it.** See above; this mode has no automatic
   trigger.

Resolve the layout per the dual-resolution rule in `jaiba-contract.md`
§1 (do not restate it, apply it). Preconditions 1 and 2 are the two
halves of that resolution seen from this mode's side.

## The governing rule: propose → confirm → enact

Migration is a write to `.ai/memory/`, so it earns each write exactly
the way `update` does — with two additions that are specific to
converting a whole brain at once:

1. **Show the plan in prose.** Before creating anything, tell the
   developer the inventory the translation will produce: how many
   concepts, of which types, and which flat sections feed each group.
   Name the gaps you already spotted while reading.
2. **Confirm.** Wait for explicit approval.
3. **Back up before the first write.** Not after, not "if it looks
   risky" — the backup is the precondition of the write phase. See
   below.
4. **Enact by translating.** Carry facts over; add nothing the flat
   source didn't say.
5. **Record.** Append a `brain-change` entry to `.ai/memory/log/`. The
   log is append-only — a correction is a new entry, never an edit.
6. **Leave the originals in place.** Deleting the flat trio is a
   separate, human-confirmed step. Not this run.

## Order of operations

Run these in order; each depends on the one before it.

| # | Step |
|---|---|
| 0 | Precondition check — `index.md` absent, flat content real |
| 1 | Read `constitution.md`, `adr-log.md`, `reference-index.md` **in full** |
| 2 | Propose the concept inventory; get confirmation |
| 3 | **Back up** the flat brain |
| 4 | Write `identity/` concepts |
| 5 | Write `decisions/` and `references/` concepts |
| 6 | Back-fill missing frontmatter on existing `log/` entries |
| 7 | Write `index.md` — last |
| 8 | Append the `brain-change` log entry |
| 9 | Report (see **Closing**) |

Step 1 is the one place in this framework where reading three files
whole is right: a translation cannot be partial. Everything after it is
writing.

## Step 3 — the backup

Copy (never move) the flat brain to a timestamped directory **outside
the bundle**:

```
.ai/.migration-backup-<YYYY-MM-DD-HHMM>/
├── .gitignore          single line: *   (the backup ignores itself)
├── constitution.md
├── adr-log.md
├── reference-index.md
└── log/                copy of the whole directory
```

- **Outside `.ai/memory/`, deliberately.** `.ai/memory/` *is* the
  bundle; a directory of non-concept files inside it reads as
  untyped concepts to `jaiba-doctor`.
- **Timestamped, so a second run never clobbers the first.** Local time,
  minute precision, sortable.
- **Self-ignoring.** The `.gitignore` holding `*` keeps transient
  machine-local safety copies out of the repository's history, the same
  way `.atl/` does. No existing file is edited to achieve it.
- **`log/` is copied although nothing deletes it.** Step 6 touches those
  files; cheap insurance.

If the copy fails for any reason, **stop**. A migration that started
without a backup cannot be safely abandoned halfway.

## Step 4–5 — the mapping

### `constitution.md`

| Flat section | Becomes | Notes |
|---|---|---|
| §1 What | `identity/project.md` (`type: project`) | name, description, status — one to one |
| §2 How | `identity/architecture.md` | style, language, framework, persistence, key packages |
| §3 Why | `identity/purpose.md` | objective and position; its `## Relations` is filled from §4 |
| §4 With Whom | **dissolved** — no concept of its own | each entry becomes (or joins) a `references/<slug>.md` carrying `role:`; `purpose.md` / `scope.md` **link** those concepts |
| §5 Scope | `identity/scope.md` | in scope, out of scope, cross-cutting packages; its `## Relations` is filled from §4 |
| §5.1 Sub-unit scope | one `identity/units/<slug>.md` per table row (`type: sub-unit`) | `path` and `depends-on` from the row's columns. "Single unit." → **no `units/` directory at all** |
| §6 Quality Gate | `identity/quality-gate.md` | both tiers, commands verbatim — never re-derive them from the repo |
| §7 Planning Conventions **+** §8 Style and Syntax | `identity/conventions.md` (**one** concept) | two flat sections, one file, read as a unit |

Two things in `constitution.md` are **not** content and are dropped:
the `> For repository maintainers` / `> Meta-instruction for the agent`
blockquotes, and §2's trailing pointer at `reference-index.md`. The
concept templates carry their own meta-instructions, and the pointer
names a layout that no longer exists. Carry the project's *facts*, not
the flat template's boilerplate.

### §4 "With Whom" — how the dissolution actually runs

This is the one place the mapping is not mechanical, and the one
duplication the bundle exists to remove (`okf-pattern.md`, "One
deliberate improvement"). Work **per surface, not per row**:

1. Build the set of surfaces named anywhere in §4 (upstream, downstream,
   infrastructure) and in `reference-index.md` §1–§6.
2. **One surface is one concept file**, even when it appears in both.
   Merge: §4 gives `role:`, the index row gives everything else.
3. A surface in §4 with no index row → its concept is created with the
   `role:` §4 stated and `resource: [MISSING: no reference-index row in
   the flat source]`.
4. A `tier: code-scope` surface with an index row but no §4 mention →
   `role: [MISSING: not stated in constitution §4]`. Do not infer the
   role from the surface's name or kind. `tier: workflow` rows take
   `role: —`; that is non-applicability, not a gap.
5. Link, don't inventory. `purpose.md`'s `## Relations` links the
   surfaces §4 listed as **upstream** and **downstream** (who the
   project serves and depends on to serve them); `scope.md`'s links the
   **infrastructure** entries and any surface §5's "out of scope" names
   as delegated. One line, one link, file-relative. A surface may be
   linked from both when both apply. **Never copy a reference's details
   into either list.**

### `adr-log.md`

| Flat element | Becomes |
|---|---|
| The Decision Index table | **nothing** — it dissolves into `index.md`'s `decision` group |
| Each `## ADR-NNN: <title>` entry | one `decisions/<NNN>-<slug>.md` (`type: decision`) |
| The `> Meta-instruction` header and the Entry Template section | **nothing** — owned by `assets/concepts/decision.md` |

Per entry:

- **`id` and filename** come from the flat entry's own number, zero
  padded: `ADR-4` → `id: ADR-004`, file `decisions/004-<slug>.md`. The
  `<slug>` is kebab-case from the title. **Never renumber**, never close
  a gap in the series, never reorder.
- **`status`** is the flat status, lowercased into the closed
  vocabulary: `Accepted` → `accepted`, `Proposed` → `proposed`,
  `Rejected` → `rejected`, `Deprecated` → `deprecated`. A flat
  `Superseded by ADR-007` becomes `status: superseded` **plus**
  `superseded-by: "[ADR-007](007-<slug>.md)"`, and ADR-007's own file
  gains the matching `supersedes:`. Both ends or neither — a one-sided
  link is a broken-link finding.
- **`date`** is the entry's stated date. If the entry has none,
  `date: [MISSING]`. Today's date is the date of the *migration*, not of
  the decision; never substitute it.
- **Body sections** (Context / Decision / Alternatives Considered /
  Consequences) carry over verbatim, prose untouched. `description:` is
  a one-line restatement of the decision — a restatement of what the
  entry already says, never a new claim.
- **One entry is one concept.** Never merge two flat entries, never
  split one across two files.

### `reference-index.md`

One row is one `references/<slug>.md`, with the frontmatter derived from
the section the row came from:

| Flat section | `tier` | `kind` | `role` |
|---|---|---|---|
| §1 Infrastructure Dependencies | `code-scope` | `infrastructure` | from §4 |
| §2 External APIs | `code-scope` | `external-api` | from §4 |
| §3 Internal Cross-Component Contracts | `code-scope` | `internal-contract` | from §4 |
| §4 Packages and SDKs | `code-scope` | `package` | from §4 |
| §5 Workflow & Verification Tooling | `workflow` | `tooling` | `—` |
| §6 Business Documentation | `workflow` | `business-doc` | `—` |
| §7 Implementation Notes (Snippets) | — | — | see **the snippet gap** below |

Column mapping, whatever the section's column names are:

- First column (Service / Contract / Package / Tool / Document) →
  `title:` and the kebab-case slug.
- Role / "Why it needs an entry" / Type → `description:` and the
  **What it is** / **How the project uses it** body sections.
- "How to consult" **and** the grounding column (Location / Endpoint /
  Spec / Docs / Where it's configured) → both fold into `resource:`,
  joined with ` / ` the way the worked examples in
  `assets/concepts/reference.md` do, and are expanded in the **How to
  consult** body section.

The trailing "How to Consult — Vocabulary" section is framework
boilerplate: it is **dropped**, because `assets/concepts/reference.md`
owns that vocabulary now.

### Template residue is not content

A flat row whose cells are all bracketed placeholders — `[PostgreSQL]`,
`[Primary DB]`, `[Auth0]`, the example sub-unit rows — is **untouched
template**, not a fact about this project. Do **not** create a concept
from it. That would fabricate a `references/stripe.md` for a project
that never integrated Stripe.

Instead: skip the row, and report at close that the section was never
filled in the flat source. Residue is not a `[MISSING]` either —
`[MISSING]` is a fact that *should* exist and couldn't be found; residue
is a section nobody ever wrote. Say which one you found, and say it in
the report rather than in the bundle.

The judgment is per row, not per section: a §1 with two real rows and
one leftover example row yields two concepts.

## The literal carry-over rule

**Every `[MISSING]`, `[NEEDS CLARIFICATION]` and unfilled `[bracket]`
found in real flat content is copied VERBATIM into the concept that
inherits its field.**

- **Never resolve one.** Not by reading the repo, not by inference, not
  by "it's obviously Postgres". Resolving gaps is `update`'s job on a
  later, deliberate run — and it has to ask the human first.
- **Never drop one.** A gap that disappears during migration is a gap
  the developer will never be told about again.
- **Never re-word one.** `[MISSING]` stays `[MISSING]`; a
  `[NEEDS CLARIFICATION: which cache TTL?]` keeps its question text
  exactly.
- **Place it in the analogous field**, not in a footnote. If §6's
  coverage threshold was `[MISSING]`, `quality-gate.md`'s coverage line
  is `[MISSING]`.
- **List every one of them at close**, grouped by concept.

If a translation would be *more useful* with the gap filled, that is the
strongest possible signal to leave it alone. A migrated brain that
silently gained facts is worse than a flat brain that honestly lacked
them.

## The snippet gap — `reference-index.md` §7

`snippet` is in the closed `type:` vocabulary, but **this skill ships no
`assets/concepts/snippet.md` template**. So:

- **Do not invent a template shape** on the fly. Inventing one makes
  every future snippet concept inconsistent with whatever template
  eventually lands.
- **Do not drop the content.** §7's rows are real project knowledge.
- **Do not create `snippets/`.**

Carry it forward as a marker instead. Append to
`identity/conventions.md`, under **Style and syntax** (snippets are
canonical examples of recurring in-project patterns, which is that
concept's neighbourhood):

```
- [MISSING: no `snippet` concept template exists yet. The flat
  `reference-index.md` §7 listed N canonical examples; their text is
  preserved verbatim at
  `.ai/.migration-backup-<YYYY-MM-DD-HHMM>/reference-index.md` §7.]
```

Then flag it in the closing report as its own line, and leave
`index.md`'s `snippet` group deleted — the group maps concepts that
exist, and none do. If §7 held only template residue, there is nothing
to carry and no marker to write.

## Step 6 — existing `log/` entries

Log entries are already concepts (`type: log-entry`); they just may
predate the frontmatter. An existing entry may **gain missing
frontmatter keys and nothing else** (`okf-pattern.md`). Its body, its
filename and its date are untouchable. Never rewrite, never reformat,
never "improve" an entry while you are in there.

## Step 7 — `index.md`

Written **last**, after every other concept exists, from
`assets/concepts/index.md` and per `okf-pattern.md`'s index rules:
grouped by `type:`, one direct link and one line per concept — that
concept's `description:` frontmatter, verbatim — and no group for a type
this repository has none of.

Two migration-specific traps: do not carry `adr-log.md`'s Decision Index
table into the `decision` group as a table, and do not carry
`reference-index.md`'s per-section prose into the `reference` group. The
index is a map. Both of those are why the flat files got heavy.

## Step 8 — the `brain-change` entry

Append one entry to `.ai/memory/log/`, shaped by
`assets/log-entry-template.md`, named `<YYYY-MM-DD>-<slug>.md` (e.g.
`2026-08-02-brain-migrated-to-okf.md`), with `kind: brain-change` and
`adr: none` unless the developer chose to record the migration as its
own decision.

It states: that the brain was converted from the flat layout to the
concept bundle; the inventory produced (counts by `type:`); **the backup
path, spelled out**; the gaps carried over, by count; and that the flat
originals were left in place pending human confirmation. That entry is
what makes the conversion auditable later without diffing git history.

## Closing

End every `migrate` run with a report:

1. **What was migrated** — concept counts grouped by `type:`, the way
   `initialize` reports: the identity concepts named individually,
   `decision` and `reference` by count plus titles. One glance, one
   shape.
2. **What was carried over unresolved** — every `[MISSING]` /
   `[NEEDS CLARIFICATION]` / unfilled `[bracket]`, grouped by the
   concept that now holds it, plus the snippet marker if §7 had content.
   Mandatory (`AGENTS.md` §5.4). Say explicitly that none of them were
   resolved, and that resolving them is a separate `update` run.
3. **What was skipped as template residue** — flat sections that were
   never filled and therefore produced no concepts.
4. **Where the backup lives** — the full path.
5. **That the flat originals are still there**, and that deleting them
   is a **separate step requiring the developer's explicit
   confirmation**. Do not delete them in this run, and do not ask for
   confirmation in a way that lets a "sounds good" be read as consent to
   delete.
6. **The state this leaves behind, said out loud.** Until the flat trio
   is deleted, `.ai/memory/` holds both `index.md` and `constitution.md`
   — the state `jaiba-contract.md` §1 calls ambiguous, where every skill
   reading the brain will stop and surface it. That is the intended,
   temporary cost of not deleting the developer's data on their behalf,
   and they need to know it so they can close the window as soon as they
   have reviewed the bundle. The backup is what makes closing it safe.

## Common failure modes

- **Migrating a bare or template flat brain.** There is nothing to
  translate; that is `initialize`. Check for real prose first.
- **Running when `index.md` already exists.** Stop, write nothing.
  Merging into or overwriting an existing bundle is the one outcome this
  mode must never produce.
- **Writing before backing up.** The backup is a precondition of the
  write phase, not a courtesy.
- **Resolving a `[MISSING]`** instead of carrying it over — the single
  most tempting failure here, because the repository is right there and
  the answer often is obvious. Carry it. Obviousness is not evidence.
- **Dropping a gap** so the migrated brain looks clean.
- **Deleting the flat originals** — in this run, or on an implied
  approval. Separate step, explicit confirmation, human's call.
- **Re-surveying the repository** instead of translating. Facts the flat
  brain never had do not enter here; drift correction is `update`, on a
  later run, with its own confirmation.
- **Migrating template residue as content** — a `references/stripe.md`
  for a project that never used Stripe, an `identity/units/api.md` from
  the example table.
- **Inventing a `snippet` template** because §7 had content — or
  silently dropping §7 because there is no template. Marker, report,
  backup.
- **Re-creating §4's inventory** inside `purpose.md` / `scope.md`
  instead of linking the `reference` concepts. That duplication is
  exactly what the bundle removed.
- **Renumbering, reordering or merging ADRs**, or dating them today.
- **Rewriting an existing `log/` entry** while back-filling its
  frontmatter.
- **Fattening `index.md`** with the Decision Index table or the flat
  index's section prose.
- **Offering migration unprompted** to a healthy flat brain. Both
  layouts are supported.
- **Finishing without the backup path and the gap list.**
