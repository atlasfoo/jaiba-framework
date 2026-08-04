---
type: decision
id: ADR-004
title: Three-lane routing policy
description: ask and fast become implicit-only lanes selected by a routing rule; conduct stays dual (implicit + explicit /conduct override).
status: accepted
date: 2026-07-06
tags: [workflow, routing]
updated: 2026-08-03
---

# ADR-004: Three-lane routing policy

## Context

With `conduct` unified (ADR-003), the framework still needed a
consistent way to dispatch a developer message to the right lane —
a question, a small contained change, and new/continuing work are
different shapes of request that shouldn't all funnel through the same
entry point or require the developer to remember three different slash
commands.

## Decision

Three lanes, one routing rule: `ask` (read-only, implicit-only — no
slash command) for questions; `fast` (inline execution, implicit-only)
for small contained changes; `conduct` (the SDD chain) for new or
continuing work, implicit *and* with `/conduct [phase]` as a
deterministic explicit override for when routing misfires. The rule
lives in the global behavioral contract so it applies the same way
across every project.

## Alternatives Considered

- *Slash commands for all three lanes* — rejected: reintroduces the
  "which command do I need" friction the unification in ADR-003 was
  meant to remove for the two lanes that don't need an explicit
  override (a question or a quick fix rarely needs one).

## Consequences

- *Positive:* the developer expresses intent in plain language; only
  `conduct` needs an explicit override, and only because it is the one
  lane with real state (an active plan) worth force-selecting a phase
  against.
- *Negative / Risks:* the routing rule itself is a single point of
  failure — a misclassified message (e.g. a continuation cue read as a
  question) sends work to the wrong lane; the contract documents the
  rule precisely for this reason.
- *Follow-ups:* none outstanding; the rule has since been re-expressed
  in concept-graph terms without changing its substance (see
  [ADR-008](008-okf-pattern-brain-serialization.md)).
