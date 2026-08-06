# Decision Concept

> **Meta-instruction for the agent:**
>
> One file is **exactly one ADR** — one architectural decision, its
> reasoning, and its consequences. Decisions live at
> `.ai/memory/decisions/<NNN>-<slug>.md`, where `NNN` is the numeric
> part of `id:` and `<slug>` is a kebab-case subject: `id: ADR-004`
> lives at `decisions/004-event-bus.md`. That keeps the directory
> sorted in decision order.
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
> **Never delete or rewrite a past decision.** A decision that no
> longer holds is *superseded*, never edited away — see **Superseding a
> decision** below. The log of decisions is only trustworthy if a past
> entry can be read as it was written.
>
> **Never back-fill history.** Do not reconstruct a decision that was
> taken *before* the brain existed, and never write an ADR to
> retroactively justify a pattern already in the code. An ADR records a
> real decision made at a real time; an antedated one is a fabrication
> that will be read as evidence later. The decision series starts at
> adoption and grows forward. When the *why* of pre-existing structure
> matters, it is surfaced read-only from `git log` / `blame` by
> `skill: ask` — not frozen into a decision concept. If the team wants
> to make an undocumented pattern explicit *now*, that is a **new**
> decision, dated today, with today's `status:` — not a historical one.
>
> **`[MISSING]` discipline is unchanged.** A fact you cannot ground —
> the real date, who decided, which alternative was actually weighed —
> is marked `[MISSING]` and surfaced to the human, never invented to
> round out the shape.

---

## Template

```markdown
---
type: decision
id: ADR-[NNN]
title: "[Short descriptive title]"
description: [One line: what was decided]
status: [proposed | accepted | rejected | deprecated | superseded]
date: "[YYYY-MM-DD]"
supersedes: "[ADR-NNN](NNN-slug.md)"
superseded-by: "[ADR-NNN](NNN-slug.md)"
tags: [tag, tag]
updated: "[YYYY-MM-DD]"
---

# ADR-[NNN]: [Short descriptive title]

## Context

[What problem or need triggered this decision. What are the current
limitations or forces in play. Keep it factual.]

## Decision

[What exactly was decided. Be specific: name the tool, the pattern,
the boundary. One paragraph is usually enough.]

## Alternatives Considered

- [Alternative] — [why it was not chosen.]
- [Alternative] — [why it was not chosen.]

[At least one alternative must be documented; "no alternative" is
itself a signal to reconsider whether this is a decision at all.]

## Consequences

- *Positive:* [what this unlocks or improves.]
- *Negative / Risks:* [what this constrains, the debt incurred, the
  failure modes introduced.]
- *Follow-ups:* [work this implies down the line — migrations,
  training, monitoring, docs.]
```

## Frontmatter keys

| Key | Status | Meaning |
|---|---|---|
| `type` | **mandatory** | always `decision` |
| `id` | mandatory in practice | `ADR-NNN`, zero-padded to three digits; matches the filename's `NNN` |
| `title` | recommended | the decision's short name, same text as the `#` heading |
| `description` | recommended | one line; this is what `index.md` shows |
| `status` | mandatory in practice | one of the five values below |
| `date` | mandatory in practice | `YYYY-MM-DD` the decision was **made**, not the day the file was last touched |
| `supersedes` | only when it applies | file-relative link to the decision this one replaces |
| `superseded-by` | only when it applies | file-relative link to the decision that replaced this one |
| `tags` | recommended | list, for grouping and search |
| `updated` | recommended | `YYYY-MM-DD` of the last substantive change to the file |

Only `type:` is a validity condition — a missing optional key is at
most a quality note, never a rejection. Omit `supersedes` /
`superseded-by` entirely when they do not apply rather than writing an
empty value.

**`status:` vocabulary.**

| Value | Means |
|---|---|
| `proposed` | drafted, not yet agreed. The usual origin is a proposal from `conduct:summarize`. |
| `accepted` | in force. This is the state most decisions sit in. |
| `rejected` | considered and deliberately not adopted. Kept, because the reasoning is what stops the question being re-litigated. |
| `deprecated` | no longer in force, and **nothing replaced it** — the need itself went away. |
| `superseded` | replaced by a specific later decision, named in `superseded-by`. |

`deprecated` and `superseded` are not interchangeable: reach for
`superseded` whenever there *is* a successor, so the chain stays
followable.

**Links are file-relative.** Both `supersedes` and `superseded-by`
point at a sibling in the same directory, so they are a bare filename:
`[ADR-002](002-rest-only.md)`. `title`, `date` and `updated` are quoted
for consistency with the rest of the bundle's concepts; `supersedes`
and `superseded-by` must be quoted regardless, so the `[…](…)` form
reads unambiguously as one value.

## Superseding a decision

Superseding is the **only** permitted edit to a decision that has
already landed, and it touches two files:

1. **Write the new decision** as its own file, with the next free
   `NNN`, `status: accepted`, and
   `supersedes: "[ADR-NNN](NNN-old-slug.md)"`. Its **Context** should
   say what changed since the old decision — a supersession without a
   stated reason is indistinguishable from an accident.
2. **Mark the old decision** in place: flip `status:` to `superseded`,
   add `superseded-by: "[ADR-MMM](MMM-new-slug.md)"`, and bump
   `updated:`. **Change nothing else.** The old Context, Decision,
   Alternatives and Consequences stay exactly as written — they are the
   record of what was true then.

Never delete the old file, never renumber it, and never fold its
content into the new one. A dangling `superseded-by` (or a `supersedes`
with no matching `superseded-by` on the other end) is a broken-link
finding for `jaiba-doctor`.

## Worked example — the seed decision

Every JAIBA repository starts with one decision: adopting the brain
itself. Set its `date` to the day the framework was initialized here,
and leave the series at this entry plus whatever the developer
explicitly asks to record **now**.

```markdown
---
type: decision
id: ADR-001
title: "Adoption of the JAIBA brain structure"
description: The project keeps agent-facing memory in .ai/ under the JAIBA framework.
status: accepted
date: "[YYYY-MM-DD]"
tags: [meta, memory, tooling]
updated: "[YYYY-MM-DD]"
---

# ADR-001: Adoption of the JAIBA brain structure

## Context

The project needed a way for AI coding agents to retain context across
sessions, sustain architectural coherence, and surface the reasoning
behind past technical choices. Without persistent structure, every
session restarts from scratch and the same questions get re-litigated.

## Decision

Adopt the JAIBA framework's `.ai/` brain: `AGENTS.md` at the repo root
for agent behavior; `.ai/memory/` as the constitutive bundle — one
concept per file, `index.md` as its entry point, `identity/` for
project identity and the quality gate, `decisions/` for ADRs,
`references/` for external surfaces, and the append-only chronological
record in `log/`; `.ai/work/` for executive memory (PRD when produced,
plan, tasks, walkthrough — gitignored, archived into `log/` at close).

## Alternatives Considered

- *No structured memory* (status quo) — rejected; sessions lose context
  and decisions are not traceable.
- *A single monolithic context file* — rejected; conflates concerns and
  becomes unmaintainable as the project grows.

## Consequences

- *Positive:* continuity across sessions; decisions become traceable;
  onboarding (human or agent) is faster.
- *Negative / Risks:* requires discipline to keep memory current; stale
  memory can mislead the agent.
- *Follow-ups:* run `jaiba-init:update-brain` after major milestones.
```
