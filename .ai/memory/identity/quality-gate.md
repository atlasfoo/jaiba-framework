---
type: quality-gate
title: "Quality Gate"
description: "Evals/JSON validity, shell-script syntax, description-length, contract lockstep, version lockstep, actions-pinned-by-SHA, injection-fixture probe, and orphaned-citation review — no test suite; this is a Markdown-skills repo."
tags: [identity, quality-gate, verification]
updated: "2026-09-15"
---

# Quality Gate

> **Meta-instruction for the agent:** this concept is the authority on
> **what "done" means here**. There is no scriptfile (no `package.json`
> scripts, no `justfile`/`Makefile`) — this repo has no build, no test
> runner, no linter in the conventional sense, because its deliverable
> is Markdown skill definitions, not compiled or executed code. The
> commands below are the real analogs this project has used in
> practice (established during the SPEC-01/SPEC-02b/OKF plans — see
> [`.ai/memory/log/`](../log/) and
> [ADR-006](../decisions/006-index-everything-toolchain-probe.md)), not
> invented placeholders. Do not add a conventional test/lint/build step
> that doesn't exist; if this gate stops matching real practice, that is
> a `jaiba-init:update-brain:update` drift-fix, not a silent edit here.

The gate is split into two tiers, run at different points in the
workflow.

## Phase Gate (runs after each phase — must be fast)

A phase is **not done** until all of these pass. If any fails, fix it
atomically before moving on.

- **Evals JSON validity:** `jq empty skills/*/evals/evals.json` — every
  skill's eval fixture file must be valid JSON.
- **Shell script syntax:** `bash -n skills/conduct/scripts/archive.sh
  skills/doctor/scripts/check-tools.sh` — every verification script
  must parse. `greeting.sh` left this list when it was deleted
  ([ADR-009](../decisions/009-first-party-pinned-skillset.md)'s plan,
  Phase 2 — a cosmetic banner script, not a security decision itself).
- **`SKILL.md` description length:** `awk '/^description: /{ if
  (length($0)-13 > 1024) print FILENAME": "length($0)-13 }'
  skills/*/SKILL.md` must produce no output (every frontmatter
  `description:` ≤ 1024 chars — the limit the skill-loading mechanism
  enforces).
- **Behavioral-contract lockstep:** `diff -q --strip-trailing-cr
  skills/jaiba-configure/assets/jaiba-contract.md
  skills/doctor/assets/jaiba-contract.md` — the canonical contract copy
  and doctor's drift-check copy must stay byte-identical.
- **Version lockstep:** every `^version:` in `skills/*/SKILL.md` must
  equal the bare `version` in `.cz.toml`; `skillset.txt`'s `ref:` and
  the pinned `jaiba-framework#v` line in `README.md` carry the
  tag-formatted value instead (`tag_format = "v$version"` in
  `.cz.toml`, e.g. `v2.1.0`), so compare those two against `v` +
  `.cz.toml`'s `version`, not against the bare field directly (see
  [ADR-011](../decisions/011-commitizen-single-version-source.md)).
- **Actions pinned by SHA:** every `uses:` in
  `.github/workflows/*.yml` must carry a 40-hex-char commit SHA, never
  a tag or branch — `grep -hE '^\s*uses:' .github/workflows/*.yml |
  grep -vE '@[0-9a-f]{40}'` must produce no output.

## Plan Gate (runs once at `conduct:validate` — may be slow)

A plan is **not done** until all of these pass. Failures block the
summary and require corrective action before closing.

- **All Phase Gate commands, repo-wide.**
- **Real toolchain probe:** `bash skills/doctor/scripts/check-tools.sh
  <installed-skills-dirs> .` against this repo — 0 required tools
  missing (unverified `mcp:` deps are reported, not failed).
- **Orphaned-citation sweep:** `rg -n
  'constitution\.md|adr-log\.md|reference-index\.md' skills/ AGENTS.md
  README.md`, reviewed manually — every remaining hit must be
  deliberate (the documented legacy branch, or migration-mapping
  prose), never a dead live-read path.
- **Dual-layout regression check:** exercise the `conduct` chain (or
  the relevant skill directly) against both supported `.ai/memory/`
  layouts — a flat-legacy fixture and a concept-bundle fixture — with
  no false-positive breakage warning on the flat one.
- **Injection fixture probe:** run `check-tools.sh` against
  `skills/doctor/evals/fixtures/injected-skills/` into a temporary
  root; the generated `.atl/tool-layout.md` must show a non-zero
  `Rejected (failed validation)` count and must never render any of
  the fixture's malicious values (see
  [ADR-010](../decisions/010-repository-content-is-data.md)).
- **No versioned executive artifacts:** `git status --short` shows
  nothing under `.ai/work/` (requires `.ai/.gitignore` to exist and
  cover it).

**Security scan:** none configured — omitted, not `[MISSING]`; this
repo ships no executable application code for a scanner to analyze.
