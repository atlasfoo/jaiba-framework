---
type: decision
id: ADR-001
title: Adoption of the JAIBA brain structure
description: This repository — which builds the JAIBA framework itself — keeps its own agent-facing memory under .ai/, dogfooding the framework it ships.
status: accepted
date: 2026-07-03
tags: [meta, memory, tooling]
updated: 2026-08-03
---

# ADR-001: Adoption of the JAIBA brain structure

## Context

This repository *is* the JAIBA framework's own source — the skills,
templates and subagent definitions that other repositories install.
Before this decision, its own working state lived in a `session/`
directory and a flat `archive/` under `.ai/memory/`, predating the
`work/`/`memory/log/` model the framework's `jaiba-init`/`conduct`
skills now install into every *other* repo. Continuing to develop the
framework without dogfooding its own memory model risked the shipped
model drifting from what its own maintainers actually found workable.

## Decision

Adopt the JAIBA framework's own `.ai/` brain in this repository:
`AGENTS.md` at the repo root for agent behavior; `.ai/memory/` as the
constitutive memory (this bundle: `index.md`, `identity/` for project
identity and the quality gate, `decisions/` for ADRs, `references/`
for external surfaces, and the append-only chronological record in
`log/`); `.ai/work/` for executive memory (PRD when produced, plan,
tasks, walkthrough — gitignored, archived into `log/` at close). The
physical `work/`/`memory/log/` split was put in place 2026-07-03; full
population of the constitutive bundle (this file and its siblings) was
completed later, 2026-08-03, via `jaiba-init:update-brain:initialize`
run against this same repository.

## Alternatives Considered

- *Keep the pre-existing `session/`/flat-`archive/` layout, unaligned
  with what the framework ships to other repos* — rejected: the
  framework's own maintainers would stop being the first users of its
  own memory model, and drift between "what JAIBA ships" and "what
  JAIBA's own repo does" would go unnoticed.
- *A single monolithic context file* — rejected: conflates concerns and
  becomes unmaintainable as the framework grows, exactly the failure
  mode the constitutive/executive split and later the concept bundle
  exist to avoid.

## Consequences

- *Positive:* continuity across sessions; decisions become traceable;
  the framework's own repository is now proof that its memory model
  works on a real, non-trivial project (dogfooding), not just the
  fixtures under `skills/jaiba-init/evals/fixtures/`.
- *Negative / Risks:* requires discipline to keep memory current; a
  self-hosting repo has an added risk of confusing "what the framework
  *is*" (its skill source) with "what this repo's own project *is*"
  (a meta case most adopting repos won't have) — see
  [identity/purpose.md](../identity/purpose.md) and
  [identity/scope.md](../identity/scope.md) for how that boundary is
  drawn.
- *Follow-ups:* run `jaiba-init:update-brain` after major milestones;
  the `AGENTS.md` carve-out that stood in for a missing constitution
  since 2026-07-28 is retired now that this bundle exists (see the
  OKF-serialización-cerebro plan's task T-029).
