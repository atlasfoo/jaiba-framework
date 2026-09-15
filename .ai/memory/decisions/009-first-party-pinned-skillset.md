---
type: decision
id: ADR-009
title: "Framework ships and pins only first-party skills"
description: jaiba-configure installs exclusively atlasfoo/jaiba-framework skills, pinned to a release ref; no third-party skill (e.g. the former caveman entry) is distributed or invoked by the framework.
status: accepted
date: "2026-09-15"
tags: [supply-chain, skills, security]
updated: "2026-09-15"
---

# ADR-009: Framework ships and pins only first-party skills

## Context

skills.sh's Agent Trust Hub audit flagged `jaiba-configure` HIGH for
installing skills from arbitrary `owner/repo` sources without pinning
a version, including a third-party skill (`caveman`, from
`juliusbrussee/caveman`) neither authored nor security-maintained by
this framework. Socket and Snyk raised the same install path as a
supply-chain risk. The framework's maintainer cannot vouch for a
third party's security posture, review cadence, or supply chain —
distributing their skill by default extends that trust implicitly.

## Decision

`jaiba-configure` installs exclusively skills from
`atlasfoo/jaiba-framework`, listed by bare name in
`assets/skillset.txt`, always pinned to the release `ref:` that
commitizen maintains in lockstep with the framework's version (see
[ADR-011](011-commitizen-single-version-source.md)). No
`owner/repo` or `owner/repo#skill` source is accepted, whether from
`skillset.txt` or a developer's inline request. Communication-style
extensions such as `caveman` remain a legitimate choice for a user to
install and manage themselves, entirely outside the framework's
distribution and its guarantees.

## Alternatives Considered

- *Keep distributing a curated third-party skill (`caveman`)* —
  rejected: the maintainer cannot vouch for a dependency it does not
  control, and all three skills.sh audits (Agent Trust Hub, Socket,
  Snyk) independently flagged this exact install path as the primary
  supply-chain risk.
- *Allow `owner/repo` installs, reviewed once before adding to
  `skillset.txt`* — rejected: an unpinned source still resolves to
  whatever is on the default branch at install time, which is the
  exact transparency hole this decision closes; a one-time review does
  not track later changes to that branch.

## Consequences

- *Positive:* eliminates the third-party attack surface from
  `jaiba-configure`'s default install path; every skill it installs
  traces to one signed release tag of one repository.
- *Negative / Risks:* a developer who wants `caveman`-style
  compression must find, install, and maintain it themselves, with no
  framework guarantee about its safety or upkeep.
- *Follow-ups:* none outstanding — covered by Phase 2 (removal of
  `caveman` and the multi-source format) and Phase 3 (ref pinning) of
  the plan that produced this decision.
