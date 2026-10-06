---
type: log-entry
date: 2026-10-05
slug: enforce-conduct-delegation
kind: work-closure
depth: design
adr: ADR-013 (proposed)
---

# Conduct dispatches available subagents

## What happened

Conduct now dispatches callable roles after checking runtime capability and required tools. Independent analysts and safe executor tasks can run concurrently; busy capacity queues work instead of prompting inline fallback. Design-depth validation uses `verify`, while doctor reports detected agent files separately from runtime availability.

## Criteria delivered

None — design depth; done = plan scope + gate.

## Phases executed

| # | Theme | Notable result |
|---|---|---|
| 1 | Reliable role delegation | Updated conduct/README guidance, generic and OpenCode verifiers, doctor inventory, and 13 delegation eval fixtures. |

## Decisions and deviations

T-005 and T-006 added for small contract and worked-example corrections found in review; approved scope did not change. Verification accepts evidence-based source inspection for static deliverables; unexercised behavior remains not verifiable. The eval fixtures were not model-replayed. No gate checks were waived.

## ADR proposals & brain updates

**Proposed — ADR-013: Require callable-role dispatch in conduct.**

- **Context:** Delegation was optional even when the runtime exposed the role and its prerequisites were satisfied. Doctor's filesystem scan also implied runtime availability without evidence.
- **Decision:** Conduct dispatches each applicable callable first-party role after checking prerequisites. It records concrete per-role/task blockers when work must run inline, queues temporary capacity exhaustion, and preserves dependency, file ownership, and single-writer safeguards. Doctor reports definition detection separately from runtime invocation, which conduct checks directly.
- **Consequences:** Independent analyst work and file-disjoint executor tasks can run concurrently; design-depth scope receives verifier review. Missing tools/roles and actual dispatch failures remain visible with evidence. The verifier and coordinator preserve command provenance and their separate gate responsibilities.
- **Alternatives:** Always run sequentially (loses the approved concurrency benefit); infer runtime availability from installed files (unsupported by the shell probe).

Enact this proposal with `jaiba-init:update-brain`. No other memory changes are proposed.

## Pointers

- [Conduct delegation contract](../../../skills/conduct/references/subagents.md)
- [Doctor tool-state report](../../../skills/doctor/references/tool-state.md)
- [Prior authorized-agent execution log](2026-10-05-contract-authorized-agent-execution.md)

## Suggested final commit

```
fix(conduct): require available subagent delegation

Dispatch callable roles by default and run independent analyses and executor tasks concurrently within the existing safety limits.
Add design-depth verification and clarify doctor runtime reporting.
```

## Gate at close

Pass. Phase and Plan Gate checks passed: eval JSON/unique IDs, shell syntax, description lengths, contract/version lockstep, pinned workflow actions, doctor probe (0 missing tools), injection probe (4 rejected entries; no unsafe markers), citation review, dual-layout fixture exercise, and clean diff formatting. Independent verification confirmed all six plan scope items. No model-based eval replay was run.
