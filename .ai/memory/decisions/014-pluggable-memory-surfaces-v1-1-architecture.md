---
type: decision
id: ADR-014
title: "Pluggable memory surfaces v1.1 architecture (archetypes, executive journal, portable bindings, and traceless onboarding)"
description: "Evolves jaiba-memory-surface to 1.1.0: adds document-tree and record-store archetypes, executive journal with O(delta) patch operations, pure Python 3 stdlib package scripts with an Efficiency Gate and upgrade/repair mode, portable binding v2 format with Step 0 Binding-First discovery, and traceless onboarding with a single cutover gate."
status: accepted
date: "2026-11-08"
tags: [memory, architecture, surfaces, archetypes, journal, engram, traceless]
updated: "2026-11-08"
---

# ADR-014: Pluggable memory surfaces v1.1 architecture (archetypes, executive journal, portable bindings, and traceless onboarding)

## Context

Following the adoption of the pluggable memory surfaces architecture ([ADR-013](013-pluggable-memory-surfaces-architecture.md)), practical experience across multiple agent runtimes (Claude Code, Cursor, OpenCode) and custom external storage backends (such as `jaiba-sdd-memory` in Issue #17) revealed five operational friction points:

1. **Host-bound certification locks:** Packaging conformance tied claim envelopes to specific host agents rather than backend protocols, requiring redundant re-evaluations across different tools.
2. **Quadratic write amplification ($O(N)$ token bloat):** Updating executive memory (PRD, plan, tasks, walkthrough) in record-oriented backends required rewriting entire monolithic documents, burning tokens and context window capacity.
3. **Fuzzy discovery and token waste in traceless repositories:** Agents inspecting repositories without local `.ai/` trees defaulted to checking filesystem paths, falsely reporting repositories as uninstrumented and prompting for manual intervention.
4. **Ad-hoc package scripts and missing efficiency gates:** Adapters lacked a standardized, dependency-free scripting layer to perform deterministic codec, chunking, and rendering operations without sending raw envelopes through the model.
5. **Multi-turn onboarding friction:** External initialization and migration interrupted developers with redundant questionnaires and scattered migration state across multiple uncoordinated directories.

## Decision

Evolve `jaiba-memory-surface` to **1.1.0** (additive, minor) across all framework skills and adapters:

### 1. Archetype Classification (`document-tree` vs `record-store`)
- Storage-nature profiles classify backends into two physical archetypes:
  - `document-tree`: File vaults, Notion, or local filesystems where each logical object is an editable Markdown document. `patch` is realized as direct in-place edits; no `context-head` or delta chain is required.
  - `record-store`: Databases, FTS stores, observation memory, and vector stores. Requires an **executive journal** (`base` + contiguous sequence of deltas) and a small `context-head` record per executive context.
- Insufficient evidence is marked `unknown` and strictly blocks derivation of a conforming adapter.

### 2. Executive Journal and $O(\delta)$ `patch` Operation
- Introduces optional capability `executive-journal` and normative operation `patch(address, expected-head, ops[])` for executive artifacts (`prd`, `plan`, `tasks`, `walkthrough`).
- Closed operation vocabulary:
  - `tasks`: `check`, `uncheck`, `add-task`, `amend-task`.
  - `plan`/`prd`: `set-frontmatter`, `replace-section`, `append-section`, `append-to-section`, `remove-section`.
  - `prd` criteria: `add-criterion`, `update-criterion`, `remove-criterion`, `set-criterion-status`.
  - `walkthrough`: `append-entry`.
- Strict criterion ID permanence: once PRD frontmatter `status` is not `draft` (e.g. `approved`), `remove-criterion` and `update-criterion` are rejected with `conflict`.
- Materialization is a deterministic pure function (`base` + active deltas in sequence order). Legacy monolithic objects serve as implicit bases at `seq: 0`.

### 3. Pure Python 3 Standard Library Scripts & Efficiency Gate
- Adapters may ship official scripts in `scripts/` using pure Python 3 standard library only (`requires: [python3]`, zero third-party `pip` dependencies).
- Declares one of three transport modes: `local-cli`, `local-http`, or `agent-relay` (where the script prepares tool arguments and verifies readbacks without direct backend I/O).
- Conformance incorporates a normative **Efficiency Gate** evaluating 5 SDD lifecycle scenarios (`initialize`, `spec` drafting, `execute` waves, plan approval, `render`); monolithic full-object overwrites on `record-store` are strictly `NONCONFORMING`.
- `create-memory` adds a 5-step `upgrade/repair` workflow to modernize 1.0.x adapters preserving empirical contrasted profiles, alongside multi-host installation.

### 4. Portable Binding v2 and Step 0 Binding-First Discovery
- Standard machine routing binding is stored at `~/.jaiba/memory/bindings/<sha256(canonical-work-root)>.yaml` (`binding-format-version: "2"`), shared across all agent runtimes of the user.
- **Step 0 Binding-First rule:** Agents inspect this path *before* touching local `.ai/` paths. If present, the binding governs unless an explicit `jaiba-memory-surface:` field exists in `AGENTS.md`. Testing `.ai/` paths on external surfaces is strictly prohibited.
- Fresh clones resolve project identity by looking up the normalized `git-remote` (`origin`) candidate in the surface's project registry, linking automatically without search or prompting.

### 5. Reference Protocol `JAIBA4` (`jaiba-engram-storage/4`)
- Reference adapter `jaiba-engram-memory` upgrades to `JAIBA4`: single-line wire `JAIBA4.<sha256>.<base64>`, keys under `jaiba/v4/<ns16>/`, 30,000-byte direct threshold with lossless chunking, and helper CLI `scripts/jaiba_engram.py` in `agent-relay` mode.
- Strict read-only decode for legacy `JAIBA3.` records; write attempts against `JAIBA3` stores are rejected with `unsupported-version` requiring explicit migration (`jaiba-init:migrate-surface JAIBA3 → JAIBA4`).

### 6. Traceless Onboarding and Issue #17 Enhancements
- External bootstrap creates zero files in the repository, excluding `.atl/` in `.git/info/exclude`.
- New project onboarding consolidates decisions into a single questionnaire of $\le 4$ questions (`C3`), suggests shared namespaces from sibling repository bindings (`C4`), verifies independent concepts in batch before catalogue publication (`C0`), offers an explicit minimal inventory with cost disclosure (`C1`, `C5–C6`), and groups unlocatable downstream consumers (`C2`).
- Surface migration runs preflight→snapshot→staging→verification continuously, concluding with a single cutover questionnaire separating activation from source retirement.

## Consequences

- *Positive:* Significant reduction in token consumption and context bloat during SDD workflows; complete elimination of false uninstrumented warnings in traceless repositories; portable cross-host adapter certification; deterministic rendering across all read lanes without search sweeps.
- *Negative / Trade-offs:* Adapters implementing `record-store` must maintain delta sequencing and `context-head` synchronization; agents must support Python 3 for package helper scripts.
