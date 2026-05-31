# Current Agentic Development state

## Tasks
- [x] Agents.md (behavioral instructions)
- [x] Long term brain artifacts
- [x] Short term brain workflows and artifacts
  - [x] `planning` skill and artifacts
  - [x] `fast` skill
  - [x] `ask` skill
- [x] Mid term brain workflows and artifacts
  - [x] `specification` skill and artifacts (brainstorm / define / archive + planning integration)
- [x] Long term brain workflows
  - [x] `update-brain` skill and artifacts (in progress)
    - Owns the memory artifact templates (constitution / adr-log /
      reference-index) under its `assets/`; `initialize` mode detects
      whether the files already exist in the target `.ai/memory/` and
      creates them from the templates only when absent.
- [x] Quality gate sectioning (after phases and after plan).
- [x] Token economy
- [ ] Meta Skills
  - [ ] `create-knowledge` skill (plugin behavior)
  - [ ] `scaffold` skill
    - Does **not** manage the artifact templates — that is
      `update-brain`'s responsibility. `scaffold` only lays down the
      `.ai/` skeleton + `AGENTS.md`, then immediately invokes
      `update-brain:initialize` to populate the brain content. No
      cross-skill runtime reference to `update-brain/assets/` (skills
      package independently); the boundary is a hand-off, not a path.
  - [ ] `doctor` skill, external index accesibility and tool testing
  - [ ] `create-workflow` skill

# Global instructions
- Keep `README.md` always up to date
- Keep framework consistent and coherent alongside skills, artifacts and AGENTS.md
- Check every task that is marked as done
