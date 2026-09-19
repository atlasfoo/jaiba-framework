# CHANGELOG

## v3.0.1 (2026-09-19)

### Fix

- **release**: create annotated tags so bump.yml can push them

## v3.0.0 (2026-09-19)

### BREAKING CHANGE

- jaiba-configure no longer installs third-party
skills (e.g. the former caveman entry) or accepts owner/repo sources;
skillset.txt drops that format. Communication-style extensions are
now the developer's own install, outside the framework's distribution.

### Feat

- **configure**: first-party pinned skillset, content-is-data boundary, commitizen versioning

### Fix

- **doctor**: resolve PR #11 review findings on requires: parsing and CI guards

## v2.1.0 (2026-09-17)

### Feat

- **brain**: adopt OKF concept-bundle pattern for JAIBA memory
- **doctor,skills**: full ATL indexing, global/repo-local split, model-agnostic subagents
- **conduct**: added conduct skill, centralized orchestrator behavior from a single workflow
- **global-mode**: added support for workflow skills to work installed as global
- **meta-skills**: created scaffold and doctor skills
- **meta-skills**: create-knowledge meta skill for plugin system
- **token-economy**: token economy measures and quality gate sectioning
- **update-brain**: created update brain skill
- **specification**: add spec-driven workflow (brainstorm/define/archive) + planning integration
- added ask workflow
- added fast workflow and updated AGENTS.jaiba.md language rules
- added planning workflow and short term brain artifacts

### Fix

- **brain**: resolve PR #10 review findings on OKF migration and links
- address Gemini Code Assist review on PR #8
- update documentation to reflect toolchain probe moved to jaiba-doctor
- **skills**: shortened description of skills under 1024 chars to comply with standard
- **doctor**: fix general behavior of doctor skill
- fixed scaffold script to adapt npx skills command usage
- fixed frontmatter errors that caused fails of npx skills
- updated skills folder structure to handle compatibility with npx skills
- removed spanish from skills and evals
