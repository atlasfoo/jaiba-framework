---
type: decision
id: ADR-015
title: "Native plan is an input, not a second chain"
description: "Host plan text is an input to conduct spec, converted outside a write-freezing mode; it does not replace the SDD chain or move the approval gate."
status: accepted
date: "2026-11-13"
tags: [workflow, conduct, native-plan]
updated: "2026-11-13"
---

# ADR-015: Native plan is an input, not a second chain

## Context

Host plan mode can freeze file writes. Treating that mode as the plan would skip JAIBA drafts and the approval gate in [ADR-003](003-unified-orchestrator-sdd-chain.md). This decision extends ADR-003. It does not replace it.

## Decision

When `native-plan-client` is `auto` or `on` and the host exposes plan mode or a plan subagent, conduct asks for the plan text and converts it in a session that can write. It does not replan the how. Empty text stops and asks. A finished native plan is preserved only if the developer accepts. `off`, or no plan mode, follows the current spec. The machine setting lives with `jaiba-configure`, not in `.ai/memory/`.

## Alternatives Considered

- Run spec inside native plan mode — the draft cannot be written while writes are frozen.
- Always replan after the host text — throws away the how the developer already accepted.

## Consequences

- *Positive:* The host's how is kept, and the approval gate does not move.
- *Negative / Risks:* A host that freezes writes still needs a second writable session before any executive file exists.
- *Follow-ups:* Enactment does not install the global contract. A later `jaiba-configure` does that.
