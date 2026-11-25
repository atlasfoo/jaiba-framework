---
host_id: opencode
display_name: OpenCode
config_root: ~/.config/opencode/
global_instruction_file: ~/.config/opencode/AGENTS.md
subagent_dir: ~/.config/opencode/agents/
frontmatter_flavor: opencode
emits_name: false
emits_requires: false
emits_mode_subagent: true
emits_permission_map: true
permissions_by_role:
  executor-high:
    read: allow
    grep: allow
    glob: allow
    edit: allow
    bash: allow
  executor-medium:
    read: allow
    grep: allow
    glob: allow
    edit: allow
    bash: allow
  executor-low:
    read: allow
    grep: allow
    glob: allow
    edit: allow
    bash: allow
  verify:
    read: allow
    grep: allow
    glob: allow
    edit: deny
    bash: allow
  code-analyst:
    read: allow
    grep: allow
    glob: allow
    edit: deny
    bash: allow
  business-analyst:
    read: allow
    grep: allow
    glob: allow
    edit: deny
    bash: deny
  researcher:
    read: allow
    grep: allow
    glob: allow
    edit: deny
    bash: deny
model_catalog_probing: cli_first_acp_fallback
effort_syntax: none
researcher_model_pin: forbidden
researcher_effort: forbidden
---

# OpenCode Host Caveats

## Host Identity & Configuration Root

- **Host ID:** `opencode`
- **Display Name:** OpenCode
- **Global Config Root:** `~/.config/opencode/`
- **Subagent Battery Directory:** `~/.config/opencode/agents/`
- **Global Behavioral Contract:** `~/.config/opencode/jaiba-contract.md`
- **Configuration Metadata:** `~/.jaiba/config.yaml` (SSOT; legacy `~/.config/opencode/jaiba-configure.yaml` is `harvest-legacy` migration input only)
- **Global Instruction File:** `~/.config/opencode/AGENTS.md`

## Subagent Frontmatter Syntax

OpenCode uses a native subagent frontmatter schema distinct from the standard
generic battery. Canonical base definitions under `~/.jaiba/agents/base/*.md`
(packaged in `skills/jaiba-configure/assets/agents/*.md`) are projected into
`~/.config/opencode/agents/` via `jaiba_ssot.py`.

### Projected Fields
- `description`: role description and contract string
- `mode: subagent`: declares the agent mode for OpenCode
- `model`: optional model pin (e.g. `anthropic/claude-3-7-sonnet`)
- `permission`: structured tool permission map

### Omitted Fields
- `name:` is **omitted** (OpenCode derives agent names from filenames).
- `requires:` is **omitted** (tool capabilities are controlled by `permission:`).

### Role Permission Matrix

| Role | `read` | `grep` | `glob` | `edit` | `bash` |
|---|---|---|---|---|---|
| `executor-high` | `allow` | `allow` | `allow` | `allow` | `allow` |
| `executor-medium` | `allow` | `allow` | `allow` | `allow` | `allow` |
| `executor-low` | `allow` | `allow` | `allow` | `allow` | `allow` |
| `verify` | `allow` | `allow` | `allow` | `deny` | `allow` |
| `code-analyst` | `allow` | `allow` | `allow` | `deny` | `allow` |
| `business-analyst` | `allow` | `allow` | `allow` | `deny` | `deny` |
| `researcher` | `allow` | `allow` | `allow` | `deny` | `deny` |

## Model Catalog Rules

OpenCode discovers models via CLI first, with ACP fallback:

1. **CLI command:** `opencode models [provider]` lists configured-provider
   models in `provider/model` (or `providerID/id`) format.
2. **ACP command:** `opencode acp` provides nd-JSON JSON-RPC stdio catalog
   fallback when CLI probing is unavailable or uninterpretable.
3. **No variant manufacturing:** OpenCode agent docs allow an optional
   `#variant` suffix on `model`. Variant names originate in the model's catalog
   and do not constitute an effort field. Do not append `#variant` to model IDs
   unless the user explicitly chooses it from the catalog.

## Effort Control Syntax

OpenCode does not support a dedicated effort frontmatter field:

- **Effort syntax:** `none` (leave unset).
- Per ADR-017, neither the `#variant` suffix nor provider pass-through keys are
  treated as a universal or verified effort control.
- Do not write `effort:` or append speculative effort parameters.

## Researcher Role Rule

Per ADR-017, `researcher.md` must always be installed with **no `model:` field**
(omitted to inherit) and **no effort control**. OpenCode permissions for
`researcher` remain strictly read-only (`edit: deny`, `bash: deny`).

## Installation Recommendations

1. **Native templates:** Project OpenCode-native subagents from canonical base
   templates (`~/.jaiba/agents/base/*.md` / `skills/jaiba-configure/assets/agents/*.md`)
   into `~/.config/opencode/agents/` via `jaiba_ssot.py`.
2. **Contract installation:** Copy `assets/jaiba-contract.md` to
   `~/.config/opencode/jaiba-contract.md`.
3. **Global instructions linkage:** Show the developer the exact line to append
   to `~/.config/opencode/AGENTS.md` and obtain consent:
   `Follow the JAIBA Behavioral Contract in ~/.config/opencode/jaiba-contract.md.`
4. **Skills discovery:** OpenCode discovers skills installed in
   `~/.config/opencode/skills/` or host-visible directories.
