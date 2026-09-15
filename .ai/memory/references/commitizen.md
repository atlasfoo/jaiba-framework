---
type: reference
title: "commitizen"
description: Computes the framework's single version from Conventional Commits and keeps skills/*/SKILL.md, skillset.txt's ref:, and README.md in lockstep via .cz.toml's version_files.
tier: workflow
kind: tooling
role: —
resource: "CLI `cz` (installed in CI via `pip install commitizen==4.18.1`) / config at `.cz.toml`"
tags: [tooling, release, versioning]
updated: "2026-09-15"
---

# commitizen

## What it is

A Python CLI (`cz_conventional_commits` provider) that computes a
semver bump from the Conventional Commits made since the last tag,
rewrites every file/regex pair declared in `version_files`, and
updates `CHANGELOG.md`. Not a general linter — its only job here is
computing and propagating the framework's single version.

## How the project uses it

`.cz.toml` pins the initial baseline `version = "2.1.0"`,
`version_scheme = "semver2"`, `tag_format = "v$version"`, and
`update_changelog_on_bump = true`. Its `version_files` keeps three
things in lockstep on every bump: every `skills/*/SKILL.md`'s
`^version:` line, `skills/jaiba-configure/assets/skillset.txt`'s
`^ref:` line, and `README.md`'s `jaiba-framework#v` pinned install
line. `.github/workflows/bump.yml` (see
[references/github-actions.md](github-actions.md)) runs
`cz --no-raise 21 bump --yes` on every push to `master` and pushes the
resulting commit and tag — see
[ADR-011](../decisions/011-commitizen-single-version-source.md) for
why this over a bump-PR flow or the `scm` provider.

## How to consult it

Read `.cz.toml` directly for the current pinned baseline, or (with a
local Python ≥ 3.10 and `pip install commitizen==4.18.1`) run
`cz bump --dry-run` to preview the next computed version from the
commits on the current branch.

## Gotchas

No local Python was installed on the machine this framework was
developed on as of this reference's writing — the real bump only runs
in CI, where `pip install commitizen==4.18.1` provisions it fresh
each run. `--no-raise 21` must precede `bump` on the CLI invocation:
exit code 21 is commitizen's `NoneIncrementExit`, raised when a push
contains only non-version-bumping commits (`docs:`, `chore:`, …) —
without `--no-raise 21` that would fail the whole workflow instead of
being a normal no-op.
