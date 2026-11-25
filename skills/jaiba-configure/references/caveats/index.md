---
title: Host Agent Caveats Catalog
catalog_version: 1.0.0
neutral_fallback:
  config_root: ~/.agents/
  subagent_dir: ~/.agents/agents/
  global_instruction_file: pointer
  frontmatter_flavor: standard
  effort_syntax: none
hosts:
  - antigravity
  - claude-code
  - opencode
  - cursor
  - gemini-cli
  - windsurf
  - github-copilot
---

# Host Agent Caveats Catalog

This directory contains the modular per-agent caveats catalog for JAIBA host
configuration (`jaiba-configure`). Each host specification defines the host's
configuration root, global instructions file, subagent frontmatter syntax, model
catalog and probing rules, effort control syntax, and installation
recommendations.

## Host Taxonomy & Summary Matrix

| Host ID | Display Name | Global Config Root | Global Instruction File | Subagent Frontmatter | Model Probing | Effort Syntax |
|---|---|---|---|---|---|---|
| `antigravity` | Antigravity | `~/.gemini/config/` | `~/.gemini/config/GEMINI.md` (or pointer) | Standard (`name`, `description`, `requires`) | Exempt (`pro`, `flash`, `inherit`) | None (unset) |
| `claude-code` | Claude Code | `~/.claude/` | `~/.claude/CLAUDE.md` | Standard (`name`, `description`, `requires`) | CLI first / ACP fallback | Top-level `effort:` (`low`..`max`) |
| `opencode` | OpenCode | `~/.config/opencode/` | `~/.config/opencode/AGENTS.md` | OpenCode (`mode: subagent`, `permission:`) | CLI first / ACP fallback (`provider/model`) | None (unset, ADR-017) |
| `cursor` | Cursor | `~/.cursor/` | Pointer-based | Standard (`name`, `description`, `requires`) | CLI first / ACP fallback | Inline `model: <id>[effort=<val>]` |
| `gemini-cli` | Gemini CLI | `~/.gemini/` | `~/.gemini/GEMINI.md` | Standard (`name`, `description`, `requires`) | CLI first / ACP fallback | None (unset, ADR-017) |
| `windsurf` | Windsurf | `~/.windsurf/` | Pointer-based | Standard (`name`, `description`, `requires`) | CLI first / ACP fallback | None (unset, ADR-017) |
| `github-copilot` | GitHub Copilot | `~/.github/copilot/` | Pointer-based | Standard (`name`, `description`, `requires`) | CLI first / ACP fallback | None (unset, ADR-017) |

## Fallback Neutral Root: `~/.agents/`

When `jaiba-configure` cannot determine the host agent by introspecting the
running environment, or when the environment resolves to more than one plausible
vendor, it falls back to the vendor-neutral default root:

- **Global config root:** `~/.agents/`
- **Subagent battery path:** `~/.agents/agents/`
- **Behavioral contract path:** `~/.agents/jaiba-contract.md`
- **Configuration metadata:** `~/.agents/jaiba-configure.yaml`
- **Global instruction file:** Pointer-based via `~/.agents/jaiba-contract.md` or
  `~/.jaiba/contract/jaiba-contract.md`
- **Subagent frontmatter flavor:** Standard generic battery (`name`,
  `description`, `requires`), omitting `model:` to inherit the parent model
- **Effort syntax:** Unset (no effort control)
- **Model discovery:** CLI first, ACP fallback per `model-discovery.md`

`~/.agents/` is the neutral default, not a vendor. Resolving to it means "vendor
unknown", not "no agent".

## Universal JAIBA Subagent Rules

The following rules apply across all hosts without exception:

1. **`researcher` role rule (ADR-017):** The `researcher` subagent is always
   projected with **no `model:` pin** and **no effort control** across all
   hosts. Even when a host has configured model tiers or effort controls for
   other subagents, `researcher.md` must never carry a `model:` or `effort:`
   field.
2. **Inheritance by omission:** "Inherit" means **omitting the `model:` field**,
   not writing `model: inherit`, an empty string, or a manufactured default.
3. **Effort control conservatism (ADR-017):** Effort controls are written only
   when the host's documentation and exact detected version verify the syntax
   and consented value. Never copy an effort field from one host to another.
4. **Declarative Markdown:** All catalog files are declarative Markdown with
   structured YAML frontmatter for machine parsing by `jaiba-configure` and
   support scripts.
