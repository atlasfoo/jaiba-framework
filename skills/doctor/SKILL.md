---
name: jaiba-doctor
description: >-
  Framework-integrity health check for a JAIBA-instrumented project — the maintenance meta-skill that diagnoses whether the `.ai/` brain, the local toolchain, and the external references are still sound, and routes the developer to the fix. Use it whenever someone wants to verify JAIBA is healthy or asks the framework to check itself: "run jaiba doctor", "/jaiba-doctor", "check jaiba health", "is the framework healthy", "diagnose jaiba", "is my brain up to date", "are my references still reachable", "did any of my tools go missing", "check framework integrity before I start planning". It runs three diagnostics — memory coherence (are constitution/adr-log/reference-index complete and consistent with each other and the repo?), tool state (are the CLI tools the installed skills/subagents/hooks need actually present? — refreshes `.ai/tools-state.md`), and external-reference health (is every reference-index entry reachable: are its MCPs/CLIs installed, are remote specs/URLs live, do vendored copies still exist, and are they stale?) — then emits one prioritized report of suggested fixes. Strongly recommended as the pre-flight check right before a `specification` or `planning` workflow, so drift and missing dependencies surface before they derail the work. doctor DIAGNOSES and ROUTES; it does not rebuild the brain (that's `update-brain`), does not bootstrap a project (that's `scaffold`), and does not answer questions about what the brain says (that's `ask`). The only file it writes is `.ai/tools-state.md` (machine state, not project memory). Do NOT use it on a repo that has no `.ai/` yet — there is nothing to diagnose; that's `scaffold`.
version: 1.0.0
author: atlasfoo<iscomejia15@outlook.com>
requires:
  - git
  - bash
  - rg
  - curl
tags:
  - jaiba
  - meta
  - jaiba-meta
  - doctor
---

# jaiba-doctor

The **checkup** skill. `jaiba-doctor` inspects a JAIBA-instrumented
project and reports whether the framework is still sound: is the brain
complete and self-consistent, is the local toolchain intact, and is
every external reference still reachable? It is the diagnostic
counterpart to the skills that *build* things — where `scaffold`
installs and `update-brain` populates, `doctor` **checks and routes**.

Its governing principle is the framework's own: **propose, don't
patch** (`AGENTS.md` §2.9, §5). doctor reads widely and writes almost
nothing. It surfaces problems and names the skill that fixes each one —
it does not rebuild the brain, re-vendor a spec, or install a tool
itself. The **single exception** is `.ai/tools-state.md`: that file is
*machine state, not project memory* (gitignored — `AGENTS.md` §6), so
refreshing it is doctor's job, not a memory mutation.

Think of it as a pre-flight check. The natural time to run it is **right
before a `specification` or `planning` workflow**, so that a stale
constitution, a missing CLI, or an unreachable API surfaces *before* it
derails the work — not three steps into a plan. It is invoked manually;
nothing calls it automatically (yet).

## When NOT to run doctor

doctor is a *maintenance* action — it presumes a brain to inspect.

| Situation | Meaning | Route to |
|---|---|---|
| No `.ai/` at all, or `.ai/memory/` is empty | Project was never instrumented | `scaffold` |
| Brain exists but the developer wants it *rebuilt/reconciled* | That's the fix, not the diagnosis | `update-brain` |
| Developer just wants to *know what the brain says* | Read-only question | `ask` |
| Brain exists and the developer wants a *health check* | — | **Continue here** |

If `.ai/memory/*.md` is missing entirely, stop and route to `scaffold`;
there is nothing to diagnose. (A brain full of bare `[brackets]` is a
*finding*, not a stop condition — that's exactly the kind of incoherence
this skill reports.)

## Universal preconditions

Run these reads once, before any diagnostic. doctor's verdicts must
reflect the repository, not the prompt's assumptions.

1. **`AGENTS.md`** — the behavioral contract. Note §5 (drift & gaps) and
   §6 (toolchain awareness): doctor operationalizes both as checks.
2. **`.ai/` exists and has a brain.** Confirm `.ai/memory/` holds the
   three artifacts. If not, see "When NOT to run doctor".
3. **Locate every skills directory in play.** JAIBA skills can be
   installed project-locally, globally (e.g. `~/.claude/skills/`,
   `~/.agents/skills/`), or split across both — `jaiba-scaffold` step 4
   now offers that choice, and skills already global before scaffold ran
   are left there. doctor's tool-state and reference checks need to scan
   *all* of them, not just the project's:

   - **Project-local:** detect the agent folder the same way `scaffold`
     does — a single vendor dir (`.claude/`, `.cursor/`, `.gemini/`, …)
     if exactly one exists at the project root; otherwise the neutral
     `.agents/`. Its `skills/` subdir is the project-local skills dir, if
     it exists.
   - **Global:** the same vendor folder name, rooted at the user's home
     directory (e.g. `~/.claude/skills`), if it exists. `npx skills list
     -g` confirms whether any JAIBA skills are installed there.

   Hold both paths (either may be absent — that's fine, a project that
   only used local or only used global is a normal configuration). The
   tool probe (diagnostic 2) takes them as a colon-separated list.

## The three diagnostics

Run all three, in this order. Each has its own reference file with the
detailed procedure — **read the reference before running that check**;
this page is the orchestrator, not the manual. Collect every finding
into the single report described under "The health report".

| # | Diagnostic | What it answers | Reference | Writes? |
|---|---|---|---|---|
| 1 | **Memory coherence** | Are constitution / adr-log / reference-index complete, and consistent with each other and the repo? | `references/memory-coherence.md` | No — routes to `update-brain` |
| 2 | **Tool state** | Are the CLI tools the installed skills / subagents / hooks declare actually present on this machine? | `references/tool-state.md` | **Yes** — refreshes `.ai/tools-state.md` |
| 3 | **External-reference health** | Is every `reference-index.md` entry reachable: MCPs/CLIs installed, remote specs live, vendored copies present and fresh? | `references/reference-health.md` | No — routes to fixes |

Why this order: memory coherence is read first because the
reference-index it validates is also the **input** to diagnostic 3 — you
want to know the index is trustworthy before you test what it points at.
Tool state sits in the middle because diagnostic 3 reuses its result
(an MCP/CLI a reference needs is the same kind of dependency the tool
probe just inventoried).

### Severity vocabulary

Use one scale across all three diagnostics so the report reads
consistently:

- ❌ **Broken** — something the framework relies on is absent or wrong
  *right now*: a missing required tool, an unreachable spec a skill
  consumes, a brain file full of unfilled `[brackets]`. A workflow will
  fail or act on false information if this isn't fixed.
- ⚠️ **Degraded / stale** — works today but is drifting toward broken:
  a vendored reference older than a month, a constitution that lags a
  recent structural change, an optional tool missing.
- ✅ **Healthy** — present, reachable, coherent.

When a check can't be completed (e.g. no web tools to test a URL, no MCP
introspection available), report it as **`[UNVERIFIED]`** with the
reason — never silently pass it. An unchecked dependency reported as
healthy is exactly the false confidence the framework's gap discipline
(§5.4) exists to prevent.

## The health report

End with **one** consolidated report — the developer should see the
whole picture in a single place, then the routes to fix it. Use this
structure:

```
# JAIBA Health Report

**Verdict:** <✅ healthy | ⚠️ degraded | ❌ needs attention>
**Checked:** <UTC timestamp>  ·  **Agent folder:** <path>

## 1. Memory coherence — <status>
<findings: file, what's wrong, why it matters>

## 2. Tool state — <status>
<findings: tool, needed by which skill/subagent/hook, present/missing>
(.ai/tools-state.md refreshed)

## 3. External-reference health — <status>
<findings: reference, channel tested, result>

## Suggested fixes (prioritized)
1. <❌ first> <one-line action> → run `<skill>` / install `<tool>` / …
2. <⚠️ next> …
```

Rules for the report:

- **Lead with severity.** Order suggested fixes ❌ before ⚠️; a developer
  skimming should hit the blocking problems first.
- **Every finding names its fix and the skill that owns it.** "Brain is
  stale" is not actionable; "constitution.md doesn't mention the new
  `payments` service — run `update-brain` (update mode)" is. doctor
  diagnoses; the *fix* lives in `update-brain`, `scaffold`, a package
  install, or a re-vendor.
- **Be honest about what you couldn't check.** List `[UNVERIFIED]` items
  explicitly with the reason (no web access, no MCP introspection, etc.).
- **If everything is green, say so plainly** and note doctor is a good
  pre-flight before `planning` / `specification`. Don't manufacture
  findings to look busy.

## Boundaries

- **Diagnose and route — don't fix.** doctor proposes; the owning skill
  enacts. The one thing it writes is `.ai/tools-state.md` (machine
  state, §6), never `.ai/memory/` (that's `update-brain`'s sole right,
  §2.9) and never a vendored file.
- **Maintenance, not bootstrap.** A repo with no `.ai/` is `scaffold`'s
  job, not a finding to repair here.
- **Carry your own tools.** Skills package independently — doctor's
  probe (`scripts/check-tools.sh`) is its own copy, not a runtime call
  into `scaffold`'s folder.
- **Read-mostly everywhere except tools-state.** If a check tempts you to
  "just fix" a `[bracket]` in the constitution or freshen a vendored
  spec, stop — that's the route, not the action.

## Common failure modes

- **Patching the brain instead of routing.** Editing `.ai/memory/` to
  "fix" an incoherence doctor found violates §2.9. Report it and point
  at `update-brain`.
- **Passing an unchecked dependency as healthy.** No web tools doesn't
  mean a URL is reachable — mark it `[UNVERIFIED]`, don't green-light it.
- **Running on an un-instrumented repo.** No `.ai/` means nothing to
  diagnose; route to `scaffold` rather than inventing findings.
- **A wall of equal-weight findings.** Without severity ordering the
  developer can't tell a missing required tool from a month-old vendored
  spec. Always lead with ❌.
- **Skipping the report.** The three checks are worthless if the
  developer doesn't get one prioritized, routed summary at the end.
