---
type: purpose
title: "Purpose"
description: "Provide a secure, standardized way to co-work with AI coding agents, keeping the human as the central decision-maker."
tags: [identity, purpose, business]
updated: "2026-08-03"
---

# Purpose

> **Meta-instruction for the agent:** this concept is the authority on
> **why this project exists** — the business objective it serves and the
> role it plays in whatever larger system it belongs to. Read it before
> judging whether proposed work is worth doing. What the project *builds*
> is the `scope` concept's job, not this one's.

- **Business objective:** Provide a secure, standardized way of
  co-working with AI agents on real software projects. JAIBA is not a
  tool, an AI model, or a collection of loose prompts — it is a
  behavioral architecture that organizes context, orchestrates
  workflows, and keeps the human as the central decision-maker at every
  significant stage of development. It targets both greenfield and
  brownfield codebases, and serves developers and teams adopting AI
  coding agents as co-pilots (not autopilots).
- **Position in the bigger picture:** Standalone. JAIBA is not a
  component of another product — it installs a skillset and a subagent
  battery *onto* an existing AI coding agent (built and dogfooded
  against Claude Code) rather than depending on one as an upstream
  service. It has no consumers other than the developer/agent pair using
  it.

## Relations

Upstream, downstream and infrastructure relationships are **not
inventoried here**. Each external surface is its own `reference` concept
carrying a `role:` (`upstream` | `downstream` | `infrastructure`) along
with how to consult it; this section only links the ones that explain the
project's *purpose* — who it serves and what it depends on to serve them.

This project has no `role`-carrying reference concepts: it has no
runtime dependencies and no consumers calling into it — it is a
self-contained skillset installed onto a host agent. The two reference
concepts this bundle does carry
([OKF v0.1](../references/okf-v0-1.md),
[the `skills` CLI](../references/skills-cli.md)) are `tier: workflow`,
where `role` does not apply.

Never copy a reference's details into this list. One line, one link; the
`reference` concept owns the facts.
