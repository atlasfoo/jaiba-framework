---
type: log-entry
date: 2026-09-15
slug: skills-sh-security-remediation-brain-update
kind: brain-change
adr: "ADR-009, ADR-010, ADR-011"
---

# Skills.sh security remediation — brain updated

## What happened

Three decisions accepted: [ADR-009](../decisions/009-first-party-pinned-skillset.md)
(framework ships and pins only first-party skills),
[ADR-010](../decisions/010-repository-content-is-data.md) (repository
and third-party content is data, not instructions — the contract's
§4.5), [ADR-011](../decisions/011-commitizen-single-version-source.md)
(commitizen + Conventional Commits as the single source of the
framework version). Four identity concepts updated:
[scope.md](../identity/scope.md) (caveman removed from cross-cutting
packages, this repo's release automation added as in-scope, hosting/a
skill registry stay out of scope), [architecture.md](../identity/architecture.md)
(release tooling line, "one vendored skill" instead of two),
[conventions.md](../identity/conventions.md) (the caveman
communication-style line removed, Conventional Commits enforcement
added), [quality-gate.md](../identity/quality-gate.md) (`greeting.sh`
dropped from the shell-syntax check, *version lockstep* /
*actions pinned by SHA* / the *injection fixture probe* added). Two
references created: [commitizen.md](../references/commitizen.md),
[github-actions.md](../references/github-actions.md); one updated:
[skills-cli.md](../references/skills-cli.md) (caveman removed from
inbound, outbound install pinned to `#<ref>`). `index.md` regenerated
to list the three new decisions and the two new references.

## Decisions and deviations

None beyond what each ADR itself records. All nine concept edits
enact proposals already scoped by Phase 8 of the plan below — no
drift-fix path was used, every change traces to a specific plan task
(T-033 through T-039).

## Pointers

Enacted from `.ai/work/plan.md` (slug `skills-sh-security-remediation`),
Phase 8. ADRs: ADR-009, ADR-010, ADR-011. No acceptance-criteria IDs
(this plan runs at `design` depth, no PRD).
