---
host_id: gemini-cli
display_name: Gemini CLI
config_root: ~/.gemini/
global_instruction_file: ~/.gemini/GEMINI.md
subagent_dir: ~/.gemini/agents/
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

# Gemini CLI Host Caveats

## Host Identity & Configuration Root

- **Host ID:** `gemini-cli`
- **Display Name:** Gemini CLI
- **Global Config Root:** `~/.gemini/` (distinct from Antigravity's `~/.gemini/config/`)
- **Subagent Battery Directory:** `~/.gemini/agents/`
- **Global Behavioral Contract:** `~/.gemini/jaiba-contract.md`
- **Configuration Metadata:** `~/.jaiba/config.yaml` (SSOT; legacy `~/.gemini/jaiba-configure.yaml` is `harvest-legacy` migration input only)
- **Global Instruction File:** `~/.gemini/GEMINI.md`

## Subagent Frontmatter Syntax

Gemini CLI consumes the standard generic subagent battery. Projected subagents
use standard generic frontmatter:

- `name`: subagent role name (e.g., `executor-low`)
- `description`: role description and boundary contract
- `requires`: list of required CLI tools (e.g., `git`, `bash`)
- `model`: optional model pin (e.g., `gemini-2.5-pro`)

Frontmatter keys `mode: subagent` and `permission:` are not emitted for
Gemini CLI.

## Model Catalog Rules

Gemini CLI model discovery follows the procedure in `model-discovery.md`:

1. **CLI discovery:** Inspect the installed Gemini CLI command line for
   documented model enumeration.
2. **ACP fallback:** Eligible if the CLI catalog command is unsupported or
   unavailable.
3. **Exact ID preservation:** Record model identifiers exactly as returned.

## Effort Control Syntax

Gemini CLI does not document a subagent effort control:

- **Effort syntax:** `none` (leave unset).
- Per ADR-017, Gemini CLI subagent documentation lists model and temperature
  parameters, not an effort field.
- Do not invent an `effort:` key or reasoning effort parameters.

## Researcher Role Rule

Per ADR-017, `researcher.md` must always be installed with **no `model:` field**
(omitted to inherit) and **no effort control**.

## Installation Recommendations

1. **Battery installation:** Copy standard agent templates from
   `skills/jaiba-configure/assets/agents/*.md` into `~/.gemini/agents/`.
2. **Contract installation:** Copy `assets/jaiba-contract.md` to
   `~/.gemini/jaiba-contract.md`.
3. **Global instructions linkage:** Show the developer the exact reference line
   being added to `~/.gemini/GEMINI.md` and obtain consent before writing:
   `Follow the JAIBA Behavioral Contract in ~/.gemini/jaiba-contract.md.`
4. **Skills discovery:** Gemini CLI discovers skills in `~/.gemini/skills/` or
   via global skill paths.
