---
type: reference
title: "Engram MCP external memory surface"
description: "Model Context Protocol interface for persistent memory; provides bounded tool surface for the optional jaiba-engram-memory adapter under the JAIBA3 protocol."
tier: external
kind: service
role: "optional pluggable memory adapter"
resource: "MCP server `mcp:engram` / tools: `mem_current_project`, `mem_save`, `mem_update`, `mem_get_observation`"
tags: [memory, mcp, engram, adapter, surface]
updated: "2026-11-01"
---

# Engram MCP external memory surface

## What it is

Engram is an external Model Context Protocol (MCP) server providing persistent observation-based memory storage across coding sessions. It exposes tools for saving observations, querying project context, and managing observation metadata.

In JAIBA, Engram is **not** an automatic dependency or default brain store; it serves as the underlying backend for the optional, first-party `jaiba-engram-memory` adapter.

## How the project uses it

The framework integrates with Engram strictly through the `jaiba-engram-memory` adapter under physical protocol `jaiba-engram-storage/3` (`JAIBA3`), implementing canonical contract `jaiba-memory-surface/1.0.0`:

- **Bounded tool surface:**
  - `mem_current_project`: Invoked with the established work root to discover and verify the authorized Engram project name, isolated from the logical JAIBA `project-id`.
  - `mem_save`: Creates observations for catalogue, direct objects, chunked slices, and immutable append-log entries under the reserved namespace prefix `jaiba/v3/<ns16>/`.
  - `mem_update`: Updates existing catalogue observations when revisions change.
  - `mem_get_observation`: Reads full untruncated payloads by numeric observation ID.

- **Prohibited / unused operations:**
  - `mem_search`: Discovery-only; never used as an authoritative catalogue or proof of absence. Authoritative inventory is exclusively maintained via the single catalogue observation.
  - `mem_judge`, `mem_judge_many`, `mem_compare`: Prohibited during surface operations. Engram's `judgment_required` notifications are treated as advisory metadata and ignored; the adapter never reads candidate bodies or blocks on judgment.
  - `mem_delete`: Not provided by Engram; selective work retirement is performed by catalogue exclusion while preserving physical rows intact.

## How to consult it

Read `skills/jaiba-engram-memory/SKILL.md` for adapter semantics, `references/engram-mapping.md` for tool-to-operation mappings, and `references/storage-integrity.md` for wire envelope and checksum verification rules.

## Constraints and limits (verified in trials)

Empirical guarantees characterized in Phase 15R (trial `efc16e3a-3764-4ae6-9454-4d9fd8bc7ac0`) and Phase 16R (trial `6c90b698-39ba-441e-9c63-35ba9f9055c3`):
- **Wire format:** Single-line JSON containing base64-encoded UTF-8 payload bytes and SHA-256 digest (`JAIBA3`). Immune to markdown whitespace trimming and redaction markers.
- **Payload thresholds:**
  - Direct objects: `≤ 30,000` raw bytes (exact byte round-trip verified).
  - Chunked objects: `> 30,000` raw bytes (verified at 55,000 B across two slices in T-087).
- **Concurrency:** No native CAS (`absent / not-assumed`). Single-writer serialization is mandatory at the workflow level.
- **Fail-closed defenses:** Corrupt chunk data triggers `digest-mismatch` before destination write; symlinked directories trigger `symlink-root` rejection before path traversal.
- **Namespace isolation:** All JAIBA data lives strictly under `jaiba/v3/<ns16>/`, preventing collision with general conversation memory. All operations specify `capture_prompt: false` to avoid narrative pollution.
