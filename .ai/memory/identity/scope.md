---
type: scope
title: "Scope"
description: "The JAIBA skillset, its memory model, and its subagent battery — not any one project built with it."
tags: [identity, scope, boundaries]
updated: "2026-09-15"
---

# Scope

> **Meta-instruction for the agent:** this concept is the authority on
> **the project's boundaries**. Work that falls outside them is surfaced
> to the human before it is planned, never absorbed silently. Why the
> project exists is the `purpose` concept; how it is built is
> `architecture`.

- **In scope:**
  - The workflow skills: `conduct` (the SDD chain: propose → spec →
    tasks → execute → validate → summarize), `fast` (implicit inline
    lane), `ask` (implicit read-only lane).
  - The meta skills: `jaiba-configure` (machine-level setup: global
    contract, skillset, subagent battery), `jaiba-init` (repo-scoped
    bootstrap + `update-brain` modes: `initialize`, `update`,
    `migrate`), `jaiba-doctor` (health checks: memory coherence, tool
    state, reference health), `create-knowledge` (converts a skill into
    a JAIBA knowledge plugin).
  - The memory model itself: the concept-bundle and legacy-flat layouts
    of `.ai/memory/`, the `.ai/work/` executive-memory shape, and the
    dual-resolution rule between them.
  - The subagent battery: `executor-high/-medium/-low`, `code-analyst`,
    `business-analyst`, `verify` — their invocation contract and
    concurrency policy.
  - The templates every one of the above writes from (`assets/` under
    each skill).
  - This repo's own release automation: commitizen's version
    computation and the two GitHub Actions that bump/tag a release and
    validate commit messages on PRs (see
    [references/commitizen.md](../references/commitizen.md),
    [references/github-actions.md](../references/github-actions.md)).
- **Out of scope:**
  - Any specific software project built *using* JAIBA — this repo ships
    the framework, not an application. The `.ai/` brain shape described
    here is what other repos adopt, not something this repo's own
    business logic depends on.
  - Domain-specific "knowledge skills" (e.g. framework best-practice
    guides) — JAIBA defines how a knowledge skill plugs into the chain
    (`create-knowledge`), but does not ship any itself.
  - Hosting a skill registry, or CI infrastructure for projects other
    than this one — distribution to third parties is delegated to the
    external `npx skills` CLI (see
    [references/skills-cli.md](../references/skills-cli.md)); this
    repo's *own* release automation (above) is in scope, a registry or
    hosting service for skills in general is not.
- **Cross-cutting packages:** None — single repository, no monorepo
  package split. The one vendored external skill (`skill-creator`,
  tracked in `skills-lock.json`) is used as-is, not a shared internal
  package.

## Sub-units

Single-unit repository: **"Single unit."** The seven skills
(`conduct`, `ask`, `fast`, `jaiba-configure`, `jaiba-init`,
`jaiba-doctor`, `create-knowledge`) are components of one deliverable —
the JAIBA skillset — not independently deliverable units with separate
consumers, so `identity/units/` does not exist.

## Relations

Upstream, downstream and infrastructure relationships are **not
inventoried here**. Each external surface is its own `reference` concept
carrying a `role:` (`upstream` | `downstream` | `infrastructure`); this
section only links the ones that draw a boundary — the surfaces that
explain why something is out of scope, or that this project must not
reimplement.

This project has no `role`-carrying reference concepts (see
[purpose.md § Relations](purpose.md#relations) for why) — nothing to
link here either.

Never copy a reference's details into this list. One line, one link; the
`reference` concept owns the facts.
