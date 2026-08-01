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
| `verify` | `assets/agents/verify.md` | Checks PRD acceptance criteria one by one | `validate` |

## What may be delegated

Four operations, each bounded to its phase:

1. **Code survey** (`spec`, and `propose` when shaping needs code
   facts) → `code-analyst`. The survey that grounds a PRD or design —
   which modules/models/endpoints exist, call-site counts, contracts
   touched, test coverage of the area — without loading those files
   into conduct's context. Conduct consumes the
   *report*, not the code.
2. **Business analysis** (`propose`, `spec`) → `business-analyst`. The
   requirement contrasted against `constitution.md`, `adr-log.md`,
   `reference-index.md` and recent `.ai/memory/log/` entries:
   conflicts with standing decisions, scope violations, integrations
   not yet indexed (NEW — for `jaiba-init:update-brain`).
3. **Task execution** (`execute`) → the executor tier matching the
   task's `load` (mapping below). Wave construction and fan-out rules
   live in `execute-mode.md § Delegating to executors`.
4. **Criteria verification** (`validate`) → `verify`. It consumes the
   PRD's parsed `criteria:` schema and returns a per-criterion verdict
   with evidence (see `validate-mode.md`).

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

Before invoking **any** subagent, check the toolchain state at
`.atl/tool-layout.md` (written by `jaiba-doctor`):

1. **The subagent exists** in the host's agents folder. Not installed
   ⇒ say so, **suggest running `jaiba-configure` to install the battery
   for this agent specifically**, and use the fallback path in the
   meantime — don't invoke and hope. Never assume the battery is
   present just because `jaiba-configure` was run on this machine
   before: it may have been run for a different host (e.g. Claude Code
   configured, Cursor — running this same repo — not).
2. **Every tool in its `requires:` is recorded as present.** A tool
   listed as **missing** ⇒ **surface it now**: name the tool, name the
   subagent that demands it, and offer the choice — install it, or
   proceed on the fallback path. A missing tool must never be
   discovered as a late failure inside the subagent's run.
3. **No `.atl/tool-layout.md` at all** ⇒ the toolchain is unprobed,
   not fine. Say so, route the developer to `jaiba-doctor` for a
   baseline probe, and until then treat subagent tool needs as
   unverified — fallback paths are the safe default.

This check is cheap (one file read) and non-negotiable: the sad path
"tool missing" is handled *before* invocation, every time.

## `load` → executor tier

The `load` label assigned in the `tasks` phase (criteria in
`tasks-mode.md § What a task is`) maps one-to-one onto the executor
battery:

| `load` | Executor | Model class (declarative) | Fits |
|---|---|---|---|
| `high` | `executor-high` | top reasoning tier — Opus/Sonnet class | design judgment, multi-file changes, ambiguity to resolve while working |
| `medium` | `executor-medium` | balanced tier — Sonnet class | bounded implementation with a clear contract |
| `low` | `executor-low` | fast/cheap tier — Haiku/Flash class | mechanical, repetitive, zero-judgment work |

The model per tier is **declarative**: each definition names the model
class, not a frozen model ID — the host resolves it to whatever
current model fills that class. If in doubt between two tiers, take
the higher one; a `low` executor improvising on a `medium` task costs
more than the tier saved.

## The invocation envelope (executors)

An executor receives exactly three things — and no more:

1. **The task** — ID, verbatim statement from `tasks.md`, `load`,
   `covers` criteria IDs.
2. **Minimal context** — the plan excerpt that governs the task, the
   concrete files/paths involved, and any constraint the plan or
   constitution imposes on this specific change. Not the whole plan,
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
- **Fan-out limit: 3.** At most three executors in flight at once,
  even if the wave is wider. Beyond that, review quality collapses and
  reintegration becomes the bottleneck. Larger waves run in batches.
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

## Fallback: no subagent support

If the host agent cannot spawn subagents (or the battery isn't
installed, or a required tool is missing and the developer chose not
to install it), every delegation above degrades to the same work done
**inline and sequentially** by conduct itself: survey the
code yourself, do the memory contrast yourself, execute tasks one by
one in dependency order, verify criteria manually
(`validate-mode.md § Fallback`). The chain's outputs are identical —
delegation is an efficiency and context-isolation device, never a
functional dependency.

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
