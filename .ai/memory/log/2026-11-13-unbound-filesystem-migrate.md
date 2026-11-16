---
type: log-entry
date: 2026-11-13
slug: unbound-filesystem-migrate
kind: work-closure
depth: spec
adr: none
---

# Allow explicit `migrate-surface` from an unbound coherent filesystem brain after a closed identity lookup

## What happened

Defined a mandatory closed-result identity lookup (`hit`, `authoritative-miss`, `blocked`) in [resolution.md](../../../skills/create-memory/references/resolution.md) and its Engram realization in [engram-mapping.md](../../../skills/jaiba-engram-memory/references/engram-mapping.md) and [SKILL.md](../../../skills/jaiba-engram-memory/SKILL.md) (sibling binding sweep, `mem_list_projects`/`mem_current_project`, exact `topic_key` or catalogue-alias probe on known locators, without `mem_search` fuzzy absence claims or a new `reg/` key). Updated [surface-migration.md](../../../skills/jaiba-init/references/surface-migration.md) and [migration-journal-template.md](../../../skills/jaiba-init/assets/migration-journal-template.md) so an explicit `migrate-surface` request after `authoritative-miss` accepts a coherent `.ai/memory/` brain (`bundle` or `legacy`, real prose) as `source-authority: filesystem-unbound` under a stable source-local path segment (`fs-` + first 16 hex of `sha256(canonical work root)`), without writing a filesystem binding or adding any gate before `MSV-011`.

## Criteria delivered

- `UNBD-001` — Origen filesystem sin binding — delivered
- `UNBD-002` — Cerebro no coherente bloquea — delivered
- `UNBD-003` — Hit exacto no crea segundo cerebro — delivered
- `UNBD-004` — Lookup con resultado cerrado — delivered
- `UNBD-005` — Sin puerta nueva ni reorden — delivered

## Phases executed

| # | Theme | Notable result |
|---|---|---|
| 1 | Closed identity lookup result | Added closed lookup outcome (`hit`, `authoritative-miss`, `blocked`) to `create-memory`, realized the 4-step Engram lookup recipe without a new `reg/` key, scoped "no locator = unresolved bootstrap" to already-named locators, and added eval 13 in `jaiba-engram-memory`. |
| 2 | Unbound filesystem migrate source | Added `filesystem-unbound` source handling after `authoritative-miss` in `surface-migration.md`, added `filesystem-unbound` fields and `fs-<16 hex>` source-local path segment to `migration-journal-template.md`, and added evals 32 and 33 in `jaiba-init`. |

## Decisions and deviations

- **Catalog alias match in step 3 of Engram lookup:** Included exact catalogue-alias matching alongside exact `topic_key` probing on known locators so registered brains recorded in catalogue aliases return `hit` as required by `UNBD-003` and [ADR-014](../decisions/014-pluggable-memory-surfaces-v1-1-architecture.md).
- **Source-local transaction path segment:** Defined the `fs-` segment as `fs-` plus the first 16 lowercase hexadecimal characters of the full SHA-256 of the canonical work root, kept stable across retries and never renamed after staging mints the registry `project-id`.
- **Deviations from plan/PRD:** None.
- **Waived gate checks:** None.

## ADR proposals & brain updates

No ADR proposed; all decisions were tactical realizations of [ADR-014](../decisions/014-pluggable-memory-surfaces-v1-1-architecture.md) and the existing [Engram MCP](../references/engram-mcp.md) surface boundary.

## Pointers

- [identity/architecture.md](../identity/architecture.md)
- [identity/conventions.md](../identity/conventions.md)
- [identity/scope.md](../identity/scope.md)
- [identity/quality-gate.md](../identity/quality-gate.md)
- [ADR-014](../decisions/014-pluggable-memory-surfaces-v1-1-architecture.md)
- [Engram MCP](../references/engram-mcp.md)

## Suggested final commit

```
feat(memory): allow unbound filesystem source in migrate-surface after closed lookup

Require a closed-result identity lookup (hit, authoritative-miss, blocked)
when no binding v2 exists, realize the exact lookup recipe in
jaiba-engram-memory, and let explicit jaiba-init:migrate-surface requests
export a coherent unbound .ai/memory brain after authoritative-miss using
a source-local fs-<16hex> journal segment without writing a filesystem
binding or adding a pre-cutover prompt.
```

## Gate at close

Pass

<!-- jaiba-close-v1
contract jaiba-memory-surface 1.0.0
binding filesystem
project prj-c4e91b7a2d06
context ctx-8f2a71e04c3b
scope d2b21f774988598d197607a79a0a4cbabdd30ca1
close 2026-11-13-unbound-filesystem-migrate
body e3209c6d3b4dcf9ad250332ed393b1cdf976856b
plan.md a84a7c1ec8051cbde34ce5da0c5c04d4d5dbfcde
tasks.md 3cb26a539e5f8f4438797a78c280914cf338ba6c
walkthrough.md be2e2d45d05739aaab76ee261479403ad300a28a
PRD.md 9109ab9ba53da34080698661b69e8f47c32c414f
.gitignore absent
-->
