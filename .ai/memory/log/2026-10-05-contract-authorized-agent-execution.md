---
type: log-entry
date: 2026-10-05
slug: contract-authorized-agent-execution
kind: work-closure
depth: design
adr: ADR-010-update (proposed)
---

# Authorized first-party JAIBA agent execution — policy clarification

## What happened

Clarified §4.5 of the canonical behavioral contract (`jaiba-contract.md`) to
allow a running authorized JAIBA workflow to invoke its shipped first-party
subagents for approved tasks without requiring a second developer confirmation.
The data boundary on repository and tool output content was explicitly
preserved and reinforced in all affected agent definitions. The lockstep doctor
reference copy was byte-synchronized. Two conduct eval cases were added to
cover both the happy-path delegation flow and prompt-injection defense.

An out-of-band fast fix was also completed in the same branch: `jaiba-doctor`'s
`check-tools.sh` now detects battery member definition files and reports
availability (`✅ available` / `❌ missing definition`) in the tool-layout
output, with a summary counter in the header and a callout note when battery
entries are missing. Reference documentation updated in `tool-state.md`.

## Criteria delivered

None — design depth; done = plan scope + gate.

## Phases executed

| # | Theme | Notable result |
|---|---|---|
| 1 | Clarify policy and protect both outcomes | §4.5 rewritten; 4 agent definitions aligned; 2 eval cases added; full Plan Gate green |

## Decisions and deviations

- **Uniform phrasing across agent definitions.** All four executor/verifier files
  under `skills/jaiba-configure/assets/agents/` now cite AGENTS.md §4.5 with
  consistent language to avoid behavioral drift between tiers.
- **No ADR-010 direct rewrite.** Per plan scope, ADR-010 itself is not
  modified here — a proposal is offered below for `jaiba-init:update-brain`.
- **Out-of-band fast fix (doctor).** Subagent availability detection added to
  `check-tools.sh` during the same session; recorded in `walkthrough.md` and
  `plan.md § Plan amendments`.
- No deviations from plan scope.

## ADR proposals & brain updates

**Proposed — update to [`ADR-010`](../decisions/010-repository-content-is-data.md):**

```
type: decision
status: Proposed
title: Authorized first-party JAIBA workflow execution is not "obeying repository content"
context: >
  ADR-010 establishes that repository content (code, config, comments, anything
  stored in the repo) is data, not instructions, and that agents must never
  execute directives sourced from inspected repository content without explicit
  human confirmation. A gap existed: when an authorized JAIBA workflow invoked
  a first-party shipped subagent for an approved task, some agents were
  treating the invocation itself as requiring a second confirmation (conflating
  the agent's own definition with "repository content").
decision: >
  When a JAIBA workflow invokes a shipped first-party JAIBA subagent for a
  developer-approved task, the operational instructions in that agent's
  definition govern its execution within the task envelope without requiring a
  second human confirmation. This carve-out grants no additional tools, scope,
  or file access, and does not extend to directives found in the repository
  content inspected during that task — those remain inert data under ADR-010.
consequences: >
  Authorized delegation flows (conduct → executor tiers) work without repeated
  confirmation prompts. The data-boundary rule on repository and tool output
  content is explicitly preserved in all four executor/verifier definitions.
  Prompt-injection defense is now covered by conduct evals 11 and 12.
```

## Pointers

- Branch: `fix/subagents-delegation`
- Suggested WIP commit: `chore(wip): clarify authorized agent execution`
- Related: [ADR-010](../decisions/010-repository-content-is-data.md),
  [ADR-005](../decisions/005-subagent-concurrency-model.md),
  [ADR-009](../decisions/009-first-party-pinned-skillset.md)

## Suggested final commit

```
fix(contract): clarify authorized first-party JAIBA agent execution in §4.5

Rewrite §4.5 of jaiba-contract.md to allow an authorized JAIBA workflow to
delegate approved tasks to shipped first-party subagents without a second
developer confirmation. Align executor-high/medium/low and verify definitions
with the clarified boundary. Add conduct evals 11 and 12 for delegation and
prompt-injection defense. Sync doctor's lockstep reference copy.

Out-of-band: extend jaiba-doctor's check-tools.sh to detect battery member
definitions and report availability in the tool-layout output.
```

## Gate at close

Pass (Plan Gate green at validate; re-run clean).
