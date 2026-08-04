---
type: index                                       # mandatory — exact value, never change
title: "[Project Name] — memory index"            # recommended — human-readable name
description: "Entry point to this repository's constitutive memory."  # recommended — one line
tags: [index]                                     # recommended — list, for grouping and search
updated: "[YYYY-MM-DD]"                           # recommended — last substantive change
---

# [Project Name] — Memory Index

> **For repository maintainers:** replace every bracketed placeholder
> (`[like this]`) with real values, and **delete** the rows and sections
> for concepts this repository doesn't have. An empty group is noise.

> **Meta-instruction for the agent:** this file is the **only** entry
> point to `.ai/memory/`. It is a map, never a summary — one link and one
> line per concept, linking **directly** to that concept. Resolving one
> fact must cost reading this file plus *one* concept file; never route a
> reader through another concept on the way. Regenerate this index
> whenever a concept is added, removed or renamed — a stale index is a
> broken-link finding from `jaiba-doctor`.

Each line below is a concept's `description:` frontmatter, verbatim.
Groups are named by the concept `type:` they hold.

## `project`

- [project.md](identity/project.md) — [its `description:`, verbatim]

## `architecture`

- [architecture.md](identity/architecture.md) — [its `description:`, verbatim]

## `purpose`

- [purpose.md](identity/purpose.md) — [its `description:`, verbatim]

## `scope`

- [scope.md](identity/scope.md) — [its `description:`, verbatim]

## `sub-unit`

> Multi-unit repositories only. A single-unit repository has no
> `identity/units/` directory — delete this whole section.

- [unit-slug](identity/units/[unit-slug].md) — [its `description:`, verbatim]

## `quality-gate`

- [quality-gate.md](identity/quality-gate.md) — [its `description:`, verbatim]

## `convention`

- [conventions.md](identity/conventions.md) — [its `description:`, verbatim]

## `decision`

One file per ADR, named `<NNN>-<slug>.md` so the directory sorts in
decision order. Superseded decisions stay listed — the link tells the
story.

- [ADR-[NNN] — [short title]](decisions/[NNN]-[slug].md) — [its `description:`, verbatim]

## `reference`

One file per external surface.

- [surface name](references/[slug].md) — [its `description:`, verbatim]

## `snippet`

> Optional group. Delete this section if the repository records no
> canonical examples.

- [pattern name](snippets/[slug].md) — [its `description:`, verbatim]

## `log-entry`

Indexed **as a group, never per entry**: [`log/`](log/) holds one
append-only file per dated record, named `<YYYY-MM-DD>-<slug>.md`. The
filename convention carries the ordering, and the directory grows without
bound — listing entries here would fatten the index until reading it
costs as much as reading the memory it maps.
