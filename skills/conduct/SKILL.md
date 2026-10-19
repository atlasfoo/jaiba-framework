---
name: conduct
description: >-
  Unified Spec-Driven-Development chain of JAIBA: propose → spec (PRD when depth demands it + design, human approval) → tasks → execute (phase by phase) → validate → summarize. Trigger when the developer describes work to shape or build, requests a PRD/design, or sends a continuation cue ("continue", "next", "go") with an active plan in the resolved executive context. Resolve logical constitutive/executive memory through the selected memory surface; filesystem retains .ai/memory/ and .ai/work/. Explicit override: /conduct [phase]. Not the host agent's native read-only plan mode: this workflow must persist full executive artifacts and approval before execution.
version: 3.2.0
author: atlasfoo<iscomejia15@outlook.com>
requires:
  - git
  - bash
tags:
  - jaiba
  - workflows
  - jaiba-workflows
  - conduct
  - sdd
---

# Conduct Skill

The workflow spine of the JAIBA framework. `conduct` owns the
whole Spec Driven Development chain — from a fuzzy idea to archived,
verified work — as **one skill with six phases**. The developer never
chooses between a "spec command" and a "plan command": they describe
what they want, the **triage** decides how deep the chain runs, and
the human approves the design before anything is built.

```
propose ──→ spec ──→ tasks ──→ execute ──→ validate ──→ summarize
(optional)  (define+design)              (loops per     (criteria      (single
            [approval gate]               phase)         check)         close step)
```

**Artifact → phase mapping** (each executive artifact belongs to
exactly one phase):

| Artifact | Phase that produces it |
|---|---|
| `PRD.md` (only at `spec` depth) | `spec` (define step) |
| `plan.md` | `spec` (design step) |
| `tasks.md` | `tasks` |
| `walkthrough.md` (change by change) + final summary | `execute` → `summarize` |

One boundary defines the front of the chain: **`propose` and `spec`
never write source code.** They produce the contract; `execute`
fulfills it.

## Not the host agent's plan mode

Host agents (Claude Code, Cursor, …) ship a native "plan mode" that
freezes file writes while the model thinks. That is **not** this
skill, and this skill must not run inside it: the `spec` phase writes
full `prd` and `plan` objects to the selected executive context, which a read-only native mode
would block. If the host is in its native plan mode, ask the developer
to exit it before entering the chain.

## Invocation: implicit first, explicit as override

- **Implicit (the normal path).** The routing rule below picks this
  skill and the right phase from the developer's message. No command
  needed.
- **Explicit — `/conduct [phase]`.** The deterministic override:
  when implicit routing misfires, or the developer wants to force a
  phase out of turn (`/conduct summarize`, `/conduct
  propose`). With no phase argument, run phase selection as if the
  message were implicit.

## Routing rule (when work is active)

While a fully read `plan` exists in the resolved executive context, every developer message routes down
one of three lanes:

| The message is… | Lane |
|---|---|
| A **continuation cue** — "continue", "next", "go", "keep going", an answer to your pending question | `execute` (this skill) |
| A **question** — asking, not asking-for-change | `ask` skill (read-only; it yields back here) |
| A **change request** outside the plan's current tasks | `fast` skill (it runs the shared triage; a contained change is done out-of-band, a big one is surfaced to fold into the plan or re-plan) |

When no work is active, a question still goes to `ask`; a change
request enters this chain through triage.

A continuation cue never grants design approval. A draft plan stays in
`spec`; only verified persisted approval permits `tasks`/`execute`.

## Brain Discovery and Validation

Resolve the effective `create-memory` installation through host skill
resolution, then read its canonical `references/memory-surface-contract.md`
and `references/resolution.md` (contract `jaiba-memory-surface` 1.0.0).
An unavailable or ambiguous dependency blocks use; do not assume sibling
installation paths. Resolve the exact work root, selected adapter,
namespace, stable project ID and executive context ID before phase selection.
Follow canonical precedence, callable-tool probes, binding validation,
authority checks and explicit context selection; never pick a latest plan,
branch-named context or another checkout's work. A changed binding is not
migration permission. No silent fallback, dual-write or local memory cache.

**External surface branch:** validate the selected owned scope and obtain
the complete constitutive catalogue (all pages), then full-read required
entry concepts. A binding, probe, marker or search hit is not instrumentation.
Require real project/architecture/purpose/scope/quality-gate/convention
content, applicable sub-units, and the standing decision/reference records.
An empty authoritative scope routes to `jaiba-init`; incomplete templates
route to its initialize path. Missing concepts are surfaced, not invented.
External instrumentation needs neither a local marker nor local memory/work
files: do not test `.ai/` paths to decide its state.

**Filesystem branch only:** read the effective `create-memory`
`references/filesystem-surface.md`. Require a non-empty JAIBA `AGENTS.md`
marker at the selected work root and resolve `.ai/memory/` there, never
relative to the skill installation. With `index.md` only, resolve the entry
concepts above through that index; with `constitution.md` only, retain the
supported legacy `constitution.md`, `adr-log.md`, `reference-index.md` and
`log/` sources without migration. Both entry files block access pending
human resolution. Neither entry file or a missing marker routes to
`jaiba-init`; bare templates route to initialize. Neither supported layout
is a warning. `.ai/work/` remains per checkout, without new context folders.

For either surface, permission errors, partial catalogues, unavailable
tools, unsupported versions and truncated reads are failures, not absence.
Stop affected work and surface the scope/error; do not bootstrap over it.
Only exact authoritative not-found or complete scoped enumeration proves
absence. `jaiba-configure` handles missing machine prerequisites, not an
empty project. `.atl/tool-layout.md` remains local toolchain evidence.

### Executive addressing and persistence

Use `(namespace, project-id, executive, context-id, logical-id)` for work,
and `(namespace, project-id, constitutive, logical-id)` for brain concepts.
Catalogue the selected executive context completely before deciding what
is active; resolve `prd`, `plan`, `tasks` and `walkthrough` by type and exact
address, then full-read the objects needed for routing. Multiple candidate
plans or conflicting identities block selection. Search results, summaries,
catalogue previews and truncated content are never a plan or PRD read.

Artifact names below are logical shorthand, **not file-existence tests**.
Only in the filesystem branch do `PRD.md`, `plan.md`, `tasks.md` and
`walkthrough.md` map to `.ai/work/` filenames. Constitutive concepts resolve
through the selected catalogue (through the index/legacy mapping on
filesystem). No backend record ID or guessed URI substitutes for an address.

Conduct is the single executive writer per context. Analysts/executors
receive exact scope, addresses, full necessary content and revision
provenance, and return reports; they do not write executive memory.
Establish serialized access before writes. For every create/update, check
authoritative absence/current full revision, preserve unknown metadata and
relations, retain the mutation receipt, and verify the complete intended
object by exact readback. A conflict or unknown/unverified outcome blocks
dependent writes; reconcile before retrying. Do not claim atomic CAS unless
the adapter supplies it. Persisted approval is subject to these same rules.

## Triage: how deep does the chain run?

Not every change deserves a PRD — a critical-library bump or a
performance pass needs a design and tasks, not product prose. The
triage maps **blast radius → depth** on the continuum
`inline → design → spec`. It lives in `references/triage.md` (read it
when entering the chain for a new piece of work) and is **shared with
`fast`**, parameterized by default and floor:

| Consumer | Default depth | Floor |
|---|---|---|
| `fast` | `inline` | `inline` |
| `conduct` | `design` | `design` |

`inline` never reaches this skill's artifacts (that's `fast`'s lane).
At `design` depth the chain skips the PRD: `spec` runs only its design
step. At `spec` depth the chain runs whole.

## Phase Selection

After discovery and executive catalogue/full reads, decide the phase
**before loading phase-specific context**. If the message is
ambiguous, ask the developer instead of guessing.

| Situation | Phase | Read |
|---|---|---|
| Requirement is fuzzy/exploratory; developer wants help shaping it ("help me think through…", "I'm not sure how this should work") | `propose` | `references/propose-mode.md` |
| Requirement is clear (or just landed in `propose`), no active `plan.md`, developer wants it specced/planned | `spec` | `references/triage.md`, then `references/spec-mode.md` |
| The context's plan is still draft, or approval was not persisted/verified | `spec` (approval/reconciliation) | `references/spec-mode.md` |
| `plan.md` exists and is approved, but `tasks.md` doesn't exist yet | `tasks` | `references/tasks-mode.md` |
| `plan.md` + `tasks.md` exist with unchecked tasks; message is a continuation cue | `execute` *(implicit)* | `references/execute-mode.md` |
| All tasks checked; acceptance criteria not yet verified (or developer asks to validate) | `validate` | `references/validate-mode.md` |
| `validate` passed; developer asks to close/wrap up — or validate just passed and they confirm closing | `summarize` | `references/summarize-mode.md` |
| Anything else — including a message unrelated to the active work | **Route or ask.** See the routing rule. | — |

**Delegation.** Whenever a phase hands work to the JAIBA subagent
battery — the code survey in `spec` (`code-analyst`), the memory
contrast in `propose`/`spec` (`business-analyst`), task execution in
`execute` (the executor tiers), criteria verification in `validate`
(`verify`) — the invocation contract in `references/subagents.md`
governs it: required dispatch, runtime capability and prerequisite checks,
and concurrency. **Dispatch every applicable role when the host permits
it, the role is callable, and its prerequisites are verified.** A single
task still uses an executor; file overlap serializes executor work.
Independent analysts and disjoint runnable executor tasks launch
concurrently within host capacity. Inline work requires a concrete
blocker recorded per role/task; convenience is never a fallback reason.
Authorized first-party JAIBA role invocation needs no separate approval;
the design approval gate and command provenance boundary still apply.

## Context Loading

Load per phase — not universally — to minimize tokens. By this point
Brain Discovery has already resolved the surface, project and context.
Load concepts by type from its constitutive catalogue and full-read them.
The physical examples below apply **only to the filesystem branch**;
they are never external discovery prerequisites.

- **`propose` / `spec`** (full context): `AGENTS.md` (or global
  contract); the `scope`, `quality-gate`, and `convention` (TDD mode)
  concepts, plus `sub-unit` concepts if the repo is multi-unit —
  `identity/scope.md`, `identity/quality-gate.md`,
  `identity/conventions.md`, `identity/units/<slug>.md` in the bundle,
  or `constitution.md` §5 / §6 / §7 / §5.1 in the legacy flat;
  `reference` concepts touched by the requirement
  (`references/<slug>.md`, or the matching `reference-index.md` rows);
  `decision` concepts recording standing decisions
  (`decisions/<NNN>-<slug>.md`, or `adr-log.md` entries); recent
  `log-entry` concepts — what was tried before (`.ai/memory/log/`,
  unchanged across both layouts); and the code the requirement
  plausibly touches, through the applicable analyst reports. Load the
  governing context needed for routing and decisions; dispatch the full
  code survey and memory contrast rather than duplicating them inline
  (`references/subagents.md § Analyst dispatch`).
- **`tasks`**: the approved `plan.md` (+ `PRD.md` if produced), plus
  the `quality-gate` and `convention` concepts to copy gate commands
  and TDD posture into `tasks.md` (`identity/quality-gate.md` +
  `identity/conventions.md` in the bundle, `constitution.md` §6/§7 in
  the legacy flat).
- **`execute`**: the selected context's `plan`, `tasks`, `walkthrough`
  only. Gate commands and TDD posture were already copied into
  `tasks.md` — no `quality-gate`/`convention` concept, and no
  `constitution.md`, is re-read.
- **`validate`**: `tasks.md § Gate Commands`, `PRD.md`'s acceptance
  criteria schema (if present), approved `plan.md` objective and Scope
  (In) at design depth, `walkthrough.md`, and relevant task diffs.
- **`summarize`**: the complete selected executive context.

If any read reveals a conflict between the request and recorded
project facts, **flag it before producing artifacts**.

## Artifacts at a Glance

Executive artifacts live in the resolved context. The following physical
paths and `archive.sh` apply **only to filesystem**; external objects use
logical addresses and contract operations, never local shadow files or
the filesystem archive script:

| File | Produced by | Lives until |
|---|---|---|
| `.ai/work/PRD.md` (spec depth only) | `spec` (define) | `summarize` |
| `.ai/work/plan.md` | `spec` (design) | `summarize` |
| `.ai/work/tasks.md` | `tasks`, updated by `execute` | `summarize` |
| `.ai/work/walkthrough.md` | stub by `tasks`, appended per change by `execute` | `summarize` |
| `.ai/work/<slug>-summary.md` | `summarize` (draft) | moved by `scripts/archive.sh` |
| `.ai/memory/log/<YYYY-MM-DD>-<slug>.md` | `summarize` (via `scripts/archive.sh`) | permanent |

Templates live in `assets/`. **Use them verbatim** — the shared
structure is what keeps work legible across sessions:
`prd-template.md`, `plan-template.md`, `tasks-template.md`,
`walkthrough-template.md`, `plan-summary-template.md`.

**Multisession by design.** The selected context survives between sessions; a
fresh session picks the chain up from wherever `tasks.md` says it is.
Phase boundaries are the safe checkpoints.

## Discrepancy Handling

When the request, the PRD, or the documented brain disagrees with what
the codebase actually shows:

1. **Ask first, write second.** Use a structured questionnaire
   (`ask_user_input_v0` when available, otherwise inline questions).
   Never emit `[NEEDS CLARIFICATION]` into executive artifacts — the
   artifact is the answer, not a list of pending doubts.
2. **Record only what survived clarification.** If the design still
   deviates from an *approved* PRD, `plan.md` carries a "Discrepancies
   vs PRD" section. Trivial deviations belong in `walkthrough.md`.

## Git Interaction Policy

JAIBA does not prescribe a versioning strategy. Within this skill:

- **At the end of every executed phase**, suggest `chore(wip): <phase
  name>` and let the developer decide. No autonomous commits.
- **At `summarize`**, propose a conventional-commit message inferred
  from the work's nature — the natural squash target for the phase-wise
  WIP commits.
- **If the developer asks you to run a git command — do it.** The
  no-autonomous-commits rule means "don't act unasked", not "refuse
  git".

## Asking the Human

- One topic per question; 2–4 mutually exclusive options when the
  answer space is closed; plain chat for open-ended rationale.
- Never proceed past the `spec` approval gate while clarification
  questions remain.

## Language

- **This skill's source** (SKILL.md, references, templates) — English.
- **Executive artifacts** (PRD, plan, tasks, walkthrough) — the
  language the developer is using in the session.
- **The constitutive `log-entry`** written at `summarize` — **English,
  always** (long-term memory). Translate the essence; don't paste a
  non-English summary into the brain.

## Hand-off Between Phases

- `propose` persists nothing; its landed requirement flows into `spec`
  **in the same conversation**.
- `spec` ends only at the developer's explicit approval of the design.
  No approval ⇒ no `tasks`, no code.
- `execute` runs **one phase of the plan at a time**, pausing for
  human review at every boundary.
- `validate` gates `summarize`: criteria unmet ⇒ back to `execute`
  (or the developer explicitly waives, recorded in the summary).
- `summarize` is one step: present the summary, propose ADRs (enacting
  them is `jaiba-init:update-brain`'s job), verify archive, then selectively
  clear the resolved context — with explicit confirmation before cleanup.
  Filesystem paths/scripts are not external operations; contract closure
  guarantees must be established before claiming safe cleanup.

## Common failure modes

- **Running the chain inside the host's native plan mode.** The spec
  phase can't write; exit native plan mode first.
- **Producing a PRD for a bump.** Triage exists so depth matches blast
  radius — don't over-formalize mechanical work.
- **Skipping the approval gate.** "Files written" is not "approved".
- **Stacking plan phases in one turn**, or chaining
  validate + summarize + archive without the human seeing the summary.
- **Writing constitutive memory directly.** Only `summarize` has the
  append-log exception for closure. Constitution/ADR/reference changes are proposals for
  `jaiba-init:update-brain`.
