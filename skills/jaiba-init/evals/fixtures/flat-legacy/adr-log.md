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

| ID  | Date       | Title                                          | Status   |
|-----|------------|-------------------------------------------------|----------|
| 001 | 2026-06-02 | Adoption of the JAIBA Brain Structure           | Accepted |
| 002 | 2026-06-10 | Retry policy for the Payments API HttpClient    | Accepted |

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

- **Date:** 2026-06-02
- **Status:** Accepted

**Context** — The project needed a way for AI coding agents to retain
context across sessions, sustain architectural coherence, and surface
the reasoning behind past technical choices. Without persistent
structure, every session restarts from scratch and the same questions
get re-litigated.

**Decision** — Adopt the JAIBA framework's `.ai/` brain structure:
`AGENTS.md` at the repo root for agent behavior; `.ai/memory/` for
constitutive memory (`constitution.md`, this file,
`reference-index.md`) plus the append-only chronological record
`.ai/memory/log/`; `.ai/work/` for executive memory (PRD when
produced, plan, tasks, walkthrough — gitignored, archived to
`memory/log/` at close).

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
- *Follow-ups:* Schedule periodic `jaiba-init:update-brain` runs after major
  milestones.

## ADR-002: Retry policy for the Payments API HttpClient

- **Date:** 2026-06-10
- **Status:** Accepted

**Context** — The typed HttpClient that calls the Payments API had no
resilience policy: a transient network blip or a Payments API 5xx
surfaced directly as a failed order, even though the underlying
payment attempt often would have succeeded on a retry. This showed up
repeatedly in the on-call rotation as false-positive order failures.

**Decision** — Wrap the Payments API typed HttpClient with a Polly
retry policy: three retries with exponential backoff on transient
HTTP failures (5xx, timeouts, connection errors), registered in the
Infrastructure layer's HttpClient configuration. Non-transient
failures (4xx) are not retried and continue to surface immediately.

**Alternatives Considered**
- *Leave retries to the caller (Application layer)* — rejected; would
  duplicate the policy across every call site that touches the
  Payments API.
- *Increase the HttpClient timeout instead* — rejected; masks
  transient failures without addressing them and delays legitimate
  error reporting.

**Consequences**
- *Positive:* Fewer false-positive order failures caused by transient
  Payments API or network issues.
- *Negative / Risks:* Retries can extend request latency on a genuine
  outage; must be paired with a circuit breaker if the Payments API
  degrades for a sustained period (not yet implemented).
- *Follow-ups:* Evaluate adding a circuit breaker if repeated
  extended outages are observed.
