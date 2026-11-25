---
host_id: antigravity
display_name: Antigravity
config_root: ~/.gemini/config/
global_instruction_file: pointer
subagent_dir: ~/.gemini/config/agents/
frontmatter_flavor: standard
emits_name: true
emits_requires: true
emits_mode_subagent: false
emits_permission_map: false
model_catalog_probing: exempt
selectable_models:
  - pro
  - flash
  - inherit
default_model_recommendation: inherit
effort_syntax: none
researcher_model_pin: forbidden
researcher_effort: forbidden
---

# Antigravity Host Caveats

## Host Identity & Configuration Root

- **Host ID:** `antigravity`
- **Display Name:** Antigravity
- **Global Config Root:** `~/.gemini/config/` (distinct from standard Gemini CLI `~/.gemini/`)
- **Subagent Battery Directory:** `~/.gemini/config/agents/`
- **Global Behavioral Contract:** `~/.gemini/config/jaiba-contract.md`
- **Configuration Metadata:** `~/.jaiba/config.yaml` (SSOT; legacy `~/.gemini/config/jaiba-configure.yaml` is `harvest-legacy` migration input only)
- **Global Instruction File:** Pointer-based via `~/.jaiba/contract/jaiba-contract.md` or vendor instructions in `~/.gemini/config/GEMINI.md`

## Subagent Frontmatter Syntax

Antigravity consumes standard subagent definitions. Projected subagents use the
standard generic frontmatter:

- `name`: subagent role name (e.g., `executor-medium`)
- `description`: role description and boundary contract
- `requires`: required CLI tools list (e.g., `git`, `bash`)
- `model`: optional model selection (`pro`, `flash`, or omitted for `inherit`)

Frontmatter keys `mode: subagent` and `permission:` are not emitted for
Antigravity.

## Model Catalog Rules (Antigravity Exception)

Antigravity is **exempt** from external CLI or ACP model catalog discovery:

1. **No CLI / ACP probing:** Skip all CLI `models` subcommand execution, ACP
   session initialization, and cross-agent bridge probes. Never launch a bridge
   process or probe endpoints for Antigravity model availability.
2. **Strict model enumeration:** The selectable model catalog on Antigravity is
   strictly limited to:
   - `inherit` (or omitting `model:`) — **recommended**
   - `pro`
   - `flash`
3. **Recommended default:** Recommend `inherit` (omitting the `model:` field)
   so the native Antigravity orchestrator manages routing and model assignment
   dynamically according to session context.
4. **Write gate:** The write gate only presents and accepts `pro`, `flash`, or
   `inherit`. Any other model identifier is invalid.

## Effort Control Syntax

Antigravity does not support subagent effort control fields:

- **Effort syntax:** `none` (leave unset).
- Do not emit `effort:`, `model: <id>[effort=...]`, or any reasoning effort
  parameters in Antigravity subagent frontmatter.
- ADR-017 strictly forbids inventing an effort control for hosts that do not
  document one.

## Researcher Role Rule

Per ADR-017, the `researcher` role (`researcher.md`) must always be installed
with **no `model:` field** (inheriting the parent model) and **no effort
control**.

## Installation Recommendations

1. **Subagent battery:** Copy standard agent templates from
   `skills/jaiba-configure/assets/agents/*.md` into
   `~/.gemini/config/agents/`.
2. **Contract placement:** Copy `assets/jaiba-contract.md` to
   `~/.gemini/config/jaiba-contract.md`.
3. **Global instruction linkage:** If linking via a vendor instructions file,
   show the exact one-line reference to `jaiba-contract.md` and obtain explicit
   user consent before appending.
4. **Skill discovery:** Skills are discovered via standard skill search roots
   such as `~/.jaiba/skills/`, `~/.agents/skills/`, or global packages listed in
   `npx skills list -g`.
