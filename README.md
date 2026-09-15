# 🦀 JAIBA

**Joint-operations Artificial Intelligence Behavioral Architecture**

> *A framework for AI agent-assisted software development, designed to keep the human always in the loop.*

---

[![Framework](https://img.shields.io/badge/framework-agentic--dev-blue?style=flat-square)](.)
[![Paradigm](https://img.shields.io/badge/paradigm-spec--driven-orange?style=flat-square)](.)
[![Human in the loop](https://img.shields.io/badge/human-in%20the%20loop-green?style=flat-square)](.)
[![Greenfield](https://img.shields.io/badge/scope-greenfield%20%2B%20brownfield-purple?style=flat-square)](.)

---

- [🦀 JAIBA](#-jaiba)
  - [🚀 Getting Started](#-getting-started)
    - [1. Configure your machine (once)](#1-configure-your-machine-once)
    - [2. Initialize JAIBA in your repository](#2-initialize-jaiba-in-your-repository)
    - [Alternative: Project-scoped installation](#alternative-project-scoped-installation)
  - [Installation modes](#installation-modes)
    - [Global installation (Recommended ✅)](#global-installation-recommended-)
    - [Project-scoped installation (Legacy)](#project-scoped-installation-legacy)
  - [What is JAIBA?](#what-is-jaiba)
    - [Core principles](#core-principles)
  - [System architecture](#system-architecture)
  - [🧭 Routing: one chain, two lanes](#-routing-one-chain-two-lanes)
  - [🧠 Memory structure: the agent's brain](#-memory-structure-the-agents-brain)
    - [The behavioral contract: global + repo marker](#the-behavioral-contract-global--repo-marker)
    - [`memory/` — Constitutive memory](#memory--constitutive-memory)
      - [Concept bundle (current default)](#concept-bundle-current-default)
      - [Legacy flat layout (still supported)](#legacy-flat-layout-still-supported)
      - [`log/`](#log)
    - [`work/` — Executive memory](#work--executive-memory)
    - [`vendored/` — Local copies of external references](#vendored--local-copies-of-external-references)
  - [⚙️ Skills: the workflows](#️-skills-the-workflows)
    - [🎼 `conduct` — the SDD chain](#-conduct--the-sdd-chain)
    - [⚡ `fast` — implicit inline lane](#-fast--implicit-inline-lane)
    - [💬 `ask` — implicit read-only lane](#-ask--implicit-read-only-lane)
    - [🧰 `jaiba-configure` — machine setup](#-jaiba-configure--machine-setup)
    - [🏗️ `jaiba-init` — repo bootstrap and brain maintenance](#️-jaiba-init--repo-bootstrap-and-brain-maintenance)
    - [🩺 `jaiba-doctor`](#-jaiba-doctor)
  - [🤖 The subagent battery](#-the-subagent-battery)
  - [Typical workflow](#typical-workflow)
  - [Design philosophy](#design-philosophy)
  - [Usage examples](#usage-examples)
    - [Example 1 — Deep requirement (spec depth: PRD + plan)](#example-1--deep-requirement-spec-depth-prd--plan)
    - [Example 2 — Executing with subagent waves](#example-2--executing-with-subagent-waves)
    - [Example 3 — Shallow change (design depth: plan only)](#example-3--shallow-change-design-depth-plan-only)
  - [Migrating from the pre-conduct layout](#migrating-from-the-pre-conduct-layout)
  - [Glossary](#glossary)


## 🚀 Getting Started

Adoption happens in **two independent runs**, because setup itself is split in two: one skill sets up your *machine*, another instruments each *repository*.

### 1. Configure your machine (once)

Install the machine-setup skill, then run it:

```bash
npx skills add atlasfoo/jaiba-framework#v2.1.0 --skill jaiba-configure -g
```

The `#v2.1.0` suffix pins the install to that git tag — the tag *is* the framework's version, and `jaiba-configure`/commitizen keep it in lockstep on every release.

```text
/jaiba-configure
```

*Or simply: "configure jaiba on this machine"*

`jaiba-configure` does exactly three things, all of them global — it touches **no repository**:
- Installs the **global JAIBA Behavioral Contract** (`jaiba-contract.md`) into your agent's user-level config
- Installs the **workflow/meta skillset** (`conduct`, `ask`, `fast`, `jaiba-init`, `jaiba-doctor`, …) globally — or project-locally, if you want one project's versions pinned
- Installs the **subagent battery** (executors + specialists) into your agent's global `agents/` folder

It is **safe to re-run**: that is how a machine gets refreshed after a framework upgrade. Anything already present but different is a question, never a silent overwrite.

Prefer to install the skillset yourself? This still works, and `jaiba-configure` will simply report everything as already current:

```bash
npx skills add -y atlasfoo/jaiba-framework#v2.1.0 -g
```

**Benefits of the global skillset:**
- Skills are available instantly in any project without per-project setup
- Consistent behavior across all your projects
- Automatic updates apply to all projects
- Reduced repository clutter (no `.agents/` folder needed per project)

### 2. Initialize JAIBA in your repository

Navigate to the root of the project you want to adopt and run:

```text
/jaiba-init
```

*Or simply: "set up jaiba in this project" or "bootstrap jaiba"*

`jaiba-init` instruments **that one repo**, end to end:
- Creates the `.ai/` brain skeleton (`memory/` + `memory/log/`, `work/`, `vendored/`) and its `.gitignore`, plus the gitignored `.atl/` for machine-local state
- Drops the minimal `AGENTS.md` marker at the repo root (offering replace / coexist if you already have one)
- **Checks** that the global contract and subagent battery exist — and only checks: if they're missing it names `jaiba-configure`, it never installs them itself
- Continues into its own `update-brain` initialize mode to populate the long-term memory — an internal mode switch, not a hand-off to another skill
- Hands off to `jaiba-doctor` for the first health check and toolchain probe (`.atl/tool-layout.md`)

Run it once per repository. On an already-instrumented repo it resumes or routes instead of bootstrapping.

### Alternative: Project-scoped installation

If you prefer JAIBA's skills scoped to individual projects rather than to your machine (not recommended), answer *project-local* when `jaiba-configure` asks where the missing skills should go; only `jaiba-configure` itself needs to stay global. Step 2 is unchanged either way — `jaiba-init` is always repo-scoped.

---

## Installation modes

### Global installation (Recommended ✅)

Skills are installed globally using `npx skills add` and are available across all your projects:

| Aspect | Global |
|--------|--------|
| **Command** | `npx skills add -y atlasfoo/jaiba-framework#v2.1.0 --skill <skill-name>` |
| **Location** | `~/.agents/skills/` (user home directory) |
| **Availability** | All projects automatically have access |
| **Setup per project** | Only instrument the repo with `/jaiba-init` |
| **Disk footprint** | Minimal — skills are stored once |
| **Updates** | `npx skills update` applies to all projects |
| **Recommended for** | Teams, multi-project workflows, clean repositories |

**How it works:**
1. Run `/jaiba-configure` once — contract, skillset and subagents land in your agent's global config
2. In each project, run `/jaiba-init` to instrument the repo (`AGENTS.md` marker + `.ai/` brain + `.atl/`)
3. All skills automatically activate in every project you work on

### Project-scoped installation (Legacy)

Skills are installed locally in each project under `.agents/` or `.claude/skills/`:

| Aspect | Project-scoped |
|--------|-----------------|
| **Command** | `jaiba-configure` installs the missing skills locally when you choose *project-local* |
| **Location** | `.agents/` or project skill folder |
| **Availability** | Only in that specific project |
| **Setup per project** | A `jaiba-configure` run per project, plus the `jaiba-init` run |
| **Disk footprint** | Each project has its own copy of skills |
| **Updates** | Must re-run `jaiba-configure`, or update manually, per project |
| **Recommended for** | Legacy setups, isolated environments |

---

## What is JAIBA?

JAIBA is an agile development framework designed for teams that work with AI agents as co-pilots in building software. It is not a tool, an AI model, or a collection of loose prompts: it is a **behavioral architecture** that defines how to organize context, how to orchestrate workflows, and how to keep the human as the central decision-maker at every significant stage of development.

JAIBA starts from a simple premise: **the code is the context**, and the agent must understand the project the way a senior developer who has been working on it for weeks would.

### Core principles

| Principle | Description |
|---|---|
| 🧠 **Code as context** | The agent works on the real foundation of the project: architecture, decisions, dependencies, and conventions living in the repository. Context is not improvised — it is built and maintained. |
| 👤 **Human in the loop** | No significant change happens without human validation. The agent proposes, reasons, and executes bounded tasks; the developer approves, redirects, and decides. |
| 📚 **Continuous learning** | The system is designed to capture knowledge: every architectural decision, every integration, every relevant change is recorded to feed future cycles. |
| 🌱 **Greenfield and brownfield** | JAIBA works on brand-new projects and on existing legacy systems. The brain-building process allows the agent to adapt to any codebase. |

---

## System architecture

JAIBA organizes its operation in three layers: the **memory structure** (the agent's brain), the **skills library** (the executable workflows), and the **subagent battery** (delegated execution).

```
~/.claude/  (or your agent's global config)
├── jaiba-contract.md                   ← Global behavioral contract (one per machine)
├── skills/                             ← JAIBA skills, installed globally
└── agents/                             ← Subagent battery: executor-high/-medium/-low,
                                          code-analyst, business-analyst, verify

project/
├── AGENTS.md                           ← Minimal marker: points at the global contract
├── .ai/                                ← Agent brain
│   ├── memory/                         ← Constitutive memory (versioned)
│   │   ├── index.md                    ← Bundle entry point (current default — see below)
│   │   ├── identity/                   ← project, architecture, purpose, scope, quality-gate, conventions
│   │   ├── decisions/                  ← one file per ADR: <NNN>-<slug>.md
│   │   ├── references/                 ← one file per external surface: <slug>.md
│   │   │                                  (legacy flat: constitution.md / adr-log.md / reference-index.md — still supported, no index.md)
│   │   └── log/                        ← Append-only: closed work + brain changelog
│   │       └── YYYY-MM-DD-slug.md
│   ├── work/                           ← Executive memory (gitignored)
│   │   ├── PRD.md                      ← Only when triage demands spec depth
│   │   ├── plan.md                     ← Active design
│   │   ├── tasks.md                    ← T-NNN task graph (depends-on, load)
│   │   └── walkthrough.md              ← Change-by-change narrative
│   └── vendored/                       ← Local copies of external references
├── .atl/                               ← Toolchain layer (gitignored)
│   └── tool-layout.md                  ← Machine probe written by jaiba-doctor
└── src/ ...                            ← Your project
```

---

## 🧭 Routing: one chain, two lanes

Since the conduct unification, the developer **does not choose between commands**. The global contract defines a routing rule the agent applies to every message:

| Your message is… | The framework routes to |
|---|---|
| A continuation cue with active work ("continue", "next", "go") | `conduct`, phase `execute` |
| A question (code, active work, past decisions) | `ask` — read-only |
| A small contained change ("quick fix", "bump X") | `fast` — inline lane |
| New work to shape or plan | the `conduct` chain (entry phase per triage) |

`ask` and `fast` are **implicit-only**: they have no slash commands. `conduct` keeps `/conduct [phase]` as a deterministic override for when routing misfires or you want to force a phase. The meta-skills (`/jaiba-configure`, `/jaiba-init`, `/jaiba-doctor`) remain explicit.

A single **triage** (shared by the chain and `fast`) maps each change's blast radius to a depth on the continuum `inline → design → spec`: an atomic edit executes on the spot; a bounded change gets a plan; a multi-faceted requirement gets a PRD *and* a plan. A critical-library bump or a performance fix does **not** produce a PRD — depth follows blast radius, not ceremony.

---

## 🧠 Memory structure: the agent's brain

The `.ai/` folder is the core of JAIBA. Memory collapses into **two categories**:

- **Constitutive** — who the project is: identity, decisions, external surfaces. Stable, versioned, in `.ai/memory/`.
- **Executive** — what is being done right now: PRD (if any), plan, tasks, walkthrough. Ephemeral per piece of work, gitignored, in `.ai/work/`.

### The behavioral contract: global + repo marker

Behavior does not live per-repo anymore. `jaiba-configure` installs the **JAIBA Behavioral Contract** (`jaiba-contract.md`) once per machine into the agent's global config: the brain map, the numbered behavioral rules, the routing rule, security and toolchain discipline. Each repo keeps only a **minimal `AGENTS.md` marker** — dropped by `jaiba-init` — that confirms instrumentation and defers to the global contract for behavior and to the constitution for project facts. The split is the same one that separates the two setup skills: `jaiba-configure` owns the machine half, `jaiba-init` the repo half.

`jaiba-doctor` checks the contract's presence and drift against the packaged version on every health check.

### `memory/` — Constitutive memory

`.ai/memory/` comes in **two supported layouts** — a repo holds one or
the other, resolved by whether `index.md` exists (both existing at once
is treated as ambiguous and surfaced to the human, never silently
picked). Neither is a fallback: the flat layout is a fully supported,
warning-free state, not drift toward the bundle. Converting one to the
other is optional and human-triggered (`jaiba-init:update-brain:migrate`)
— it is never offered unprompted.

#### Concept bundle (current default)

What `jaiba-init:update-brain:initialize` builds today: one file per
concept, of a closed `type:` (`project`, `architecture`, `purpose`,
`scope`, `sub-unit`, `quality-gate`, `convention`, `decision`,
`reference`, `snippet`, `log-entry`, plus the `index` type below), all
reachable in one hop from `.ai/memory/index.md`. Relations are
file-relative markdown links, never section-number citations. The
closed vocabulary and per-type frontmatter live in
`jaiba-init/references/okf-pattern.md`.

- **`index.md`** — the bundle's only entry point: one link and one line
  (each concept's `description:`) per concept, grouped by `type:`.
- **`identity/`** — `project.md`, `architecture.md`, `purpose.md`,
  `scope.md`, `quality-gate.md`, `conventions.md`, and
  `units/<slug>.md` for monorepos / multi-project solutions.
- **`decisions/<NNN>-<slug>.md`** — one file per Architecture Decision
  Record. Superseded decisions stay in place, flipped to
  `status: superseded` with a `superseded-by:` link — never deleted,
  never renumbered.
- **`references/<slug>.md`** — one file per **external surface** (APIs,
  packages, services) or **internal cross-component contract** (event
  schemas, APIs between sub-units), carrying `tier`, `kind`, `role` and
  its consultation point; when vendored, the local copy path.

#### Legacy flat layout (still supported)

Projects instrumented before the concept bundle, or that simply haven't
converted, keep three files instead — same content, one file each:

- **`constitution.md`** — the project's **executive summary**: what the
  system does and for whom, stack and architecture, team conventions,
  sub-unit scopes, and the **Quality Gate**.
- **`adr-log.md`** — the **curated** decision memory: ADRs currently in
  force. Superseded entries are marked, never deleted.
- **`reference-index.md`** — the index of **external surfaces** and
  **internal cross-component contracts**, one entry each.

#### `log/`
The **chronological** memory: an append-only record fusing closed work and the brain's changelog, one dated file per entry (`YYYY-MM-DD-slug.md`, kinds `work-closure` and `brain-change`). Where the decision concepts (or `adr-log.md` in the legacy flat layout) answer "what do we hold true today", `log/` answers "what happened, in order" — identical in both layouts. Written by `conduct:summarize` (work closures) and `jaiba-init:update-brain` (brain changes) — the framework's one sanctioned carve-out to the "only `jaiba-init:update-brain` writes memory" rule.

### `work/` — Executive memory

The active piece of work, gitignored (multi-session; plan phases are the checkpoints):

| File | Produced by | Purpose |
|---|---|---|
| `PRD.md` | `spec` phase (only at spec depth) | The *what/why*: business problem + acceptance criteria `<PREFIX>-NNN` in Given/When/Then happy/sad, serialized as a parseable schema the `verify` subagent consumes. |
| `plan.md` | `spec` phase (design) | The approved design: objective, scope, technical approach, amendments. |
| `tasks.md` | `tasks` phase | The work graph: tasks with IDs `T-NNN`, `depends-on`, cognitive `load` (high/medium/low), and covered criteria — the input for parallel execution waves. |
| `walkthrough.md` | `execute` phase | Change-by-change narrative: what, why, deviations, ADR candidates. |

When the work closes, `conduct:summarize` distills the essence into `.ai/memory/log/` and cleans `work/` — in a single, human-confirmed step.

### `vendored/` — Local copies of external references

Not a memory category, but a **store** backing the `reference` concepts (or `reference-index.md` in the legacy flat layout). When an external reference can't (or shouldn't) be fetched live — an OpenAPI contract, a Repomix bundle of a dependency — a copy lives here and the reference's `resource:` (or index entry) points at it. Versioned alongside the code; `jaiba-doctor` warns when a vendored copy goes stale (older than a month by git date).

---

## ⚙️ Skills: the workflows

### 🎼 `conduct` — the SDD chain

The unified workflow (it absorbed the former `planning` and `specification` skills). One chain of Spec Driven Development phases; the triage decides how deep each change enters:

| Phase | Artifact | What happens |
|---|---|---|
| **`propose`** *(optional)* | — (conversational) | Shape a fuzzy requirement: questions, ambiguities, scope. Persists nothing; flows into `spec`. |
| **`spec`** | `PRD.md` (spec depth only) + `plan.md` (always) | *Define*: PRD with numbered, parseable acceptance criteria — only when triage demands it. *Design*: the plan. Ends at **explicit human approval** of the design. |
| **`tasks`** | `tasks.md` | Decompose the design into a task graph: `T-NNN`, `depends-on`, `load`, covered criteria. Phases act as multi-session checkpoints with their own gate. |
| **`execute`** *(implicit)* | `walkthrough.md` | Advance the work — directly or by delegating task waves to the executor subagents. Triggered by continuation cues; no command needed. |
| **`validate`** | — | Run the plan's quality gate and check acceptance criteria one by one (delegating to the `verify` subagent when available), reporting met/unmet per criterion. |
| **`summarize`** | log entry in `.ai/memory/log/` | Single closing step: present the final summary, propose ADRs/constitution changes for `jaiba-init:update-brain`, archive the essence, clean `work/` — one confirmation. |

> **Golden rules:** the human approves the design before anything executes; execution pauses at phase boundaries; the plan never silently drifts — structural deviations amend `plan.md` explicitly.

### ⚡ `fast` — implicit inline lane

Direct execution for small, well-scoped, low-risk changes — the sanctioned exception to "no blind coding". Not user-invocable: the routing rule triggers it on "quick fix" / "bump X" / "rename this" style requests.

- **Shares conduct's triage** with default and floor `inline`: if the change triages `design` or deeper, `fast` refuses and routes into the chain.
- **Free-standing:** acts directly, writes nothing to `.ai/work/`; git history plus a one-line recap is the record.
- **Plan adjustment:** with an active plan, executes the out-of-band change and — after developer confirmation — records it into the plan artifacts.
- **Big out-of-band change during an active plan:** surfaces it and offers exactly two exits — fold it in as a new plan phase, or park-and-replan. Never builds a second plan silently.

### 💬 `ask` — implicit read-only lane

Pure query mode, triggered by interrogative messages. Strictly read-only: reads, searches, explains; never edits code, never writes artifacts.

- **Answers cold** — orients from the repository, so questions about the active work (`.ai/work/`) or past decisions (`.ai/memory/`) work on a session's first message.
- **Four domains:** code, active plan, active PRD, decisions (`decision` concepts, or `adr-log.md` in the legacy flat layout, plus `memory/log/`).
- **Hands off to action:** a continuation cue routes to `conduct:execute`; new work enters the chain; a contained change goes to `fast` — carrying the context it already gathered.

### 🧰 `jaiba-configure` — machine setup

The **machine** half of setup, and nothing else: the global behavioral contract, the workflow/meta skillset, the subagent battery. It never touches a repository — no `.ai/`, no `.atl/`, no `AGENTS.md` — and carries no brain templates at all. Run from anywhere, once per machine, and **safe to re-run** as the upgrade path: every divergence from the packaged version is a question, never a silent overwrite. It names `jaiba-init` as the next step for a specific project, but never invokes it.

### 🏗️ `jaiba-init` — repo bootstrap and brain maintenance

The **repo** half of setup, and the framework's long-term memory owner. Two modes:

- **Bootstrap** (bare `jaiba-init`) — instrument this repository: the `AGENTS.md` marker, the `.ai/` skeleton and `.atl/`, then the constitutive memory, then the first `jaiba-doctor` checkup. It *checks* for the global contract and battery and routes to `jaiba-configure` if they're absent; it never installs them.
- **Maintain** (`jaiba-init:update-brain`) — the constitutive-memory workflow, and the **only** skill that writes `.ai/memory/` (log appends excepted). Its `initialize` sub-mode builds the brain from repository analysis (essential for brownfield onboarding), producing the concept bundle by default; `update` applies proposed decisions, references and identity changes (bundle) or ADRs, reference-index entries and constitution changes (legacy flat), or reconciles the brain after structural drift; `migrate` converts an existing flat brain to the bundle, human-triggered only. Every brain change leaves a `brain-change` entry in `memory/log/`.

Bootstrap ends *inside* `initialize`: laying the skeleton and filling the brain are two modes of the same skill, so there is no hand-off between them — `jaiba-init` owns the templates and the initialize logic outright.

### 🩺 `jaiba-doctor`

The framework health check — a pre-flight before entering the conduct chain. **Diagnoses and routes; never repairs.** Three diagnostics, one severity-ordered report:

| Diagnostic | What it checks | Where the fix routes |
|---|---|---|
| **Memory coherence** | Behavioral contract present and drift-free (repo marker + global copy vs packaged version); resolves the `.ai/memory/` layout first (concept bundle vs legacy flat, per the dual-resolution rule) and checks it — bundle graph integrity (no broken links, every concept carries `type:`) or the three flat files — complete, mutually consistent, and not drifting from the repo; curated-vs-chronological separation intact. | `jaiba-init` (brain, repo marker) / `jaiba-configure` (global contract) |
| **Tool state** | Are the CLI tools that installed skills, **subagents**, and hooks declare (`requires:`) actually present? Refreshes `.atl/tool-layout.md` with provenance. | install the tool |
| **External-reference health** | Every `reference` concept (or `reference-index.md` entry, legacy flat) reachable: MCP/CLI installed, remote spec live, vendored copy present and fresh. | install · fix endpoint · re-vendor via `jaiba-init:update-brain` |

---

## 🤖 The subagent battery

`jaiba-configure` installs six native subagent definitions into the agent's global `agents/` folder. The invocation contract (`conduct/references/subagents.md`) governs delegation: which operations delegate, the `requires:` tool convention, a **pre-invocation toolchain check** against `.atl/tool-layout.md` (a missing tool surfaces *before* invocation, never as a mid-run failure), and the concurrency policy.

| Subagent | Role | Used in phase |
|---|---|---|
| `executor-high` | Design-heavy, multi-file tasks (`load: high`) | `execute` |
| `executor-medium` | Bounded implementation tasks (`load: medium`) | `execute` |
| `executor-low` | Mechanical, repetitive tasks (`load: low`) | `execute` |
| `code-analyst` | Code survey without loading conduct's context | `spec` (define/design) |
| `business-analyst` | Contrasts the requirement against the identity/decision/reference concepts (or constitution / adr-log / reference-index, legacy flat) | `propose`, `spec` |
| `verify` | Consumes the PRD's criteria schema; reports met/unmet per criterion | `validate` |

**Parallelism:** `execute` builds **waves** from the `tasks.md` `depends-on` graph — fan-out capped at 3, two tasks run in parallel only if they don't share files, subagents write source only (conduct is the single writer of `.ai/work/`), and results reintegrate into the walkthrough before the next wave. Hosts without subagent support fall back to sequential execution under the same contract.

---

## Typical workflow

```
    ┌────────────────────────────┐   ┌─────────────────────────────┐
    │   Your machine (once)      │   │    New or legacy project     │
    └─────────────┬──────────────┘   └──────────────┬──────────────┘
                  │                                 │
          /jaiba-configure                     /jaiba-init
   (contract + skillset + subagents)   (AGENTS.md marker + .ai/ + .atl/)
                  │                                 │
                  │  independent: neither           │
                  │  invokes the other; init        ▼
                  └── only *checks* for it ─▶ update-brain:initialize
                                                    │  (internal mode switch)
                                                    ▼
                                              jaiba-doctor
                                          (first checkup + probe)
                                                    │
                                   ┌────────────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │        Brain ready           │
                    └──────────────┬──────────────┘
                                   │
                        ── routing rule per message ──
                                   │
        ┌──────────────┬───────────┴──────────┬─────────────────┐
        │              │                      │                 │
    New work      Continuation            Question        Small change
        │              │                      │                 │
  conduct    conduct:            ask (read-        fast (inline;
  chain: propose? → execute                only lane)        refuses > inline
  spec (PRD? + plan   (waves of                              and routes into
  → approval) →       subagents)                             the chain)
  tasks → execute →
  validate → summarize
        │
        └──→ .ai/memory/log/ entry + proposed ADRs → jaiba-init:update-brain
                                   │
                              ┌────▼────┐
                              │  repeat  │
                              └─────────┘
```

---

## Design philosophy

### The agent as co-pilot, not pilot

JAIBA does not seek to automate development. It seeks to amplify the developer's capacity while maintaining human authorship over the decisions that matter. The agent is an extraordinarily productive collaborator that needs direction, context, and validation.

### Memory as a first-class citizen

The source code and the `.ai/` files are equally part of the project. The agent's memory is not a temporary file or a throwaway prompt: it is a team artifact that lives in the repository, evolves with the project, and is readable by any human collaborator.

### Workflows as contracts

Each skill defines clear expectations for both the agent and the human. Knowing which phase conduct is operating in eliminates ambiguity and reduces errors from context misunderstandings.

---

## Usage examples

The following examples are based on **TripNest**, a travel planning application built with Python and Django.

---

### Example 1 — Deep requirement (spec depth: PRD + plan)

> 👤 *"I want users to be able to create itineraries and share them with other people so they can edit them together."*

The routing rule reads this as **new work**; the triage scores a cross-cutting blast radius → **spec depth**. The chain enters at `propose`: the agent (optionally delegating a memory contrast to `business-analyst`) asks the narrowing questions — real-time or asynchronous editing? roles? conflict policy?

In `spec`, it drafts `.ai/work/PRD.md` with numbered, parseable criteria:

```markdown
## Acceptance criteria

​```yaml
criteria:
  - id: COL-001
    kind: happy
    given: an itinerary owner with a collaborator's email
    when: they send an invitation
    then: the collaborator receives edit access with the assigned role
  - id: COL-002
    kind: sad
    given: a reader-role collaborator
    when: they attempt to modify an activity
    then: the change is rejected and the UI explains the missing permission
​```
```

…then the design (`plan.md`). The human approves the design; `tasks` produces the graph (`T-001 … T-014`, each with `depends-on`, `load`, and `covers:` pointing at criteria IDs).

### Example 2 — Executing with subagent waves

> 👤 *"continue"*

Routing: continuation cue → `conduct:execute`. Conduct checks `.atl/tool-layout.md` against each subagent's `requires:`, builds the first wave from the `depends-on` graph, and fans out: `T-003` (model, `load: high`) to `executor-high`, `T-004` (serializer, `load: medium`) to `executor-medium` — in parallel, because they share no files. Each executor returns a diff + report; conduct reviews, logs the walkthrough entry, flips the checkboxes, and runs the phase gate before the next wave.

At the end, `validate` hands the PRD's criteria schema to `verify`, which reports per criterion:

```
COL-001  ✅ met      — invitation flow test green (test_invite_by_email)
COL-002  ✅ met      — permission rejection covered (test_reader_cannot_edit)
COL-003  ❌ not met  — change history endpoint returns 404; T-012 unchecked
```

`summarize` then closes in one step: final summary presented, `2026-07-05-collaborative-itineraries.md` appended to `.ai/memory/log/`, an ADR proposed (object permissions via `django-guardian`) for `jaiba-init:update-brain`, and `work/` cleaned — after one confirmation.

### Example 3 — Shallow change (design depth: plan only)

> 👤 *"We have an N+1 problem in the itinerary list view. We need to optimize the queries."*

New work, but the triage scores it **design depth** — bounded blast radius, no business dimension. **No PRD is produced**: the chain enters at `spec`'s design half, writes a short `plan.md` (profiling phase + fix phase), gets approval, and executes. A performance fix never pays the ceremony of a spec.

*(Had the developer instead said "bump `requests` to 2.32", the routing rule would have sent it to `fast`: triage `inline`, executed on the spot, no executive artifacts at all.)*

---

## Migrating from the pre-conduct layout

> Not to be confused with converting `.ai/memory/` from the legacy flat
> layout to the concept bundle — that's `jaiba-init:update-brain:migrate`,
> optional and human-triggered. This section covers an older, unrelated
> migration: off the pre-`conduct` skillset entirely.

Projects instrumented before the conduct unification use `planning`/`specification` skills and an older brain layout. There is no automatic migration; the manual route:

1. `.ai/session/` → `.ai/work/` (rename; add `work/` to `.ai/.gitignore`, remove `session/` from tracking if needed).
2. `.ai/memory/archive/plans/` and `archive/specs/` → `.ai/memory/log/` (move files; keep their dated names).
3. `.ai/specs/<name>/` — fold any *active* spec's PRD into `.ai/work/PRD.md` (user stories become the PRD's criteria section); delivered specs go to `memory/log/`.
4. Replace the full per-repo `AGENTS.md` with the minimal marker (`jaiba-init` bootstrap step 3 offers replace/coexist) and run `jaiba-configure` to install the global contract (its step 2).
5. Uninstall the `planning` and `specification` skills; install `conduct`.
6. Run `/jaiba-doctor` — it detects leftover old-layout directories and contract drift, and routes the remainder.

---

## Glossary

| Term | Definition |
|---|---|
| **Brain** | The set of files in `.ai/` that make up the agent's persistent context |
| **Constitutive memory** | `.ai/memory/`: identity, decision and reference concepts reachable from `index.md` (or constitution / curated ADR log / reference index, legacy flat) plus the chronological log — who the project is |
| **Concept bundle** | The current-default `.ai/memory/` layout: one file per constitutive concept, closed `type:` vocabulary, all reachable from `index.md` |
| **Legacy flat layout** | The pre-bundle `.ai/memory/` layout — three files (`constitution.md`, `adr-log.md`, `reference-index.md`) plus `log/`. Still fully supported; converting to the bundle is optional and human-triggered |
| **Executive memory** | `.ai/work/`: PRD (if any), plan, tasks, walkthrough — what is being done right now (gitignored) |
| **Behavioral contract** | `jaiba-contract.md`, installed once per machine in the agent's global config; each repo keeps a minimal `AGENTS.md` marker pointing at it |
| **Triage** | The shared blast-radius → depth mapping (`inline → design → spec`) that decides how deep a change enters the chain |
| **Chain** | Conduct's SDD phases: `propose → spec → tasks → execute → validate → summarize` |
| **Lane** | An implicit, routing-triggered skill: `ask` (read-only) or `fast` (inline execution) |
| **Wave** | A set of file-disjoint tasks `execute` fans out to executor subagents in parallel (cap 3) |
| **Skill** | An executable workflow with defined phases/modes and human validation checkpoints |
| **Subagent battery** | The six globally-installed agents: three executors by cognitive load + `code-analyst`, `business-analyst`, `verify` |
| **Human in the loop** | The principle that the human validates and approves before each significant stage |

---

<div align="center">

**JAIBA** · Joint-operations Artificial Intelligence Behavioral Architecture 🦀

*AI-assisted development should not be black magic. It should be engineering.*

</div>
