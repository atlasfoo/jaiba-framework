---
type: quality-gate
title: "Quality Gate"
description: "Evals/JSON validity, shell-script syntax, description-length, contract lockstep, and orphaned-citation review — no test suite; this is a Markdown-skills repo."
tags: [identity, quality-gate, verification]
updated: "2026-08-03"
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
  skills/doctor/scripts/check-tools.sh
  skills/jaiba-configure/scripts/greeting.sh` — every verification
  script must parse.
- **`SKILL.md` description length:** `awk '/^description: /{ if
  (length($0)-13 > 1024) print FILENAME": "length($0)-13 }'
  skills/*/SKILL.md` must produce no output (every frontmatter
  `description:` ≤ 1024 chars — the limit the skill-loading mechanism
  enforces).
- **Behavioral-contract lockstep:** `diff -q --strip-trailing-cr
  skills/jaiba-configure/assets/jaiba-contract.md
  skills/doctor/assets/jaiba-contract.md` — the canonical contract copy
  and doctor's drift-check copy must stay byte-identical.

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
- **No versioned executive artifacts:** `git status --short` shows
  nothing under `.ai/work/` (requires `.ai/.gitignore` to exist and
  cover it).

**Security scan:** none configured — omitted, not `[MISSING]`; this
repo ships no executable application code for a scanner to analyze.
