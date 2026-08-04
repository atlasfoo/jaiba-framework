---
type: decision
id: ADR-007
title: Framework must not assume a single vendor or a single machine
description: Setup splits into jaiba-configure (global, machine-level) and jaiba-init (repo-local); the shipped subagent battery drops hardcoded model IDs.
status: accepted
date: 2026-08-01
tags: [setup, subagents, model-agnostic]
updated: 2026-08-03
---

# ADR-007: Framework must not assume a single vendor or a single machine

## Context

The former `scaffold`/`update-brain` skill bundled global machine setup
(behavioral contract, subagent battery, skillset) together with
repo-local instrumentation, and the shipped subagent battery hardcoded
Claude-Code-specific model IDs — both assumed the framework runs for
one agent, on one machine, from one vendor.

## Decision

Split into `jaiba-configure` (global: contract, skillset, battery — no
brain templates) and `jaiba-init` (repo-local: `AGENTS.md` marker,
`.ai/` skeleton, constitutive memory — checks for but never installs
the global side), with no shared file paths and hand-off only by
naming the other skill, never invoking it. Subagent definitions ship
with no `model:` field (absent = inherit the orchestrator's model);
`jaiba-configure` discovers the host's actual model roster at install
time and offers per-tier pinning, never a hardcoded list.

## Alternatives Considered

- *Keeping one bundled skill with conditional logic* — rejected: the
  coupling is exactly what caused the "configured for one agent, not
  another on the same machine" gap that surfaced during the plan that
  produced this decision.

## Consequences

- *Positive:* every repo-state routing failure converges on
  `jaiba-init`; every agent-coverage gap converges on `jaiba-configure`.
  This repository's own [architecture.md](../identity/architecture.md)
  and [scope.md](../identity/scope.md) reflect the split directly.
- *Negative / Risks:* two setup skills to keep in sync (e.g. the
  `jaiba-contract.md` lockstep check in the Quality Gate) instead of
  one; a developer must run both once per machine/repo pair.
- *Follow-ups:* none outstanding.
