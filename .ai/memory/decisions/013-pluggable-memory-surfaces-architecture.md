---
type: decision
id: ADR-013
title: "Pluggable memory surfaces architecture and opt-in Engram adapter"
description: "Decouples canonical logical memory contract 1.0.0 from backend physical storage via storage-nature profiles; ships opt-in jaiba-engram-memory adapter using JAIBA3 protocol while retaining filesystem as default, and accepts the ~355-line global behavioral contract size."
status: accepted
date: "2026-11-01"
tags: [memory, architecture, surfaces, engram, contract]
updated: "2026-11-01"
---

# ADR-013: Pluggable memory surfaces architecture and opt-in Engram adapter

## Context

JAIBA's memory model originally operated exclusively on the local filesystem ([ADR-002](002-two-category-memory-model.md)), structured either as a concept bundle ([ADR-008](008-okf-pattern-brain-serialization.md)) or legacy flat layout. As agents collaborate across multiple work roots, team repositories, and persistent host toolchains, memory backends beyond local disk become valuable: external databases, remote storage vaults, and Model Context Protocol (MCP) memory servers such as Engram.

However, naive integrations of external memory backends frequently violate JAIBA core tenets:
1. Conflating backend documentation with empirical capability (e.g. assuming native atomic Compare-And-Swap or transactions where none exist).
2. Allowing narrative conversational memories or full-text search to act as an authoritative catalogue or proof of absence.
3. Breaking authority boundaries: letting background memory sweeps or unverified writes mutate constitutive or executive states without human oversight.
4. Expanding the behavioral contract without formally acknowledging the size boundary.

A formal, pluggable memory-surface architecture was required to decouple canonical logical requirements from physical backend adapters while preserving strict data boundaries and fail-closed security.

## Decision

Adopt the **pluggable memory surfaces architecture**, structured into three strictly decoupled layers:

### 1. Three-Tier Architectural Separation
1. **Canonical Logical Contract (`jaiba-memory-surface/1.0.0`):** Defines canonical memory invariants, concept categories (constitutive vs executive), operations (`catalogue`, `get`, `put`, `append-log`, `archive-context`, `clear-work`), and schema validation across both concept-bundle and legacy-flat layouts. Owned by `skills/create-memory/references/memory-surface-contract.md`.
2. **Storage-Nature Profile (`references/storage-nature.md`):** Empirically characterizes backend guarantees through a finite native experiment (persistence, single-writer serialization, operating thresholds, absent capabilities like native CAS, and error boundaries). A mapping is a derived conclusion from a contrasted profile, never a speculative assumption.
3. **Physical Adapter Protocol:** The derived concrete wire and storage serialization format matching backend guarantees.

### 2. Default Filesystem Surface Retained
- The built-in filesystem surface remains the zero-config default for greenfield and brownfield repositories.
- Both concept-bundle and legacy-flat layouts remain fully supported without deprecation or automatic migration.
- Selection precedence is strictly deterministic: explicit project `AGENTS.md` field (`jaiba-memory-surface: <id>`) → host-visible local adapter → host-visible global adapter → built-in filesystem. Multiple candidates at the winning level require explicit human resolution; there is no silent fallback.

### 3. Opt-in First-Party Engram Adapter (`jaiba-engram-memory`)
- Ships as an optional first-party package, kept strictly outside the core skillset (`skills/jaiba-configure/assets/skillset.txt`). Installing it is an explicit opt-in choice in `jaiba-configure`.
- Declares `category: memory-surface` with `conformance-status: verified` on bounded trial evidence (`efc16e3a-3764-4ae6-9454-4d9fd8bc7ac0`).
- Implements physical protocol `jaiba-engram-storage/3` (`JAIBA3`): single-observation JSON+base64+SHA-256 envelope under namespace prefix `jaiba/v3/<ns16>/`.
- Characterized and verified limits:
  - Single-catalogue observation per `(namespace, project)` eliminating search dependencies.
  - Direct payload objects `≤ 30,000` raw bytes with exact round-trip fidelity.
  - Chunked payload objects `> 30,000` raw bytes (verified at 55,000 B across two slices in T-087) with lossless reassembly.
  - Native CAS is absent (`absent / not-assumed`); application single-writer serialization is mandatory.
  - MCP `judgment_required` notifications are treated as advisory metadata; the adapter never calls `mem_judge`, `mem_judge_many`, or `mem_compare`, and never blocks on judgment.
  - Strict namespace isolation: ordinary conversational memories stay outside `jaiba/v3/<ns16>/`, and surface operations enforce `capture_prompt: false`.

### 4. Verified Multi-Hop Migration and Fail-Closed Guards
- Surface migration (`jaiba-init:migrate-surface`) is verified lossless across multi-hop trials (filesystem ↔ Engram `JAIBA3` ↔ external vault `posix-file/1` under trial `6c90b698-39ba-441e-9c63-35ba9f9055c3`).
- A staging verification barrier and explicit human approval are required before any binding switch or activation.
- Fail-closed guards: corrupt chunks trigger `digest-mismatch` without writing, and symlink traversals trigger `symlink-root` rejection before modifying storage.

### 5. Accepted Global Behavioral Contract Size Deviation (~355 lines)
- The global behavioral contract (`jaiba-contract.md`) expanded from historical ~250 lines to ~355 lines.
- This deviation is accepted: encoding the memory surfaces architecture, data-boundary rules ([ADR-010](010-repository-content-is-data.md), [ADR-012](012-authorized-first-party-agent-execution.md)), and subagent delegation within a single, unified contract prevents rule fragmentation across different host agent platforms.

## Alternatives Considered

1. *Direct tool-binding without storage-nature profile* — rejected: guessing backend topology leads to corrupted state, uncharacterized limits, and CAS illusions.
2. *Making Engram or external surfaces the default* — rejected: violates zero-dependency bootstrap, requires external MCP runtime, and compromises repository portability.
3. *Hard-trimming global contract to <300 lines by omitting memory surface / data-boundary rules* — rejected: creates prompt injection vectors and ambiguity in delegation across agent runtimes.

## Consequences

- *Positive:* Strict isolation of concerns; canonical logical contract remains stable at 1.0.0; external backends can be characterized and added without modifying core workflows; verified lossless migrations across heterogeneous protocols (`filesystem`, `JAIBA3`, `posix-file/1`); no dependency on full-text search for authoritative inventory.
- *Negative / Risks:* External adapters require explicit installation, configuration, and verification; absence of native CAS in services like Engram requires strict single-writer discipline.
- *Follow-ups:* `jaiba-init:update-brain` writes this ADR to `.ai/memory/decisions/013-pluggable-memory-surfaces-architecture.md`, adds `references/engram-mcp.md`, and links both in `.ai/memory/index.md`.
