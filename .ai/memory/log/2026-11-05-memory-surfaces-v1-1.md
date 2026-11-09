---
type: log-entry
date: 2026-11-08
slug: memory-surfaces-v1-1
kind: work-closure
depth: spec
adr: ADR-014
---

# Pluggable memory surfaces v1.1 — portable, efficient, readable, and traceless

> The work-closure entry for `.ai/memory/log/` — drafted in
> `.ai/work/` by `conduct:summarize`, moved by
> `scripts/archive.sh`. **English, always** (long-term memory).
> Concise: one screen. The walkthrough was the narrative; this is the
> record. Follows the log-entry contract owned by `jaiba-init`
> (`log-entry-template.md`): append-only once archived — corrections
> are new entries.

## What happened

Evolved `jaiba-memory-surface` from 1.0.0 to **1.1.0** (additive, minor), delivering four core capabilities: package conformance decoupled from session readiness with portable v2 bindings and Step 0 Binding-First discovery; two backend archetypes (`document-tree` and `record-store`) with an executive journal enabling $O(\delta)$ mutations via the `patch` operation; self-contained Python 3 stdlib helper scripts with an Efficiency Gate and `upgrade/repair` mode in `create-memory`, alongside reference protocol `JAIBA4` in `jaiba-engram-memory`; and fully traceless onboarding/migration with a single cutover gate and Issue #17 enhancements (C0–C6) in `jaiba-init`.

## Criteria delivered

- `MSV-001` — Conformidad certificada una vez, válida en todos los agentes — delivered
- `MSV-002` — Binding agnóstico de agente en ruta estándar — delivered
- `MSV-003` — Instalación multi-host de superficies — delivered
- `MSV-004` — Arquetipos de superficie document-tree y record-store — delivered
- `MSV-005` — Executive journal base más deltas en record-store — delivered
- `MSV-006` — Scripts stdlib Python en paquetes de superficie — delivered
- `MSV-007` — Efficiency gate en la conformidad — delivered
- `MSV-008` — Lectura determinista y legible de artefactos JAIBA en sesión — delivered
- `MSV-009` — Modo upgrade/repair en create-memory — delivered
- `MSV-010` — jaiba-engram-memory con protocolo JAIBA4 — delivered
- `MSV-011` — Migración a traceless con un único gate de corte — delivered
- `MSV-012` — Vincular o inicializar en modo traceless sin archivos en el repo — delivered
- `MSV-013` — Verificación agrupada de creaciones independientes en initialize externo — delivered
- `MSV-014` — Una sola ronda de decisiones con inventario mínimo opcional y costo visible — delivered
- `MSV-015` — Namespace sugerido para repos hermanos — delivered
- `MSV-016` — Referencias agrupadas para consumidores sin contrato localizable — delivered
- `MSV-017` — conduct consciente de los límites de la superficie — delivered

## Phases executed

| # | Theme | Notable result |
|---|---|---|
| 1 | Contrato 1.1.0, arquetipos y portabilidad | Normative `executive-journal.md`, contract 1.1.0 with `patch`, binding v2 format, and lockstep global contract sync (360 lines). |
| 2 | Fábrica `create-memory` | Pure Python 3 stdlib scripts (`agent-relay` and local transports), normative Efficiency Gate, 5-step `upgrade/repair` mode, and multi-host installation. |
| 3 | Adaptador `jaiba-engram-memory` JAIBA4 | Executable helper CLI `jaiba_engram.py` (9 canonical subcommands), protocol `jaiba-engram-storage/4`, strict legacy read-only decode for JAIBA3, and verified conformance record. |
| 4 | Consumidores (`conduct`, `ask`, `fast`, `doctor`) | Limit-aware budgeting without chunking (`MSV-017`), $O(\delta)$ SDD patch workflows, deterministic rendering (`render` without search), and traceless `.atl/` exclusion in `git info/exclude`. |
| 5 | `jaiba-init` modo traceless e Issue #17 | Zero-repo-file onboarding, single questionnaire $\le 4$ questions (C3), sibling namespace detection (C4), C0 grouped verification, C1/C5-C6 minimal inventory with cost disclosure, C2 downstream stubs, continuous migration with single cutover gate (`MSV-011`), and plan amendment T-020 (Step 0 Binding-First discovery). |
| 6 | Evals, fixtures y documentación | 12/12 static checks in `run_jaiba4_static.py`, AST validator `validate_scripts_ast.py`, 7 new evals in `create-memory`, expanded consumer evals, and comprehensive `README.md` update. |

## Decisions and deviations

- **Step 0 Binding-First discovery (T-020)**: To eliminate LLM token waste and false "uninstrumented" warnings in traceless repos, agents check `~/.jaiba/memory/bindings/<sha256(canonical-work-root)>.yaml` before testing local `.ai/`. If present, the binding governs unless an explicit `AGENTS.md` override pin exists.
- **Portability decoupling**: Conformance certification is a property of the adapter package and backend protocol, portable across all agent hosts. Certifying host is recorded as provenance only.
- **Pure Python 3 stdlib scripts**: Allowed official package scripts without external pip dependencies or drivers. `agent-relay` mode prepares MCP tool arguments without direct I/O, while local modes perform direct I/O without token passing.
- **Efficiency Gate**: Monolithic full-object overwrites on `record-store` during executive drafting or task updates are graded `NONCONFORMING`.
- **Single cutover gate (`MSV-011`)**: Migration executes continuously; cutover presents a single questionnaire with two separate decisions (activate target and retire source).

## ADR proposals & brain updates

- **Proposed [ADR-014](../decisions/014-pluggable-memory-surfaces-v1-1-architecture.md)**: Pluggable Memory Surfaces v1.1 Architecture (Archetypes, Executive Journal, Portable Bindings, and Traceless Onboarding). Promotes contract 1.1.0, archetypes, $O(\delta)$ deltas, pure stdlib scripts, binding v2, Step 0 Binding-First discovery, and traceless onboarding.
- **Scope drift update in [identity/scope.md](../identity/scope.md)**: Explicitly list `create-memory` and `jaiba-engram-memory` as core framework and first-party reference adapter components.
- Enactment of these proposals is handed off to `jaiba-init:update-brain`.

## Pointers

- Plan: `.ai/work/plan.md` (slug `memory-surfaces-v1-1`)
- PRD: `.ai/work/PRD.md` (criteria `MSV-001`..`MSV-017`)
- Tasks & Walkthrough: `.ai/work/tasks.md`, `.ai/work/walkthrough.md`
- Related log entries: [2026-10-16-memory-surfaces.md](2026-10-16-memory-surfaces.md), [ADR-013](../decisions/013-pluggable-memory-surfaces-architecture.md)

## Suggested final commit

```
feat(memory-surfaces): release jaiba-memory-surface 1.1.0 and traceless workflows

Evolve jaiba-memory-surface to 1.1.0:
- Add document-tree and record-store archetypes and executive journal with O(delta) patch operations.
- Add portable binding v2 format with Step 0 Binding-First discovery and project identity reinforcement.
- Authorize Python 3 stdlib package scripts with Efficiency Gate, upgrade/repair mode, and multi-host install.
- Upgrade jaiba-engram-memory to protocol JAIBA4 (jaiba-engram-storage/4) with stdlib helper CLI.
- Add traceless onboarding and migration with single cutover gate and Issue #17 enhancements (C0-C6).
```

## Gate at close

Pass — Plan Gate green repo-wide (eval syntax, bash syntax, awk description limits, contract lockstep, version lockstep v3.3.0, workflow action pinning, injection probe 2 rejected entries, validate_scripts_ast 3/3, and run_jaiba4_static 12/12). 17/17 acceptance criteria delivered. Clean git working tree.

<!-- jaiba-close-v1
contract jaiba-memory-surface 1.0.0
binding filesystem
project jaiba-framework
context default
scope 7ad1c040fcd69c24e48b27520c090b15128eafae
close 2026-11-05-memory-surfaces-v1-1
body 65d3dd397d650f4b8f01e5d39f4dec5673829062
plan.md 558e26a5e42f62841191abaf339da46f3a4cfc7d
tasks.md ef19f35f57b93996a1a9b5686d614ca947e06dea
walkthrough.md 365ba4d81b14b6306d7ec0153e9789cc8b303b34
PRD.md b84519ddbfaee56d1acf3020398387d697ec1167
.gitignore absent
-->
