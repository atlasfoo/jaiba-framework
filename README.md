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
    - [1. Install the Scaffold Skill globally](#1-install-the-scaffold-skill-globally)
    - [2. Initialize JAIBA in your repository](#2-initialize-jaiba-in-your-repository)
  - [What is JAIBA?](#what-is-jaiba)
    - [Core principles](#core-principles)
  - [System architecture](#system-architecture)
  - [🧠 Memory structure: the agent's brain](#-memory-structure-the-agents-brain)
    - [`AGENTS.md` — Behavior guidelines](#agentsmd--behavior-guidelines)
    - [`memory/` — Long-term memory](#memory--long-term-memory)
      - [`constitution.md`](#constitutionmd)
      - [`adr-log.md`](#adr-logmd)
      - [`reference-index.md`](#reference-indexmd)
      - [`archive/plans/`](#archiveplans)
    - [`specs/` — Mid-term memory](#specs--mid-term-memory)
      - [`PRD.md` (Product Requirements Document)](#prdmd-product-requirements-document)
      - [`user-stories.md`](#user-storiesmd)
    - [`session/` — Short-term memory](#session--short-term-memory)
      - [`plan.md`](#planmd)
      - [`tasks.md`](#tasksmd)
      - [`walkthrough.md`](#walkthroughmd)
      - [`<slug>-summary.md`](#slug-summarymd)
    - [`vendored/` — Local copies of external references](#vendored--local-copies-of-external-references)
  - [⚙️ Skills: the workflows](#️-skills-the-workflows)
    - [📋 `skill: planning`](#-skill-planning)
    - [📐 `skill: specification`](#-skill-specification)
    - [🔄 `skill: update-brain`](#-skill-update-brain)
    - [⚡ `skill: fast`](#-skill-fast)
    - [💬 `skill: ask`](#-skill-ask)
    - [🩺 `skill: doctor`](#-skill-doctor)
  - [Typical workflow](#typical-workflow)
  - [Design philosophy](#design-philosophy)
    - [The agent as co-pilot, not pilot](#the-agent-as-co-pilot-not-pilot)
    - [Memory as a first-class citizen](#memory-as-a-first-class-citizen)
    - [Workflows as contracts](#workflows-as-contracts)
  - [Usage examples](#usage-examples)
    - [Example 1 — `skill: specification` · New requirement](#example-1--skill-specification--new-requirement)
    - [Example 2 — `skill: planning` within an active spec](#example-2--skill-planning-within-an-active-spec)
    - [Example 3 — `skill: planning` standalone (outside a spec)](#example-3--skill-planning-standalone-outside-a-spec)
  - [Glossary](#glossary)


## 🚀 Getting Started

To adopt JAIBA in your project, follow these two steps:

### 1. Install the Scaffold Skill globally
First, install the meta-skill that handles the JAIBA bootstrap process.

```bash
npx skills add -y atlasfoo/jaiba-framework --skill jaiba-scaffold
```

### 2. Initialize JAIBA in your repository
Navigate to the root of your project and ask the agent to set up the framework. This will create the brain skeleton, install the project-scoped skills, and probe your local toolchain.

```text
/jaiba-scaffold
```
*Or simply: "set up jaiba in this project"*

Once the scaffold is complete, it will hand over to `update-brain:initialize` to analyze your repository and populate the long-term memory.

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

JAIBA organizes its operation in two layers: the **memory structure** (the agent's brain) and the **skills library** (the executable workflows).

```
project/
├── AGENTS.md                           ← Agent behavior guidelines
├── .ai/                                ← Agent brain
│   ├── memory/                         ← Long-term memory
│   │   ├── constitution.md             ← Project executive summary
│   │   ├── adr-log.md                  ← Architectural decision history
│   │   ├── reference-index.md          ← Index of dependencies and external APIs
│   │   └── archive/                    ← Archived summaries of closed work
│   │       ├── plans/                   ← Closed plan summaries (planning:cleanup)
│   │       │   └── YYYY-MM-DD-slug.md
│   │       └── specs/                   ← Delivered spec archives (specification:archive)
│   │           └── YYYY-MM-DD-spec-slug.md
│   ├── specs/                          ← Mid-term memory
│   │   └── [spec-name]/
│   │       ├── PRD.md                  ← Formalized business requirement
│   │       └── user-stories.md         ← User story checklist
│   ├── session/                        ← Short-term memory
│   │   ├── plan.md                     ← Active plan
│   │   ├── tasks.md                    ← Task checklist
│   │   ├── walkthrough.md              ← Session log
│   │   └── <slug>-summary.md           ← Plan summary, until cleanup archives it
│   └── vendored/                       ← Local copies of external references
│       ├── stripe-openapi.yaml          ← e.g. a vendored API contract
│       └── internal-sdk.txt             ← e.g. a Repomix bundle of a dependency
└── src/ ...                            ← Your project
```

---

## 🧠 Memory structure: the agent's brain

The `.ai/` folder is the core of JAIBA. It functions as the agent's persistent memory, divided into three time horizons: long-, mid-, and short-term.

---

### `AGENTS.md` — Behavior guidelines

Located at the project root, `AGENTS.md` is the agent's entry point: the file that defines **how it should behave**, what tools it can use, what conventions it must respect, and how it should interact with the human.

Its role is **behavior configuration, not project context**. Project information (architecture, stack, decisions) lives in `.ai/memory/constitution.md`. `AGENTS.md` points there and is deliberately kept short, establishing only the operating rules.

Typical structure of an `AGENTS.md` in JAIBA:

```markdown
# AGENTS.md

## General behavior
- Always operate within the active skill and its declared mode
- Do not modify code outside the scope agreed upon in the active plan or spec
- When in doubt, use `skill: ask` before executing

## Project context
The full project context (architecture, stack, conventions, and dependencies)
is in `.ai/memory/constitution.md`. Read it at the start of each session.

## Memory and learning
- Consult `.ai/memory/` before proposing solutions
- Record relevant decisions in `session/walkthrough.md`
- Propose updates to the brain when closing plans or specs

## Restrictions
- Do not install new dependencies without explicit human approval
- Do not commit or push autonomously (do so only if the developer explicitly asks)
- Maintain the agreed scope; if you detect out-of-scope work, notify before proceeding
```

> `AGENTS.md` is the agent's operating contract with the team. It should be the first read for any agent joining the project.

---

### `memory/` — Long-term memory

Contains the structural and permanent knowledge of the project. It is the first thing the agent consults when starting any workflow.

#### `constitution.md`
The project's **executive summary**. Answers the most important questions about the system at a glance:

- What does this project do and for whom?
- What is its technology stack and architecture?
- What are the team's conventions and scope rules?
- How does it interact with external systems?
- What is the project's stance on TDD and other planning conventions?

> It is the equivalent of the technical README a new developer should read before making their first commit.

#### `adr-log.md`
The project's **architectural decision history** (Architecture Decision Records). Each entry records:

- The decision made
- The context that motivated it
- The alternatives considered
- The expected consequences

> Allows the agent to understand *why* the project is the way it is, not just *how* it is.

#### `reference-index.md`
The **index of external dependencies**: integrated APIs, key packages, third-party services, and important libraries. For each entry it documents its purpose, where it is configured, and how it is used within the project.

> Prevents the agent from "reinventing" integrations that already exist or using incorrect versions.
>
> When a reference is stored locally rather than fetched live, the entry points at its copy under `.ai/vendored/` (see below).

#### `archive/plans/`
**Archived summaries** of already-closed plans. Each file is the output of the `planning:summarize` skill, archived by the `cleanup` mode in the format `YYYY-MM-DD-<slug>.md`. They function as the project's historical log: a developer (human or agent) can browse this directory to understand what was done, when, and why, without having to reconstruct it from commits.

> Summaries are written to be concise by design — the live detail lives in `walkthrough.md` during the session; what survives the close is the distilled version.

---

### `specs/` — Mid-term memory

Stores the project's active specifications, generated through the **Specification** workflow. Each spec lives in its own folder and represents a unit of work oriented around a business requirement.

```
specs/
└── oauth-authentication/
    ├── PRD.md              ← Formalized business requirement
    └── user-stories.md     ← User story checklist
```

#### `PRD.md` (Product Requirements Document)
Defines the **what and why** of the requirement: the business problem, acceptance criteria, assumptions, and constraints.

#### `user-stories.md`
Breaks the PRD down into **concrete user stories**, each a deliverable increment (a screen, an endpoint, an improvement, a fix). Every story is numbered `<PREFIX>-NNN` (a short uppercase prefix unique to the spec) and carries acceptance criteria split into **happy path** and **sad paths** as Given/When/Then — the direct input to business design and integration tests. Functions as a progress checklist during implementation: `planning:summarize` flips each story to `[x]` as plans deliver it.

> A spec can span multiple work sessions. It remains active until all its stories are delivered and `specification:archive` closes it.

---

### `session/` — Short-term memory

Contains the artifacts of the **Planning** workflow: the immediate working context for a session or bounded sprint. It is independent of the Specification workflow and focuses on tactical execution.

#### `plan.md`
The active work plan: session objective, relevant context, and scope agreed upon with the human.

#### `tasks.md`
The list of concrete tasks derived from the plan, organized in **phases with architectural cohesion**. Each phase declares its dependencies and leaves the code in a reversible, buildable state (suitable for a `chore(wip)` commit if the developer prefers).

#### `walkthrough.md`
The narrative record of the session: decisions made, problems encountered, and the agent's reasoning. Updated when closing each phase, not task by task. Serves as a log for human review and as a source for building the final summary.

#### `<slug>-summary.md`
The plan summary, produced by `planning:summarize` when all tasks are complete. It lives temporarily in `session/` so the developer can review it alongside the rest of the session material, and is then moved to `.ai/memory/archive/plans/` by the `cleanup` mode.

> Files in `session/` are **ephemeral**: when `planning:cleanup` runs, the summary is archived in `memory/` and the other files are deleted, leaving the space ready for the next plan.

---

### `vendored/` — Local copies of external references

Not a memory horizon, but a **store** that backs `reference-index.md`. When an external reference can't (or shouldn't) be fetched live every time it's needed, a local copy is kept here and the index entry points at it.

Typical contents:

- **Vendored API contracts** — a physical copy of a third-party or internal API's OpenAPI/GraphQL spec or docs, so the agent reads the contract from disk instead of guessing at it.
- **Repomix (or similar) bundles** — a compressed, single-file snapshot of a dependency's source or documentation, useful for libraries with non-obvious usage or internal forks.

The reference-index's *"Vendored at `<path>`"* consultation method always resolves to a path under `.ai/vendored/`. Keeping these copies in-repo means the agent's understanding of an external surface is **versioned alongside the code** — it doesn't drift when the upstream changes, and it works offline.

> Populated and curated by `update-brain`, which records the pointer in `reference-index.md`. The `doctor` skill checks that each vendored path the index references actually exists, and warns when a vendored copy is more than a month old (using git to read its last-commit date) so a stale snapshot gets re-vendored.

---

## ⚙️ Skills: the workflows

Skills are the agent's executable capabilities within JAIBA. Each skill implements a specific workflow with well-defined modes, clear transitions, and human validation checkpoints.

---

### 📋 `skill: planning`

The tactical work workflow. Designed for concrete tasks that do not require a full formal specification, but do require organization and traceability.

| Mode | Description |
|---|---|
| **`define`** | The agent collaborates with the human to define the objective, scope, and tasks of the plan. It investigates the code, detects discrepancies between the prompt/spec and the repository's reality, asks questions to resolve them, and generates `plan.md` and `tasks.md`. |
| **`execute`** *(implicit)* | The agent works through the tasks in the active plan, phase by phase. No explicit invocation is required: it activates when there is an approved plan and the developer's message is a continuation signal (`continue`, `next`, `proceed`). Updates `tasks.md` and `walkthrough.md`, suggests a `chore(wip)` commit at the close of each phase, and pauses at each phase boundary for human review. |
| **`summarize`** | The agent closes the plan: produces `<slug>-summary.md` with the distilled result of the work, evaluates whether any decision warrants an ADR entry (proposes it, does not write it), and suggests a final commit message in conventional commit format. |
| **`cleanup`** | The agent archives the summary to `.ai/memory/archive/plans/<YYYY-MM-DD>-<slug>.md` and empties `.ai/session/`. This is destructive: it requires explicit human confirmation. |

> **Golden rules of planning:**
> - The human must approve the plan before the agent enters `execute` mode. Nothing is executed without a validated plan.
> - Before each `execute` phase, the agent reviews `git status` and suggests starting with a clean worktree.
> - `summarize` and `cleanup` are separate steps by design: the developer must be able to read the summary before the session is destroyed.

---

### 📐 `skill: specification`

The specification-driven development workflow. For requirements of greater complexity or scope that need to be formalized before implementation. It owns the *what* and the *why* — it **never writes source code**; implementation belongs to `planning`.

| Mode | Description |
|---|---|
| **`brainstorm`** | Open-ended, **conversational** exploration of a fuzzy requirement. The agent loads full context, asks questions, identifies ambiguities, and helps land the business problem. Writes nothing to disk — its output flows into `define` within the same conversation. |
| **`define`** | Formalization of the spec: the agent drafts `PRD.md` and `user-stories.md` (each story numbered `<PREFIX>-NNN`, with happy/sad acceptance criteria). Open doubts are resolved via a questionnaire *before* writing — never punted into the artifact. Ends at explicit human approval. Also handles amending an active spec (e.g. adding a retroactive corrective story). |
| **`archive`** | Formal closure of a fully-delivered spec (all stories `[x]`): the agent drafts an English archive document, proposes ADRs/brain updates, and — after explicit confirmation — moves it to `.ai/memory/archive/specs/` and removes the active spec folder. A single mode with a confirmation gate. |

> Querying an active spec read-only ("what does this spec cover?") is the job of `skill: ask`, not a mode here.

> A well-defined spec is the best investment before writing a single line of code.

---

### 🔄 `skill: update-brain`

The knowledge maintenance workflow. Updates the `memory/` files based on project analysis or in response to significant changes.

**Use cases:**

- **Initialization:** The agent analyzes the existing repository (code, README, configs, documentation) and generates the `memory/` files for the first time. Essential for onboarding into brownfield projects.
- **Structural maintenance:** When the project evolves significantly (new modules, new integrations, architectural changes), `constitution.md` and `reference-index.md` are re-analyzed and updated.
- **Applying proposed ADRs:** Takes the ADRs proposed by `planning:summarize` or `specification:archive` and integrates them into `adr-log.md` after human validation.

> The brain is only as useful as it is up to date. **Update Brain** is the skill that closes the learning loop at the project level, complementing the individual closures done by `planning:summarize` and `specification:archive`.

---

### ⚡ `skill: fast`

Direct execution without formal planning. For small, well-defined, low-risk tasks where the overhead of creating a plan is not justified. It can run free-standing (e.g. *"bump requests to 2.32"*) or as an unplanned adjustment to an active plan (e.g. *"add a validation to the endpoint that wasn't in the plan"*).

- **Triages before acting.** The agent first estimates the change's blast radius. If the work is too large for `fast` (many files, contract changes, migrations, cascading breaking changes), it refuses and routes the developer to `planning` instead of half-applying it.
- **Free-standing:** the agent acts directly and writes nothing to `.ai/session/`; git history plus a one-line recap is the record. Does not generate `plan.md` or `tasks.md`.
- **Plan adjustment:** the agent executes the change, then — only after the developer confirms it is correct — records it into the active session artifacts (`tasks.md`, `plan.md` amendments, `walkthrough.md`), so the plan never drifts ahead of reality.

> Use it judiciously. If the task has more than 2-3 steps, touches multiple files, or changes shared contracts, `fast` itself will hand it back to **planning**.

---

### 💬 `skill: ask`

Pure query mode. The agent answers questions, explains code, analyzes architecture, or evaluates options **without modifying anything**. It is strictly read-only: it reads, searches, and explains, but never edits code, writes to `.ai/`, or runs the Quality Gate.

- **Strictly read-only.** The agent does not write or edit code or brain artifacts — safe to invoke reflexively before any action.
- **Answers cold.** It orients itself from the repository, so questions about the active plan (`session/`) or the active spec (`specs/`) work on the first message of a session, with no prior context.
- **Three domains.** Code (with `git log`/`blame` for the *why-historical*), the active plan, and the active spec — plus past decisions via `adr-log.md`.
- **Hands off to action.** When the developer stops asking and asks to *act*, `ask` routes to the owning skill — `planning:execute` for a continuation cue, `planning` for a new plan, `fast` for a contained change — carrying everything it already read into that skill within the same session.
- Triggers explicitly (`/ask`) and **implicitly** on interrogative/exploratory messages, deliberately yielding to the action skills on imperative or continuation cues.

> Separating query mode from execution mode prevents accidental changes and keeps the human's intent clear. Asking first is not overhead: the context gathered while answering carries straight into whichever skill executes the change.

---

### 🩺 `skill: doctor`

The framework health check. A maintenance meta-skill the developer runs manually — ideally as a **pre-flight right before `specification` or `planning`** — to confirm JAIBA is still sound before drift or a missing dependency derails the work. It **diagnoses and routes**; it does not repair (the framework's *propose, don't patch* rule). The one file it writes is `.ai/tools-state.md` — machine state, not project memory.

It runs three diagnostics and emits a single severity-ordered report of suggested fixes:

| Diagnostic | What it checks | Where the fix routes |
|---|---|---|
| **Memory coherence** | Are `constitution.md` / `adr-log.md` / `reference-index.md` complete (no unfilled `[brackets]`/`[MISSING]`), consistent with each other, and not drifting from the repo? | `update-brain` |
| **Tool state** | Are the CLI tools the installed skills, subagents, and hooks declare actually present? Refreshes `.ai/tools-state.md` with a *"Needed by"* provenance column. | install the tool |
| **External-reference health** | Is every `reference-index.md` entry reachable — its MCP/CLI installed, its remote spec/URL live, its vendored copy present and **fresh** (git last-commit date, flagged if older than a month)? | install the MCP/CLI · fix the endpoint · re-vendor via `update-brain` |

> doctor presumes a brain to inspect: on a repo with no `.ai/` it routes to `scaffold` rather than inventing findings. Anything it can't verify in the current session (no web tools, no MCP introspection) is reported as `[UNVERIFIED]`, never silently passed.

---

## Typical workflow

```
                    ┌─────────────────────────────┐
                    │    New or legacy project     │
                    └──────────────┬──────────────┘
                                   │
                          skill: update-brain
                           (build the brain)
                                   │
                    ┌──────────────▼──────────────┐
                    │       .ai/memory/ ready      │
                    └──────────────┬──────────────┘
                                   │
               ┌───────────────────┼───────────────────┐
               │                   │                   │
        Business               Concrete             Question /
       requirement            task or fix           Exploration
               │                   │                   │
    skill: specification    skill: planning         skill: ask
    (brainstorm → define)   (define → execute      (response without
               │             → summarize             modifying)
               │             → cleanup)
               │                   │
               └─────────┬─────────┘
                         │
                skill: update-brain
               (consolidate learnings
                at the project level)
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

Each skill defines clear expectations for both the agent and the human. Knowing which mode the agent is operating in eliminates ambiguity and reduces errors from context misunderstandings.

---

## Usage examples

The following examples are based on **TripNest**, a travel planning application built with Python and Django. They illustrate the three main work cycles in JAIBA.

---

### Example 1 — `skill: specification` · New requirement

The team wants to add a collaborative itineraries module. It is a requirement with multiple business dimensions, so they start with a spec.

**Brainstorm:**
> 👤 *"I want users to be able to create itineraries and share them with other people so they can edit them together."*

The agent asks questions to narrow the scope: real-time or asynchronous editing? Can any user edit, or are there roles within the itinerary? What happens if two people edit the same day of the trip at the same time?

**Define:**
The agent drafts `.ai/specs/collaborative-itineraries/PRD.md`:

```markdown
## Business problem
Users need to coordinate travel plans with companions without relying on
external tools (WhatsApp, Google Docs). Today there is no way to co-edit
an itinerary within TripNest.

## Proposed solution
Add an invitation-based collaboration system on top of existing itineraries,
with roles (owner / editor / reader) and optimistic conflict control
(last-write-wins with change history).

## Acceptance criteria
- The owner can invite collaborators by email
- Editors can add, modify, and delete days and activities
- Readers can only view
- Changes are reflected in less than 5 seconds for all active collaborators
- The system records who made each change
```

And the resulting `user-stories.md` includes stories such as:
- `[ ]` As an owner, I want to invite a collaborator by email so they can edit my itinerary
- `[ ]` As an editor, I want to add an activity to a day of the itinerary
- `[ ]` As a reader, I want to view the itinerary in read-only mode without being able to modify it
- `[ ]` As an owner, I want to see the change history of my itinerary

> The stories then get implemented through `skill: planning`, one or more per plan. Each plan declares the stories it covers, derives its tests from their happy/sad criteria, and marks them `[x]` on close. (Read-only questions that arise mid-development — *"should roles reuse `django-guardian`?"* — are answered by `skill: ask`, not by this workflow.)

**Archive:**
Once every story in the spec is `[x]`, the team closes it.

> 👤 *"All the collaboration stories are done — archive the spec."*

The agent verifies completeness, drafts an English archive document summarizing the delivered requirement and the plans that built it, proposes an ADR (object permissions via `django-guardian`), and — after explicit confirmation — moves it to `.ai/memory/archive/specs/2026-05-30-collaborative-itineraries.md` and removes the active spec folder.

---

### Example 2 — `skill: planning` within an active spec

With the collaborative itineraries spec approved, the team starts the first implementation session: the data model and base permissions.

**Define:**

> 👤 *"Let's start with the collaborative itineraries spec. I want to implement the collaborator model and the permissions logic with django-guardian."*

The agent reads `.ai/specs/collaborative-itineraries/user-stories.md`, reviews the code (discovering that `Itinerary` uses `created_by` instead of `owner`, a discrepancy it clarifies with the developer before proceeding), and proposes the following `plan.md`:

```markdown
## Plan: Collaborator model and permissions integration
**Active spec:** collaborative-itineraries
**Covered stories:**
- Invite collaborator by email
- Assign role (owner / editor / reader)

## Tasks (TDD active)
Phase 1 — Domain model (reversible)
- [ ] Failing test for ItineraryCollaborator creation and role validation
- [ ] Implement ItineraryCollaborator (FK to Itinerary and User, role CharField with choices)
- [ ] Migration
- [ ] Failing test for role-based permissions
- [ ] Wire django-guardian (view/change/delete by role)
```

> 👤 *"Approved, go ahead."*

**Execute *(implicit in "continue")*:**
The agent verifies `git status` (clean), implements the phase task by task following TDD order, updates `tasks.md` with progress, and at the close of the phase writes in `walkthrough.md`:

```markdown
## Phase 1 — Domain model   2026-05-26

**Outcome.** ItineraryCollaborator model operational with role-based permissions
using django-guardian. Migration applied.

**Decisions.**
- role as CharField with choices (owner/editor/reader): roles are fixed,
  extensibility is not expected in the short term. If dynamic roles are
  needed in the future, migration to a separate table will be considered.

**Quality gate.** Pass.
```

And suggests the commit `chore(wip): domain model for itinerary collaborators`, without executing it. Then pauses.

**Summarize *(at plan close)*:**
When all phases are complete, the developer says *"let's close this"*. The agent produces `collaborative-itineraries-base-model-summary.md`, marks the corresponding stories in `user-stories.md` as `[x]`, proposes an ADR entry about the choice of `CharField` for `role`, and suggests a final commit like `feat(itineraries): collaborator invitations with role-based access`.

**Cleanup:**
> 👤 *"go ahead, clean it up"*

The agent runs the skill's `scripts/cleanup.sh`, archiving the summary to `.ai/memory/archive/plans/2026-05-26-collaborative-itineraries-base-model.md` and emptying `session/`.

---

### Example 3 — `skill: planning` standalone (outside a spec)

During a code review, the team detects that itinerary queries are generating N+1 problems. There is no open spec for this: it is a targeted technical task.

**Define:**

> 👤 *"We have an N+1 problem in the itinerary list view. We need to optimize the queries."*

The agent reviews the relevant code and proposes:

```markdown
## Plan: Query optimization in itinerary listing

## Context
The `ItineraryListView` loads itineraries with their collaborators and
activities lazily, generating N+1 queries per itinerary.

## Tasks
Phase 1 — Profiling (reversible)
- [ ] Regression test that counts queries with assertNumQueries
- [ ] Profile with django-debug-toolbar and document baseline count

Phase 2 — Fix (depends on: Phase 1)
- [ ] Add select_related('owner') and prefetch_related('collaborators', 'days__activities')
- [ ] Adjust serializer if needed
- [ ] Verify that assertNumQueries drops to the expected range
```

**Execute → Summarize → Cleanup:**
The agent implements the changes phase by phase, verifies the query reduction, and summarizes with a suggested commit like `perf(itineraries): eliminate N+1 in list view`. Since it is an optimization with no architectural impact, the summary explicitly states *"No ADR proposed; all decisions were tactical."*

---

## Glossary

| Term | Definition |
|---|---|
| **Brain** | The set of files in `.ai/` that make up the agent's persistent context |
| **Spec** | A formal specification of a business requirement, with PRD and user stories |
| **Plan** | A tactical work plan bounded to a session or short sprint |
| **Skill** | An executable workflow with defined modes and human validation checkpoints |
| **Summary** | The archivable summary of a closed plan, produced by `planning:summarize` |
| **Update Brain** | The process of updating long-term memory after significant project-level changes |
| **Human in the loop** | The principle that the human validates and approves before each significant stage |

---

<div align="center">

**JAIBA** · Joint-operations Artificial Intelligence Behavioral Architecture 🦀

*AI-assisted development should not be black magic. It should be engineering.*

</div>
