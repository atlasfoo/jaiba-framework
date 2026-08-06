---
type: convention                                  # mandatory — exact value, never change
title: "Conventions"                              # recommended — human-readable name
description: "[one line: how plans are structured and where code style is defined for this project]" # recommended — this is what index.md shows
tags: [identity, convention, planning, style]     # recommended — list, for grouping and search
updated: "[YYYY-MM-DD]"                           # recommended — last substantive change
---

# Conventions

> **For repository maintainers:** replace every bracketed placeholder
> (`[like this]`) with the team's real norms. Defaults are stated where
> one exists — keeping a default is a valid answer, but state it
> explicitly rather than leaving the bracket.

> **Meta-instruction for the agent:** this concept is the authority on
> **how work is shaped for this project** — planning conventions and
> where code style is defined. `conduct` reads it to decide phase
> structure and task ordering. It is one concept read as a unit; it does
> not define what "done" means (`quality-gate`).

## Planning conventions

- **TDD mode:** `enabled`

  Set to `enabled` (default) or `disabled`. When `enabled`, plans are
  structured red → green → refactor: every implementation task is
  preceded by a failing-test task **within the same phase**. When
  `disabled`, tests are scheduled at the team's discretion (typically as
  a dedicated phase). Opting out should be a deliberate, documented
  choice — coverage-chasing after the fact tends to produce confabulated
  tests that pass for the wrong reasons.

- **Atomicity granularity:** [e.g., One user story per plan; one task per
  commit. Adjust to project norms.]

- **Phase structure:** Phases group tasks by **architectural cohesion**,
  not by chronology. Each phase declares its dependencies on prior phases
  and must leave the codebase reversible and buildable on completion. The
  default `conduct:execute` flow pauses at every phase boundary for human
  review.

- **Git strategy (suggestion, not enforcement):** `conduct` suggests a
  `chore(wip): <phase>` message at each phase boundary and a
  conventional-commit message at plan close. The developer chooses what
  to do with those suggestions — squash, merge, or commit phase by phase.
  Document the team's preferred flow here if it should bias the agent's
  suggestions:
  - [e.g., "Phase-wise `chore(wip)` commits, squashed at plan close with
    the suggested conventional-commit message." OR "Single commit at plan
    close." OR "Per-task commits." Default: the agent suggests both
    options at close and the developer picks.]

- **Definition of ready** (before a plan enters `execute` mode):
  - Plan is written to `.ai/work/plan.md`
  - Tasks are decomposed in `.ai/work/tasks.md`
  - All clarifying questions have been resolved (no
    `[NEEDS CLARIFICATION]` blocks in the artifacts)
  - Human has explicitly approved the plan

## Style and syntax

Granular code style — naming, formatting, lint rules, language idioms —
is delegated to the project's own style and lint configuration
(`.editorconfig`, `eslint.config.js`, `ruff.toml`, `pyproject.toml`
`[tool.ruff]`, `.prettierrc`, …). Read and obey those files; they are the
source of truth, and restating their rules here only creates drift.

For non-trivial design decisions, document the *why* in code comments,
and when the decision is structural, **propose a `decision` concept** for
the human to accept.
