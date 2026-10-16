---
type: log-entry
date: 2026-10-15
slug: model-discovery-and-github-releases
kind: work-closure
depth: design
adr: none
---

# Validated agent models and automated GitHub releases

## What happened

`jaiba-configure` now specifies host-verified CLI-first model discovery with constrained ACP fallback, shared by initial selection and exact-ID migration. The bump workflow now publishes a generated-notes GitHub Release for the exact new tag after push, with no-bump, duplicate, failure, and retry handling.

## Criteria delivered

None — design depth; completion is the approved plan scope plus its gate.

## Phases executed

| # | Theme | Notable result |
|---|---|---|
| 1 | Model discovery | Shared CLI→ACP validation policy and seven model/migration evals. |
| 2 | GitHub Releases | Run-specific tag recovery, post-push release publication, and isolated harness. |
| 3 | Verification | Release harness 8/8; repo-wide Plan gate passed. Model behavior was statically reviewed, not exercised against a live host. |

## Decisions and deviations

CLI catalogs are authoritative when valid; ACP is only an eligible fallback, and no verifiable catalog means no new pin. Release retries identify the exact run's annotated tag; API/authentication failures remain failures. No scope deviations or gate waivers. Live model behavior, remote publication, and effective App permissions were not verified locally.

## ADR proposals & brain updates

No ADR proposed; implementation decisions were tactical. Propose a new `reference` concept for host model discovery across CLI/ACP, and update the existing GitHub Actions reference with release publication behavior. Enact both only through `jaiba-init:update-brain`.

## Pointers

- Commits: `79ef0a2` (skills/evals), `d587ee9` (CI/CD/harness).
- Consulted concepts: [architecture](../identity/architecture.md), [conventions](../identity/conventions.md), [quality gate](../identity/quality-gate.md), [Commitizen](../references/commitizen.md), [GitHub Actions](../references/github-actions.md).

## Suggested final commit

Suggested squash target only; no additional commit created:

```
feat(release): validate agent models and publish GitHub releases
```

## Gate at close

Pass — nine design-scope targets met; release harness 8/8; Phase and Plan gates passed. Runtime and remote verification limits are recorded above.
