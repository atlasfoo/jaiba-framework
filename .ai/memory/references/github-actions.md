---
type: reference
title: "GitHub Actions (release automation)"
description: Two workflows — bump.yml (push to master, creates a version tag and generated-notes GitHub Release via a GitHub App) and commit-check.yml (PR, validates Conventional Commits) — both with every `uses:` pinned by full commit SHA.
tier: workflow
kind: tooling
role: —
resource: "CI config at `.github/workflows/bump.yml`, `.github/workflows/commit-check.yml`"
tags: [tooling, ci, release]
updated: "2026-10-15"
---

# GitHub Actions (release automation)

## What it is

GitHub's native CI, scoped in this repo to exactly the release
process — not a general build/test pipeline (this repo has no
build or test suite to run; see
[identity/quality-gate.md](../identity/quality-gate.md)).

## How the project uses it

Two workflows:

- **`bump.yml`** — triggers on push to `master` and avoids re-triggering
  on its own output by checking whether the triggering commit author's
  GitHub username ends in `[bot]`. It mints a token via
  `actions/create-github-app-token`, checks out with `fetch-depth: 0`,
  installs commitizen, and runs `cz --no-raise 21 bump --yes` with an
  annotated tag identifying the workflow run and source SHA. A real bump
  atomically pushes the commit and exact new tag before creating a GitHub
  Release with `gh release create <tag> --verify-tag --title <tag>
  --generate-notes`; no-bump runs stop without publishing. On retry, the
  run-specific tag is recovered without another bump. A successful
  paginated release listing prevents duplicates; API/authentication
  failures are not treated as absence. See
  [Commitizen](commitizen.md) for version computation.
- **`commit-check.yml`** — triggers on `pull_request` to `master` and
  runs `cz check` twice: against the PR's commit range, and against
  the PR title, which arrives via `env:` and is never interpolated
  directly into a `run:` step — interpolating
  `${{ github.event.pull_request.title }}` into shell is a known
  script-injection vector, and this workflow exists specifically to
  enforce the commit convention that [ADR-011](../decisions/011-commitizen-single-version-source.md)
  relies on, so it does not itself introduce the injection class
  [ADR-010](../decisions/010-repository-content-is-data.md) is about.

The App token is used for checkout, push and release API calls. The
workflow's `permissions: contents: read` applies to `GITHUB_TOKEN`; it
does not grant permissions to the separate App token. The App installation
must have the required Contents write permission and branch-protection
access configured by the maintainer.

## How to consult it

Read the two workflow files directly, or check the repository's
Actions tab for run history.

## Gotchas

Every `uses:` step in both workflows is pinned to a 40-hex-character
commit SHA, never a tag or branch — a supply-chain hardening measure
the Quality Gate enforces (`identity/quality-gate.md`'s
*actions pinned by SHA* check). Updating an action means re-resolving
its SHA for the new version (e.g. via `gh api`), not just bumping a
version string. The App's required write and ruleset-bypass permissions
are maintainer-configured account settings this automation depends on
but does not create. Real release publication and effective App
permissions must be verified in CI; local mocked tests do not establish
them.
