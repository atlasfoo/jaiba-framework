---
type: decision
id: ADR-005
title: "Subagent concurrency model"
description: Task waves built from the depends-on graph, fan-out capped at 3, parallel only across disjoint file footprints, conduct is the single writer of .ai/work/.
status: accepted
date: "2026-07-06"
tags: [subagents, execution, concurrency]
updated: "2026-08-03"
---

# ADR-005: Subagent concurrency model

## Context

`conduct:execute` needed a way to delegate task implementation to
subagents without either serializing everything (losing throughput) or
letting subagents run fully unconstrained (risking file-footprint
collisions and an inconsistent `.ai/work/`, since multiple writers to
the same executive artifacts would race).

## Decision

Build **waves**: from the active phase's unchecked tasks, take every
task whose `depends-on` IDs are already checked; partition by inferred
file footprint so overlapping tasks never share a wave; fan out capped
at 3 in flight, one executor tier per task's `load` (`executor-high` /
`-medium` / `-low`); reintegrate every result — review against `git
diff`, write the walkthrough entry, flip the checkbox — before the
next wave starts. Subagents write source only; `conduct` remains the
single writer of `.ai/work/`. Hosts without subagent support fall back
to the same contract run sequentially.

## Alternatives Considered

- *Unconstrained parallel dispatch* — rejected: no protection against
  two tasks touching the same file, and no single writer for the
  walkthrough/checkboxes risks a corrupted or racing executive record.
- *Fully sequential execution always* — rejected: throws away real
  throughput gains on large phases with genuinely independent,
  file-disjoint tasks.

## Consequences

- *Positive:* parallelism where it's safe, serialization where it
  isn't, and a clean audit trail (walkthrough entries always written by
  `conduct`, never by an executor).
- *Negative / Risks:* the cap-3 discipline has to be actively enforced —
  see the process note in this repo's own OKF plan walkthrough (Phase
  2 checkpoint), which recorded a real violation (6 concurrent
  executors briefly in flight) with no observed consequence, but the
  discipline was corrected for subsequent waves.
- *Follow-ups:* the invocation contract (envelope, `requires:`
  convention, pre-invocation toolchain check) is documented in
  `skills/conduct/references/subagents.md`.
