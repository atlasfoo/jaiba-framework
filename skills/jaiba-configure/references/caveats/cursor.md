---
host_id: cursor
display_name: Cursor
config_root: ~/.cursor/
global_instruction_file: pointer
subagent_dir: ~/.cursor/agents/
frontmatter_flavor: standard
emits_name: true
emits_requires: true
emits_mode_subagent: false
emits_permission_map: false
model_catalog_probing: cli_first_acp_fallback
effort_syntax: inline_model_parameter
effort_parameter_pattern: "<id>[effort=<val>]"
researcher_model_pin: forbidden
researcher_effort: forbidden
---

# Cursor Host Caveats

## Host Identity & Configuration Root

- **Host ID:** `cursor`
- **Display Name:** Cursor
- **Global Config Root:** `~/.cursor/`
- **Subagent Battery Directory:** `~/.cursor/agents/`
- **Global Behavioral Contract:** `~/.cursor/jaiba-contract.md`
- **Configuration Metadata:** `~/.jaiba/config.yaml` (SSOT; legacy `~/.cursor/jaiba-configure.yaml` is `harvest-legacy` migration input only)
- **Global Instruction File:** Pointer-based via `~/.jaiba/contract/jaiba-contract.md` or vendor rules in `~/.cursor/`

## Subagent Frontmatter Syntax

Cursor consumes the standard generic subagent battery. Projected subagents use
standard generic frontmatter:

- `name`: subagent role name (e.g., `executor-medium`)
- `description`: role description and boundary contract
- `requires`: list of required tools (e.g., `git`, `bash`)
- `model`: optional model pin, optionally carrying inline effort parameters

Frontmatter keys `mode: subagent` and `permission:` are not emitted for
Cursor. There is no separate Cursor scaffold in this package.

## Model Catalog Rules

Cursor model discovery follows the standard procedure in `model-discovery.md`:

1. **CLI / executable version check:** Inspect the installed Cursor agent binary
   and verify its supported models.
2. **ACP fallback:** Eligible when CLI probing is unavailable or uninterpretable.
3. **No custom scaffold:** Do not invent a custom Cursor scaffold or custom
   directories. Install directly into `~/.cursor/agents/`.

## Effort Control Syntax

Cursor documents effort as an inline model ID parameter:

- **Syntax:** `model: <id>[effort=<val>]` on the specific model ID line.
- **Validation gate:** Write this parameter syntax only when the detected
  version's documentation still confirms that exact parameter syntax and lists
  the consented value for that specific model.
- **Inheritance & omission:** When `model` is omitted (to inherit the
  orchestrator's model), there is no verified effort parameter syntax. Leave
  effort unset.
- **No separate key:** Do not emit a top-level `effort:` key on Cursor.
- **No unofficial suffixes:** Do not append forum suffixes (e.g., `-high`) to
  model names.

## Researcher Role Rule

Per ADR-017, `researcher.md` must always be installed with **no `model:` field**
(omitted to inherit) and **no effort parameter**.

## Installation Recommendations

1. **Battery installation:** Copy standard agent templates from
   `skills/jaiba-configure/assets/agents/*.md` into `~/.cursor/agents/`.
2. **Contract installation:** Copy `assets/jaiba-contract.md` to
   `~/.cursor/jaiba-contract.md`.
3. **Instruction linkage:** Link the global behavioral contract via a pointer in
   the global instruction or rules configuration after obtaining user consent.
4. **Skills discovery:** Cursor discovers skills in `~/.cursor/skills/` or
   globally installed skill paths.
