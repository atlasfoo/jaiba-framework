---
type: log-entry
date: 2026-10-05
slug: brain-update-adr-012
kind: brain-change
---

# Brain change — ADR-012 enacted

## What changed

- **Created** `.ai/memory/decisions/012-authorized-first-party-agent-execution.md` (`status: accepted`): clarifies that ADR-010's data-boundary rule does not prevent an authorized JAIBA workflow from executing a shipped first-party subagent's own role definition without a second developer confirmation. The carve-out grants no extra tools or scope and does not relax the data-boundary rule on inspected repository or tool output content.
- **Updated** `.ai/memory/index.md`: added ADR-012 line to the `decision` group; bumped `updated: 2026-10-05`.

## Provenance

Enacted from the proposal in `.ai/memory/log/2026-10-05-contract-authorized-agent-execution.md` (§ ADR proposals & brain updates), produced by `conduct:summarize` at the close of plan `contract-authorized-agent-execution`.

## What was deliberately left untouched

- ADR-010 — not superseded; ADR-012 complements it by clarifying the scope of "repository content" in the context of first-party workflow invocations.
- All identity, reference, and quality-gate concepts — no identity event occurred.
