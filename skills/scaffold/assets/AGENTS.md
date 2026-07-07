# AGENTS.md — JAIBA project marker

This repository is **JAIBA-instrumented** (Joint-operations Artificial
Intelligence Behavioral Architecture). This file is deliberately
minimal: behavior does not live per-repo.

1. **Behavior** — follow the **JAIBA Behavioral Contract** installed
   globally in your agent configuration (file `jaiba-contract.md` in
   the agent's global config folder, e.g. `~/.claude/` or `~/.agents/`;
   installed once per machine by `jaiba-scaffold`). It defines the
   brain map, the routing rule (continuation → `conduct:execute` ·
   question → `ask` · small change → `fast`), and the numbered
   behavioral rules.

   *If you cannot find the global contract*, say so before doing
   substantive work and route the developer to `jaiba-doctor` (checks
   presence/drift) or `jaiba-scaffold` (reinstalls it). Do not
   improvise the missing rules.

2. **Project facts** — identity, stack, scope, and the Quality Gate
   live in `.ai/memory/constitution.md`, which is authoritative on
   project specifics. Decisions in force: `.ai/memory/adr-log.md`.
   External surfaces: `.ai/memory/reference-index.md`. Active work:
   `.ai/work/`.

Anything project-specific a maintainer wants agents to know belongs in
the constitution, not appended here.
