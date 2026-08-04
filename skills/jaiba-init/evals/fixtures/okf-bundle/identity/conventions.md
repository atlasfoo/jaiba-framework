---
type: convention
title: "Conventions"
description: "Planning follows JAIBA defaults (TDD enabled, phase-cohesive plans); code style is delegated to the project's own lint/format config."
tags: [identity, convention, planning, style]
updated: "2026-06-02"
---

# Conventions

## Planning conventions

- **TDD mode:** `enabled`

  Set to `enabled` (default) or `disabled`. When `enabled`, plans are
  structured red → green → refactor: every implementation task is
  preceded by a failing-test task **within the same phase**. When
  `disabled`, tests are scheduled at the team's discretion (typically as
  a dedicated phase). Opting out should be a deliberate, documented
  choice — coverage-chasing after the fact tends to produce confabulated
  tests that pass for the wrong reasons.

- **Atomicity granularity:** One user story per plan; one task per commit.

- **Phase structure:** Phases group tasks by **architectural cohesion**,
  not by chronology. Each phase declares its dependencies on prior phases
  and must leave the codebase reversible and buildable on completion. The
  default `conduct:execute` flow pauses at every phase boundary for human
  review.

- **Git strategy (suggestion, not enforcement):** `conduct` suggests a
  `chore(wip): <phase>` message at each phase boundary and a
  conventional-commit message at plan close. The developer chooses what
  to do with those suggestions — squash, merge, or commit phase by phase.
  Default: the agent suggests both options at close and the developer
  picks.

- **Definition of ready** (before a plan enters `execute` mode):
  - Plan is written to `.ai/work/plan.md`
  - Tasks are decomposed in `.ai/work/tasks.md`
  - All clarifying questions have been resolved (no
    `[NEEDS CLARIFICATION]` blocks in the artifacts)
  - Human has explicitly approved the plan

## Style and syntax

Granular code style — naming, formatting, lint rules, language idioms
— is delegated to the project's own style and lint configuration
(`.editorconfig`). Read and obey those files; they are the source of
truth, and restating their rules here only creates drift.

For non-trivial design decisions, document the *why* in code comments,
and when the decision is structural, **propose a `decision` concept** for
the human to accept.
