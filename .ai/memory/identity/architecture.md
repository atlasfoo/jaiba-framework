---
type: architecture
title: "Architecture"
description: "Skill-based agentic framework: declarative Markdown skills, no traditional application layers or runtime service."
tags: [identity, architecture, stack]
updated: "2026-09-15"
---

# Architecture

> **Meta-instruction for the agent:** this concept is the authority on
> **how this project is built** — its architectural style and its stack.
> Obey the style recorded here when placing new code. It does not define
> what the project is for (`purpose`) or where its boundaries run
> (`scope`).

- **Architecture style:** Skill-based agentic framework. The unit of
  delivery is a `SKILL.md` (frontmatter + instructions) plus its
  `assets/` (templates), `references/` (loaded on demand), `scripts/`
  (verification shell scripts) and `evals/` (eval fixtures). There is no
  running service and no traditional layering (MVC/hexagonal/clean) —
  the "runtime" is the AI coding agent interpreting the skill at
  invocation time.
- **Primary language:** Agent Skills (Markdown) for the skills
  themselves; Bash for verification/toolchain scripts
  (`skills/*/scripts/*.sh`).
- **Primary framework:** The Agent Skills convention (`SKILL.md` +
  `requires:`/`tags:` frontmatter). Built and dogfooded against Claude
  Code; the shipped subagent battery is deliberately model-agnostic
  (no hardcoded `model:` — see
  [ADR-007](../decisions/007-global-repo-local-setup-split.md)) so the
  framework is not tied to one vendor.
- **Persistence:** None. Project state lives in the repository itself:
  `.ai/memory/` (constitutive memory, this bundle, versioned) and
  `.ai/work/` (executive memory — PRD/plan/tasks/walkthrough,
  gitignored).
- **Key packages:** None — no traditional package manifest. The one
  external skill dependency this repo vendors (`skill-creator`) is
  tracked in `skills-lock.json` and installed via the `npx skills`
  CLI — see [references/skills-cli.md](../references/skills-cli.md).
  It needs no non-default configuration, so it gets no `package`
  reference of its own.
- **Release tooling:** commitizen computes the framework's single
  version from Conventional Commits, and two GitHub Actions bump/tag
  a release and validate commit messages on PRs — see
  [references/commitizen.md](../references/commitizen.md) and
  [references/github-actions.md](../references/github-actions.md).

> The **complete** dependency map lives in `skills-lock.json` and each
> integration lives in its own `reference` concept. Do not duplicate
> either here — this concept holds the shape of the system, not its
> inventory.
