---
name: conduct
description: >-
  Unified Spec-Driven-Development chain of the JAIBA framework — the single entry point that routes any development request to the right depth and phase. SDD chain: propose (shape a fuzzy requirement) → spec (PRD only when triage demands it + design/plan.md, human approval gate) → tasks (T-NNN task graph) → execute (implicit, phase by phase) → validate (quality gate + acceptance criteria) → summarize (archive to `.ai/memory/log/`, clean `.ai/work/`). Trigger implicitly when the developer describes work to plan or build, formalizes a requirement ("let's plan", "let's spec this", "write a PRD", "we need a feature that…"), or sends a continuation cue ("continue", "next", "go") while `.ai/work/plan.md` exists. Trigger explicitly on "/conduct [phase]" as deterministic override when routing fails or to force a phase (e.g. "/conduct summarize"). NOT the host agent's native plan mode — it writes artifacts under `.ai/work/` and needs file-write access; never run it inside a read-only plan mode.
version: 2.0.0
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
`PRD.md` and `plan.md` to `.ai/work/`, which a read-only native mode
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

While `.ai/work/plan.md` exists, every developer message routes down
one of three lanes:

| The message is… | Lane |
|---|---|
| A **continuation cue** — "continue", "next", "go", "keep going", an answer to your pending question | `execute` (this skill) |
| A **question** — asking, not asking-for-change | `ask` skill (read-only; it yields back here) |
| A **change request** outside the plan's current tasks | `fast` skill (it runs the shared triage; a contained change is done out-of-band, a big one is surfaced to fold into the plan or re-plan) |

When no work is active, a question still goes to `ask`; a change
request enters this chain through triage.

## Brain Discovery and Validation

This skill can be installed per-project (`.claude/skills/`,
`.agents/skills/`) or **globally** (e.g. `~/.claude/skills/`), shared
across every repository you work in. Either way, "the brain" means
`.ai/` and `AGENTS.md` at the root of the **project you're currently
in** — where `.git/` lives — never a path relative to this skill's own
installation location.

Before selecting a phase, confirm the project is JAIBA-instrumented:

1. **`AGENTS.md` exists at the project root, is non-empty, and is the
   JAIBA behavioral contract** (or points to the global JAIBA contract
   installed in the agent's config). An `AGENTS.md` that exists but is
   unrelated doesn't count.
2. **`.ai/memory/constitution.md`, `adr-log.md`, and
   `reference-index.md` exist and hold real content** — not the bare
   `[bracket]` templates.

If either check fails, **stop here** — do not enter any phase or write
to `.ai/work/`. An orphaned plan with no constitution to ground it
helps no one. Route instead:

- No `.ai/` at all → `jaiba-scaffold`.
- `.ai/` exists but `.ai/memory/` is bare templates → `update-brain`
  in `initialize` mode.
- `AGENTS.md` missing or not the JAIBA contract → `jaiba-scaffold`.

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

Decide the phase **before** reading anything else. If the message is
ambiguous, ask the developer instead of guessing.

| Situation | Phase | Read |
|---|---|---|
| Requirement is fuzzy/exploratory; developer wants help shaping it ("help me think through…", "I'm not sure how this should work") | `propose` | `references/propose-mode.md` |
| Requirement is clear (or just landed in `propose`), no active `plan.md`, developer wants it specced/planned | `spec` | `references/triage.md`, then `references/spec-mode.md` |
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
governs it: delegable operations, the pre-invocation toolchain check,
and the concurrency policy. Delegation is optional by construction:
every phase has an inline sequential fallback.

## Context Loading

Load per phase — not universally — to minimize tokens.

- **`propose` / `spec`** (full context): `AGENTS.md` (or global
  contract), `constitution.md` (scope, Quality Gate §6, TDD mode §7,
  sub-unit scope §5.1), `reference-index.md` (integrations touched),
  `adr-log.md` (standing decisions), recent `.ai/memory/log/` entries
  (what was tried before), and the code the requirement plausibly
  touches.
- **`tasks`**: the approved `plan.md` (+ `PRD.md` if produced), plus
  `constitution.md` §6/§7 to copy gate commands and TDD posture into
  `tasks.md`.
- **`execute`**: `.ai/work/plan.md`, `tasks.md`, `walkthrough.md`
  only. Gate commands and TDD posture were already copied into
  `tasks.md` — the constitution is not re-read.
- **`validate`**: `tasks.md § Gate Commands`, `PRD.md`'s acceptance
  criteria schema (if present), `walkthrough.md`.
- **`summarize`**: everything in `.ai/work/`.

If any read reveals a conflict between the request and recorded
project facts, **flag it before producing artifacts**.

## Artifacts at a Glance

All executive artifacts live in `.ai/work/` (gitignored — phases are
the durable checkpoints, commits carry the code):

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

**Multisession by design.** `.ai/work/` survives between sessions; a
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
- **`.ai/work/` artifacts** (PRD, plan, tasks, walkthrough) — the
  language the developer is using in the session.
- **The `.ai/memory/log/` entry** written at `summarize` — **English,
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
  them is `update-brain`'s job), archive to `.ai/memory/log/`, clean
  `.ai/work/` — with one explicit confirmation before the destructive
  part.

## Common failure modes

- **Running the chain inside the host's native plan mode.** The spec
  phase can't write; exit native plan mode first.
- **Producing a PRD for a bump.** Triage exists so depth matches blast
  radius — don't over-formalize mechanical work.
- **Skipping the approval gate.** "Files written" is not "approved".
- **Stacking plan phases in one turn**, or chaining
  validate + summarize + archive without the human seeing the summary.
- **Writing to `.ai/memory/` directly.** Only the `summarize` step's
  log entry (via `scripts/archive.sh`) touches memory, and only
  `log/`. Constitution/ADR/reference changes are proposals for
  `update-brain`.
