# Project Constitution

> **For repository maintainers:** Replace every bracketed placeholder
> (`[like this]`) with real project values. Until then, the agent
> should treat placeholders as *to be filled*, not as literal
> requirements, and ask before proceeding.

> **Meta-instruction for the agent:** This document is the authority
> on *project identity, architecture, scope, planning conventions,
> and the Quality Gate*. Read it before any substantive planning or
> implementation. `AGENTS.md` defines your general behavior; this
> file defines what applies to **this project specifically**. On
> conflict over project facts, this document wins.

## 1. What

- **Project name:** [Project Name]
- **Description:** [1–2 lines: what this software does]
- **Status:** [e.g., MVP / production / legacy migration]

## 2. How

- **Architecture style:** [e.g., Hexagonal / Clean / Layered / MVC / Serverless]
- **Primary language:** [e.g., Python 3.12 / TypeScript 5.x]
- **Primary framework:** [e.g., Django 5 / Next.js App Router]
- **Persistence:** [e.g., PostgreSQL via Django ORM / Prisma + MySQL]
- **Key packages:** [List 5–10 packages central to the project,
  beyond framework-default dependencies]

> The complete dependency map lives in the package manifest
> (`pyproject.toml`, `package.json`, `pom.xml`, etc.) and the
> integration map lives in `.ai/memory/reference-index.md`. Do not
> duplicate them here.

## 3. Why

- **Business objective:** [What problem this solves and for whom]
- **Position in the bigger picture:** [If this project is one
  component of a multi-component solution, describe its role and
  what it enables for the rest of the system. Otherwise: "Standalone."]

## 4. With Whom

> Every entry should also exist in `reference-index.md` with access
> details (how to consult, endpoints, credentials location). This
> section is a high-level inventory; the index is the operational map.

- **Upstream** (services this project consumes):
  - [e.g., Central Auth API / Shared PostgreSQL instance / Stripe]
- **Downstream** (consumers of this project):
  - [e.g., Web frontend / Mobile app / Reporting service]
- **Infrastructure dependencies:**
  - [e.g., AWS S3 for media / Redis for cache / SendGrid for email]

## 5. Scope

What belongs inside this project, and what does not.

- **In scope:**
  - [e.g., Itinerary domain logic, collaborator management, REST API]
- **Out of scope:**
  - [e.g., Authentication (delegated to upstream Auth service),
    payment processing (handled by Stripe), email delivery (SendGrid)]
- **Cross-cutting packages:**
  - [If the project lives in a monorepo or shares packages across
    services, list them here, e.g., `@org/logger`, `@org/ui-components`.
    Otherwise: "None."]

## 6. Quality Gate

The Quality Gate is split into two tiers run at different points in the
workflow. Both tiers read their commands from the repository's scriptfile
(`justfile`, `Makefile`, `package.json` scripts, `pyproject.toml [tool.*]`,
etc.) or `README.md`. If neither documents the commands, **stop and ask
the maintainer to add them** — do not invent commands from memory.

### Phase Gate (runs after each phase — must be fast)

A phase is **not done** until all of these pass. If any fails, fix it
atomically before moving on.

- **Tests (affected):** [e.g., Run only the tests for changed modules.]
- **Linting:** [Zero errors, zero warnings.]
- **Type checking:** [Zero errors from the project's type checker.]
- **Formatting:** [Code conforms to the project's formatter; no diffs.]

### Plan Gate (runs once at `planning:summarize` — may be slow)

A plan is **not done** until all of these pass. Failures block the summary
and require corrective action before closing.

- **Full test suite:** [All tests pass, including integration and e2e.]
- **Coverage:** [e.g., ≥ 85% on new business logic.]
- **Build:** [Production build succeeds.]
- **Security scan:** [e.g., Zero critical issues from SonarQube. Omit if not configured.]

## 7. Planning Conventions

How plans and specs are structured for this project. The `planning`
skill reads this section to decide phase structure and task ordering.

- **TDD mode:** `enabled`

  Set to `enabled` (default) or `disabled`. When `enabled`, plans are
  structured red → green → refactor: every implementation task is
  preceded by a failing-test task **within the same phase**. When
  `disabled`, tests are scheduled at the team's discretion (typically
  as a dedicated phase). Opting out should be a deliberate, documented
  choice — coverage-chasing after the fact tends to produce
  confabulated tests that pass for the wrong reasons.

- **Atomicity granularity:** [e.g., One user story per plan; one task
  per commit. Adjust to project norms.]

- **Phase structure:** Phases group tasks by **architectural
  cohesion**, not by chronology. Each phase declares its dependencies
  on prior phases and must leave the codebase reversible and
  buildable on completion. The default `planning:execute` flow pauses
  at every phase boundary for human review.

- **Git strategy (suggestion, not enforcement):** The `planning`
  skill suggests a `chore(wip): <phase>` message at each phase
  boundary and a conventional-commit message at plan close. The
  developer chooses what to do with those suggestions — squash, merge,
  or commit phase by phase. Document the team's preferred flow here
  if it should bias the agent's suggestions:
  - [e.g., "Phase-wise `chore(wip)` commits, squashed at plan close
    with the suggested conventional-commit message." OR "Single
    commit at plan close." OR "Per-task commits." Default: agent
    suggests both options at close and the developer picks.]

- **Definition of ready** (before a plan enters `execute` mode):
  - Plan is written to `.ai/session/plan.md`
  - Tasks are decomposed in `.ai/session/tasks.md`
  - All clarifying questions have been resolved (no
    `[NEEDS CLARIFICATION]` blocks in the artifacts)
  - Human has explicitly approved the plan

## 8. Style and Syntax

Granular code style (naming, formatting, lint rules, language idioms)
is delegated to the project's style and lint configuration files
(e.g., `.editorconfig`, `eslint.config.js`, `ruff.toml`, `pyproject.toml`
`[tool.ruff]`, `.prettierrc`). The agent must read and obey those.

For non-trivial design decisions, document the *why* in code comments
and propose an entry in `.ai/memory/adr-log.md` when the decision is
structural.
