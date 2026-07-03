---
slug: spec-02a-atl-tool-layout
created: 2026-07-02
archived: 2026-07-02
spec: .ai/specs/jaiba-improvement-plan.md#SPEC-02a
adr_proposed: none
---

# Plan summary: Fixes de `doctor` + capa `.atl/tool-layout`

> Concise, archivable. One screen, no more. The walkthrough was the
> narrative; this is the record.

## Outcome

Migrated the machine-local tool probe state to a dedicated, gitignored layer `.atl/tool-layout.md` in both the `scaffold` and `doctor` skills. Enhanced Windows shell detection to distinguish between Git Bash and WSL, hardened the behavioral rules in `AGENTS.md` to prevent mid-run failures via a "read-and-honor before invoking" rule, and added a per-skill health rollup section in the doctor checkup report to identify broken skill dependencies.

## Spec coverage

- **AC-happy-1** (Windows Git Bash/WSL distinction) — closed
- **AC-happy-2** (Honoring tool layout before invoking skills) — closed
- **AC-sad-1** (Fallback routing for missing tool layout file) — closed
- **AC-extra-1** (Per-skill health rollup under doctor probe) — closed

## Phases executed

| # | Theme | Notable result |
|---|---|---|
| 1 | Layer Relocation | Moved tools-state to `.atl/tool-layout.md`, updated all documentation and evals, and added asset `atl.gitignore`. |
| 2 | Windows Environment Probe | Implemented shell flavor detection (`git-bash`, `wsl`, `native`) and annotated baseline bash row. |
| 3 | Behavioral Rule Enforcement | Hardened section 6 of `AGENTS.md` to mandate pre-invocation checks on absent tools. |
| 4 | Skill Health Rollup | Built a declarative health rollup per skill source based on `requires:` in doctor checkup report. |

## Deviations and corrections

In addition to the planned SPEC-02a phases, we performed an extra refactoring step: we completely removed the duplicate `check-tools.sh` logic from the `scaffold` skill and updated the bootstrap sequence to run `scaffold -> update-brain -> doctor`. This prevents duplication of probe scripts and ensures that the initial environment state is populated after long-term memory has been initialized by doctor. Deleted `skills/scaffold/scripts/check-tools.sh`.

## ADR proposal

No ADR proposed; all decisions were tactical.

## Suggested final commit

```
refactor(atl): relocate toolchain probe to .atl/tool-layout.md and add per-skill rollup

Relocated toolchain state from .ai/tools-state.md to local gitignored .atl/tool-layout.md.
Enhanced shell host flavor detection under Windows. Hardened AGENTS.md §6 rules to
read-and-honor before invoking skills. Added skill health rollup under doctor checks.
Removed duplicate check-tools.sh logic from scaffold to enforce scaffold->update-brain->doctor.
```

## Quality gate at close

Pass | Syntax checks (`bash -n`) and file searches pass.
