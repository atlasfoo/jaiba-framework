---
type: quality-gate                                # mandatory — exact value, never change
title: "Quality Gate"                             # recommended — human-readable name
description: "[one line: the phase gate and plan gate commands this project verifies with]" # recommended — this is what index.md shows
tags: [identity, quality-gate, verification]      # recommended — list, for grouping and search
updated: "[YYYY-MM-DD]"                           # recommended — last substantive change
---

# Quality Gate

> **For repository maintainers:** replace every bracketed placeholder
> (`[like this]`) with the project's real commands. Omit a check the
> project genuinely doesn't run rather than leaving it bracketed.

> **Meta-instruction for the agent:** this concept is the authority on
> **what "done" means here**, and it is the one concept whose contents
> you must not improvise. Both tiers read their commands from the
> repository's scriptfile (`justfile`, `Makefile`, `package.json`
> scripts, `pyproject.toml [tool.*]`, …) or `README.md`. If neither
> documents a command, **stop and ask the maintainer to add it** — do not
> invent commands from memory.

The gate is split into two tiers, run at different points in the
workflow.

## Phase Gate (runs after each phase — must be fast)

A phase is **not done** until all of these pass. If any fails, fix it
atomically before moving on.

- **Tests (affected):** [e.g., Run only the tests for changed modules.]
- **Linting:** [Zero errors, zero warnings.]
- **Type checking:** [Zero errors from the project's type checker.]
- **Formatting:** [Code conforms to the project's formatter; no diffs.]

## Plan Gate (runs once at `conduct:validate` — may be slow)

A plan is **not done** until all of these pass. Failures block the
summary and require corrective action before closing.

- **Full test suite:** [All tests pass, including integration and e2e.]
- **Coverage:** [e.g., ≥ 85% on new business logic.]
- **Build:** [Production build succeeds.]
- **Security scan:** [e.g., Zero critical issues from the project's
  scanner. Omit this line if none is configured.]
