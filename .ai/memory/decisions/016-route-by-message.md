---
type: decision
id: ADR-016
title: "Route by the message, not by its name"
description: "With an active plan, an out-of-task change enters fast even if it does not say fast; a received /btw enters ask; an undelivered host command is a limit, not a hook."
status: accepted
date: "2026-11-13"
tags: [workflow, routing, fast, ask]
updated: "2026-11-13"
---

# ADR-016: Route by the message, not by its name

## Context

[ADR-004](004-three-lane-routing-policy.md) routes by intent and gives `ask` and `fast` no slash commands. An amendment that did not say `fast`, and a received `/btw`, could still follow execute and mutate the active plan. This decision extends ADR-004. It does not replace it.

## Decision

With an active plan, a change outside the current tasks enters `fast` even if the message does not say `fast`. `continue`, `next`, and `go` stay on execute. A received `/btw`, or a documented equivalent delivered as a message, enters `ask` and does not mutate executive work. A command the agent never receives is a limit, not a hook. A change that triages to `design` or deeper is still refused and offered for fold-in or replan.

## Alternatives Considered

- Add `/fast` and `/ask` — rejected; the lanes stay implicit.
- Treat every side command as intercepted — false when the host does not deliver it.

## Consequences

- *Positive:* Side questions and unnamed amendments no longer depend on the developer naming the lane.
- *Negative / Risks:* A host that swallows `/btw` still will not enter `ask`. That limit is written, not papered over.
- *Follow-ups:* None.
