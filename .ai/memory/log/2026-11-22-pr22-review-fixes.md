---
type: log-entry
date: 2026-11-22
slug: pr22-review-fixes
kind: work-closure
depth: design
adr: none
---

# PR #22 Adversarial Review Fixes

## What happened

Resolved all 13 findings (4 High, 6 Medium, 3 Low) from the Adversarial Review Report on PR #22 (`fix/memory-migration`), aligning Step 0 `filesystem` pin short-circuiting, the local `filesystem` `v2` routing-sync exception for `ask` and `jaiba-doctor`, instrumented-only `.atl/framework-version.json` freshness checks, `migrate-mode` Notice 2 direct Step 9 entry, `category: memory-surface` selection rules, `1.1.0` receipt stamping in `archive.sh`, evals, fixtures, and documentation.

## Criteria delivered

None — design depth; done = plan scope + gate.

## Phases executed

| # | Theme | Notable result |
|---|---|---|
| 1 | Contract, Root Marker, and Surface Resolution | Updated both lockstep `jaiba-contract.md` copies, `resolution.md`, and root `AGENTS.md` (`H-1`, `H-2`, `H-3`, `M-1`, `M-5`). |
| 2 | Skill References, Subagent Assets, and `archive.sh` | Aligned `ask`, `doctor`, `conduct`, `jaiba-init`, `opencode/code-analyst.md`, and `archive.sh` `1.1.0`/`1.0.0` receipt handling (`H-1`, `H-4`, `M-1`–`M-6`, `L-3`). |
| 3 | Evals, Fixtures, and Reader Docs | Aligned `jaiba-init/evals/evals.json`, `selection-cases.json`, `README.md`, and `jaiba-configure/SKILL.md` (`M-2`, `L-1`, `L-2`). |

## Decisions and deviations

- **H-1 (Read-only routing-sync exception):** Permitted `ask` and `jaiba-doctor` to auto-generate missing local `filesystem` `v2` bindings when `AGENTS.md` already pins `filesystem` over `index.md` (mirroring `.atl/` in `doctor`), while forbidding external binding or memory mutations.
- **M-1 (Daily version check):** Scoped `.atl/framework-version.json` to JAIBA-instrumented projects only after guaranteeing `.atl/` exclusion, sourcing local versions from `SKILL.md`/`skillset.txt`, querying via `git ls-remote` (`curl` fallback), and standardizing `checked_at`/`local_version`/`latest_remote_tag`.
- **M-5 (`category: memory-surface` alignment):** Removed stale `jaiba-engram-memory` draft-category sentences across contract and skill references to match `skills/jaiba-engram-memory/SKILL.md`.
- **Deviations:** None; `code-analyst` and `business-analyst` were kept inline at triage/spec because `.atl/tool-layout.md` marked `rg` missing (later verified present by `check-tools.sh`).

## ADR proposals & brain updates

No ADR proposed; all decisions were tactical alignments implementing [ADR-019](../decisions/019-proactive-memory-migration.md).

## Pointers

- Commit `80c177e` on `fix/memory-migration` (PR #22), verified against [quality-gate.md](../identity/quality-gate.md) and [conventions.md](../identity/conventions.md).
- Follows prior closure [2026-11-17-proactive-memory-migration.md](2026-11-17-proactive-memory-migration.md).

## Suggested final commit

```
fix(memory): resolve PR #22 adversarial review findings

Align Step 0 filesystem pin precedence, read-only v2 routing-sync
exception, instrumented-only daily version check, Notice 2 Step 9
migration entry, 1.1.0 archive receipts, evals, and docs.
```

## Gate at close

Pass — Phase Gate, Plan Gate (`check-tools.sh`, injection fixture probe, `archive.sh` `1.1.0`/`1.0.0` smoke test, `cz check`), and `verify` (`SCOPE-01`–`SCOPE-11` met) all green.

<!-- jaiba-close-v1
contract jaiba-memory-surface 1.1.0
binding filesystem
project prj-c4e91b7a2d06
context ctx-8f2a71e04c3b
scope d2b21f774988598d197607a79a0a4cbabdd30ca1
close 2026-11-22-pr22-review-fixes
body 101617eb68fd9ba0a99d678e5289573b17317f00
plan.md 662a34fe43d0fbd0be86c60eb51e4a1f64edc96a
tasks.md 6854300dc2ed0b7dabce3d0f5655463dd8dc0148
walkthrough.md bc9d08877e34bb1c06f3cf57dd290ccbdf116be8
PRD.md absent
.gitignore absent
-->
