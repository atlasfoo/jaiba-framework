---
type: decision
id: ADR-002
title: Memory splits into constitutive and executive categories
description: .ai/memory/ (curated, versioned, who-the-project-is) and .ai/work/ (ephemeral, gitignored, what-is-being-done) replace a single memory tree.
status: accepted
date: 2026-07-06
tags: [memory, architecture]
updated: 2026-08-03
---

# ADR-002: Memory splits into constitutive and executive categories

## Context

Early framework memory mixed long-lived project facts (identity,
decisions, external references) with the transient state of whatever
piece of work was active (plan, tasks, in-progress narrative) in one
undifferentiated tree. That made it hard to answer "what does the
project stand for" without wading through closed-work detail, and hard
to gitignore the ephemeral half without also losing the durable one.

## Decision

Split memory into two categories: **constitutive** —
`.ai/memory/` (curated, versioned, who the project is: identity,
decisions, references, plus the append-only `log/`) — and
**executive** — `.ai/work/` (PRD if any, plan, tasks, walkthrough;
ephemeral per piece of work, gitignored). `conduct:summarize` is the
single writer that bridges the two: it appends a distilled
`work-closure` entry to `.ai/memory/log/` and then clears `work/`.

## Alternatives Considered

- *A single versioned tree holding both* — rejected: conflates
  "durable project truth" with "what's in flight right now," forces
  either versioning transient work-in-progress noise or gitignoring
  facts that should survive, and gives `conduct:summarize` no clean
  boundary to close against.

## Consequences

- *Positive:* `conduct:summarize` gains a clean carve-out — append to
  `log/`, then clear `work/`, one confirmed step; a fresh session can
  read `.ai/memory/` alone to understand the project without executive
  noise.
- *Negative / Risks:* two directories to keep straight; a skill that
  writes to the wrong one (e.g. a proposal landing directly in
  `.ai/memory/` instead of being proposed through `summarize`) is a
  governance violation the framework has to guard against explicitly
  (`AGENTS.md` §2.9).
- *Follow-ups:* this split is the substrate the concept bundle
  (`index.md` + `identity/`/`decisions/`/`references/`) was later built
  on top of within `.ai/memory/` — see
  [ADR-008](008-okf-pattern-brain-serialization.md).
