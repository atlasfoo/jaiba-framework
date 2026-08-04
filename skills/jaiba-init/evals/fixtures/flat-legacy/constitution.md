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

- **Project name:** Orders API
- **Description:** ASP.NET Core 8 Web API that owns the order
  lifecycle for the e-commerce platform — creation, status
  transitions, and fulfillment — and delegates payment capture to an
  upstream Payments API.
- **Status:** production

## 2. How

- **Architecture style:** Layered (Api / Application / Domain / Infrastructure)
- **Primary language:** C# / .NET 8
- **Primary framework:** ASP.NET Core 8 Web API
- **Persistence:** PostgreSQL via Entity Framework Core (EFCore.Npgsql)
- **Key packages:** EFCore.Npgsql, MediatR, Serilog

> The complete dependency map lives in `Orders.csproj` and the
> integration map lives in `.ai/memory/reference-index.md`. Do not
> duplicate them here.

## 3. Why

- **Business objective:** Provide the order-management backend for
  the e-commerce platform — create, track, and fulfill customer
  orders — while delegating payment capture to the upstream Payments
  API.
- **Position in the bigger picture:** One of several backend services
  behind the e-commerce platform; owns the order lifecycle end to
  end. The rest of the platform's topology beyond the Payments API
  boundary is not evident from the repository.

## 4. With Whom

> Every entry should also exist in `reference-index.md` with access
> details (how to consult, endpoints, credentials location). This
> section is a high-level inventory; the index is the operational map.

- **Upstream** (services this project consumes):
  - Payments API — external payment processor, called via a typed
    HttpClient; its OpenAPI contract is vendored at
    `docs/openapi/payments-v2.yaml`.
- **Downstream** (consumers of this project):
  - [MISSING] — no caller registry, consumer contract, or
    API-consumer documentation was found in the repository; ask the
    maintainer which services or clients consume Orders API.
- **Infrastructure dependencies:**
  - PostgreSQL (via EFCore.Npgsql).

## 5. Scope

What belongs inside this project, and what does not.

- **In scope:**
  - Order domain logic (creation, status transitions, fulfillment)
  - REST API surface (Api layer)
  - Payment capture orchestration via the Payments API (Application layer)
  - Persistence of orders (Infrastructure layer, PostgreSQL)
- **Out of scope:**
  - Payment authorization and settlement itself (owned by the
    upstream Payments API)
  - Any UI or client application (this project is API-only)
- **Cross-cutting packages:**
  - None. Single-project layered solution, not a monorepo.

### 5.1 Sub-unit scope

Single unit.

## 6. Quality Gate

The Quality Gate is split into two tiers run at different points in the
workflow. This project has no scriptfile — `.github/workflows/ci.yml`
is the only place commands live, so both tiers read their commands
from there.

### Phase Gate (runs after each phase — must be fast)

A phase is **not done** until all of these pass. If any fails, fix it
atomically before moving on.

- **Tests (affected):** `dotnet test` (per `.github/workflows/ci.yml`;
  the pipeline does not scope by affected module, so this runs the
  full suite).

> Linting, type checking and formatting have no dedicated step in CI
> and no scriptfile documents them — omitted rather than invented.

### Plan Gate (runs once at `conduct:validate` — may be slow)

A plan is **not done** until all of these pass. Failures block the
summary and require corrective action before closing.

- **Full test suite:** `dotnet test`
- **Security scan:** `snyk test` (per `.github/workflows/ci.yml`)

> Coverage and a dedicated build step are not configured in CI beyond
> the Dockerfile — omitted rather than invented.

## 7. Planning Conventions

How plans and specs are structured for this project. The `conduct`
skill reads this section to decide phase structure and task ordering.

- **TDD mode:** `enabled`

  Set to `enabled` (default) or `disabled`. When `enabled`, plans are
  structured red → green → refactor: every implementation task is
  preceded by a failing-test task **within the same phase**. When
  `disabled`, tests are scheduled at the team's discretion (typically
  as a dedicated phase). Opting out should be a deliberate, documented
  choice — coverage-chasing after the fact tends to produce
  confabulated tests that pass for the wrong reasons.

- **Atomicity granularity:** One user story per plan; one task per commit.

- **Phase structure:** Phases group tasks by **architectural
  cohesion**, not by chronology. Each phase declares its dependencies
  on prior phases and must leave the codebase reversible and
  buildable on completion. The default `conduct:execute` flow pauses
  at every phase boundary for human review.

- **Git strategy (suggestion, not enforcement):** The `conduct`
  skill suggests a `chore(wip): <phase>` message at each phase
  boundary and a conventional-commit message at plan close. The
  developer chooses what to do with those suggestions — squash, merge,
  or commit phase by phase. Default: the agent suggests both options
  at close and the developer picks.

- **Definition of ready** (before a plan enters `execute` mode):
  - Plan is written to `.ai/work/plan.md`
  - Tasks are decomposed in `.ai/work/tasks.md`
  - All clarifying questions have been resolved (no
    `[NEEDS CLARIFICATION]` blocks in the artifacts)
  - Human has explicitly approved the plan

## 8. Style and Syntax

Granular code style (naming, formatting, lint rules, language idioms)
is delegated to the project's style and lint configuration files
(e.g., `.editorconfig`). The agent must read and obey those.

For non-trivial design decisions, document the *why* in code comments
and propose an entry in `.ai/memory/adr-log.md` when the decision is
structural.
