---
type: decision
id: ADR-006
title: Index-everything, verify-what-you-can toolchain probe
description: The ATL probe indexes every scanned source unconditionally and renders an explicit [UNVERIFIED] state instead of a silent zero.
status: accepted
date: 2026-08-01
tags: [toolchain, doctor, atl]
updated: 2026-08-03
---

# ADR-006: Index-everything, verify-what-you-can toolchain probe

## Context

A skill or subagent with no `requires:` was invisible in
`.atl/tool-layout.md`, and a missing `jq` silently skipped the hooks
scan — both looked identical to "nothing needed," which is a false
"present" the framework's own quality bar forbids.

## Decision

`skills/doctor/scripts/check-tools.sh` indexes every scanned source
unconditionally, classifies `mcp:`-prefixed dependencies into a
separate never-present/never-missing `[UNVERIFIED]` state (verified
downstream by `jaiba-doctor`'s external-reference-health diagnostic),
and renders an explicit unverified marker instead of a silent zero when
`jq` is absent.

## Alternatives Considered

- *Enumerating `.mcp.json`/vendor configs directly* — rejected:
  convention-only `mcp:` in `requires:` keeps the probe declarative.
- *Leaving unverified hooks as a silent zero* — rejected:
  indistinguishable from "needs nothing."

## Consequences

- *Positive:* every skill/subagent/hook layer is now visible in
  `.atl/tool-layout.md` with honest provenance, even when it declares
  no tools.
- *Negative / Risks:* `find -L` must follow symlinks (this framework's
  own recommended install layout uses them) and must prune `evals/`
  directories during the walk rather than filtering by path after —
  both surfaced as real bugs during the plan that produced this
  decision (fixed the same session).
- *Follow-ups:* none outstanding.
