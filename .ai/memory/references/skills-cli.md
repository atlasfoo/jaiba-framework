---
type: reference
title: "`skills` CLI (`npx skills`)"
description: Package manager for Agent Skills; installs/updates this repo's vendored external skills and is how downstream repos adopt JAIBA itself.
tier: workflow
kind: tooling
role: —
resource: "CLI `npx skills`"
tags: [tooling, distribution, skills]
updated: "2026-09-15"
---

# `skills` CLI (`npx skills`)

## What it is

An external `npx`-invoked CLI for installing and updating Agent
Skills from GitHub sources, either globally (`~/.claude/skills/` or
equivalent) or project-locally. It is this project's package manager
for skill-level dependencies, the way `npm`/`pip` are for code
dependencies — but there is no traditional package manifest in this
repo; `skills-lock.json` is the CLI's own lockfile.

## How the project uses it

Two directions:

- **Inbound:** this repo vendors one external skill through it —
  `skill-creator` (source `anthropics/skills`) — tracked with its
  computed hash in [`skills-lock.json`](../../../skills-lock.json) at
  the repo root, installed under `.agents/skills/`. A second entry,
  `caveman`, was removed
  ([ADR-009](../decisions/009-first-party-pinned-skillset.md)): the
  framework distributes only its own first-party skills.
- **Outbound:** `README.md`'s "Getting Started" section documents this
  as the literal install path for adopting JAIBA itself, always pinned
  to the release tag commitizen maintains —
  `npx skills add atlasfoo/jaiba-framework#v2.1.0 --skill
  jaiba-configure -g` — and `npx skills update` as the upgrade path.
  `jaiba-configure`'s own skillset install (`assets/skillset.txt`)
  follows the same `#<ref>` pin (see
  [ADR-009](../decisions/009-first-party-pinned-skillset.md),
  [ADR-011](../decisions/011-commitizen-single-version-source.md)).

## How to consult it

Run `npx skills --help`, or read the commands as documented in
`README.md § Getting Started` / `§ Installation modes`. No MCP server,
no API — command-line only.

## Gotchas

`skills-lock.json` pins each vendored skill by `computedHash`; a
mismatch on re-fetch is a supply-chain integrity signal, not something
to silently re-hash away.
