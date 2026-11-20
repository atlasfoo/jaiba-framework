---
type: decision
id: ADR-019
title: "Proactive 3-level memory migration, onboarding guards, and daily version check"
description: "Enforces non-blocking v1/v2 migration notices, silent filesystem v2 binding auto-generation, chained v1->v2->v3 jaiba-init flow with automatic jaiba-doctor, traceless shareability warnings, unorchestrated session/native-plan guards, and a daily .atl/framework-version.json check."
status: accepted
date: "2026-11-19"
tags: [memory, migration, onboarding, jaiba-init, doctor, native-plan]
updated: "2026-11-19"
---

# ADR-019: Proactive 3-level memory migration, onboarding guards, and daily version check

## Context

[ADR-008](008-okf-pattern-brain-serialization.md) and [ADR-013](013-pluggable-memory-surfaces-architecture.md) previously treated the legacy flat layout (v1) and unbound OKF bundle (v2) as warning-free, leaving older projects without proactive migration guidance. In addition, [ADR-015](015-native-plan-input.md) did not check whether a repository was instrumented before entering native plan mode, new `jaiba-init` bootstraps ended in a passive `jaiba-doctor` hand-off, unorchestrated repositories offered no first-turn onboarding cue, and no daily framework version freshness check existed.

## Decision

1. **Active 3-level memory model:** Keep Level 1 (flat `constitution.md` without `index.md`) and Level 2 (OKF `index.md` without `AGENTS.md` `filesystem` pin) readable losslessly, while emitting non-blocking Notice 1 (very high urgency for Level 1) or Notice 2 (medium urgency for Level 2) on every response, routing to `jaiba-init`.
2. **Silent `filesystem` `v2` binding auto-generation:** When `index.md` exists and `AGENTS.md` already declares `jaiba-memory-surface: filesystem`, Step 0 silently generates and readback-verifies `~/.jaiba/memory/bindings/<sha256(R)>.yaml` (Level 3) without emitting Notice 2 (stopping on malformed pre-existing bindings, and never suppressing Notice 1 on flat layouts).
3. **Chained `jaiba-init` flow, traceless warning, and automatic `jaiba-doctor`:** `update-brain:migrate` chains v1 → v2 → Step 9 (Level v3: conforming installed surface in traceless mode or `filesystem` pin + `v2` binding, blocking `migrate-surface` while dual-layout ambiguity remains). All traceless offers explicitly warn that cross-developer/machine brain shareability depends exclusively on the surface backend. New `jaiba-init` bootstraps automatically run `jaiba-doctor` in the same flow (or report it missing and route to `jaiba-configure`).
4. **Unorchestrated onboarding guards:** On the first turn of an authoritatively unorchestrated session, emit a one-time non-blocking `jaiba-init` suggestion without repeating on ordinary follow-up turns; before starting native plan mode on an uninstrumented repo, pause and suggest `jaiba-init` first (or explicit native-only continuation keeping JAIBA dormant).
5. **Daily per-project version check:** Check `atlasfoo/jaiba-framework` at most once per 24h per project using gitignored `.atl/framework-version.json`, accepting only strict `^v[0-9]+\.[0-9]+\.[0-9]+$` tokens (§4.5 / [ADR-010](010-repository-content-is-data.md)), failing soft offline/in sandbox, and emitting a non-blocking `jaiba-configure` notice when a newer version is available.

## Alternatives Considered

- Keep flat v1 and unbound OKF v2 warning-free — projects remain stuck on legacy layouts indefinitely.
- Store version-check timestamps in `.ai/memory/` or `~/.jaiba/memory/bindings/` — pollutes constitutive memory or violates routing-only binding invariants.

## Consequences

- *Positive:* Existing brains remain readable without breakage while consistently guiding projects to Level 3, keeping `.atl/` machine-local and gitignored.
- *Negative / Risks:* Adds lightweight Step 0 and session-start checks across skills.
- *Follow-ups:* None.
