# AGENTS.md — JAIBA project marker

This repository is **JAIBA-instrumented** (Joint-operations Artificial
Intelligence Behavioral Architecture). This file is deliberately
minimal: behavior does not live per-repo.

1. **Behavior** — follow the **JAIBA Behavioral Contract** installed
   globally in your agent configuration (file `jaiba-contract.md` in
   the agent's global config folder, e.g. `~/.claude/` or `~/.agents/`;
   installed once per machine by `jaiba-configure`). It defines the
   brain map, the routing rule (continuation → `conduct:execute` ·
   question → `ask` · small change → `fast`), and the numbered
   behavioral rules.

   *If you cannot find the global contract*, say so before doing
   substantive work and route the developer to `jaiba-doctor` (checks
   presence/drift) or `jaiba-configure` (reinstalls it). Do not
   improvise the missing rules.

   *If the JAIBA workflow/meta skills (`conduct`, `ask`, `fast`,
   `jaiba-doctor`, `jaiba-init`, `create-knowledge`, …) aren't
   available to **you specifically*** — check your own skill list, not
   the machine's — **say so before doing substantive work** and route
   the developer to `jaiba-configure` to install them for this agent.
   A machine can have JAIBA configured for one agent (e.g. Claude Code)
   and not another (e.g. Cursor) at the same time; never assume a prior
   `jaiba-configure` run covered the agent you're running as now.

2. **Project facts** — identity, stack, scope, the Quality Gate,
   decisions in force, and external surfaces live in the constitutive
   memory under `.ai/memory/` (resolved per `jaiba-contract.md` §1
   — Brain Map — once populated). Active work: `.ai/work/`.

Anything project-specific a maintainer wants agents to know belongs in
the constitutive memory, not appended here.
