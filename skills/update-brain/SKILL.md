---
name: update-brain
description: >-
  Long-term memory (brain) maintenance workflow inside the JAIBA framework. Use this skill whenever the project's long-term brain in `.ai/memory/` must be created or reconciled with reality: building the brain for the first time on a new or legacy project, or updating it after the project has evolved. Trigger on explicit calls like "update-brain initialize / update", and on phrases like "set up jaiba here", "build the brain", "initialize the memory", "onboard this repo", "the brain is out of date", "the constitution is stale", "reconcile memory with the code", "apply the proposed ADR", "record this decision in the adr log", "add this integration to the reference index". Also the natural next step whenever `specification:archive` or `planning:summarize` has *proposed* ADRs, reference-index entries, or constitution changes — this skill is the only one allowed to write `.ai/memory/`. Two modes: `initialize` (analyze the repo — code, manifests, README, CI, scriptfiles — and populate constitution.md, adr-log.md and reference-index.md, flagging what it cannot determine instead of inventing it) and `update` (apply proposed brain changes, or re-analyze and reconcile the brain after structural drift). Prefer this over editing `.ai/memory/` by hand; memory is read-mostly everywhere else, only `update-brain` enacts it.
version: 1.0.0
author: atlasfoo<iscomejia15@outlook.com>
requires:
  - git
tags:
  - jaiba
  - workflows
  - jaiba-workflows
  - brain
---

# Update Brain Skill

The long-term memory workflow of the JAIBA framework. `update-brain` is
the **only skill allowed to write `.ai/memory/`**. Everywhere else the
brain is read-mostly: `planning:summarize` and `specification:archive`
*propose* ADRs and brain changes, but they never enact them — they hand
off here (`AGENTS.md` §2.9, §5).

It exists to close the learning loop at the **project** level. Where
`planning:summarize` closes a single plan and `specification:archive`
closes a single requirement, `update-brain` is what keeps the three
long-term artifacts — `constitution.md`, `adr-log.md`,
`reference-index.md` — true to the repository over the project's life.

This skill has **two modes**, each documented in its own reference
file. Read the relevant reference *before* taking action — the
selection table below tells you which one.

## Mode Selection

Decide the mode **before** reading anything else. If the message is
ambiguous, ask the developer instead of guessing.

| Situation | Mode | Read |
|---|---|---|
| The brain does not exist yet (no `.ai/memory/*.md`, or the files are bare templates) and the developer wants it built — "set up jaiba", "build the brain", "onboard this repo", "update-brain initialize". Also: invoked by `scaffold` right after it lays the skeleton. | `initialize` | `references/initialize-mode.md` |
| The brain already exists and must be reconciled with reality — either **apply proposals** ("apply the proposed ADR", "record this decision", "add this integration") handed over by `planning:summarize` / `specification:archive`, or **fix drift** ("the constitution is stale", "reconcile memory with the code") after the project evolved. | `update` | `references/update-mode.md` |
| Anything else — a pure question about the brain (that's `ask`), or *implementing* code (that's `planning`/`fast`) | **Route, don't guess.** See "Hand-off" below. | — |

## Universal Preconditions

Before entering any mode, do these reads. The whole point of the brain
is to mirror the repository, not the prompt's assumptions — so load the
ground truth before writing a word.

1. **`AGENTS.md`** — your behavioral contract. Always. Note especially
   §2.9 (memory is read-mostly; propose, don't patch) and §5 (drift
   handling) — they *are* this skill's mandate.
2. **The current state of `.ai/memory/`** — do the three files exist?
   Are they real content or untouched templates (full of `[brackets]`)?
   This is what disambiguates `initialize` from `update`.
3. **The repository itself** — for `initialize`, the whole evidence
   sweep (see its reference); for `update`, the slice that changed.

If a precondition is unclear (e.g. the files are half-filled — neither
fresh templates nor complete), surface it and ask which mode the
developer means rather than guessing.

## Artifacts at a Glance

`update-brain` owns the **templates** for the three long-term artifacts.
They live in this skill's `assets/` and are the single source of truth
for the brain's shape — `scaffold` does **not** carry its own copies; it
hands off to `initialize`, which materializes them.

| File written | Lives in | Template |
|---|---|---|
| `.ai/memory/constitution.md` | long-term memory | `assets/constitution-template.md` |
| `.ai/memory/adr-log.md` | long-term memory | `assets/adr-log-template.md` |
| `.ai/memory/reference-index.md` | long-term memory | `assets/reference-index-template.md` |
| `README.md` (repo root, *conditional*) | repo root | `assets/readme-skeleton.md` |

**Use the templates verbatim** as the structure — the shared shape is
what keeps the brain legible across the project's life. Fill the
`[brackets]` from evidence; don't restructure them.

> `README.md` is special: it is **not** part of `.ai/memory/`, it is a
> human-facing repo file. See "The README" below for exactly when this
> skill touches it.

## What each artifact may contain — and when it may change

These rules are the heart of the skill. They hold in **both** modes:
`initialize` fills the artifact for the first time under them; `update`
only changes an artifact when its specific trigger below is met.

### `constitution.md` — project identity

Change it **only** when the project's identity actually shifts:

- A new **upstream** dependency (a service this project now consumes) or
  **downstream** consumer (something that now depends on this project).
- A change in **consumers** / who the project serves.
- A change to the **Quality Gate** (new threshold, new required check).
- A change in **scope** (something moves in or out of "what this
  project does").

A bug fix, a refactor, or a routine version bump does **not** touch the
constitution. If the change doesn't move identity/scope/gate, leave it
alone.

### `adr-log.md` — architectural decision history

- Record an entry **only** for an architectural decision made **after**
  the framework was initialized in this project. The seed entry
  `ADR-001` (adoption of the JAIBA brain) is the boundary.
- **Never back-fill history.** Do not reconstruct ADRs for decisions
  taken *before* the brain existed — `initialize` does not mine the git
  history for past architecture choices. The log starts at adoption and
  grows forward. (The *why* of pre-existing structure, when it matters,
  is surfaced read-only by `skill: ask` via `git log`/`blame`, not
  frozen into the ADR log retroactively.)
- **Never delete or rewrite** a past ADR. Supersede it with a new entry
  that references the old one by ID (the template spells this out).
- The usual source of new ADRs is a *proposal* from
  `planning:summarize` or `specification:archive`; `update` applies it,
  flipping the status `Proposed → Accepted`.

### `reference-index.md` — external references

The index maps every **external** surface the project touches. Two
tiers, in precedence order (the template enforces this):

1. **Code-scope references** — infrastructure, external APIs, packages
   the *running code* depends on. **Primary.**
2. **Workflow & verification tooling** — scanners, security audits,
   remote review agents the *workflow* depends on. **Secondary**, and
   the input surface that the future `doctor` skill tests for
   reachability.

Two hard rules:

- **The consumption point is the external one.** For an API, point at
  its OpenAPI/vendored spec or docs URL — **not** the internal assembly
  where the data contracts are written. A local-only copy of an
  OpenAPI is referenced at the *vendored* path, not at the code that
  consumes it.
- **Never invent a consumption point.** Every "how to consult" must be
  grounded in real repo evidence (a config file, an env var, a CI step,
  a vendored spec). If you cannot find where a reference is consumed,
  **do not guess** — record it as `[MISSING]` and tell the human.
- **Prune sections that don't apply.** If the project has no entries for
  a whole category — no external APIs, no business documentation, no
  verification tooling — **remove that section** rather than leaving a
  heading full of bracket rows. This is the inverse of `[MISSING]`:
  `[MISSING]` marks a fact that *should* be there but couldn't be found
  (ask the human); pruning removes a category that genuinely *doesn't
  apply*. Renumber the remaining sections so they stay contiguous. A
  reference-index padded with empty template sections reads as
  unfinished and erodes trust in the brain.

Locally stored ("vendored") copies of external references — Repomix
bundles, a physical copy of an API's OpenAPI/docs — live under
`.ai/vendored/`, and an index entry points at that path. See the
framework README for the folder's role.

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

This is where `update-brain` deliberately differs from `planning` and
`specification`. Those skills *forbid* `[NEEDS CLARIFICATION]` in their
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
- **`.ai/memory/` artifacts** (constitution, adr-log, reference-index) —
  **English, always.** They are agent-facing long-term memory. Even when
  the developer is working in another language, the brain is English.
- **`README.md`** — the project's own language; it is human-facing.

## Relationship with the rest of the framework

```
  scaffold ──(lays .ai/ skeleton, then invokes)──▶ update-brain:initialize
                                                          │
        ┌─────────────────────────────────────────────────┘
        ▼
  [ project work: planning / specification ]
        │  summarize / archive *propose* ADRs, refs, scope changes
        ▼
  update-brain:update ──(applies proposals, fixes drift)──▶ brain stays true
```

- **`scaffold` → `initialize`.** `scaffold` (a meta skill, not yet
  built) creates the `.ai/` directory skeleton and copies `AGENTS.md`,
  then immediately invokes `update-brain:initialize`. `scaffold` does
  **not** manage the artifact templates — that is this skill's job. The
  boundary is a hand-off, never a cross-skill file path (skills package
  independently; see `state.md`).
- **`planning:summarize` / `specification:archive` → `update`.** Both
  *propose* ADRs / reference-index entries / constitution changes and
  point the developer here. `update` is where those proposals are
  enacted.
- **`doctor` (future) reads `reference-index.md`.** This skill *records*
  references (including the secondary verification-tooling tier);
  `doctor` *tests* their reachability. Don't test reachability here.
- **Drift (`AGENTS.md` §5).** When any skill notices the brain
  contradicts the repo, it notifies and routes here — it does not patch
  memory itself.

## Hand-off

| The developer now wants… | Route to |
|---|---|
| To just ask what the brain says, read-only | `ask` |
| To plan/implement a code change | `planning` (or `fast` for a contained one) |
| To formalize a new requirement | `specification` |
| To set up the `.ai/` skeleton from scratch | `scaffold` (which then calls back here) |

## Common failure modes

- **Confabulating facts.** Filling the business objective or a downstream
  consumer with a plausible guess because asking felt slower. The brain's
  value is that it's *true*; a confident wrong fact poisons every later
  session. Ask, or mark `[MISSING]`.
- **Back-filling ADRs.** Reconstructing pre-adoption architecture
  decisions into `adr-log.md`. The log starts at `ADR-001` and grows
  forward; history before the brain is `ask`'s territory, not the log's.
- **Touching the constitution for non-identity changes.** A refactor or
  version bump is not a constitution event. Only identity / scope /
  consumers / Quality Gate changes are.
- **Inventing a consumption point in the index.** Pointing at the
  internal assembly instead of the external spec, or fabricating a URL.
  Ground every entry in real evidence or mark `[MISSING]`.
- **Overwriting a populated README.** Only an *empty* README gets the
  skeleton. A non-empty one gets advice, not a rewrite.
- **A non-English brain.** `.ai/memory/` is English-only even when the
  session language is not. (The README is the exception.)
- **Silent gaps.** Finishing without listing the `[MISSING]` /
  `[NEEDS CLARIFICATION]` placeholders that remain. Always warn.
