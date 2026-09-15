---
name: jaiba-init
description: "Repo-scoped JAIBA setup and long-term memory. Bootstraps one repository — AGENTS.md marker, `.ai/` skeleton, constitutive memory, then hands to jaiba-doctor — and afterwards owns `.ai/memory/` maintenance via its update-brain mode (populate templates, apply ADRs, fix drift)."
version: 2.1.0
author: atlasfoo<iscomejia15@outlook.com>
requires:
  - git
tags:
  - jaiba
  - meta
  - jaiba-meta
  - bootstrap
  - brain
---

# jaiba-init

The **repo-scoped** half of JAIBA setup, and the framework's long-term
memory owner. `jaiba-init` does two things, in two modes:

- **Bootstrap** (`jaiba-init`, bare) — instrument *this repository*:
  the `AGENTS.md` marker, the `.ai/` brain skeleton and `.atl/`, the
  constitutive memory, then the first `jaiba-doctor` checkup.
- **Maintain** (`jaiba-init:update-brain`) — keep the brain true to the
  repository for the rest of the project's life.

Everything here is scoped to **one repo**. The machine-level half of
setup — the global behavioral contract, the skillset, the subagent
battery — belongs to **`jaiba-configure`** and is never performed here.

In its `update-brain` mode this is the **only skill allowed to write
`.ai/memory/`**. Everywhere else the brain is read-mostly:
`conduct:summarize` *proposes* ADRs and brain changes, but never enacts
them — it hands off here (`AGENTS.md` §2.9, §5).

That mode exists to close the learning loop at the **project** level.
Where `conduct:summarize` closes a single piece of work,
`jaiba-init:update-brain` is what keeps the constitutive concept
graph — `.ai/memory/`'s identity concepts, decisions, and
references — true to the repository over the project's life.

Each mode is documented in its own reference file. Read the relevant
reference *before* taking action — the selection table below tells you
which one.

## Mode Selection

Decide the mode **before** reading anything else. If the message is
ambiguous, ask the developer instead of guessing.

| Situation | Mode | Read |
|---|---|---|
| The repo is not instrumented at all — no `.ai/` whatsoever — and the developer wants JAIBA adopted here: "set up jaiba in this repo", "onboard this project", "jaiba-init", or the skill invoked bare with no sub-mode. | **bootstrap** (the default) | `references/bootstrap-mode.md` |
| The `.ai/` skeleton exists but the brain does not (no `.ai/memory/index.md`, or the concept files it links to are bare templates) and the developer wants it built — "build the brain", "initialize the memory". Also: reached from bootstrap mode's step 4, and from a half-bootstrapped repo (see the resume table in `references/bootstrap-mode.md`). | `update-brain:initialize` | `references/initialize-mode.md` |
| The brain already exists and must be reconciled with reality — either **apply proposals** ("apply the proposed ADR", "record this decision", "add this integration") handed over by `conduct:summarize`, or **fix drift** ("the identity concepts are stale", "reconcile memory with the code") after the project evolved. | `update-brain:update` | `references/update-mode.md` |
| The brain exists in populated flat layout (`constitution.md`, `adr-log.md`, `reference-index.md` with real content, no `index.md`) and the developer explicitly wants to convert it to the OKF concept bundle — "convert the brain to OKF", "migrate to the new format", "I want the concept bundle". Also: optional and human-triggered, never offered unprompted. | `update-brain:migrate` | `references/migrate-mode.md` |
| Anything else — a pure question about the brain (that's `ask`), *implementing* code (that's `conduct`/`fast`), or **machine-level** setup (that's `jaiba-configure`) | **Route, don't guess.** See "Hand-off" below. | — |

Bare `jaiba-init` means bootstrap; `jaiba-init:update-brain` selects the
maintenance mode, which then picks `initialize` or `update` from the two
rows above. Bootstrap always ends by entering `initialize` itself — that
transition is internal to this skill, not a hand-off.

## Universal Preconditions

Before entering any mode, do these reads. The whole point of the brain
is to mirror the repository, not the prompt's assumptions — so load the
ground truth before writing a word.

1. **`AGENTS.md`** — your behavioral contract. Always. Note especially
   §2.9 (memory is read-mostly; propose, don't patch) and §5 (drift
   handling) — they *are* this skill's mandate.

   This skill, like the rest of the framework, can be installed
   per-project or **globally** (e.g. `~/.claude/skills/`), shared
   across every repository. `.ai/` and `AGENTS.md` always mean the
   *current project's* root — where `.git/` lives — never a path
   relative to this skill's own installation location.

   If `AGENTS.md` is missing entirely, or exists but isn't the JAIBA
   marker (no pointer to the global contract, no `.ai/` Brain Map), this
   project was never instrumented. In **bootstrap** mode that is the
   expected starting state — dropping the marker is step 3, carry on. In
   the **`update-brain`** modes it is a finding: the brain can still be
   populated if a `.ai/` skeleton exists, but flag it clearly and
   recommend a `jaiba-init` bootstrap run, then continue with
   `initialize` if the developer wants `.ai/memory/` built anyway.

   Separately, the *machine-level* behavioral contract
   (`jaiba-contract.md` in the agent's user-level config) and the
   subagent battery are **`jaiba-configure`**'s responsibility, not this
   skill's. If they're absent, say so and point the developer at
   `jaiba-configure` — never install them from here.
2. **The current state of `.ai/`** — does the directory exist at all
   (no `.ai/` → **bootstrap**)? Does `.ai/memory/index.md` exist, and
   are the identity concepts it links to real content or untouched
   templates (full of `[brackets]`)? This is what disambiguates
   bootstrap from `initialize` from `update`.
3. **The repository itself** — for `initialize`, the whole evidence
   sweep (see its reference); for `update`, the slice that changed.
   Bootstrap defers this to the `initialize` step it ends in.

If a precondition is unclear (e.g. the files are half-filled — neither
fresh templates nor complete), surface it and ask which mode the
developer means rather than guessing.

## Artifacts at a Glance

`jaiba-init` owns every template it writes into a repository — both the
concept templates that populate `.ai/memory/` and the bootstrap files.
They live in this skill's `assets/` and are the single source of truth
for their shape. No other skill carries copies: `jaiba-configure` owns
only the *machine-level* assets (the global contract, the skillset, the
subagent battery).

The brain itself follows the **OKF pattern** (full authority:
`references/okf-pattern.md`): one concept per file, each carrying a
`type:` in its frontmatter, `.ai/memory/index.md` as the single entry
point. Each concept type has its own template under
`assets/concepts/<name>.md`:

| Concept `type:` | Template | Instance written to |
|---|---|---|
| `index` | `assets/concepts/index.md` | `.ai/memory/index.md` |
| `project` | `assets/concepts/project.md` | `.ai/memory/identity/project.md` |
| `architecture` | `assets/concepts/architecture.md` | `.ai/memory/identity/architecture.md` |
| `purpose` | `assets/concepts/purpose.md` | `.ai/memory/identity/purpose.md` |
| `scope` | `assets/concepts/scope.md` | `.ai/memory/identity/scope.md` |
| `sub-unit` (multi-unit repos only) | `assets/concepts/sub-unit.md` | `.ai/memory/identity/units/<slug>.md` |
| `quality-gate` | `assets/concepts/quality-gate.md` | `.ai/memory/identity/quality-gate.md` |
| `convention` | `assets/concepts/conventions.md` | `.ai/memory/identity/conventions.md` |
| `decision` (one per ADR) | `assets/concepts/decision.md` | `.ai/memory/decisions/<NNN>-<slug>.md` |
| `reference` (one per external surface) | `assets/concepts/reference.md` | `.ai/memory/references/<slug>.md` |
| `log-entry` (append-only) | `assets/log-entry-template.md` | `.ai/memory/log/<YYYY-MM-DD>-<slug>.md` |

Plus the bootstrap files, which aren't concepts at all:

| File written | Lives in | Written by | Template |
|---|---|---|---|
| `AGENTS.md` (repo marker) | repo root | bootstrap | `assets/AGENTS.md` |
| `.ai/.gitignore` | brain skeleton | bootstrap | `assets/ai.gitignore` |
| `.atl/.gitignore` | machine state | bootstrap | `assets/atl.gitignore` |
| `README.md` (repo root, *conditional*) | repo root | `initialize` | `assets/readme-skeleton.md` |

> **Two authoring conventions inside `assets/concepts/`.** The eight
> single-instance identity types (`index`, `project`, `architecture`,
> `purpose`, `scope`, `sub-unit`, `quality-gate`, `convention`) are each
> written as raw-frontmatter-first, copy-and-fill documents — read the
> template, replace the `[brackets]`, done. `decision` and `reference`
> are **N-instance** types — a repository accumulates many ADRs and many
> external surfaces over its life — so their templates read instead as
> prose guidance plus a fenced ` ```markdown ` example: the guidance
> covers when a new instance is warranted and the naming/precedence
> rules that don't fit a single fillable file, and the fenced block is
> what gets copied per new instance. This is a **deliberate split**, not
> drift to normalize — expect both conventions when reading or writing
> to `assets/concepts/`.

**Use each template's fillable content as the structure** — the shared
shape is what keeps the brain legible across the project's life. For the
eight identity types, copy the file and fill the `[brackets]` from
evidence. For `decision` and `reference`, copy the fenced example
verbatim per new instance and follow the surrounding guidance for when
to create one. Don't restructure either style.

> `README.md` is special: it is **not** part of `.ai/memory/`, it is a
> human-facing repo file. See "The README" below for exactly when this
> skill touches it.

## What each concept may contain — and when it may change

These rules are the heart of the `update-brain` mode. They hold in
**both** its sub-modes: `initialize` fills the concept for the first
time under them; `update` only changes a concept when its specific
trigger below is met. They are mode-selection-level guidance —
the full frontmatter contract, the closed `type:` vocabulary, and the
link convention are `references/okf-pattern.md`'s job; each
`assets/concepts/<name>.md` template is the per-type authority on its
own fields and examples. Don't restate either here.

### Identity concepts — `identity/*.md`

Covers `project`, `architecture`, `purpose`, `scope`, `sub-unit`,
`quality-gate`, and `convention`. Change one **only** when the
project's identity actually shifts:

- A new **upstream** dependency (a service this project now consumes) or
  **downstream** consumer (something that now depends on this project) —
  as a `reference` concept carrying the matching `role`, linked from
  `purpose.md` or `scope.md`.
- A change in **consumers** / who the project serves.
- A change to the **Quality Gate** (new threshold, new required check).
- A change in **scope** (something moves in or out of "what this
  project does"), including a unit added to or removed from a
  multi-unit repo (`sub-unit`).

A bug fix, a refactor, or a routine version bump does **not** touch
identity. If the change doesn't move identity/scope/gate, leave the
concepts alone.

### `decision` concepts — `decisions/<NNN>-<slug>.md`

- Write a new file **only** for an architectural decision made **after**
  the framework was initialized in this project. The seed entry
  `ADR-001` (adoption of the JAIBA brain) is the boundary.
- **Never back-fill history.** Do not reconstruct decisions for choices
  taken *before* the brain existed — `initialize` does not mine the git
  history for past architecture choices. The series starts at adoption
  and grows forward. (The *why* of pre-existing structure, when it
  matters, is surfaced read-only by `skill: ask` via `git log`/`blame`,
  not frozen into a decision concept retroactively.)
- **Never delete or rewrite** a past decision. Supersede it with a new
  file that links to the old one by ID (`assets/concepts/decision.md`
  spells out the two-file mechanics).
- The usual source of a new decision is a *proposal* from
  `conduct:summarize`; `update` applies it, flipping `status:`
  `proposed → accepted`.
- Full propose/don't-propose triggers, the `status:` vocabulary, and the
  `ADR-001` worked example: `assets/concepts/decision.md`.

### `reference` concepts — `references/<slug>.md`

One file per **external** surface the project touches. Two tiers, in
precedence order (`assets/concepts/reference.md`'s `tier:` key
enforces this):

1. **`code-scope`** — infrastructure, external APIs, internal
   cross-component contracts, packages the *running code* depends on.
   **Primary.**
2. **`workflow`** — scanners, security audits, remote review agents the
   *workflow* depends on. **Secondary**, and the input surface that the
   future `doctor` skill tests for reachability.

Two hard rules:

- **The consumption point is the external one.** For an API, point at
  its OpenAPI/vendored spec or docs URL — **not** the internal assembly
  where the data contracts are written. A local-only copy of an
  OpenAPI is referenced at the *vendored* path, not at the code that
  consumes it.
- **Never invent a consumption point.** Every `resource:` must be
  grounded in real repo evidence (a config file, an env var, a CI step,
  a vendored spec). If you cannot find where a reference is consumed,
  **do not guess** — record it as `[MISSING]` and tell the human.

There is no monolithic index to prune anymore: a category the project
has no entries for — no external APIs, no business documentation, no
verification tooling — simply has **no files** under `references/`.
Never write a placeholder reference concept for a surface the project
doesn't have; that is the graph's equivalent of the old "prune the
empty section" rule.

Locally stored ("vendored") copies of external references — Repomix
bundles, a physical copy of an API's OpenAPI/docs — live under
`.ai/vendored/`, and a reference concept's `resource:` points at that
path. See the framework README for the folder's role. Full `tier:`,
`kind:`, `role:`, and `resource:` vocabulary plus worked examples:
`assets/concepts/reference.md`.

### `.ai/memory/log/` — the chronological record

The brain has a fourth surface: an **append-only log**, one file per
entry (`log/<YYYY-MM-DD>-<slug>.md`, shape in
`assets/log-entry-template.md`). It fuses two streams into one
timeline:

- **`work-closure` entries** — written by the *workflow* close step
  (`summarize`) when it archives the essence of `.ai/work/` before
  clearing it. This is the one carve-out to "only
  `jaiba-init:update-brain` writes `.ai/memory/`": the close step
  appends here, and only here. The identity, decision, and reference
  concepts above remain exclusively this skill's.
- **`brain-change` entries** — written by *this skill*, one per
  `update` run that enacts a change, recording what changed in the
  constitutive memory and why. This is what makes brain evolution
  auditable without diffing git history.

Rules that keep the log trustworthy:

- **Append-only.** Never rewrite, rename, or delete an entry. A
  correction is a new entry pointing at the old one.
- **The log is not the decision record.** `decisions/` stays separate as
  *curated* memory — decisions currently in force, explicitly
  superseded. The log is *chronological* — what happened, in order.
  Don't let decision records live only as log entries (propose a
  `decision` concept instead), and don't narrate work history inside
  `decisions/` (that belongs here).
- `initialize` creates nothing in `log/` — it starts empty and grows
  as work closes and the brain evolves.

### The README

The README is not in `.ai/memory/`, but JAIBA assigns it a role and
this skill owns keeping that role intact. The README must serve a
**human developer** by carrying two things:

- **Requirements** — mandatory and optional, to run/develop the project.
- **How-to** — how to run it, run tests, get coverage, run a quality /
  security scan, lint, and format.

Behavior:

- **Empty README** → fill it from `assets/readme-skeleton.md` (then fill
  the skeleton's brackets from evidence). This is the only case where
  the skill writes the README outright.
- **Non-empty but incomplete** → do **not** overwrite it. Tell the
  developer which of the two roles it's missing and *suggest* what to
  add. The README may already be structured very differently and that's
  fine — the test is whether it *fulfills the role*, not whether it
  matches the skeleton.
- The README may be in **any language** (it serves humans and agents).
  This is the opposite of `.ai/memory/`, which is English-only.

## The `[MISSING]` / `[NEEDS CLARIFICATION]` discipline

This is where `jaiba-init` deliberately differs from `conduct`.
That skill *forbids* `[NEEDS CLARIFICATION]` in their
artifacts — they resolve doubts before writing. The brain can't always
work that way: a brownfield project has facts that simply aren't
derivable from code (the business objective, the downstream consumers,
the Quality Gate thresholds the team intends).

So the order is:

1. **Prefer to ask.** For anything you can't determine from evidence,
   ask the developer with a structured questionnaire (`ask_user_input_v0`
   if available, otherwise chat). One topic per question; closed options
   when the answer space is closed.
2. **Mark, don't confabulate.** If the developer defers a question, leave
   the canonical placeholder — `[MISSING]` for an absent fact,
   `[NEEDS CLARIFICATION]` for an ambiguous one — rather than inventing a
   plausible-sounding answer. A wrong "fact" in the brain is worse than a
   visible gap.
3. **Always warn.** Whenever a brain file you wrote or touched still
   carries a `[MISSING]` / `[NEEDS CLARIFICATION]` (or an unfilled
   `[bracket]` from the template), say so explicitly at the end, listing
   each file and what's outstanding (`AGENTS.md` §5.4). The human must
   never discover an incomplete brain by accident.

## Language

Per `AGENTS.md` §3.5:

- **This skill's source** (SKILL.md, references, templates) — English.
- **`.ai/memory/` concepts** (identity, decisions, references, log) —
  **English, always.** They are agent-facing long-term memory. Even when
  the developer is working in another language, the brain is English.
- **`README.md`** — the project's own language; it is human-facing.

## Relationship with the rest of the framework

```
  jaiba-configure  [independent — machine-level setup: contract, skillset, subagents]
                   (jaiba-init step 3 only checks for it; never installs it — no shared file path)

  jaiba-init ──(marker, .ai/ skeleton, .atl/)──▶ :update-brain:initialize
        │                                   (internal mode transition)
        └──────────────────────────────▶ jaiba-doctor (first checkup)
                          │
        ┌─────────────────┘
        ▼
  [ project work: conduct chain ]
        │  summarize / archive *propose* ADRs, refs, scope changes
        ▼
  jaiba-init:update-brain:migrate ──(convert flat → OKF bundle)──▶ brain in new layout
  jaiba-init:update-brain:update ──(applies proposals, fixes drift)──▶ brain stays true
```

- **`jaiba-configure` ∥ `jaiba-init`.** They are **independent**: one
  configures the *machine*, the other instruments a *repo*. Neither
  invokes the other. `jaiba-init` only *detects* whether the global
  contract and subagent battery exist and, if not, names
  `jaiba-configure` as the prerequisite the developer should run.
- **bootstrap → `initialize` is internal.** Laying the skeleton and
  filling the brain are two modes of *this* skill, so bootstrap
  transitions into `initialize` directly rather than handing off. The
  artifact templates have always belonged here.
- **`jaiba-init` → `jaiba-doctor`.** Bootstrap's closing hand-off: the
  first checkup and the local toolchain probe (`.atl/tool-layout.md`).
  A real cross-skill boundary, never a cross-skill file path (skills
  package independently; see `state.md`).
- **`conduct:summarize` → `update`.** It
  *propose* `decision` concepts / `reference` entries / identity
  changes and point the developer here. `update` is where those
  proposals are enacted.
- **`doctor` reads `reference` concepts.** This skill *records*
  references (including the secondary verification-tooling tier);
  `doctor` *tests* their reachability. Don't test reachability here.
- **Drift (`AGENTS.md` §5).** When any skill notices the brain
  contradicts the repo, it notifies and routes here — it does not patch
  memory itself.

## Hand-off

| The developer now wants… | Route to |
|---|---|
| To just ask what the brain says, read-only | `ask` |
| To plan/implement a code change or formalize a requirement | `conduct` (or `fast` for a contained one) |
| Machine-level setup — the global behavioral contract, the skillset, the subagent battery | `jaiba-configure` |
| A health check of an already-instrumented repo | `jaiba-doctor` |

## Common failure modes

- **Bootstrapping an instrumented repo.** A populated `.ai/memory/` or an
  existing `AGENTS.md` is the developer's; check state before laying
  anything down (bootstrap-mode's "When NOT to bootstrap" table).
- **Doing `jaiba-configure`'s job.** Installing a global contract, a
  skillset or the subagent battery from here re-creates the coupling
  this skill was split to remove. Detect, report, route.
- **Confabulating facts.** Filling the business objective or a downstream
  consumer with a plausible guess because asking felt slower. The brain's
  value is that it's *true*; a confident wrong fact poisons every later
  session. Ask, or mark `[MISSING]`.
- **Back-filling decisions.** Reconstructing pre-adoption architecture
  choices as `decision` concepts. The series starts at `ADR-001` and
  grows forward; history before the brain is `ask`'s territory, not the
  decisions directory's.
- **Touching identity concepts for non-identity changes.** A refactor or
  version bump is not an identity event. Only identity / scope /
  consumers / Quality Gate changes are.
- **Inventing a consumption point in a reference concept.** Pointing at
  the internal assembly instead of the external spec, or fabricating a
  URL. Ground every `resource:` in real evidence or mark `[MISSING]`.
- **Overwriting a populated README.** Only an *empty* README gets the
  skeleton. A non-empty one gets advice, not a rewrite.
- **A non-English brain.** `.ai/memory/` is English-only even when the
  session language is not. (The README is the exception.)
- **Silent gaps.** Finishing without listing the `[MISSING]` /
  `[NEEDS CLARIFICATION]` placeholders that remain. Always warn.
