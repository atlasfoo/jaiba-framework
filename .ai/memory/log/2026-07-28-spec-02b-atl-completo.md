---
date: 2026-08-01
slug: spec-02b-atl-completo
kind: work-closure
depth: design
adr: ADR-P5, ADR-P6
---

# SPEC-02b: full ATL indexing + global/repo-local skill split + model-agnostic subagent battery

## What happened

Extended the ATL toolchain probe (`doctor/scripts/check-tools.sh` +
`.atl/tool-layout.md`) to index every agent layer — skills (framework
and external), subagents, and hooks — even when they declare no
`requires:`, and introduced an honest `[UNVERIFIED]` state for what the
probe can't check (`mcp:` deps, hooks when `jq` is missing). Beyond the
original scope, the developer authorized two related extensions:
splitting `scaffold`/`update-brain` into `jaiba-configure` (global
machine setup) and `jaiba-init` (repo-local bootstrap + brain
maintenance), and making the shipped subagent battery model-agnostic
(no hardcoded `model:`; `jaiba-configure` gained an install-time
per-tier selection step driven by the host's actual runtime roster).

## Criteria delivered

None — design depth; done = plan scope + gate. All 7 Scope (In) items
confirmed during `validate`'s walk: Agent Layers inventory, the
`[UNVERIFIED]` state and its rollup-dominance rules, the `mcp:`
convention documented, contract/docs lockstep (both copies identical),
evals updated, the `jaiba-configure`/`jaiba-init` split with lockstep
cross-references, and the model-agnostic battery with its selection
step.

SPEC-02b's three roadmap checkboxes in `.ai/specs/jaiba-improvement-plan.md`
are marked delivered (happy-1: external skill indexed with `requires:`
resolved; happy-2: missing tool reported with its demandant; sad:
`[UNVERIFIED]` never given as present).

## Phases executed

| # | Theme | Notable result |
|---|---|---|
| 1 | Probe script: inventory, MCP classification, honest `jq` guard | Every scanned source registered even with no `requires:`; `mcp:*` routed to its own map; `jq`-missing hooks scan now flagged, not silently skipped |
| 2 | `tool-layout.md` rendering | New `## Agent Layers` inventory section; `[UNVERIFIED]` rows for MCP; rollup verdict logic (`broken` > `unverified` > `satisfied`) |
| 3 | Contract & docs lockstep | `mcp:` convention documented in `subagents.md` + `tool-state.md`; both `jaiba-contract.md` copies kept identical |
| 4 | Verification | Real probe run against this repo; sad-path runs for MCP and jq-missing; discovered and fixed `find` not following symlinks (T-016) and indexing eval fixtures as real skills (T-017) |
| 5 | Global/repo-local split | `scaffold` → `jaiba-configure` (global-only); `update-brain` → `jaiba-init` (repo-local bootstrap + brain maintenance mode); full cross-reference sweep |
| 6 | Model-agnostic subagent battery | Removed hardcoded `model:` from all 6 assets; added host-introspecting per-tier selection step to `jaiba-configure` |
| — | Out-of-band (fast, post-phase) | Missing-framework-skills detector (T-027); PR #9 code-review fixes — `find` evals-path mis-anchor, provenance-dedup space bug, stale doc marker, missing skillset check, printf escaping (T-028); stale `update-brain` names in `jaiba-configure` eval fixtures, found during `validate` (T-029) |

## Decisions and deviations

- **Scope extended twice by explicit developer decision** (2026-08-01,
  recorded in `plan.md § Plan amendments`): the global/repo-local split
  and the model-agnostic battery were not in the original design but
  are direct consequences of the doctor/ATL layer this plan delivered.
- **Two review/validation gaps found and fixed in the same session,
  both out-of-band via `fast`:** T-028 (5 fixes from an external code
  review of PR #9 — a `find` path-filter mis-anchor that could
  silently empty the entire skill/subagent inventory, a provenance
  string-dedup bug, a stale doc marker, an incomplete skillset check,
  and a cosmetic printf escaping bug) and T-029 (four stale
  `update-brain` mentions in `jaiba-configure/evals/evals.json` that
  T-021's closing `rg` sweep missed because it excluded eval-fixture
  prose from its scope). Both verified with synthetic repros and real
  probe runs; no gate check waived.
- No deviations from the (twice-amended) plan's task graph itself.

## ADR proposals & brain updates

This repo has no `adr-log.md` yet (no `constitution.md` either —
`AGENTS.md` stands in per developer decision, 2026-07-28). Both
proposals below are **status: Proposed**, held here for whenever
`jaiba-init:update-brain` initializes this repo's own brain:

**ADR-P5 — Index-everything, verify-what-you-can toolchain probe.**
*Context:* a skill/subagent with no `requires:` was invisible in
`.atl/tool-layout.md`, and a missing `jq` silently skipped the hooks
scan — both looked identical to "nothing needed," which is a false
"present" the framework's own quality bar forbids. *Decision:* the
probe indexes every scanned source unconditionally, classifies `mcp:`-
prefixed dependencies into a separate never-present/never-missing
`[UNVERIFIED]` state (verified downstream by doctor diagnostic 3), and
renders an explicit unverified marker instead of a silent zero when
`jq` is absent. *Alternatives considered:* enumerating `.mcp.json`/
vendor configs directly (rejected — convention-only `mcp:` in
`requires:` keeps the probe declarative); leaving unverified hooks as
a silent zero (rejected — indistinguishable from "needs nothing").
*Consequences:* `find -L` must follow symlinks (this framework's own
recommended install layout uses them) and must prune `evals/`
directories during the walk, not filter by path after — both bugs
surfaced live in this plan (T-016, T-017, and T-028's follow-up fix to
T-017's mis-anchored filter).

**ADR-P6 — Framework must not assume a single vendor or a single
machine's coverage.** *Context:* `scaffold` and `update-brain` bundled
global machine setup (behavioral contract, subagent battery, skillset)
with repo-local instrumentation, and the shipped subagent battery
hardcoded Claude-Code-specific model IDs — both assume the framework
runs for one agent, on one machine, from one vendor. *Decision:* split
into `jaiba-configure` (global: contract, skillset, battery — no brain
templates) and `jaiba-init` (repo-local: `AGENTS.md` marker, `.ai/`
skeleton, constitutive memory — checks for but never installs the
global side), with no shared file paths and hand-off only by naming
the other skill, never invoking it. Subagent definitions ship with no
`model:` field (absent = inherit the orchestrator's model);
`jaiba-configure` discovers the host's actual model roster at
install time and offers per-tier pinning, never a hardcoded list.
*Alternatives considered:* keeping one bundled skill with conditional
logic (rejected — the coupling is exactly what caused the "configured
for one agent, not another on the same machine" gap T-027 had to
detect). *Consequences:* every repo-state routing failure converges on
`jaiba-init`; every agent-coverage gap converges on `jaiba-configure`.

No new `reference-index.md` entries (none exists yet in this repo) and
no constitution changes proposed.

## Pointers

- Commits on `feature/atl-and-okf`: `4680e8a` … `e2b325e` (Phases 1–6),
  `56258a1` (T-028, PR #9 review fixes), `7e8d57c` (T-029, eval
  fixture fix found during validate).
- PR: #9 — "SPEC-02b: ATL full indexing, global/local skill split,
  model-agnostic subagents".
- Roadmap: `.ai/specs/jaiba-improvement-plan.md § SPEC-02b` (checkboxes
  now `[x]`); next up per the roadmap's execution order is `SPEC-05`.
- Related prior log entry: `.ai/memory/log/2026-07-03-orquestador-unificado-memoria.md`
  (ADR-P1…P4, same "no adr-log.md yet" carve-out).

## Suggested final commit

```
feat(doctor,skills): full ATL indexing, global/repo-local split, model-agnostic subagents

Extends the ATL probe to index every skill/subagent/hook layer with
an honest [UNVERIFIED] state for mcp: deps and jq-missing hooks;
splits scaffold/update-brain into jaiba-configure (global) and
jaiba-init (repo-local); removes hardcoded model IDs from the shipped
subagent battery in favor of host-introspected per-tier selection.
```

(Natural squash target for the phase-wise `chore(wip)`/`feat`/`docs`/
`refactor` commits already on the branch, plus the two post-close
fixes `56258a1`/`7e8d57c` — squash is optional; the branch already
reads cleanly phase by phase.)

## Gate at close

Pass — `bash -n check-tools.sh`, `jq empty` on both touched
`evals.json` files, real probe run against this repo (0 missing of 4,
no stale `skill:jaiba-scaffold`/`skill:update-brain` rows). No waivers.
