---
type: decision
id: ADR-001
title: Adoption of the JAIBA brain structure
description: The project keeps agent-facing memory in .ai/ under the JAIBA framework.
status: accepted
date: 2026-06-02
tags: [meta, memory, tooling]
updated: 2026-06-02
---

# ADR-001: Adoption of the JAIBA brain structure

## Context

The project needed a way for AI coding agents to retain context across
sessions, sustain architectural coherence, and surface the reasoning
behind past technical choices. Without persistent structure, every
session restarts from scratch and the same questions get re-litigated.

## Decision

Adopt the JAIBA framework's `.ai/` brain structure: `AGENTS.md` at the
repo root for agent behavior; `.ai/memory/` for constitutive memory
(`constitution.md`, this file, `reference-index.md`) plus the
append-only chronological record `.ai/memory/log/`; `.ai/work/` for
executive memory (PRD when produced, plan, tasks, walkthrough —
gitignored, archived to `memory/log/` at close).

## Alternatives Considered

- *No structured memory* (status quo) — rejected; sessions lose context
  and decisions are not traceable.
- *A single monolithic context file* — rejected; conflates concerns and
  becomes unmaintainable as the project grows.

## Consequences

- *Positive:* continuity across sessions; decisions become traceable;
  onboarding (human or agent) is faster.
- *Negative / Risks:* requires discipline to keep memory current; stale
  memory can mislead the agent.
- *Follow-ups:* Schedule periodic `jaiba-init:update-brain` runs after
  major milestones.
