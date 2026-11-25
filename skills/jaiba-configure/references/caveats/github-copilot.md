---
host_id: github-copilot
display_name: GitHub Copilot
config_root: ~/.github/copilot/
global_instruction_file: pointer
subagent_dir: ~/.github/copilot/agents/
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

# GitHub Copilot Host Caveats

## Host Identity & Configuration Root

- **Host ID:** `github-copilot`
- **Display Name:** GitHub Copilot
- **Global Config Root:** `~/.github/copilot/`
- **Subagent Battery Directory:** `~/.github/copilot/agents/`
- **Global Behavioral Contract:** `~/.github/copilot/jaiba-contract.md`
- **Configuration Metadata:** `~/.jaiba/config.yaml` (SSOT; legacy `~/.github/copilot/jaiba-configure.yaml` is `harvest-legacy` migration input only)
- **Global Instruction File:** Pointer-based via `~/.jaiba/contract/jaiba-contract.md` or vendor instructions in `~/.github/copilot/`

## Subagent Frontmatter Syntax

GitHub Copilot consumes the standard generic subagent battery. Projected
subagents use standard generic frontmatter:

- `name`: subagent role name (e.g., `business-analyst`)
- `description`: role description and boundary contract
- `requires`: list of required tools (e.g., `git`, `bash`)
- `model`: optional model pin

Frontmatter keys `mode: subagent` and `permission:` are not emitted for
GitHub Copilot.

## Model Catalog Rules

GitHub Copilot model discovery follows `model-discovery.md`:

1. **CLI discovery:** Check supported models via GitHub Copilot CLI command
   reference.
2. **ACP fallback:** Eligible when CLI inspection is unsupported or
   unavailable.
3. **Exact ID preservation:** Record model identifiers byte-for-byte.

## Effort Control Syntax & Path Caveat

GitHub Copilot does not receive an effort control on the installed battery:

- **Effort syntax:** `none` (leave unset).
- **Critical path distinction (ADR-017):** The GitHub Copilot CLI reference
  documents a `reasoningEffort` field on Copilot agent profiles loaded from
  `~/.copilot/agents/` and `.github/agents/`. However, `jaiba-configure`
  installs the generic subagent battery into `~/.github/copilot/agents/`.
- Per ADR-017 and `model-discovery.md`, do **not** copy `reasoningEffort` onto
  the definitions installed under `~/.github/copilot/agents/`.
- Do not emit an `effort:` key or any speculative effort controls.

## Researcher Role Rule

Per ADR-017, `researcher.md` must always be installed with **no `model:` field**
(omitted to inherit) and **no effort control**.

## Installation Recommendations

1. **Battery installation:** Copy standard agent templates from
   `skills/jaiba-configure/assets/agents/*.md` into
   `~/.github/copilot/agents/`.
2. **Contract installation:** Copy `assets/jaiba-contract.md` to
   `~/.github/copilot/jaiba-contract.md`.
3. **Instruction linkage:** Link the global behavioral contract via a pointer
   reference in the user's global instruction file after obtaining consent.
4. **Skills discovery:** Discover skills via `~/.github/copilot/skills/` or
   global skill directories.
