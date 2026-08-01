# JAIBA Framework maintenance instructions for Agents

> **For repository maintainers:** Replace every bracketed placeholder
> (`[like this]`) with real project values. Until then, the agent
> should treat placeholders as *to be filled*, not as literal
> requirements, and ask before proceeding.

> **Meta-instruction for the agent:** This document is the authority
> on *project identity, architecture, scope, planning conventions,
> and the Quality Gate*. Read it before any substantive planning or
> implementation. `AGENTS.md` defines your general behavior; this
> file defines what applies to **this project specifically**. On
> conflict over project facts, this document wins.

## 1. What

- **Project name:** JAIBA Framework
- **Description:** Joint-Operations Artificial Intelligence Behavioral Architecture framework. A fast, secure, harnessed framework for AI Augmented Software development
- **Status:** MVP

## 2. How

- **Primary language:** Agent Skills, Markdown

## 3. Why

- **Business objective:** Provide a secure, standarized way of co working with AI Agents. Read README.md for information

## 4. File structure

### Framework composition

```mermaid
graph TD
    subgraph Artifacts
        AA[ARTIFACTS]

        AA --> AX([AGENTS.md — minimal repo marker])
        AA --> AZ([jaiba-contract.md — global behavioral contract])
        AA --> AY([README.md])
        AA --> AB[Constitutive memory  .ai/memory/]
        AA --> AD[Executive memory  .ai/work/  — gitignored]
        AA --> AE[Toolchain  .atl/ — gitignored]

        AB --> AF([constitution.md])
        AB --> AG([adr-log.md — curated decisions])
        AB --> AH([reference-index.md])
        AB --> AM[log/ — append-only: closed work + brain changelog]

        AD --> AI([PRD.md — only at spec depth])
        AD --> AK([plan.md])
        AD --> AL([tasks.md — T-NNN graph: depends-on, load])
        AD --> AN([walkthrough.md])

        AE --> AO([tool-layout.md])
    end

    subgraph skills
        A[SKILLS]
        A --> B[Workflow Skills]
        A --> C[Knowledge Skills]
        A --> D[Meta Skills]

        B --> E([Conduct — SDD chain: propose → spec → tasks → execute → validate → summarize])
        B --> G([Fast — implicit inline lane])
        B --> H([Ask — implicit read-only lane])

        C --> J[[e.g. ASP.NET CORE best practices]]
        C --> L[[e.g. How to TDD]]

        D --> K[[Jaiba-configure — machine setup]]
        D --> I[[Jaiba-init — repo bootstrap + update-brain modes]]
        D --> N[[Doctor]]
        D --> M[[Create-knowledge]]
    end

    subgraph subagents
        S[SUBAGENT BATTERY — installed globally by jaiba-configure]
        S --> S1([executor-high / -medium / -low])
        S --> S2([code-analyst])
        S --> S3([business-analyst])
        S --> S4([verify])
    end
```

Routing (defined in the global contract, `jaiba-contract.md` §7):
continuation cue → `conduct:execute` · question → `ask` · small
contained change → `fast` · new work → the `conduct` chain.
`/conduct [phase]` stays available as explicit override.

### File hierarchy

The final output of this framework are skills, template artifacts will be packaged within this skills

```
└── skills
    ├── conduct
    │   ├── assets
    │   │   ├── prd-template.md          (criteria as parseable schema)
    │   │   ├── plan-template.md
    │   │   ├── tasks-template.md        (T-NNN, depends-on, load)
    │   │   ├── walkthrough-template.md
    │   │   └── plan-summary-template.md (log-entry compatible)
    │   ├── references     (triage, subagents, one per phase: propose,
    │   │                   spec, tasks, execute, validate, summarize)
    │   └── scripts
    │       └── archive.sh (moves closed work essence to .ai/memory/log/)
    ├── ask                (implicit lane — no slash command)
    ├── fast               (implicit lane — no slash command)
    ├── jaiba-init         (repo-scoped: bootstrap + update-brain modes)
    │   ├── assets
    │   │   ├── AGENTS.md           (minimal per-repo marker)
    │   │   ├── ai.gitignore / atl.gitignore
    │   │   ├── constitution-template.md
    │   │   ├── adr-log-template.md
    │   │   ├── reference-index-template.md
    │   │   ├── log-entry-template.md
    │   │   └── readme-skeleton.md
    │   └── references     (bootstrap, initialize, update)
    ├── jaiba-configure    (machine-scoped: contract, skillset, battery)
    │   └── assets
    │       ├── jaiba-contract.md   (global behavioral contract — canonical)
    │       ├── agents/             (subagent battery: executors + specialists)
    │       └── skillset.txt
    ├── create-knowledge
    └── doctor
        ├── assets
        │   └── jaiba-contract.md   (lockstep reference copy for drift check)
        ├── references     (memory-coherence, tool-state, reference-health)
        └── scripts
            └── check-tools.sh
```

> Ownership follows the repo/machine split. **`jaiba-init` owns
> everything a repository gets**: the `AGENTS.md` marker, the `.ai/` and
> `.atl/` gitignores, and the memory artifact templates — it lays the
> skeleton *and*, in its `update-brain` mode, materializes the brain
> from those templates (it is the only skill that writes `.ai/memory/`).
> There is no hand-off between the two: they are modes of one skill.
> **`jaiba-configure` owns everything the machine gets**: the canonical
> global behavioral contract, the skillset, the subagent battery — and
> carries no brain templates at all. The contract is the one file with
> two copies: `jaiba-configure` holds the canonical one and `doctor` a
> lockstep reference copy for drift detection — keep both identical when
> the contract changes.


## 5. Project status

Read project status and tasks at `.ai/session/` (`plan.md`, `tasks.md`,
`walkthrough.md`) when requested with a full plan. (This repo predates
the `work/` layout its own skills now install; its in-flight session
stays in `session/` until the active plan closes.)

## 6. Behavior

To save tokens, use `caveman` skill for communication
