---
type: reference
title: "Engram MCP external memory surface"
description: "Model Context Protocol interface for persistent memory; provides bounded tool surface for the optional jaiba-engram-memory adapter under the JAIBA4 protocol."
tier: external
kind: service
role: "optional pluggable memory adapter"
resource: "MCP server `mcp:engram` / tools: `mem_current_project`, `mem_save`, `mem_update`, `mem_get_observation`"
tags: [memory, mcp, engram, adapter, surface]
updated: "2026-11-08"
---

# Engram MCP external memory surface

## What it is

Engram is an external Model Context Protocol (MCP) server providing persistent observation-based memory storage across coding sessions. It exposes tools for saving observations, querying project context, and managing observation metadata.

In JAIBA, Engram is **not** an automatic dependency or default brain store; it serves as the underlying backend for the optional, first-party `jaiba-engram-memory` adapter.

## How the project uses it

The framework integrates with Engram strictly through the `jaiba-engram-memory` adapter under physical protocol `jaiba-engram-storage/4` (`JAIBA4`), implementing canonical contract `jaiba-memory-surface/1.1.0`:

- **Bounded tool surface:**
  - `mem_current_project`: Invoked with the established work root to discover and verify the authorized Engram project name, isolated from the logical JAIBA `project-id`.
  - `mem_save`: Creates observations for catalogue, direct objects, chunked slices, context-head, exec-base, exec-deltas, and immutable append-log entries under the reserved namespace prefix `jaiba/v4/<ns16>/`.
  - `mem_update`: Updates existing catalogue, base, and context-head observations when revisions change.
  - `mem_get_observation`: Reads full untruncated payloads by numeric observation ID.

- **Prohibited / unused operations:**
  - `mem_search`: Discovery-only; never used as an authoritative catalogue, for rendering known artifacts, or as proof of absence.
  - `mem_judge`, `mem_judge_many`, `mem_compare`: Prohibited during surface operations. Engram's `judgment_required` notifications are treated as advisory metadata and ignored; the adapter never reads candidate bodies or blocks on judgment.
  - `mem_delete`: Not provided by Engram; selective work retirement is performed by catalogue exclusion while preserving physical rows intact.

## How to consult it

Read `skills/jaiba-engram-memory/SKILL.md` for adapter semantics, `references/engram-mapping.md` for tool-to-operation mappings, and `references/storage-integrity.md` for wire envelope (`JAIBA4.<sha256>.<base64>`) and checksum verification rules. Package CLI helper `scripts/jaiba_engram.py` handles encoding, decoding, deltas, and rendering in `agent-relay` mode.

## Constraints and limits (verified in trials)

Empirical guarantees characterized in Phase 15R (trial `efc16e3a-3764-4ae6-9454-4d9fd8bc7ac0`), Phase 16R (trial `6c90b698-39ba-441e-9c63-35ba9f9055c3`), and JAIBA4 static suite (`run_jaiba4_static.py`):
- **Wire format:** Single-line ASCII string containing base64-encoded UTF-8 payload bytes and SHA-256 digest (`JAIBA4`). Strict read-only decode for legacy `JAIBA3` snapshots; write attempts on unmigrated JAIBA3 stores are refused with `unsupported-version`.
- **Payload thresholds:**
  - Direct objects: `≤ 30,000` raw bytes (exact byte round-trip verified).
  - Chunked objects: `> 30,000` raw bytes (lossless multi-slice chunking).
- **Executive journal:** Archetype `record-store` implements $O(\delta)$ mutations via `patch` operations, sequenced deltas, and `context-head` synchronization.
- **Concurrency:** No native CAS (`absent / not-assumed`). Single-writer serialization is mandatory at the workflow level.
- **Fail-closed defenses:** Corrupt chunk data triggers `digest-mismatch` before destination write; symlinked directories trigger `symlink-root` rejection before path traversal.
- **Namespace isolation:** All JAIBA data lives strictly under `jaiba/v4/<ns16>/`, preventing collision with general conversation memory. All operations specify `capture_prompt: false` to avoid narrative pollution.
