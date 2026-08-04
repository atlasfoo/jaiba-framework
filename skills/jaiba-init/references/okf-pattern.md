# The OKF pattern in JAIBA

How the brain is serialized: **one concept per file**, each file a plain
markdown document carrying a `type:` in its frontmatter, each relation a
file-relative markdown link, and `.ai/memory/index.md` as the single
entry point. This is the long-form reference for *writing* those
concepts — the closed `type:` vocabulary, the bundle layout, the
frontmatter keys per type, the link convention, and the tolerance rule.

It lives here because `jaiba-init:update-brain` is the only writer of
`.ai/memory/` (`AGENTS.md` §2.9, with `conduct:summarize`'s append-only
carve-out for `log/`). Every other skill only *reads* the brain, and
reading needs far less than this file: the dual-resolution rule and the
`type:` vocabulary, both of which live in `jaiba-contract.md` §1 so all
skills inherit them equally. **Do not restate the resolution rule
here** — resolve the layout per the contract, then come back for the
writing rules.

## Convention, never dependency

The pattern is adopted from Open Knowledge Format v0.1, which is a
draft. JAIBA takes the *shape*, not the dependency:

- Reading and writing a concept is reading and writing **plain
  markdown**. Nothing in the framework may invoke an OKF-specific tool,
  parser, or validator.
- **No skill, script, or subagent declares a `requires:`** because of
  this pattern. If a change to the brain format would add one, the
  change is wrong.
- Conformance to the upstream spec is not tested and not claimed. An
  upstream revision of OKF is not an event for this repository.

The tolerance rule below is what makes that stance hold in practice.

## The bundle

`.ai/memory/` **is** the bundle — there is no extra `okf/` level. `log/`
was already a thematic subfolder and stays exactly where it is.

```
.ai/memory/
├── index.md                       type: index        ← entry point
├── identity/
│   ├── project.md                 type: project
│   ├── architecture.md            type: architecture
│   ├── purpose.md                 type: purpose
│   ├── scope.md                   type: scope
│   ├── quality-gate.md            type: quality-gate
│   ├── conventions.md             type: convention
│   └── units/<slug>.md            type: sub-unit     (only multi-unit repos)
├── decisions/<NNN>-<slug>.md      type: decision     (one ADR per file)
├── references/<slug>.md           type: reference    (one surface per file)
├── snippets/<slug>.md             type: snippet      (optional)
└── log/<YYYY-MM-DD>-<slug>.md     type: log-entry    (append-only)
```

Two things are deliberately **outside** the bundle:

- **`.atl/tool-layout.md`** — machine state, not project memory. It is
  always local filesystem and never enters `.ai/`.
- **`.ai/vendored/`** — local copies of external material. A `reference`
  concept *points at* a vendored path; the copy itself is not a concept.

`.ai/work/` is a separate matter: it adopts the same convention (see
**Executive memory** below) but is not part of the constitutive bundle
and is not reachable from `index.md`. It is gitignored, per-developer,
and short-lived.

### One deliberate improvement over the flat layout

The mapping from the three monolithic files is otherwise mechanical, but
`constitution.md` §4 "With Whom" **duplicated** `reference-index.md` —
the old template even instructed *"Every entry should also exist in
reference-index.md"*. In the graph that duplication disappears: each
`reference` concept carries its own `role`, and `purpose.md` / `scope.md`
**link to those concepts** instead of repeating the inventory. Never
re-create the duplicated list.

## The `type:` vocabulary

Closed set. Sixteen values, in two families.

**Constitutive — the `.ai/memory/` bundle:**

| `type:` | Lives at | One file is | Flat-layout origin |
|---|---|---|---|
| `index` | `index.md` | the bundle's entry point | (new) |
| `project` | `identity/project.md` | name, description, status | constitution §1 |
| `architecture` | `identity/architecture.md` | style, language, framework, persistence, key packages | constitution §2 |
| `purpose` | `identity/purpose.md` | business objective and position | constitution §3 |
| `scope` | `identity/scope.md` | in / out of scope, cross-cutting packages | constitution §5 |
| `sub-unit` | `identity/units/<slug>.md` | one deliverable unit of a multi-unit repo | constitution §5.1 |
| `quality-gate` | `identity/quality-gate.md` | the phase gate and the plan gate | constitution §6 |
| `convention` | `identity/conventions.md` | planning conventions, style and syntax | constitution §7–§8 |
| `decision` | `decisions/<NNN>-<slug>.md` | exactly one ADR | one `adr-log.md` entry |
| `reference` | `references/<slug>.md` | exactly one external surface | one `reference-index.md` row |
| `snippet` | `snippets/<slug>.md` | one canonical example of a recurring pattern | reference-index §7 |
| `log-entry` | `log/<YYYY-MM-DD>-<slug>.md` | one dated record | unchanged |

**Executive — the `.ai/work/` artifacts:**

| `type:` | Lives at |
|---|---|
| `prd` | `.ai/work/PRD.md` |
| `plan` | `.ai/work/plan.md` |
| `tasks` | `.ai/work/tasks.md` |
| `walkthrough` | `.ai/work/walkthrough.md` |

**The set is closed.** If a concept you need to write doesn't fit any of
these sixteen, that is a framework change, not a judgment call — stop and
surface it. Inventing a seventeenth type silently makes the brain
unreadable to every skill that resolves by `type:`.

Two shapes are worth naming explicitly:

- `convention` is one file (`conventions.md`) even though the flat
  layout split it across two sections. It is read as a unit.
- `sub-unit` files exist **only** when the repository holds more than one
  deliverable unit (packages in a monorepo, projects in a `.sln`, apps in
  a workspace). A single-unit repository has no `identity/units/` at all
  — do not create the directory to hold a "single unit" placeholder.

## Frontmatter

### Universal keys

| Key | Status | Meaning |
|---|---|---|
| `type` | **mandatory** | one of the sixteen values above |
| `title` | recommended | human-readable name of the concept |
| `description` | recommended | one line; this is what `index.md` shows |
| `tags` | recommended | list, for grouping and search |
| `updated` | recommended | `YYYY-MM-DD` of the last substantive change |

`type` is the only key whose absence is a finding. Everything else is a
quality signal, not a validity condition.

### Type-specific keys

| `type:` | Additional keys |
|---|---|
| `decision` | `id` (`ADR-NNN`), `status` (`proposed` \| `accepted` \| `rejected` \| `deprecated` \| `superseded`), `date`, `supersedes` / `superseded-by` (link to the other decision) |
| `reference` | `tier` (`code-scope` \| `workflow`), `kind` (`infrastructure` \| `external-api` \| `internal-contract` \| `package` \| `tooling` \| `business-doc`), `role` (`upstream` \| `downstream` \| `infrastructure`), `resource` (where it is consulted) |
| `sub-unit` | `path` (repo-relative path of the unit), `depends-on` (list of links to sibling `sub-unit` concepts) |
| `log-entry` | `date`, `slug`, `kind` (`work-closure` \| `brain-change`), `adr` |
| `index` | none |
| all other constitutive types | none |

Notes on `reference`, which carries the most:

- **`tier` is the precedence** the flat index expressed as §1–§4 vs §5:
  `code-scope` (the running code depends on it) outranks `workflow`
  (the development workflow depends on it).
- **`kind` is what the surface *is*; `role` is how *this project* relates
  to it.** They overlap on the word `infrastructure` and that is fine —
  a Redis instance is `kind: infrastructure` and `role: infrastructure`,
  while an upstream auth service is `kind: external-api`,
  `role: upstream`. `role` is what `purpose.md` and `scope.md` navigate
  by, and it is only meaningful at `tier: code-scope`; omit it on
  workflow tooling.
- **`resource` must be grounded**, never invented. It uses the
  established consultation vocabulary — `MCP <server>`, `CLI <tool>`,
  `URL: <address>`, `vendored at <path>`, `spec at <path>` — and for an
  external API it names the **external** surface (the OpenAPI, the
  vendored docs), never the internal assembly that consumes it. If you
  cannot find it, `[MISSING]` and ask.

`decision` files are named `<NNN>-<slug>.md` where `NNN` matches the
numeric part of `id`, so `id: ADR-004` lives at
`decisions/004-event-bus.md`. That keeps the directory sorted in
decision order.

### The tolerance rule

**Unknown frontmatter keys are ignored without error. The only key whose
absence is a finding is `type`.**

This is the rule that makes the pattern survivable. Concretely:

- A concept carrying keys JAIBA does not use — from an upstream OKF
  revision, from another tool, from a human's own annotation — is read
  normally. Skip what you don't recognize; do not warn, do not strip,
  do not "clean up".
- A key JAIBA *does* use but which is absent is at most a quality note,
  never a rejection. A `decision` without `updated` is still a decision.
- A file with no `type:` at all — or a `type:` outside the closed
  vocabulary — is the one reportable case: `jaiba-doctor` names the file
  and routes here, and this skill fixes it with the human.
- Never write a validator that rejects on unknown keys. The tolerance is
  the feature; strictness would re-couple JAIBA to a draft spec.

## Relations are file-relative links

Every relation between concepts is an ordinary markdown link, resolved
**relative to the file it is written in**.

| From | To | Written as |
|---|---|---|
| `index.md` | a decision | `[ADR-004 …](decisions/004-event-bus.md)` |
| `identity/scope.md` | a reference | `[Stripe](../references/stripe.md)` |
| `identity/units/api.md` | a sibling unit | `[shared](shared.md)` |
| `decisions/004-…md` | the decision it supersedes | `[ADR-002](002-rest-only.md)` |
| `.ai/work/plan.md` | the quality gate | `[quality gate](../memory/identity/quality-gate.md)` |

Never write:

- **Absolute repo paths** (`/repo/.ai/memory/references/stripe.md`) or paths
  rooted at the repo (`.ai/memory/…`) from inside the bundle. They break
  the moment the bundle moves, and the bundle's portability is the whole
  point.
- **Textual section citations** — `` `reference-index.md` §3 ``,
  "constitution §6". Those numbers no longer exist. A skill that needs a
  fact now **names the `type:` of the concept it wants**, and `index.md`
  resolves where it lives.
- **A bare filename with no path** when the target is in another
  directory. `../` is not optional.

Links may point outside the bundle (a repo file, a vendored copy, a URL)
when the target genuinely lives there — `resource:` values and README
pointers do this routinely. Those are references *out*, not relations
*between* concepts, and they follow whatever form the target needs.

## `index.md` — the entry point

The index is what makes the bundle navigable to a cold agent, and it
carries a hard cost constraint: **resolving a single concept must cost
reading that one concept file.** An agent that needs only the quality
gate reads `index.md` and then `identity/quality-gate.md` — never
identity, scope and conventions on the way.

So the index:

- **Groups entries by `type:`**, with the type name visible.
- Gives every concept in the bundle **one link and one line of
  description** (its `description:` frontmatter). Nothing more — the
  index is a map, not a summary. Duplicating a concept's content into the
  index is how the single-file cost gets silently broken.
- **Links directly to the concept**, never through an intermediate
  concept. There is no "read identity first" step.
- Is regenerated whenever a concept is added, removed or renamed. A stale
  index is a broken-link report from `jaiba-doctor`.

`log/` entries grow without bound; index them as a group (the directory
and its convention) rather than one line per dated entry, and let the
filename convention carry the ordering.

## Writing a concept

- **One concept per file.** If a file needs the word "also" to describe
  what it holds, it is two concepts.
- **Self-contained.** A concept must be readable alone, without its
  siblings. That is what the single-file cost rule buys.
- **No duplication across concepts.** When two concepts need the same
  fact, one owns it and the other links. The `With Whom` collapse above
  is the canonical example.
- **English, always.** `.ai/memory/` is agent-facing long-term memory and
  is English even when the session is not (`AGENTS.md` §3.5). The
  repository's `README.md` remains the exception; it is human-facing.
- **Kebab-case slugs** in filenames, matching the concept's subject:
  `references/postgres.md`, not `references/PostgreSQL_DB.md`.
- **`[MISSING]` / `[NEEDS CLARIFICATION]` discipline is unchanged.** A
  fact you cannot ground is marked and surfaced, never confabulated —
  and the graph makes gaps *more* visible, not less.

## Executive memory

`.ai/work/`'s four artifacts adopt the same convention: each gains a
`type:` (`prd`, `plan`, `tasks`, `walkthrough`) and keeps the keys it
already carries — `PRD.md` and `plan.md` already had frontmatter,
`tasks.md` and `walkthrough.md` gain theirs. Citations from a plan into
the brain become **navigable links** (`../memory/…`) rather than prose
references, which is what makes a broken citation detectable.

Their exact per-artifact shape is owned by the templates in `conduct`'s
`assets/`, not by this file. What this file governs is the part they
share with the bundle: `type:` is mandatory, unknown keys are tolerated,
links are file-relative.

## Common failure modes

- **Inventing a `type:`.** The vocabulary is closed. A concept that fits
  nothing is a framework question, not a local decision.
- **Writing a validator.** Rejecting unknown frontmatter re-creates the
  dependency the pattern exists to avoid.
- **Treating a missing optional key as an error.** Only `type:` counts.
- **Fattening `index.md`** with summaries until reading it costs as much
  as the monolith it replaced.
- **Indirect indexing** — pointing the index at `identity/project.md` and
  expecting the agent to find the quality gate from there. Every concept
  is one hop from the index.
- **Absolute or section-numbered references.** `` §6 `` resolves to
  nothing now; link the `quality-gate` concept.
- **Re-duplicating the reference inventory** into `purpose.md` /
  `scope.md` instead of linking the `reference` concepts.
- **Two concepts in one file**, or one concept split across two because
  its source section was long. Sections are not the unit; concepts are.
- **Editing a `log-entry`.** Append-only survives the reserialization
  intact: an existing entry may gain missing frontmatter, and nothing
  else. Corrections are new entries.
- **Writing `.ai/memory/` from anywhere but this skill.** The graph
  changes nothing about §2.9.
