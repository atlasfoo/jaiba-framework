---
type: log-entry
date: 2026-11-24
slug: global-ssot-multiagent-orchestration
kind: work-closure
depth: spec
adr: "ADR-020, ADR-021"
---

# Global SSOT (`~/.jaiba/`) and multi-agent orchestration

## What happened

Replaced isolated per-agent JAIBA installs with a single machine **Global SSOT at `~/.jaiba/`** (`config.yaml`, `mappings.yaml`, `contract/jaiba-contract.md`, `skills/`, `agents/base/*.md`) projecting native wrappers and contract links to `enabled: true` hosts (`N >= 1`) via a pure Python 3 stdlib projector/harvester (`skills/jaiba-configure/scripts/jaiba_ssot.py`) and modular host caveats (`skills/jaiba-configure/references/caveats/*.md`). Extended `jaiba-doctor` (`check-tools.sh`, Layer 0, and MCP readiness matrix), atomic `temp + rename` Step 0 `v2` bindings, and `conduct` multi-agent orchestration Patterns 1–3 (task `affinity:` hints, Coordinator + bounded worktree Workers `/conduct execute T-NNN`, and optional cross-agent CLI/ACP bridge dispatch).

## Criteria delivered

- `ADE-001` — Global SSOT at `~/.jaiba/` and multi-host projection (`N >= 1`) — delivered
- `ADE-002` — Lossless automatic migration (`harvest-legacy`) from per-agent setups — delivered *(corrective adapter test `T-013`)*
- `ADE-003` — Modular per-agent caveats catalog in `jaiba-configure` — delivered *(corrective metadata prose cleanup `T-013`)*
- `ADE-004` — Multi-host `jaiba-doctor` diagnostics and atomic `v2` binding writes — delivered *(corrective runtime test suite `T-013`)*
- `ADE-005` — Pattern 1: `host/tier` affinity projection in `tasks.md` and phase handoff — delivered
- `ADE-006` — Pattern 2: Parallel git-worktree execution under single-writer Coordinator and bounded Workers (`/conduct execute T-NNN`) — delivered
- `ADE-007` — Pattern 3: Cross-agent subagent dispatch via optional CLI/ACP bridge — delivered

## Phases executed

| # | Theme | Notable result |
|---|---|---|
| 1 | `~/.jaiba/` SSOT, caveats, `jaiba_ssot.py` | 8 caveat files, stdlib projector/harvester, removed static `opencode/` agent fork |
| 2 | Lockstep contract, atomic `v2` bindings, multi-host doctor | Lockstep `jaiba-contract.md`, atomic `temp + rename`, `Host Projections` + MCP `⚠️ Degraded` |
| 3 | `conduct` multi-agent Patterns 1, 2, 3 | `affinity:` hints, `Worktree Worker Link` + `/conduct execute T-NNN`, CLI/ACP bridge fallback |
| 4 | Evals, rehearsal fixtures, unit suites (`+ T-013`) | Updated all skill evals, `reviewed-source-drift.json`, `test_jaiba_ssot.py`, `test_check_tools.py` |

## Decisions and deviations

- **Pure stdlib YAML subset (`jaiba_ssot.py` & `check-tools.sh`):** Rejects tabs, duplicate keys, anchors/aliases, YAML tags, and `..` path traversal under [ADR-010](../decisions/010-repository-content-is-data.md) §4.5, honoring [architecture.md](../identity/architecture.md) zero-external-dependency rules.
- **Corrective task `T-013` after Validation Run 1:** Initial `verify` flagged `ADE-004` as `not verifiable` due to missing automated tests for `check-tools.sh`'s multi-host `config.yaml` branches; added `skills/doctor/evals/test_check_tools.py` (`4` tests), `memory-adapters` coverage in `test_jaiba_ssot.py` (`9` tests), and caveat metadata bullet cleanup before Run 2 passed 7/7 `met`.
- **Single-writer & Pattern 3 safety:** Bounded worktree workers resolve Coordinator context strictly read-only (`executive.role: worker`), and failed CLI/ACP bridges audit `git status`/`git diff` for partial writes before falling back to native subagents or inline execution.

## ADR proposals & brain updates

- **Proposed `ADR-020` (`type: decision`, `status: Proposed`):** *Global machine SSOT (`~/.jaiba/`) and multi-host projection* — evolves [ADR-007](../decisions/007-global-repo-local-setup-split.md); replaces standalone per-agent silo writes with `~/.jaiba/` canonical assets projected to `enabled: true` hosts via `jaiba_ssot.py` and `references/caveats/*.md`.
- **Proposed `ADR-021` (`type: decision`, `status: Proposed`):** *Multi-agent orchestration patterns and atomic `v2` bindings* — extends [ADR-005](../decisions/005-subagent-concurrency-model.md) and [ADR-014](../decisions/014-pluggable-memory-surfaces-v1-1-architecture.md) with `tasks.md` `affinity:` hints, Coordinator + bounded worktree Workers (`/conduct execute T-NNN`), optional CLI/ACP bridge dispatch, and same-directory `temp + rename` `v2` persistence.
- **Proposed `quality-gate` & `reference` updates (`jaiba-init:update-brain`):** Add the 3 Python stdlib suites (`conduct/evals`, `jaiba-configure/evals`, `doctor/evals`) to [quality-gate.md](../identity/quality-gate.md) and index `Multi-agent orchestration & SSOT projection`.

## Pointers

- Branch `feature/ade-compatibility` (`a19420b`, `f480ea9`, `f9ac697`, plus Phase 4 / `T-013` working tree)
- Related logs: [2026-11-17-proactive-memory-migration.md](2026-11-17-proactive-memory-migration.md), [2026-11-22-pr22-review-fixes.md](2026-11-22-pr22-review-fixes.md)
- Governing refs: [quality-gate.md](../identity/quality-gate.md), [ADR-006](../decisions/006-index-everything-toolchain-probe.md), [ADR-012](../decisions/012-authorized-first-party-agent-execution.md), [ADR-015](../decisions/015-native-plan-input.md), [ADR-017](../decisions/017-documented-effort-only.md), [ADR-019](../decisions/019-proactive-memory-migration.md), [model-discovery.md](../references/model-discovery.md), [engram-mcp.md](../references/engram-mcp.md)

## Suggested final commit

```
feat!: migrate jaiba-configure to global ~/.jaiba/ SSOT and multi-agent orchestration

Replace standalone per-agent silo installs with ~/.jaiba/ SSOT projection,
lossless legacy harvesting, modular host caveats, multi-host jaiba-doctor,
atomic Step 0 v2 bindings, and conduct Patterns 1-3 (affinity, worktree
workers, and optional CLI/ACP bridge).

BREAKING CHANGE: jaiba-configure no longer writes standalone per-agent silos
(adds python3 requirement and removes static assets/agents/opencode/ fork);
existing setups migrate losslessly via harvest-legacy.
```

## Gate at close

Pass — Phase/Plan Gate green, 38/38 Python tests (`4` doctor + `9` jaiba-configure + `25` conduct), injection probe `Rejected (failed validation): 4`, `verify` Run 2 7/7 `delivered`.

<!-- jaiba-close-v1
contract jaiba-memory-surface 1.1.0
binding filesystem
project github.com/atlasfoo/jaiba-framework
context ctx-0d0e6bae406e4f19
scope 46f63e43a6611999bfea088e2247f7288cd5e4f3
close 2026-11-22-global-ssot-multiagent-orchestration
body 7149ca78a6327edcb6bc2c0c4764d12fda70e985
plan.md a20a37070bc07d3b488504a4dd765fe94c0c2182
tasks.md d3b6e20ad7860bdd6be3c4852885cdfe831500b9
walkthrough.md b80a46f8247476541c41cae311d578bd21eeda1f
PRD.md 59fe24a291796f5bc5fe07ada83c7b1291eac58b
.gitignore absent
-->
