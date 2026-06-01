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
- [~] Meta Skills
  - [x] `create-knowledge` skill (plugin behavior)
  - [x] `scaffold` skill (`skills/meta/scaffold/`, name `jaiba-scaffold`)
    - Does **not** manage the artifact templates — that is
      `update-brain`'s responsibility. `scaffold` only lays down the
      `.ai/` skeleton + `AGENTS.md`, then immediately invokes
      `update-brain:initialize` to populate the brain content. No
      cross-skill runtime reference to `update-brain/assets/` (skills
      package independently); the boundary is a hand-off, not a path.
    - Global skill (installed into the agent, run inside a project).
      Installs the project-scoped set from `assets/skillset.txt` via the
      `skills` CLI into the detected agent folder (`.agents/` default;
      a single vendor dir like `.claude/` if exactly one exists;
      `.agents/` again if many). Ships the behavioral `AGENTS.md` (moved
      here from root `AGENTS.jaiba.md`) + `.ai/.gitignore`, and a
      `check-tools.sh` that derives required tools from installed skills'
      `requires:` and writes the gitignored `.ai/tools-state.md` (warn,
      never block). The shipped `AGENTS.md` gained §6 Toolchain Awareness
      + a brain-map row so missing tools are surfaced each session.
  - [x] `doctor` skill, external index accesibility and tool testing
    (`skills/meta/doctor/`, name `jaiba-doctor`). Project-scoped meta
    skill, run manually as a pre-flight before `planning` /
    `specification`. Three diagnostics: memory coherence (read-only →
    routes to `update-brain`), tool state (the only write — refreshes
    `.ai/tools-state.md`; its own `check-tools.sh` extends scaffold's
    with provenance + subagents + hooks), and external-reference health
    (MCP/CLI/URL/vendored reachability + git-based vendored staleness >1
    month). Diagnoses and routes; never patches the brain. Added to
    `scaffold`'s `assets/skillset.txt` so it installs per-project.
  - [ ] `create-workflow` skill

# Global instructions
- Keep `README.md` always up to date
- Keep framework consistent and coherent alongside skills, artifacts and AGENTS.md
- Check every task that is marked as done
