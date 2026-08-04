---
type: decision
id: ADR-003
title: Unified orchestrator with an SDD chain and blast-radius triage
description: specification and planning dissolve into one conduct skill (propose→spec→tasks→execute→validate→summarize); depth follows blast radius, not the command chosen.
status: accepted
date: 2026-07-06
tags: [workflow, conduct]
updated: 2026-08-03
---

# ADR-003: Unified orchestrator with an SDD chain and blast-radius triage

## Context

Before this decision, `specification` and `planning` were separate
skills the developer had to choose between, and there was no shared
rule for how much ceremony (PRD vs. plan-only vs. inline) a given
change deserved — depth tracked which command was invoked, not how big
the change actually was.

## Decision

Dissolve `specification`/`planning` into a single orchestrator skill
(later named `conduct`) running one Spec-Driven-Development chain:
`propose → spec → tasks → execute → validate → summarize`. A shared
triage maps blast radius to depth on the continuum
`inline → design → spec`: an atomic edit executes on the spot
(`fast`'s territory), a bounded change gets a plan only, a
multi-faceted requirement gets a PRD *and* a plan. The developer no
longer chooses a command — routing and triage choose the entry point
and depth.

## Alternatives Considered

- *Keep `specification` and `planning` as separate skills* — rejected:
  requires the developer to correctly guess which one a given request
  needs, and produces two independently-maintained artifact schemas for
  what is really one continuum of work.

## Consequences

- *Positive:* one entry point, conditional PRD (no ceremony for a
  library bump or a performance fix), phases as consistent
  multi-session checkpoints.
- *Negative / Risks:* the triage itself becomes load-bearing — a
  miscalibrated depth either over-formalizes trivial work or
  under-specs something that needed a PRD; `fast` shares the same
  triage (floor `inline`) specifically to keep the boundary consistent.
- *Follow-ups:* `fast`/`ask` become implicit lanes routed to by the same
  rule — see
  [ADR-004](004-three-lane-routing-policy.md).
