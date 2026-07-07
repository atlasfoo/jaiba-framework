---
slug: orquestador-unificado-memoria
created: 2026-07-03
archived: 2026-07-06
spec: .ai/specs/jaiba-improvement-plan.md § SPEC-01 + SPEC-03 (absorbida)
adr_proposed: ADR-P1, ADR-P2, ADR-P3, ADR-P4
---

# Plan summary: Orquestador unificado + memoria constitutiva/ejecutiva + subagentes

> Concise, archivable. The walkthrough was the narrative; this is the record.

## Outcome

`specification` y `planning` disueltas en una única skill **`orchestrator`**
con cadena SDD (`propose → spec → tasks → execute → validate → summarize`)
y triage por blast radius que decide la profundidad (inline/design/spec —
no todo cambio produce PRD). Memoria reorganizada en dos categorías:
constitutiva (`.ai/memory/` + `log/` append-only) y ejecutiva (`.ai/work/`,
gitignored). Batería de 6 subagentes (3 ejecutores por tier + `code-analyst`,
`business-analyst`, `verify`) con contrato de invocación, oleadas paralelas
por grafo `depends-on` y fallback secuencial. `ask`/`fast` pasan a carriles
implícitos vía regla de ruteo; contrato conductual global instalado una vez
por máquina (`jaiba-contract.md`) con marker mínimo per-repo y drift-check
en `doctor`.

## Spec coverage

- `SPEC-01` (workflow unificado adaptativo) — entregada, criterios `[x]` en el roadmap
- `SPEC-03` (subagentes + paralelismo, absorbida) — entregada; SPEC-02b repuntada a esta entrega

## Phases executed

| # | Theme | Notable result |
|---|---|---|
| 1 | Modelo físico de memoria | `work/` + `memory/log/` append-only; back-constraints SPEC-04/06 en templates |
| 2 | Skill `orchestrator` (rename de `planning`) | Cadena SDD completa, 7 references, PRD con esquema YAML parseable, `archive.sh`; `specification` retirada |
| 3 | `ask`/`fast` implícitas | `user-invocable: false`, triage compartida, plan-adjustment fold/park-and-replan |
| 4 | Batería de subagentes | `subagents.md` (contrato + concurrencia), 6 definiciones nativas, oleadas en execute, `verify` en validate |
| 5 | Contrato conductual global | `jaiba-contract.md` global + marker per-repo; doctor Layer 0 con drift-check lockstep |
| 6 | Coherencia del repo y cierre | AGENTS.md/README/evals/roadmap al modelo nuevo + guía de migración manual |

## Deviations and corrections

- Fases 3 y 4 ejecutadas en paralelo vía subagentes (dependían solo de Phase 2; orden del desarrollador).
- El estado de toolchain real es `.atl/tool-layout.md` (el plan citaba `.ai/tools-state.md`, inexistente).
- Barridos de coherencia fuera de la letra: `ask/orientation.md`, seed ADR-001, ejemplos en scaffold.
- **En summarize (2026-07-06):** el Plan Gate detectó `create-knowledge` aún vinculada a los sockets retirados y ejemplos `planning`/`specification` residuales en scaffold/doctor — re-vinculada al modelo `orchestrator` y barridos; gate re-ejecutado en verde.
- Las copias globales instaladas (`~/.claude/skills/planning`, `specification`) quedan obsoletas — reinstalar tras el merge.

## ADR proposal

Cuatro propuestas (status: Proposed) para cuando `update-brain:initialize` cree el `adr-log.md` de este repo:

1. **Memoria en dos categorías** — constitutiva (`.ai/memory/` curada + `log/` cronológico append-only) vs ejecutiva (`.ai/work/` gitignored). Alternativa descartada: un solo árbol versionado. Consecuencia: `summarize` gana el carve-out de anexar a `log/`.
2. **Orquestador único con cadena SDD y triage por blast radius** — disolución de `specification`/`planning`; profundidad decidida por triage, no por el comando elegido. Consecuencia: un solo punto de entrada, PRD condicional.
3. **Política de tres carriles** — `ask`/`fast` implícitas-only por regla de ruteo; `orchestrator` dual (implícita + override explícito determinista).
4. **Modelo de concurrencia de subagentes** — oleadas por grafo `depends-on`, fan-out ≤3, paralelo solo con archivos disjuntos, single-writer de la ejecutiva, tier de modelo declarativo por alias (sin IDs congelados).

## Suggested final commit

```
feat!: unify spec+planning into orchestrator with SDD chain, two-tier memory and subagent battery

Dissolves specification/planning into a single orchestrator skill
(propose→spec→tasks→execute→validate→summarize) with blast-radius
triage; splits memory into constitutive (.ai/memory/ + append-only
log/) and executive (.ai/work/); adds a 6-agent battery with wave
parallelism; makes ask/fast implicit lanes and globalizes the
behavioral contract (jaiba-contract.md + per-repo marker).

BREAKING CHANGE: skills `specification`/`planning` removed; `.ai/`
layout migrates session/→work/, memory/archive/→memory/log/ (manual
migration guide in README).
```

## Quality gate at close

Pass — 7/7 evals.json válidos; descriptions ≤1024; sin citas huérfanas;
AGENTS.md/README/roadmap consistentes; criterios SPEC-01/SPEC-03
verificados y marcados. (Corregido en summarize: deriva de
create-knowledge/scaffold/doctor, ver Deviations.)
