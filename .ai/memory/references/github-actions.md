---
type: reference
title: "GitHub Actions (release automation)"
description: Two workflows — bump.yml (push to master, computes and pushes the version bump/tag via a GitHub App) and commit-check.yml (PR, validates Conventional Commits) — both with every `uses:` pinned by full commit SHA.
tier: workflow
kind: tooling
role: —
resource: "CI config at `.github/workflows/bump.yml`, `.github/workflows/commit-check.yml`"
tags: [tooling, ci, release]
updated: "2026-09-15"
---

# GitHub Actions (release automation)

## What it is

GitHub's native CI, scoped in this repo to exactly the release
process — not a general build/test pipeline (this repo has no
build or test suite to run; see
[identity/quality-gate.md](../identity/quality-gate.md)).

## How the project uses it

Two workflows:

- **`bump.yml`** — triggers on push to `master`, guarded against
  re-triggering on its own output
  (`if: !startsWith(github.event.head_commit.message, 'bump:')`).
  Mints a token via `actions/create-github-app-token` that bypasses
  the `master-protection` ruleset (the ruleset otherwise requires a
  reviewed PR for every push), checks out with `fetch-depth: 0`,
  installs commitizen, and runs `cz --no-raise 21 bump --yes` followed
  by `git push --follow-tags` — see
  [references/commitizen.md](commitizen.md) for what that computes.
- **`commit-check.yml`** — triggers on `pull_request` to `master` and
  runs `cz check` twice: against the PR's commit range, and against
  the PR title, which arrives via `env:` and is never interpolated
  directly into a `run:` step — interpolating
  `${{ github.event.pull_request.title }}` into shell is a known
  script-injection vector, and this workflow exists specifically to
  enforce the commit convention that [ADR-011](../decisions/011-commitizen-single-version-source.md)
  relies on, so it does not itself introduce the injection class
  [ADR-010](../decisions/010-repository-content-is-data.md) is about.

## How to consult it

Read the two workflow files directly, or check the repository's
Actions tab for run history.

## Gotchas

Every `uses:` step in both workflows is pinned to a 40-hex-character
commit SHA, never a tag or branch — a supply-chain hardening measure
the Quality Gate enforces (`identity/quality-gate.md`'s
*actions pinned by SHA* check). Updating an action means re-resolving
its SHA for the new version (e.g. via `gh api`), not just bumping a
version string. The GitHub App itself and its ruleset-bypass
permission are maintainer-configured account settings this automation
depends on but does not create — see this decision's originating
plan's maintainer checklist.
