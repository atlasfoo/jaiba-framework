---
type: decision
id: ADR-011
title: "Commitizen + Conventional Commits as single source of the framework version"
description: .cz.toml computes the framework's version from Conventional Commits and keeps it in lockstep across every SKILL.md, skillset.txt's ref:, and README.md; a GitHub Action bumps and tags on merge to master via a GitHub App bypassing branch protection.
status: accepted
date: "2026-09-15"
tags: [versioning, release, tooling]
updated: "2026-09-15"
---

# ADR-011: Commitizen + Conventional Commits as single source of the framework version

## Context

The repository had no git tags and no single source of truth for its
version: the seven `skills/*/SKILL.md` files carried independent
`version:` values ranging `1.0.0`–`2.1.0`, hand-edited and prone to
drift. That made it impossible for `jaiba-configure` to pin an install
to a specific, verifiable release — Agent Trust Hub flagged the
resulting unpinned install as HIGH. Fixing it requires both a
versioning scheme and an automated way to keep every `version:` line
and the packaged `ref:` in sync, so manual edits cannot drift them
apart again.

## Decision

Adopt commitizen with the `cz_conventional_commits` provider.
`.cz.toml` holds the single version (`version_scheme = "semver2"`,
`tag_format = "v$version"`, baseline `version = "2.1.0"`), and its
`version_files` keeps every `skills/*/SKILL.md`'s `^version:`,
`skillset.txt`'s `^ref:`, and `README.md`'s pinned
`jaiba-framework#v` line in lockstep on every bump. A GitHub Action
(`bump.yml`) runs `cz --no-raise 21 bump --yes` on every push to
`master`, guarded against re-triggering on its own `bump:` commits,
using a GitHub App token that bypasses the repository's
`master-protection` ruleset to push the bump commit and tag directly —
the ruleset's own PR-required policy would otherwise block CI from
ever landing a bump. A second workflow (`commit-check.yml`) validates
Conventional Commits on every pull request, both commit range and PR
title.

## Alternatives Considered

- *A separate bump PR per release* (a bot proposes the bump commit, a
  human merges it) — rejected: doubles the merges required per release
  for no added safety, since the bump itself is entirely mechanical,
  derived from commits already reviewed and merged.
- *commitizen's `scm` version provider* (computed from `git describe`
  at read time, no file writes) — rejected: it cannot maintain
  `skillset.txt`'s `ref:` or `README.md`'s pinned install line, both of
  which must be real, committed values that `jaiba-configure` reads
  directly — not something recomputed on the fly on a machine that
  isn't running this exact build.

## Consequences

- *Positive:* one version, everywhere, automatically — a `SKILL.md`'s
  `version:` can never silently drift from the tag `jaiba-configure`
  would pin an install to.
- *Negative / Risks:* release automation now depends on a correctly
  scoped GitHub App and its ruleset-bypass permission (maintainer
  setup, outside this plan's automated scope); misconfiguration would
  silently stop tags from being pushed. `jaiba-doctor` verifies the
  version-lockstep *result*, not the release pipeline's health itself.
- *Follow-ups:* none outstanding — the maintainer checklist (this
  plan's `plan.md`) covers the GitHub App setup and the baseline
  `v2.1.0` tag as manual prerequisites outside the agent's authority.
