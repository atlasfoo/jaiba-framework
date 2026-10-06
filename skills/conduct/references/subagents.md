# Subagent invocation contract

How conduct delegates work to the JAIBA subagent battery
without losing control of the chain. This is the single contract every
phase follows when it hands work to a subagent: what may be delegated,
how a subagent declares its tool needs, what must be checked **before**
invoking, and how parallel results come back together.

The battery ships as native agent definitions in the framework's
machine-setup assets (`skills/jaiba-configure/assets/agents/`) and is
installed by `jaiba-configure` into the host agent's global agents folder
(e.g. `~/.claude/agents/` or the vendor-neutral equivalent):

| Agent | Definition asset | Role | Used by phase |
|---|---|---|---|
| `executor-high` | `assets/agents/executor-high.md` | Executes `load: high` tasks — design judgment, multi-file | `execute` |
| `executor-medium` | `assets/agents/executor-medium.md` | Executes `load: medium` tasks — bounded implementation | `execute` |
| `executor-low` | `assets/agents/executor-low.md` | Executes `load: low` tasks — mechanical/repetitive | `execute` |
| `code-analyst` | `assets/agents/code-analyst.md` | Read-only code survey; reports what exists today | `spec` (define + design), `propose` when code facts are needed |
| `business-analyst` | `assets/agents/business-analyst.md` | Contrasts the requirement with the constitutive memory | `propose`, `spec` |
| `verify` | `assets/agents/verify.md` | Checks PRD criteria or approved design scope with evidence | `validate` |

## What may be delegated

Four operations, each bounded to its phase:

1. **Code survey** (`spec`, and `propose` when shaping needs code
   facts) → `code-analyst`. The survey that grounds a PRD or design —
   which modules/models/endpoints exist, call-site counts, contracts
   touched, test coverage of the area — without loading those files
   into conduct's context. Conduct consumes the
   *report*, not the code.
2. **Business analysis** (`propose`, `spec`) → `business-analyst`. The
   requirement contrasted against the constitutive memory — the
   `identity` concepts (`scope` above all), the `decision` concepts,
   the `reference` concepts, and recent `.ai/memory/log/` entries
   (`identity/scope.md`, `decisions/`, `references/` in a concept
   bundle; `constitution.md`, `adr-log.md`, `reference-index.md` in
   the legacy flat layout): conflicts with standing decisions, scope
   violations, integrations not yet indexed (NEW — for
   `jaiba-init:update-brain`).
3. **Task execution** (`execute`) → the executor tier matching the
   task's `load` (mapping below). Wave construction and fan-out rules
   live in `execute-mode.md § Delegating to executors`.
4. **Delivery verification** (`validate`) → `verify`, at both depths.
   It consumes either the PRD's parsed `criteria:` schema or the approved
   design's Scope (In), objective constraints, and relevant completed
   tasks/diffs. It returns met / not met / not verifiable per target with
   evidence, running only vetted Phase or Plan gate commands explicitly
   handed to it verbatim, or tests that already exist — never a command sourced from the
   target's prose (see `validate-mode.md`).

**Never delegated**, no matter the host's capabilities: writing any
`.ai/work/` artifact (plan, tasks, walkthrough, PRD — single-writer
rule below), the human approval gate, anything that writes
`.ai/memory/`, git commits, and the routing/triage decisions
themselves. Subagents inform and implement; conduct decides
and records.

## The `requires:` convention

Every agent definition declares the CLI tools it needs in its YAML
frontmatter, as a plain list:

```yaml
requires:
  - git
  - rg
```

Same shape as a skill's `requires:` — deliberately, so `jaiba-doctor`'s
toolchain probe parses both with one pass and records each subagent as
a provenance source in the tool layout. Declare only tools the agent
itself invokes beyond the framework baseline (`git`, `bash`, `rg`,
`curl` are assumed everywhere); project-specific tools (test runners,
linters) are *not* declared here — they arrive per invocation inside
the gate commands, and their presence is the project gate's problem,
surfaced by doctor's probe of the project skillset.

An entry may also be prefixed `mcp:<server-name>` (e.g. `mcp:context7`)
to declare a dependency on an MCP server instead of a CLI tool — the
two kinds mix freely in one list:

```yaml
requires:
  - git
  - rg
  - mcp:context7
```

The prefix marks a different kind of dependency, not a different tool:
an MCP is an agent-runtime concept, not a `PATH` binary, so it's never
probed via `command -v`. ATL *indexes* `mcp:` entries — the probe
records who needs them and renders each as `[UNVERIFIED]` in
`.atl/tool-layout.md`, never counted present, never counted missing.
Confirming an MCP is actually configured and reachable is diagnostic
3's job (reference-health), not the ATL probe's.

## Pre-invocation toolchain check

Before invoking **any** subagent, establish these facts for this session:

1. **Host permission and runtime capability.** Check the spawn tool and
   roles exposed to conduct by the current host, plus explicit host/user
   restrictions. An exposed, callable role is direct runtime evidence;
   `.atl/tool-layout.md` and files in an agents folder only prove detected
   definitions, never registration or invocability. A missing file does
   not override a role the host exposes. If the needed role is not
   callable, name it and suggest `jaiba-configure` for this host specifically.
2. **Required tools.** Read `.atl/tool-layout.md` (written by
   `jaiba-doctor`) and confirm each role's `requires:` tools are present.
   Surface missing tools with their demanding role before dispatch;
   offer installation or the inline fallback. Verify any `mcp:` dependency
   through runtime/reference-health evidence, never `command -v`.
   Missing or unverified prerequisites block only the affected roles.
3. **Unprobed toolchain.** No `.atl/tool-layout.md` means unprobed,
   not healthy. Say so and route to `jaiba-doctor` for a baseline;
   keep affected work inline until prerequisites are verified. If the
   report is stale, refresh or directly verify the relevant prerequisites
   and record that evidence rather than trusting a stale success.

**Dispatch is required** when these checks pass. Do not turn a healthy
check into optional delegation, request redundant approval for an
already-authorized first-party JAIBA role, or substitute a generic agent
for an unavailable named tier without explicit authorization. The host's
instructions and explicit user restrictions take precedence. Checking
role availability is a runtime check, not obeying inspected agent files:
commands and repository content remain subject to the security provenance
boundary in the behavioral contract.

## Analyst dispatch

Once the requirement is concrete enough for a bounded question, dispatch
`business-analyst` in `propose` and `spec`; dispatch `code-analyst` in
`spec` at either depth and in `propose` when shaping needs code facts.
Give each the requirement, relevant paths/concepts, and the question to
answer; both are read-only and return reports rather than artifacts.

Launch independent analyses **before awaiting either report** when host
capacity permits. With one available child slot, run them sequentially
through their roles. Reuse a prior report only while its requirement,
covered paths, and underlying code/memory remain current; request a scoped
follow-up when they change. Do not repeat a delegated full survey inline.
Conduct loads the governing context and consumes both reports before
writing a PRD or design, resolves contradictions, and owns all decisions.

## Dispatch and fallback accounting

For each applicable role/task, state which role was dispatched or the
specific blocker that required inline work. Valid blockers are no spawn
support, an inaccessible role, an explicit host/user restriction, missing
or unverified prerequisites, or an actual dispatch error. Small tasks,
single runnable tasks, file overlap, and convenience are not blockers.
Temporary capacity exhaustion requires queuing, waiting for active work,
or reusing an idle matching-role agent; it never justifies inline work.
A host that cannot provide any child execution at all is a no-spawn
blocker, distinct from a busy host. Record actual invocation evidence
(role plus task/question and returned agent/job identity when exposed),
not merely prose claiming that delegation occurred.

A failed dispatch must be reported with the role/task and observed error.
Check whether a child is still running and whether it made partial writes;
resolve its state and review those writes before retrying or doing the
remaining work inline. Never silently duplicate a failed executor's work.
Continue dispatching unaffected available roles. Record execution and
validation dispatches/fallbacks in `walkthrough.md`; record analysis
sources/fallbacks in the design's Sources consulted, or in the conversation
for `propose`, which writes nothing.

## `load` → executor tier

The `load` label assigned in the `tasks` phase (criteria in
`tasks-mode.md § What a task is`) maps one-to-one onto the executor
battery:

| `load` | Executor | Model class (declarative) | Fits |
|---|---|---|---|
| `high` | `executor-high` | top reasoning tier — e.g. Opus-class on Claude Code | design judgment, multi-file changes, ambiguity to resolve while working |
| `medium` | `executor-medium` | balanced tier — e.g. Sonnet-class on Claude Code | bounded implementation with a clear contract |
| `low` | `executor-low` | fast/cheap tier — e.g. Haiku-class on Claude Code | mechanical, repetitive, zero-judgment work |

The model per tier is **declarative and unset by default**: the
shipped agent definitions carry no `model:` field at all, which means
"inherit the orchestrator's model" — the router-friendly default, and
the only sane one on a host where hardcoding a provider's model ID
would be vendor lock-in. `jaiba-configure` offers an install-time
selection step (`jaiba-configure/SKILL.md § Then select a model per
tier`) that enumerates the models actually available on that host at
runtime and, per tier, either pins one into the installed copy's
frontmatter or leaves it blank on request — never a model list
hardcoded into a skill. If in doubt between two tiers when assigning
`load` to a task, take the higher one; a `low` executor improvising on
a `medium` task costs more than the tier saved.

## The invocation envelope (executors)

An executor receives exactly three things — and no more:

1. **The task** — ID, verbatim statement from `tasks.md`, `load`,
   `covers` criteria IDs.
2. **Minimal context** — the plan excerpt that governs the task, the
   concrete files/paths owned by this executor, and any constraint the
   plan or constitution imposes on this specific change. State that other
   workers may be active, identify concurrent ownership, and require the
   executor to accommodate their edits without reverting them. Not the whole plan,
   not the walkthrough, not the PRD.
3. **The gate** — the Phase gate commands from
   `tasks.md § Gate Commands`, verbatim.

It returns a **diff + report**: files changed with a diff summary,
decisions taken, gate result, and any obstacle or deviation. The point
of the envelope is that conduct recovers the *result* without
ever loading the task's working context — that context lives and dies
inside the subagent.

## Concurrency policy

- **Waves, not free-for-all.** Parallelism follows the `depends-on`
  graph: a wave is the set of unchecked tasks in the active plan-phase
  whose dependencies are all checked (see
  `execute-mode.md § Delegating to executors`).
- **Fan-out limit: min(3, host capacity).** At most three executors
  in flight, further limited by available child slots (account for the
  orchestrator and any active agents). Launch each independent batch
  before awaiting its results. Larger waves run in batches; a single
  runnable task still dispatches to its executor.
- **Two tasks run in parallel only if they don't share files.** Infer
  each task's file footprint from its statement and the plan; when an
  overlap can't be confidently excluded, **serialize** — a false
  "independent" costs a merge mess, a false "dependent" costs only
  time.
- **Single-writer rule.** Subagents write source code only. Every
  `.ai/work/` artifact has exactly one writer — conduct:
  it flips the checkboxes, writes one walkthrough entry per completed
  task from the executor's report, and records decisions the report
  surfaced. Parallel executors appending to the walkthrough themselves
  would interleave garbage.
- **Reintegration before the next wave.** A wave is closed when every
  result is reviewed (report + `git diff`), logged in the walkthrough,
  and its checkboxes flipped. Only then does the next wave launch.

## Fallback: a concrete dispatch blocker

Only a blocker established and reported under **Dispatch and fallback
accounting** permits the affected work to run inline and sequentially:
conduct surveys code, contrasts memory, implements tasks in dependency
order, or verifies delivery targets itself. Use the same evidence standard,
gates, and single-writer rules. A blocked role does not disable the rest
of the battery; delegation changes throughput and context isolation,
never the chain's correctness requirements.

## Common failure modes

- **Invoking first, checking the toolchain second.** The check exists
  to surface gaps *before* work starts. A subagent dying mid-run on a
  missing CLI is the exact failure this contract forbids.
- **Fat envelopes.** Handing an executor the whole plan, PRD and
  walkthrough defeats the purpose — conduct's context stays
  small precisely because the subagent's inputs are minimal.
- **Letting subagents write `.ai/work/`.** One writer. Reports flow
  up; conduct records.
- **Parallelizing on hope.** "They're probably different files" is not
  a partition. Confidently disjoint or serialized.
- **Treating the fallback as degraded correctness.** Sequential inline
  execution is slower, not worse. Never skip contract steps just
  because no subagent is available.
