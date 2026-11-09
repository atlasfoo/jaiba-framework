---
type: log-entry
date: 2026-11-08
slug: brain-change-adr-014-surfaces-v1-1
kind: brain-change
---

# Brain change — ADR-014 enacted & scope drift updated

## What changed

- **Created** `.ai/memory/decisions/014-pluggable-memory-surfaces-v1-1-architecture.md` (`status: accepted`): enacts the pluggable memory surfaces v1.1 architecture (archetypes `document-tree` and `record-store`, executive journal $O(\delta)$ `patch` operations, Python 3 stdlib package scripts, Efficiency Gate, `upgrade/repair` mode, portable binding v2 with Step 0 Binding-First discovery, reference protocol `JAIBA4` in `jaiba-engram-memory`, and traceless onboarding).
- **Updated** `.ai/memory/identity/scope.md`: resolved scope drift by explicitly listing `create-memory` and `jaiba-engram-memory` as in-scope core meta and first-party reference adapter components, and updating the sub-units count to nine skills.
- **Updated** `.ai/memory/identity/architecture.md`: documented Python 3 standard library scripts for package helpers, and updated persistence to reflect external pluggable memory surfaces under ADR-013 and ADR-014.
- **Updated** `.ai/memory/references/engram-mcp.md`: updated to protocol `jaiba-engram-storage/4` (`JAIBA4`), `record-store` archetype, and `scripts/jaiba_engram.py` helper CLI in `agent-relay` mode.
- **Updated** `.ai/memory/index.md`: added ADR-014 to the `decision` group, updated `engram-mcp.md` description, and bumped `updated: 2026-11-08`.

## Provenance

Enacted from the proposals in `.ai/memory/log/2026-11-05-memory-surfaces-v1-1.md` (§ ADR proposals & brain updates), produced by `conduct:summarize` at the close of plan `memory-surfaces-v1-1`.

## What was deliberately left untouched

- ADR-013 — not superseded; ADR-014 evolves the memory surfaces architecture to 1.1.0 while preserving the foundational three-tier separation of ADR-013.
- `identity/project.md`, `identity/purpose.md`, `identity/quality-gate.md`, `identity/conventions.md` — no project purpose or quality-gate thresholds changed.
