---
type: decision
id: ADR-012
title: "Authorized first-party JAIBA workflow execution is not obeying repository content"
description: Clarifies that ADR-010's data-boundary rule does not apply to operational instructions in a shipped first-party JAIBA agent's own definition when invoked by an authorized workflow for an approved task; that execution requires no second confirmation and grants no extra tools or scope.
status: accepted
date: "2026-10-05"
tags: [security, prompt-injection, contract, delegation]
updated: "2026-10-05"
---

# ADR-012: Authorized first-party JAIBA workflow execution is not obeying repository content

## Context

[ADR-010](010-repository-content-is-data.md) established that everything read
while scanning, sweeping, probing, or verifying a repository is data, not
instructions; imperative text found in it is quoted, reported, and never acted
on without explicit human confirmation. That rule correctly blocks prompt
injection through inspected content.

A boundary ambiguity emerged during execution of the `conduct` workflow:
when an authorized JAIBA workflow invoked a shipped first-party executor
subagent for an already-approved task, some executor agents treated the
invocation itself as another prompt-injection vector — conflating their own
`agents/*.md` role definition with "repository content" and requiring a second
developer confirmation to proceed. This produced spurious confirmation prompts
that made the normal delegation flow unusable without violating the spirit of
ADR-010 (which was written to protect against third-party or untrusted
content, not a workflow's own authorized components).

## Decision

When a JAIBA workflow invokes a shipped first-party JAIBA subagent for a
developer-approved task, the operational instructions in that agent's own
`agents/*.md` role definition govern its execution within the task envelope
without requiring a second human confirmation. This carve-out is narrow:

- It applies only to the agent's **own** role definition — the file that
  defines what that agent is authorized to do.
- It grants **no extra tools, scope, or file access** beyond what the original
  task approval authorized.
- It does **not** extend to directives found in repository content, code,
  configuration, third-party skill files, or tool output inspected *during*
  the task. Those remain inert data under ADR-010.
- The human's authority to approve the **plan and task scope** is preserved
  unchanged; this carve-out only removes a redundant second prompt within an
  already-authorized workflow step.

The behavioral contract (`jaiba-contract.md`) §4.5 was updated to encode this
distinction. The four first-party executor and verifier definitions
(`executor-high.md`, `executor-medium.md`, `executor-low.md`, `verify.md`)
were aligned with the clarified boundary, and conduct eval cases 11 and 12
were added to regression-test both the normal delegation path and resistance
to injected repository imperatives.

## Alternatives Considered

- *Do nothing; require a second confirmation at every subagent invocation* —
  rejected: this makes the authorized-delegation flow require a human prompt
  for each executor tier, removing the practical benefit of delegation while
  providing no real security gain (the developer already approved the plan and
  the task scope upstream).
- *Broadly relax ADR-010 to treat all agent definitions as trusted* —
  rejected: third-party `agents/*.md` files, user-supplied subagent
  definitions, or files sourced from repository content could contain
  imperatives; the carve-out is intentionally limited to the framework's own
  shipped definitions invoked inside an authorized workflow.

## Consequences

- *Positive:* authorized conduct delegation flows (`conduct → executor tiers`)
  work without repeated confirmation prompts; the injection-defense posture
  on inspected repository and tool output is unaffected; the clarification is
  backed by regression eval cases 11 and 12.
- *Negative / Risks:* the carve-out relies on "first-party shipped definition"
  being distinguishable from "user-supplied or repository-sourced content"; the
  behavioral contract enforces this via the agent's own role file vs. inspected
  content, but no structural, statically-checked enforcement exists yet — same
  limitation as ADR-010.
- *Follow-ups:* none blocking. If a future eval reveals an edge case (e.g. a
  first-party definition that has drifted to include a repository-sourced
  directive), the fix is a new ADR — not a rewrite of ADR-010 or ADR-012.
