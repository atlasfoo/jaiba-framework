---
type: log-entry
date: 2026-09-14
slug: skills-sh-security-remediation
kind: work-closure
depth: design
adr: "ADR-009, ADR-010, ADR-011"
---

# Skills.sh security remediation + commitizen versioning

> The work-closure entry for `.ai/memory/log/` — drafted in
> `.ai/work/` by `conduct:summarize`, moved by `scripts/archive.sh`.

## What happened

Remediated all 10 findings from skills.sh's audits (Agent Trust Hub,
Socket, Snyk) across `jaiba-configure`, `jaiba-init`, `jaiba-doctor`:
the framework now ships and pins only first-party skills to a release
tag, treats every scanned repository/skill as data never instructions
(a new contract rule, cited across the sweep-mode skills), sanitizes
the toolchain probe's inputs against injection, restricts `verify` to
only gate commands and existing tests, and makes `jaiba-configure`'s
global-config footprint and consent explicit. Introduced commitizen +
Conventional Commits as the framework's single version source, with
two SHA-pinned GitHub Actions automating the bump/tag and validating
commit messages on PRs.

## Criteria delivered

None — design depth; done = plan scope + gate.

## Phases executed

| # | Theme | Notable result |
|---|---|---|
| 1 | Commitizen versioning | `.cz.toml` + `bump.yml`/`commit-check.yml`, 7 `SKILL.md` normalized to `2.1.0` |
| 2 | First-party-only skillset | `caveman` and the `owner/repo` format removed from `skillset.txt`, `SKILL.md`, evals, `skills-lock.json`; `greeting.sh` deleted |
| 3 | Pin to release ref | `skillset.txt` gains `ref: v2.1.0`; installs pinned `#<ref>` with a pre-install manifest + one confirmation |
| 4 | Content-is-data boundary | Contract §4.5 (lockstep, both copies), cited across `jaiba-init`/`jaiba-doctor`/`verify`/executors, 2 injection evals |
| 5 | Toolchain-probe sanitization | `check-tools.sh` allow-lists tokens/labels; `## Rejected entries` section; injection fixture + Plan-gate check |
| 6 | `verify` command provenance | Only Phase-gate commands (verbatim) or existing tests; a criterion-sourced command is *not verifiable* |
| 7 | `jaiba-configure` transparency | Declared read/write footprint; consent+diff before editing the global instructions file; `*.bak-<date>` backups; README uninstall guide |
| 8 | Brain update | ADR-009/010/011 enacted; `scope`/`architecture`/`conventions`/`quality-gate` updated; 2 new `reference` concepts |
| 9 | Verification | Real probes (0 missing / fixture rejects cleanly); workflow static review; eval walk-through fixed 5 stale cases incl. a real gap in the `owner/repo` filter |

## Decisions and deviations

- T-014 merged the scope-choice and manifest-confirmation into one
  structured question rather than two, and used the installed
  `version:` (not `npx skills list -g`, which carries no ref) as the
  primary drift signal in Case A.
- T-030 established one concrete backup convention
  (`<path>.bak-<YYYY-MM-DD>`) that the contract table, step 2, and the
  subagent-battery step all now point back to instead of restating.
- T-042's eval audit caught a real prose gap, not just eval drift:
  `jaiba-configure/SKILL.md` had no explicit filter rejecting a stray
  `owner/repo`-shaped line in `skillset.txt` — fixed, reporting a
  count only, never the line's content (mirrors `check-tools.sh`'s
  `## Rejected entries` pattern).
- Two out-of-scope findings were flagged via `spawn_task` rather than
  expanding task scope: pinning `jaiba-configure`'s own self-install
  example line, and a stale "run commands" phrasing in
  `conduct`'s own eval suite (predates Phase 6's `verify` contract
  change).
- Every citation of the new contract rule spells out "§4.5" or names
  the contract file explicitly, never bare "§4" — that number already
  names an unrelated section in `constitution.md` in several of the
  same files.

## ADR proposals & brain updates

Not proposed here — **already enacted** during `execute` (Phase 8 of
this plan), via `jaiba-init:update-brain`'s own propose → confirm →
enact procedure (run directly by conduct, since writing
`.ai/memory/` is never delegated to a subagent): [ADR-009](../decisions/009-first-party-pinned-skillset.md),
[ADR-010](../decisions/010-repository-content-is-data.md),
[ADR-011](../decisions/011-commitizen-single-version-source.md), plus
updates to [scope.md](../identity/scope.md),
[architecture.md](../identity/architecture.md),
[conventions.md](../identity/conventions.md),
[quality-gate.md](../identity/quality-gate.md),
[skills-cli.md](../references/skills-cli.md), and two new references,
[commitizen.md](../references/commitizen.md) and
[github-actions.md](../references/github-actions.md). `index.md` was
regenerated. No further brain action is outstanding from this plan.

## Pointers

Commits (phase-wise, `master`): `e695969` (Phase 1), `e42f10c`
(Phase 2), `70a851e` (Phase 3), `c5af0bf` (Phase 4), `e36637e`
(Phase 5), `c459b45` (Phase 6), `162e998` (Phase 7), `084eb3f`
(Phase 8), `57627f0` (Phase 9). ADR IDs: ADR-009, ADR-010, ADR-011.
Follow-up tasks flagged, not yet started: `task_29973038` (pin
jaiba-configure's self-install line), `task_56935225` (cover
`SKILL.md` ref examples in `.cz.toml` `version_files`),
`task_c3c4dde0` (fix stale `verify` wording in `conduct`'s evals).
Source audits: skills.sh Agent Trust Hub / Socket / Snyk reports for
`jaiba-configure`, `jaiba-init`, `jaiba-doctor`, `update-brain`
(2026-08-12 / 2026-06-19).

## Suggested final commit

```
feat(configure)!: first-party pinned skillset, content-is-data boundary, commitizen versioning

Remediates all 10 skills.sh findings (Agent Trust Hub, Socket, Snyk):
jaiba-configure installs only first-party skills pinned to a release
tag; scanned content is treated as data, never instructions, across
the sweep-mode skills; the toolchain probe sanitizes its inputs;
verify only runs gate commands or existing tests; jaiba-configure's
footprint and consent are explicit. Introduces commitizen + GitHub
Actions as the framework's single version source.

BREAKING CHANGE: jaiba-configure no longer installs third-party
skills (e.g. the former caveman entry) or accepts owner/repo sources;
skillset.txt drops that format. Communication-style extensions are
now the developer's own install, outside the framework's distribution.
```

## Gate at close

Pass — full Plan gate (repo-wide Phase gate, real toolchain probe
against this machine's skillset, injection-fixture probe, orphaned-
citation sweep, dual-layout check, clean `git status --short`,
security scan correctly omitted) all green.
