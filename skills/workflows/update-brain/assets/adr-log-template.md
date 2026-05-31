# Architecture Decision Record Log

> **Meta-instruction for the agent:**
>
> This file is the project's structural memory: every non-trivial
> architectural decision and its reasoning lives here.
>
> **Propose a new ADR when** the work involves any of:
> - Introducing or removing a framework, database, or major library
> - Changing the architectural style or a core pattern (adding a new
>   layer, switching from REST to GraphQL, adopting an event bus, etc.)
> - Establishing a new convention that other code will need to follow
> - Replacing a third-party integration with another
> - Changing data ownership boundaries between services
> - Deprecating or superseding a previously accepted decision
>
> **Do not propose an ADR for:** bug fixes, refactors that preserve
> behavior and structure, dependency version bumps without API impact,
> or style/formatting changes.
>
> **Never delete or rewrite past ADRs.** Supersede them with a new
> entry that references the deprecated one by ID.

## Decision Index

| ID  | Date       | Title                                  | Status   |
|-----|------------|----------------------------------------|----------|
| 001 | YYYY-MM-DD | Adoption of the JAIBA Brain Structure  | Accepted |
| 002 | YYYY-MM-DD | [e.g., Migration from REST to GraphQL] | Proposed |

---

## Entry Template

When proposing a new ADR, follow this structure:

**Heading:** `## ADR-[XXX]: [Short descriptive title]`

- **Date:** YYYY-MM-DD
- **Status:** Proposed | Accepted | Rejected | Deprecated | Superseded by ADR-[YYY]

**Context** — What problem or need triggered this decision. What are
the current limitations or forces in play. Keep it factual.

**Decision** — What exactly was decided. Be specific: name the tool,
the pattern, the boundary. One paragraph is usually enough.

**Alternatives Considered** — Other options evaluated and why they
were not chosen. At least one alternative should be documented;
"no alternative" is itself a signal to reconsider.

**Consequences**
- *Positive:* what this unlocks or improves.
- *Negative / Risks:* what this constrains, the new debt incurred,
  or failure modes introduced.
- *Follow-ups:* work this implies down the line (migrations,
  training, monitoring, docs).

---

## ADR-001: Adoption of the JAIBA Brain Structure

- **Date:** [YYYY-MM-DD]
- **Status:** Accepted

**Context** — The project needed a way for AI coding agents to retain
context across sessions, sustain architectural coherence, and surface
the reasoning behind past technical choices. Without persistent
structure, every session restarts from scratch and the same questions
get re-litigated.

**Decision** — Adopt the JAIBA framework's `.ai/` brain structure:
`AGENTS.md` at the repo root for agent behavior; `.ai/memory/` for
long-term memory (`constitution.md`, this file, `reference-index.md`);
`.ai/specs/` for mid-term product specifications; `.ai/session/` for
short-term planning and execution artifacts.

**Alternatives Considered**
- *No structured memory* (status quo): rejected; sessions lose
  context and decisions are not traceable.
- *Single monolithic context file*: rejected; conflates concerns
  and becomes unmaintainable as the project grows.

**Consequences**
- *Positive:* Continuity across sessions; decisions become
  traceable; onboarding (human or agent) is faster.
- *Negative / Risks:* Requires discipline to keep memory current;
  stale memory can mislead the agent.
- *Follow-ups:* Schedule periodic `update-brain` runs after major
  milestones.
