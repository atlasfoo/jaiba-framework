---
type: log-entry
date: 2026-10-05
slug: opencode-configure-update
kind: work-closure
depth: spec
adr: ADR-013 (proposed)
---

# OpenCode agents and targeted configure updates

## What happened

`jaiba-configure` now installs six OpenCode-native subagents and offers
targeted contract or battery refreshes. Battery update also supports
exact model-ID migration across JAIBA agents while protecting divergent
files and leaving unrelated configuration untouched.

## Criteria delivered

- CONF-001 — Install OpenCode-native subagents — delivered
- CONF-002 — Refresh one selected configure target — delivered
- CONF-003 — Replace an exact model ID across the battery — delivered
- CONF-004 — Protect customized files during packaged refresh — delivered

## Phases executed

| # | Theme | Notable result |
|---|---|---|
| 1 | OpenCode subagent support | Six native definitions; host-aware battery selection and evals. |
| 2 | Targeted configure updates | Contract/battery refresh, drift protection, exact model migration and evals. |

## Decisions and deviations

Model migration searches only the six known JAIBA agent filenames in the
detected host's agent directory. No plan deviations or gate waivers.
Consulted [architecture](../identity/architecture.md),
[conventions](../identity/conventions.md), [scope](../identity/scope.md),
[quality gate](../identity/quality-gate.md), and
[ADR-007](../decisions/007-global-repo-local-setup-split.md).

## ADR proposals & brain updates

- **ADR-013 — Host-specific JAIBA agent assets (Proposed).** Keep native
  agent formats in host-specific asset sets selected during configure.
  This avoids emitting invalid cross-host definitions; the trade-off is
  maintaining parallel packaged files. Alternative: generate each host's
  format from a shared intermediate definition.
- **Reference proposal:** add OpenCode Markdown agent configuration as a
  `reference` concept through `jaiba-init:update-brain`:
  https://opencode.ai/docs/agents/

## Pointers

- [PR #14](https://github.com/atlasfoo/jaiba-framework/pull/14)
- Commit `4d716d0` (to be amended with this closure entry)

## Suggested final commit

```text
feat(configure): add OpenCode agents and targeted updates
```

## Gate at close

Pass — repository gates, injection probe, and GitHub commit check passed.
The local OpenCode CLI load check could not start because it could not
open its global log file; static frontmatter and permission checks passed.
