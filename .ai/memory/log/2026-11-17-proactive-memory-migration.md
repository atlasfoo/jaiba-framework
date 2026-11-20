---
type: log-entry
date: 2026-11-17
slug: proactive-memory-migration
kind: work-closure
depth: spec
adr: ADR-019 (Proposed)
---

# Proactive 3-level memory migration, onboarding guards, and daily version check

## What happened

Implemented the active 3-level memory model (Level 1 flat, Level 2 unbound OKF, Level 3 bound surface or `filesystem` with `AGENTS.md` pin + `~/.jaiba` `v2` binding) across the global contract, `create-memory`, `jaiba-init`, `conduct`, `ask`, `fast`, `doctor`, `jaiba-configure`, subagent definitions, `README.md`, and `evals.json`. Added non-blocking Notice 1 (very high urgency) and Notice 2 (medium urgency) on every response, silent `v2` binding auto-generation over OKF + `filesystem` pin, chained `v1 → v2 → v3` migration and `v3` bootstrap in `jaiba-init`, explicit traceless shareability warnings, automatic `jaiba-doctor` execution on new `jaiba-init` bootstrap, pre-planning `jaiba-init` suggestion in native plan mode on uninstrumented repos, one-time first-turn `jaiba-init` suggestion in unorchestrated sessions, and a daily per-project framework version freshness check in `.atl/framework-version.json`.

## Criteria delivered

- `MMIG-001` — Aviso 1 de urgencia muy alta en cada respuesta para memoria v1 (layout flat en filesystem) — delivered
- `MMIG-002` — Aviso 2 de urgencia media en cada respuesta para memoria v2 (OKF en filesystem sin binding/pin v3) — delivered
- `MMIG-003` — Auto-generación silenciosa del binding v2 en `~/.jaiba` cuando `AGENTS.md` ya tiene el pin `filesystem` — delivered
- `MMIG-004` — Flujo secuencial guiado en `jaiba-init` (v1 flat → v2 OKF → v3 superficie o fijación filesystem) y bootstrap v3 — delivered
- `MMIG-005` — Advertencia explícita sobre la no garantía de compartibilidad del cerebro en modo traceless — delivered
- `MMIG-006` — Diagnóstico de niveles de memoria en `jaiba-doctor` y eliminación de cláusulas pasivas en contrato y skills — delivered
- `MMIG-007` — Ejecución automática de `jaiba-doctor` al completar un `jaiba-init` nuevo (bootstrap) — delivered
- `MMIG-008` — Sugerencia de orquestación previa con `jaiba-init` antes de planear en modo plan nativo en proyectos no instrumentados — delivered
- `MMIG-009` — Sugerencia no bloqueante de orquestar con `jaiba-init` en el primer mensaje de sesión de un proyecto no orquestado — delivered
- `MMIG-010` — Chequeo diario por proyecto de nueva versión disponible del framework JAIBA — delivered

## Phases executed

| # | Theme | Notable result |
|---|---|---|
| 1 | Global contract & surface resolution | Lockstep `jaiba-contract.md` + `create-memory` 3-level rules, `filesystem` `v2` binding schema, silent auto-generation, traceless warning |
| 2 | `jaiba-init` v3 bootstrap & chained migration | `assets/AGENTS.md` `filesystem` pin + `v2` binding persistence, Step 9 v3 transition, automatic `jaiba-doctor` on bootstrap |
| 3 | Consumers, diagnostics, agents & docs | `conduct`, `ask`, `fast`, `doctor` `⚠️ Degraded` findings, subagents, `README.md`, native-plan & first-turn unorchestrated guards |
| 4 | Evals, fixtures & Plan Gate | Updated 6 `evals.json` + `layout-legacy.json`; `verify` confirmed 9/9 met; fixed minor duplicated text in 3 agent defs |
| 5 | Daily per-project version check | Added 24h `.atl/framework-version.json` check (§6), strict semver §4.5 validation, fail-soft offline, eval id `18`; `verify` confirmed `MMIG-010` met |

## Decisions and deviations

- Preserved `UNBD-001` boundary: cancelling `migrate-surface` on `filesystem-unbound` still writes no `filesystem` `v2` binding as a side effect.
- Blocked `migrate-surface` in `migrate-mode.md` / `surface-migration.md` if the user deferred deleting the flat trio (`index.md` + `constitution.md` ambiguous state).
- Added 4 plan amendments (`MMIG-007` through `MMIG-010`) during spec/post-validate review.
- Subagent executors (`executor-high`, `executor-medium`, `executor-low`) lacked write/shell tools in this host runtime, so `T-001`–`T-014` executed inline sequentially while `verify` (`575d978e-1f12-4e08-a25a-15fabd1541ba`, `617b93fd-5704-4d1d-925f-17ec3e284868`) performed read-only criteria verification.

## ADR proposals & brain updates

- **Proposed `ADR-019` (`status: Proposed`) — Proactive 3-level memory migration, onboarding guards, and daily version check:**
  - *Context:* [ADR-008](../decisions/008-okf-pattern-brain-serialization.md) and [ADR-013](../decisions/013-pluggable-memory-surfaces-architecture.md) previously treated flat v1 and unbound OKF v2 as warning-free, [ADR-015](../decisions/015-native-plan-input.md) did not guard uninstrumented repos before native planning, new `jaiba-init` bootstraps ended in a passive `jaiba-doctor` hand-off, and no daily framework version check existed.
  - *Decision:* Enforce active non-blocking migration notices (Notice 1 for v1 flat, Notice 2 for v2 unbound OKF), silent `v2` binding auto-generation on OKF + `AGENTS.md` `filesystem` pin, chained `v1 → v2 → v3` flow in `jaiba-init`, traceless shareability warnings, automatic `jaiba-doctor` on new bootstrap, pre-planning & first-turn `jaiba-init` suggestions on unorchestrated repos, and a fail-soft 24h per-project version check in `.atl/framework-version.json` under strict §4.5 semver validation.
  - *Consequences:* Projects stay readable losslessly while consistently nudging toward Level 3 (`v3`) and keeping toolchain/version state gitignored in `.atl/`. Enactment belongs to `jaiba-init:update-brain`.

## Pointers

- References: [quality-gate.md](../identity/quality-gate.md), [okf-v0-1.md](../references/okf-v0-1.md), [engram-mcp.md](../references/engram-mcp.md), [ADR-008](../decisions/008-okf-pattern-brain-serialization.md), [ADR-013](../decisions/013-pluggable-memory-surfaces-architecture.md), [ADR-014](../decisions/014-pluggable-memory-surfaces-v1-1-architecture.md), [ADR-015](../decisions/015-native-plan-input.md).
- Prior WIP commit on branch `fix/memory-migration`: `47d669d`.

## Suggested final commit

```
feat(memory): enforce 3-level migration notices, onboarding guards, and daily version check

Add proactive v1/v2 migration notices, silent filesystem v2 binding
auto-generation, chained v1->v2->v3 jaiba-init flow with automatic
jaiba-doctor execution, traceless shareability warnings, unorchestrated
session/native-plan guards, and a 24h per-project version check in .atl/.
```

## Gate at close

Pass | Verified after final edit: `jq empty`, `bash -n`, `description <= 1024`, `diff -q --strip-trailing-cr` on `jaiba-contract.md`, version lockstep (`3.5.0`), SHA-pinned actions, injection fixture (`2` rejected).

<!-- jaiba-close-v1
contract jaiba-memory-surface 1.0.0
binding filesystem
project github.com/atlasfoo/jaiba-framework
context default
scope cce572e7d57de15ca64adb292c7f3218fa9ddb77
close 2026-11-17-proactive-memory-migration
body 5e67537295e95591b3925f85c1bc4e1084886035
plan.md b1dc79726154c3ac7e6f090cfdba3cb3e6071ab8
tasks.md 51b8602ac36a5adde1ab7259cebf41e8da999aad
walkthrough.md 7efcca4171fafebaefebc717475ccfe6fcd52f04
PRD.md 9a72a16a7976ec566247530fb5399685a75904d5
.gitignore absent
-->
