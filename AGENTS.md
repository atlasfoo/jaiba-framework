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

        AA --> AX([AGENTS.md])
        AA --> AY([README.md])
        AA --> AB[Memory]
        AA --> AC[Spec]
        AA --> AD[Session]
        AA --> AE[Configuration]

        AB --> AF([CONSTITUTION.md])
        AB --> AG([adr_log.md])
        AB --> AH([reference_index.md])

        AC --> AI([PRD.md])
        AC --> AJ([user_stories.md])

        AJ -."each one generates one".-> AK

        AD --> AK([plan.md])
        AD --> AL([tasks.md])
    end


    subgraph skills
        A[SKILLS]
        A --> B[Workflow Skills]
        A --> C[Knowledge Skills]
        A --> D[Meta Skills]

        B --> E([Spec])
        B --> F([Plan])
        B --> G([Fast])
        B --> H([Ask])
        B --> I([Update Brain])

        C --> J[[ASP.NET CORE best practices]]
        C --> L[[How to TDD]]

        D --> K[[Scaffold]]
        D --> M[[Custom workflow creator]]
    end
```

### File hierarchy

The final output of this framework are skills, template artifacts will be packaged within this skills

```
└── skills
    ├── workflows
    │   ├── planning
    │   │   └── assets
    │   │       ├── plan.template.md
    │   │       ├── tasks.template.md
    │   │       ├── walkthrough.template.md
    │   │       └── plan-summary.template.md
    │   ├── specification
    │   │   └── assets
    │   │       ├── prd.template.md
    │   │       ├── user-stories.template.md
    │   │       └── spec-summary.template.md
    │   ├── ask
    │   ├── fast
    │   └── update-brain
    └── meta
        └── scaffold
            └── assets
                ├── constitution.template.md
                ├── adr-log.template.md
                └── reference-index.template.md
```

> Since scaffold script is not already done, memory artifacts templates live in `templates` temporary folder.
