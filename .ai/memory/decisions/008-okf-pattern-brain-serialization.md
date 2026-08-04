---
type: decision
id: ADR-008
title: OKF pattern adopted as brain serialization convention
description: .ai/memory/ gains a concept-bundle layout (one file per concept, closed type: vocabulary, file-relative links) shaped after OKF v0.1, alongside the still-supported legacy flat layout.
status: accepted
date: 2026-08-02
tags: [memory-model, okf, architecture]
updated: 2026-08-03
---

# ADR-008: OKF pattern adopted as brain serialization convention

## Context

The JAIBA constitutive brain was three monolithic files —
`constitution.md` (8 sections), `adr-log.md` (tabular index plus every
decision in one file), and `reference-index.md` (7 sections of
tables) — plus `.ai/memory/log/`, already one-file-per-entry. Three
concrete consequences: (1) all-or-nothing reads — an agent needing
only the Quality Gate loaded all eight sections; (2) relations were
prose, not a graph — citations like `reference-index.md §3` were never
validated, a renumbered section left them dangling silently; (3)
unbounded accumulation — `adr-log.md` and `reference-index.md` grew
without bound inside a single file, already flagged by `jaiba-doctor`
diagnosis 1 as "work narrative accumulating inside `adr-log.md`."

## Decision

Adopt [OKF v0.1](../references/okf-v0-1.md)'s *shape*, not a
dependency on it: one concept per file, `type:` as the sole mandatory
frontmatter key (closed vocabulary in
`skills/jaiba-init/references/okf-pattern.md`), file-relative markdown
links for every relation, `.ai/memory/index.md` as the bundle's single
entry point. No skill/script/subagent declares a `requires:` because
of this pattern; conformance to upstream OKF is never tested or
claimed; unknown frontmatter keys are tolerated and ignored — the only
key whose absence is a finding is `type:`. The pre-existing flat
layout (`constitution.md`/`adr-log.md`/`reference-index.md`) remains a
fully supported, warning-free alternative — resolved by a dual-
resolution rule (`index.md` present → bundle; only the three flat files
→ legacy; both → ambiguous, surface it; neither → route to
`jaiba-init`) — never a fallback to migrate away from unprompted.

## Alternatives Considered

1. *A JAIBA-proprietary format* — rejected: solves the same problems
   but with an unvetted design and no shared vocabulary to onboard
   against.
2. *Staying monolithic* — rejected: resolves none of the three concrete
   problems above.
3. *Depending literally on OKF v0.1 as a versioned dependency* —
   rejected: OKF v0.1 is a draft; pinning JAIBA's code paths to its
   evolution would force migrations JAIBA does not control.

## Consequences

- *Positive:* one-hop navigability from `index.md`, tolerance to
  upstream drift, per-concept growth instead of unbounded files,
  individually addressable/supersedable decisions.
- *Negative / Risks:* more files; `index.md` must stay in sync (a
  stale index is a broken-link finding for `jaiba-doctor`); existing
  flat-layout repos face an optional migration decision — mitigated by
  dual resolution being non-mandatory and human-triggered
  (`jaiba-init:update-brain:migrate`).
- *Follow-ups:* this repository's own bundle (this file included) was
  populated via `jaiba-init:update-brain:initialize`, landing this ADR
  plus [ADR-001](001-jaiba-brain-adoption.md) through
  [ADR-007](007-global-repo-local-setup-split.md) as real `decision`
  concepts, and indexing OKF v0.1 as a real `reference` concept.
