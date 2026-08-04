---
type: architecture                                # mandatory — exact value, never change
title: "Architecture"                             # recommended — human-readable name
description: "[one line: the architectural style and stack this project is built on]" # recommended — this is what index.md shows
tags: [identity, architecture, stack]             # recommended — list, for grouping and search
updated: "[YYYY-MM-DD]"                           # recommended — last substantive change
---

# Architecture

> **For repository maintainers:** replace every bracketed placeholder
> (`[like this]`) with real project values, read from the repository
> itself (manifests, config, source layout) — never from memory. A fact
> you cannot ground is `[MISSING]`, not a guess.

> **Meta-instruction for the agent:** this concept is the authority on
> **how this project is built** — its architectural style and its stack.
> Obey the style recorded here when placing new code. It does not define
> what the project is for (`purpose`) or where its boundaries run
> (`scope`).

- **Architecture style:** [e.g., Hexagonal / Clean / Layered / MVC / Serverless]
- **Primary language:** [e.g., Python 3.12 / TypeScript 5.x]
- **Primary framework:** [e.g., Django 5 / Next.js App Router]
- **Persistence:** [e.g., PostgreSQL via Django ORM / Prisma + MySQL]
- **Key packages:** [List 5–10 packages central to the project, beyond
  framework-default dependencies]

> The **complete** dependency map lives in the package manifest
> (`pyproject.toml`, `package.json`, `pom.xml`, …) and each integration
> lives in its own `reference` concept. Do not duplicate either here —
> this concept holds the shape of the system, not its inventory.
