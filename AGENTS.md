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
   memory under `.ai/memory/` (resolved per `jaiba-contract.md` §1 —
   Brain Map. This repository uses the concept bundle: start at
   [`.ai/memory/index.md`](.ai/memory/index.md)).

Anything project-specific a maintainer wants agents to know belongs in
the constitutive memory, not appended here. (This repo is the special
case where "the project" and "the JAIBA framework" are the same thing
— see [`.ai/memory/identity/purpose.md`](.ai/memory/identity/purpose.md)
and [`scope.md`](.ai/memory/identity/scope.md) for how that boundary is
drawn. For the framework's own architecture as a reader-facing
document, see `README.md`, not this file.)
