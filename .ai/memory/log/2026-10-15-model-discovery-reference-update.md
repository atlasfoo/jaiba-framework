---
type: log-entry
date: 2026-10-15
slug: model-discovery-reference-update
kind: brain-change
adr: none
---

# Model discovery and release references recorded

## What happened

Added the `reference` concept for host model discovery across CLI and ACP, updated the GitHub Actions reference to describe run-specific tags and GitHub Release publication, and regenerated the memory index. The trigger was the proposal in the [work-closure entry](2026-10-15-model-discovery-and-github-releases.md).

## Decisions and deviations

The discovery surface is workflow tooling, not a runtime dependency; its reference points to the public ACP protocol/schema and the detected host's version-specific CLI documentation. No ADR was proposed or enacted. The GitHub Actions reference now distinguishes the App token's permissions from `GITHUB_TOKEN` and records local verification limits.

## Pointers

- [Model discovery reference](../references/model-discovery.md)
- [GitHub Actions reference](../references/github-actions.md)
- [Memory index](../index.md)
- Source implementation: `skills/jaiba-configure/references/model-discovery.md` and `.github/workflows/bump.yml`.
