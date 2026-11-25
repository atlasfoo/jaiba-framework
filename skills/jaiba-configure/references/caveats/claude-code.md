---
host_id: claude-code
aliases:
  - claude
display_name: Claude Code
config_root: ~/.claude/
global_instruction_file: ~/.claude/CLAUDE.md
subagent_dir: ~/.claude/agents/
frontmatter_flavor: standard
emits_name: true
emits_requires: true
emits_mode_subagent: false
emits_permission_map: false
model_catalog_probing: cli_first_acp_fallback
effort_syntax: top_level_key
effort_key: effort
effort_documented_values:
  - low
  - medium
  - high
  - xhigh
  - max
effort_forbidden_values:
  - ultracode
researcher_model_pin: forbidden
researcher_effort: forbidden
---

# Claude Code Host Caveats

## Host Identity & Configuration Root

- **Host ID:** `claude-code` (alias: `claude`)
- **Display Name:** Claude Code
- **Global Config Root:** `~/.claude/`
- **Subagent Battery Directory:** `~/.claude/agents/`
- **Global Behavioral Contract:** `~/.claude/jaiba-contract.md`
- **Configuration Metadata:** `~/.jaiba/config.yaml` (SSOT; legacy `~/.claude/jaiba-configure.yaml` is `harvest-legacy` migration input only)
- **Global Instruction File:** `~/.claude/CLAUDE.md`

## Subagent Frontmatter Syntax

Claude Code consumes standard subagent definitions. Projected subagents use
standard generic frontmatter:

- `name`: subagent role name (e.g., `executor-high`)
- `description`: role description and boundary contract
- `requires`: list of required tools (e.g., `git`, `bash`)
- `model`: optional model pin (e.g., `claude-3-7-sonnet-20250219`)
- `effort`: optional top-level effort level (see below)

Frontmatter keys `mode: subagent` and `permission:` are not emitted for
Claude Code.

## Model Catalog Rules

Claude Code model discovery follows the standard procedure in
`model-discovery.md`:

1. **CLI first:** Query host-scoped model lists or version/help interfaces
   matching the installed Claude Code executable.
2. **ACP fallback:** Eligible only when CLI probing is unavailable, timed out,
   or uninterpretable, subject to the 30-second deadline and safe transport
   requirements.
3. **Exact ID preservation:** Preserve returned model IDs byte-for-byte,
   including casing and version suffixes.
4. **Inheritance:** Inheriting the model means omitting the `model:` field
   entirely.

## Effort Control Syntax

Claude Code supports an optional top-level `effort:` frontmatter key:

- **Syntax:** `effort: <value>` placed directly in the subagent frontmatter.
- **Documented values:** `low`, `medium`, `high`, `xhigh`, `max`.
- **Validation gate:** Write `effort:` only when the installed version's public
  documentation specifically verifies that field and the consented value for
  the selected model.
- **Forbidden values:** Never write `ultracode`. `ultracode` is an interactive
  session setting, not a valid frontmatter effort field.
- **Omission rule:** If the model is omitted (inherited), or the installed
  version's docs do not explicitly list the field for that model, leave
  `effort:` unset and note it in the configure report.

## Researcher Role Rule

Per ADR-017, `researcher.md` must always be installed with **no `model:` field**
and **no `effort:` field**. Claude Code subagent effort configuration does not
apply to `researcher`.

## Installation Recommendations

1. **Contract installation:** Copy `assets/jaiba-contract.md` to
   `~/.claude/jaiba-contract.md`.
2. **Global instructions linkage:** If `~/.claude/CLAUDE.md` exists or is to be
   updated, show the developer the exact one-line reference being appended:
   `Follow the JAIBA Behavioral Contract in ~/.claude/jaiba-contract.md.`
   Obtain explicit consent before writing. Never append silently.
3. **Subagent battery:** Copy agent templates from
   `skills/jaiba-configure/assets/agents/*.md` into `~/.claude/agents/`.
4. **Skills installation:** Install global skills into `~/.claude/skills/` or
   manage them via `npx skills list -g`.
