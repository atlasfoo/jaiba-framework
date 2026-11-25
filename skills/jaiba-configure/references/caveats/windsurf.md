---
host_id: windsurf
display_name: Windsurf
config_root: ~/.windsurf/
global_instruction_file: pointer
subagent_dir: ~/.windsurf/agents/
frontmatter_flavor: standard
emits_name: true
emits_requires: true
emits_mode_subagent: false
emits_permission_map: false
model_catalog_probing: cli_first_acp_fallback
effort_syntax: none
researcher_model_pin: forbidden
researcher_effort: forbidden
---

# Windsurf Host Caveats

## Host Identity & Configuration Root

- **Host ID:** `windsurf`
- **Display Name:** Windsurf
- **Global Config Root:** `~/.windsurf/`
- **Subagent Battery Directory:** `~/.windsurf/agents/`
- **Global Behavioral Contract:** `~/.windsurf/jaiba-contract.md`
- **Configuration Metadata:** `~/.jaiba/config.yaml` (SSOT; legacy `~/.windsurf/jaiba-configure.yaml` is `harvest-legacy` migration input only)
- **Global Instruction File:** Pointer-based via `~/.jaiba/contract/jaiba-contract.md` or vendor instructions in `~/.windsurf/`

## Subagent Frontmatter Syntax

Windsurf consumes the standard generic subagent battery. Projected subagents use
standard generic frontmatter:

- `name`: subagent role name (e.g., `code-analyst`)
- `description`: role description and boundary contract
- `requires`: list of required tools (e.g., `git`, `bash`)
- `model`: optional model pin

Frontmatter keys `mode: subagent` and `permission:` are not emitted for
Windsurf.

## Model Catalog Rules

Windsurf model discovery follows `model-discovery.md`:

1. **CLI discovery:** Query host-scoped model options from the installed
   Windsurf environment.
2. **ACP fallback:** Eligible when the CLI interface is unavailable or
   unsupported.
3. **Inheritance:** Omit `model:` to inherit the default editor model.

## Effort Control Syntax

Windsurf does not document a subagent effort control:

- **Effort syntax:** `none` (leave unset).
- Per ADR-017, Windsurf's public docs index does not document an effort field.
- Do not invent an `effort:` key or copy effort parameters from other hosts.

## Researcher Role Rule

Per ADR-017, `researcher.md` must always be installed with **no `model:` field**
(omitted to inherit) and **no effort control**.

## Installation Recommendations

1. **Battery installation:** Copy standard agent templates from
   `skills/jaiba-configure/assets/agents/*.md` into `~/.windsurf/agents/`.
2. **Contract installation:** Copy `assets/jaiba-contract.md` to
   `~/.windsurf/jaiba-contract.md`.
3. **Instruction linkage:** Link the global contract via a pointer reference
   in Windsurf's global rules or instructions file after obtaining user consent.
4. **Skills discovery:** Windsurf discovers skills located in
   `~/.windsurf/skills/` or global skill directories.
