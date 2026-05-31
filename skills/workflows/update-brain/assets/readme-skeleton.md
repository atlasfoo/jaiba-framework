<!--
  JAIBA README skeleton.

  This is the default structure `update-brain:initialize` writes when a
  project's README.md is *completely empty*. It is intentionally
  human-first: unlike `.ai/memory/` (which is for agents and English-only),
  the README serves humans and agents alike and may be written in the
  project's own language.

  The README's role in JAIBA is to answer two questions a human developer
  asks on day one:
    1. What do I need to run this?            (Requirements)
    2. How do I actually do things with it?   (How-to / Getting started)

  Fill each [bracket] from real project evidence (manifests, scriptfiles,
  CI). Do NOT invent commands — if a verification command can't be found
  in a scriptfile (justfile/Makefile/package.json scripts/pyproject) or
  here, mark it [MISSING] and tell the human, per the Quality Gate rule in
  constitution.md.

  Remove these comments once filled.
-->

# [Project Name]

[One or two lines: what this project is and who it's for.]

## Requirements

What a developer must have installed and configured to work on this
project.

**Mandatory**
- [e.g., Python 3.12+ / Node 20+ / .NET 8 SDK]
- [e.g., PostgreSQL 16 running locally or via the provided compose file]
- [e.g., `just` (or `make`) for the task commands below]

**Optional**
- [e.g., Docker, to run the full stack with one command]
- [e.g., the project's linter/formatter editor plugin]

## Getting Started

How to go from a fresh clone to a running project.

```bash
# 1. Install dependencies
[e.g., uv sync  /  npm install  /  dotnet restore]

# 2. Configure environment
cp .env.example .env   # then fill the values

# 3. Run it
[e.g., just dev  /  npm run dev  /  dotnet run]
```

## Developer Commands

The verification commands that back the project's Quality Gate. These
should live in the scriptfile (`justfile`, `Makefile`, `package.json`
scripts, `pyproject.toml [tool.*]`); this section points at them so the
Quality Gate in `.ai/memory/constitution.md` stays runnable.

| Task | Command |
|---|---|
| Run tests | `[e.g., just test]` |
| Coverage | `[e.g., just coverage]` |
| Lint | `[e.g., just lint]` |
| Format | `[e.g., just fmt]` |
| Type check | `[e.g., just typecheck]` |
| Build | `[e.g., just build]` |
| Quality / security scan | `[e.g., just scan — or MISSING]` |

## Project Context (for AI agents)

This repository follows the **JAIBA** framework. The agent's persistent
context lives in `.ai/` — read `AGENTS.md` and
`.ai/memory/constitution.md` before any substantive work.
