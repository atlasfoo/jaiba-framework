---
type: reference
title: OKF v0.1 (Open Knowledge Format)
description: Draft spec this framework's concept-bundle memory layout borrows its shape from — not a runtime dependency.
tier: workflow
kind: business-doc
role: —
resource: "URL: `https://openknowledgeformat.com/`"
tags: [memory-model, spec, design]
updated: "2026-08-03"
---

# OKF v0.1 (Open Knowledge Format)

## What it is

A draft external specification (published 2026-06-12) for representing
a knowledge base as one concept per file, with a closed `type:`
vocabulary in frontmatter and file-relative markdown links as
relations. JAIBA's `.ai/memory/` concept-bundle layout adopts this
*shape* — not a versioned dependency on it.

## How the project uses it

`skills/jaiba-init/references/okf-pattern.md` documents JAIBA's own
closed `type:` vocabulary (16 values), bundle layout, per-type
frontmatter and link convention — patterned after OKF v0.1's approach,
but self-contained: no skill, script, or subagent declares a
`requires:` on OKF, no conformance to the upstream spec is tested or
claimed, and unknown frontmatter keys are tolerated rather than
rejected. See
[ADR-008](../decisions/008-okf-pattern-brain-serialization.md) for the
full adoption decision and the alternatives considered (a
JAIBA-proprietary format; staying monolithic; a literal versioned
dependency on the draft spec).

## How to consult it

Fetch `https://openknowledgeformat.com/` directly (web tools) when the
upstream spec's current wording matters — this project keeps no
vendored copy, since it deliberately does not track the spec's
evolution.

## Gotchas

OKF v0.1 is a **draft** — it may change incompatibly upstream. JAIBA
does not follow such changes automatically; any future re-alignment is
a new, explicit decision, not silent drift.
