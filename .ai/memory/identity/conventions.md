---
type: convention
title: "Conventions"
description: "TDD disabled by default (no test suite exists); phase-wise chore(wip) commits; style deferred to .editorconfig."
tags: [identity, convention, planning, style]
updated: "2026-08-03"
---

# Conventions

> **Meta-instruction for the agent:** this concept is the authority on
> **how work is shaped for this project** — planning conventions and
> where code style is defined. `conduct` reads it to decide phase
> structure and task ordering. It is one concept read as a unit; it does
> not define what "done" means (`quality-gate`).

## Planning conventions

- **TDD mode:** `disabled`

  Explicit, not a default left unfilled: this repo has no test runner
  (its deliverable is Markdown skill definitions), so there is no
  "failing test" step to precede implementation. The analog `conduct`
  uses instead is a dedicated verification phase/task per plan
  (evals-fixture checks, real probe runs, dual-layout regression) —
  established practice since SPEC-02b, not a gap. See
  [quality-gate.md](quality-gate.md).

- **Atomicity granularity:** One task (`T-NNN`) per unit of work in
  `tasks.md`; not strictly one task per commit — phase-wise commits
  (below) are the norm.

- **Phase structure:** Phases group tasks by **architectural cohesion**,
  not chronology. Each phase declares its dependencies on prior phases
  and must leave the repository reversible and consistent on
  completion. `conduct:execute` pauses at every phase boundary for
  human review.

- **Git strategy:** Phase-wise `chore(wip): <phase>` commits at each
  phase boundary, suggested by `conduct:execute`; the developer decides
  whether to commit as suggested. At plan close, `conduct:summarize`
  proposes a conventional-commit message as the natural squash target
  — squashing is optional, the phase-wise history already reads
  cleanly on its own (established practice: see the `Suggested final
  commit` sections in
  [`.ai/memory/log/2026-07-03-orquestador-unificado-memoria.md`](../log/2026-07-03-orquestador-unificado-memoria.md)
  and
  [`.ai/memory/log/2026-07-28-spec-02b-atl-completo.md`](../log/2026-07-28-spec-02b-atl-completo.md)).

- **Definition of ready** (before a plan enters `execute` mode):
  - Plan is written to `.ai/work/plan.md`.
  - Tasks are decomposed in `.ai/work/tasks.md`.
  - All clarifying questions have been resolved (no
    `[NEEDS CLARIFICATION]` blocks in the artifacts).
  - Human has explicitly approved the plan.

## Communication style

- **Token efficiency:** use the `caveman` skill (ultra-compressed
  communication mode) for session communication in this repo. Carried
  forward from the pre-OKF `AGENTS.md` (§6, retired by
  [ADR-001](../decisions/001-jaiba-brain-adoption.md)'s follow-up) —
  a real, standing preference, not a default this bundle invented.

## Style and syntax

Granular style — Markdown conventions, YAML frontmatter formatting,
shell-script style — is delegated to
[`.editorconfig`](../../../.editorconfig) at the repo root. Read and
obey it; it is the source of truth, and restating its rules here only
creates drift. There is no linter/formatter beyond it (no ESLint,
Ruff, Prettier config exists — this is not `[MISSING]`, the project
genuinely has none).

For non-trivial design decisions, document the *why* in the relevant
skill's prose (references/SKILL.md), and when the decision is
structural, **propose a `decision` concept** for the human to accept —
see [`decisions/`](../decisions/).
