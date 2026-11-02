---
type: log-entry
date: 2026-11-01
slug: memory-surfaces
kind: work-closure
depth: spec
adr: ADR-013
---

# Pluggable memory surfaces architecture and verified adapter protocols

> The work-closure entry for `.ai/memory/log/` — drafted in
> `.ai/work/` by `conduct:summarize`, archived by
> `scripts/archive.sh`. **English, always**. Concise: one screen.

## What happened

Delivered JAIBA SPEC-04 pluggable memory surfaces architecture. Decoupled the canonical logical memory contract (`jaiba-memory-surface/1.0.0`) from empirical backend storage via storage-nature profiles (`storage-nature.md`) and derived physical adapter protocols (`JAIBA3` single-observation envelope for Engram, `posix-file/1` for external file vaults, and directory tree for `filesystem`). Retained `filesystem` as the default surface across concept-bundle and legacy-flat layouts, while verifying lossless cross-surface migrations and fail-closed guards without modifying or activating this repository.

## Criteria delivered

- `MEM-001` — Compatibilidad filesystem — delivered
- `MEM-002` — Generación de una skill memory-surface — delivered
- `MEM-003` — Selección determinista y excepciones — delivered
- `MEM-004` — Identidad y contextos de trabajo — delivered
- `MEM-005` — Modelo lógico íntegro y direccionable — delivered
- `MEM-006` — Workflow externo y bootstrap sin marcador — delivered
- `MEM-007` — Aislamiento de memoria ajena a JAIBA — delivered
- `MEM-008` — Fallos visibles y recuperación segura — delivered
- `MEM-009` — Migración entre cualquier par de superficies — delivered
- `MEM-010` — Archivo verificable y limpieza acotada — delivered
- `MEM-011` — Superficie Engram de referencia — delivered
- `MEM-012` — Diagnóstico y extensibilidad del contrato — delivered
- `MEM-013` — Perfil de naturaleza previo al mapeo — delivered *(corrective)*
- `MEM-014` — Caracterización experimental acotada — delivered *(corrective)*
- `MEM-015` — Representación nativa y complejidad justificada — delivered *(corrective)*
- `MEM-016` — Efectos semánticos separados de conflictos lógicos — delivered *(corrective)*

## Phases executed

| # | Theme | Notable result |
|---|---|---|
| 1–5 | Contract, factory & rehearsal base | Established `create-memory`, canonical contract `1.0.0`, resolution, and test fixtures (`T-001`..`T-027`). |
| 6–12 | Operational adapter & migration baseline | Exercised initial Engram/filesystem interactions; suspended upon discovering fragmentation gaps (`T-029`..`T-046`). |
| 13–13S | Corrective reform & hygiene abstention | Adopted storage-nature procedure, finite experiment bounds; accepted user choice to abstain from mutating protected observations (`T-055`..`T-061`). |
| 14R | JAIBA3 protocol & factory unblock | Defined direct single-observation `JAIBA3` envelope; updated rehearsals without backend calls (`T-083`..`T-085`, `60a4c2b`). |
| 15R | Contrasted profiles & Engram E2E | Characterized profiles; ran live E2E lifecycle with 55 KB chunking (`T-086`..`T-087`, trial `efc16e3a-3764-4ae6-9454-4d9fd8bc7ac0`); promoted `jaiba-engram-memory` as verified opt-in (`6fe0555`). |
| 16R | Second surface & 3-way migration | Generated external `jaiba-vault-memory` (`T-089`); verified lossless 3-way migration (`filesystem ↔ Engram ↔ vault ↔ filesystem`, 37 calls) and fail-closed guards for corrupt chunks and symlink roots (`8d56836`). |
| 17R | Documentation & validation matrix | Aligned `README.md` and `skills/create-memory/`; drafted constitutive proposals (`phase17r-update-brain-proposals.md`); consolidated 4-tier evidence matrix (`phase17r-evidence-matrix.md`) (`1d3a5f2`). |

## Decisions and deviations

- **Accepted global contract deviation:** Retained global contract (`jaiba-contract.md`) at 355 identical lines across configure and doctor assets (exceeding historical ~260 lines) to avoid rule fragmentation across agents ([ADR-013](../decisions/013-pluggable-memory-surfaces-architecture.md)).
- **JAIBA3 single-observation envelope:** Replaced COW/WAL manifest chains with direct JSON+base64+SHA-256 envelope, using chunks only when raw payloads exceed 30,000 bytes.
- **Measured call costs:** `T-087` required 44 native calls (16 mutations) due to fresh-reader verification and single catalogue updates, accepted under the 45-call cap.
- **Vault adapter scope:** `jaiba-vault-memory` (`T-089`) generated outside repo using `posix-file/1`; resides on the same ext4 device as filesystem and is not a separate durability domain.
- **Engram advisory handling:** MCP `judgment_required` notifications treated as advisory metadata without calling `mem_judge*` tools.
- **Disposable migrations:** Multi-hop migrations (`T-090`) conducted in isolated disposable roots (`activation: not-performed`); this repository remains on `filesystem`.

## ADR proposals & brain updates

- **ADR-013 (`status: accepted`):** Pluggable memory surfaces architecture, opt-in `jaiba-engram-memory` adapter, default `filesystem`, and accepted 355-line global contract ([ADR-013](../decisions/013-pluggable-memory-surfaces-architecture.md)).
- **Reference concept `engram-mcp`:** External surface reference documenting verified tools (`mem_current_project`, `mem_save`, `mem_update`, `mem_get_observation`), `JAIBA3` protocol constraints, and advisory conflict notifications ([references/engram-mcp.md](../references/engram-mcp.md)).
- Enacting these proposals into `.ai/memory/` is handed off to `jaiba-init:update-brain`.

## Pointers

- Commits: `60a4c2b` (Phase 14R), `6fe0555` (Phase 15R), `8d56836` (Phase 16R), `1d3a5f2` (Phase 17R).
- Trial artifacts:
  - Phase 15R E2E: `/home/atlasfoo/.local/state/jaiba/trials/memory-surfaces/phase15r-efc16e3a-3764-4ae6-9454-4d9fd8bc7ac0/`
  - Phase 16R Vault & Migrations: `/home/atlasfoo/.local/state/jaiba/trials/memory-surfaces/phase16r-6c90b698-39ba-441e-9c63-35ba9f9055c3/`
  - Phase 17R Evidence Matrix: `/home/atlasfoo/.local/state/jaiba/trials/memory-surfaces/phase17r-evidence-matrix.md`
  - Update-Brain Proposals: `/home/atlasfoo/.local/state/jaiba/trials/memory-surfaces/phase17r-update-brain-proposals.md`
- Quality Gate authority: [../identity/quality-gate.md](../identity/quality-gate.md)

## Suggested final commit

```
feat(memory): pluggable memory surfaces architecture and verified adapter protocols

Delivers SPEC-04 pluggable memory surfaces layer:
- Canonical logical contract 1.0.0 and storage-nature empirical characterization.
- First-party opt-in jaiba-engram-memory adapter using direct JAIBA3 envelope.
- External jaiba-vault-memory adapter generation and lossless 3-way migration.
- Fail-closed guards for corrupt chunks and symlink root traversal.
- Zero-drift preservation of default filesystem memory across bundle and legacy layouts.
```

## Gate at close

Pass — Plan Gate green; 21/21 unittest cases OK; 16/16 criteria delivered; toolchain probe 0 missing of 4; injection probe 2 rejected entries.

<!-- jaiba-close-v1
contract jaiba-memory-surface 1.0.0
binding filesystem
project jaiba-framework
context default
scope 7ad1c040fcd69c24e48b27520c090b15128eafae
close 2026-10-16-memory-surfaces
body 0e586690c510ccd333650e5d400b31a769c6563a
plan.md 7fd6caa8f8727639f475fbfc7e8e1367b6bf02ef
tasks.md bfdb51ff9513295b65b783dd52b917d4b66e4b93
walkthrough.md 29901fb3f8328d827735f5d4c13408e7076ff833
PRD.md 7d77974302f8609cb1b9b48d643104db9ab29ef9
.gitignore absent
-->
