---
name: specification
description: >-
  Spec-driven development workflow inside the JAIBA framework. Use this skill whenever the developer wants to turn a product or business requirement into a formal specification — a PRD and a numbered list of user stories — before any implementation. The input can be a description typed in chat, a referenced document/file, or (via a knowledge skill) a tracker ticket. Trigger on explicit calls like "specification brainstorm / define / archive", and on phrases like "let's spec this", "let's make a spec for this", "write a PRD", "formalize this requirement", "I want users to be able to…", "we need a feature that…", "help me think through this feature", "let's brainstorm this requirement", "close the spec", "archive the spec". This skill owns the *what* and the *why* (PRD + user stories with happy/sad acceptance criteria); it does NOT write source code — implementation belongs to `planning`. Three modes: `brainstorm` (shape a fuzzy requirement, conversational), `define` (draft and get approval on PRD.md + user-stories.md), and `archive` (close a fully-delivered spec into long-term memory). Prefer this skill over `planning` when the work is a multi-faceted requirement that needs formalizing before it can be planned; prefer `planning` when the requirement is already clear and the developer just wants a tactical plan.
version: 1.0.0
author: atlasfoo<iscomejia15@outlook.com>
requires:
  - git
tags:
  - jaiba
  - workflows
  - jaiba-workflows
  - spec-driven
---

# Specification Skill

The spec-driven workflow of the JAIBA framework. `specification` takes
a product requirement and turns it into two durable artifacts — a
**PRD** (the *what* and *why*) and a list of **user stories** (the
deliverable increments, each with happy/sad acceptance criteria) — that
the `planning` skill then implements, story by story.

This is the deliberate front end of the framework. Where `planning` is
the tactical workhorse for a concrete piece of work, `specification`
exists for requirements big enough that writing them down *before*
touching code pays for itself. A well-defined spec is the best
investment you can make before the first line of implementation.

One boundary defines the skill: **`specification` never writes source
code.** It produces the contract; `planning` fulfills it. When the
developer wants to start building, hand off to `planning`.

This skill has **three modes**, each documented in its own reference
file. Read the relevant reference *before* taking action — the
selection table below tells you which one.

## Mode Selection

Decide the mode **before** reading anything else. If the message is
ambiguous, ask the developer instead of guessing.

| Situation | Mode | Read |
|---|---|---|
| The requirement is fuzzy, exploratory, or under-specified, and the developer wants help shaping it ("help me think through…", "I'm not sure how this should work", "specification brainstorm") | `brainstorm` | `references/brainstorm-mode.md` |
| The requirement is clear enough to formalize — or a brainstorm in *this same conversation* already landed it — and the developer wants the PRD and stories ("let's spec this", "write the PRD", "specification define") | `define` | `references/define-mode.md` |
| An active spec exists under `.ai/specs/<slug>/`, all its user stories are checked `[x]`, and the developer wants to close it ("archive the spec", "close this spec", "specification archive") | `archive` | `references/archive-mode.md` |
| Anything else — including a request to *implement* a story (that's `planning`), or a pure question about the spec (that's `ask`) | **Route, don't guess.** See "Hand-off" below. | — |

## Universal Preconditions

Before entering any mode, do these reads. The whole point of the spec
is to be grounded in reality, not in the prompt's assumptions — so load
the brain and the code before you write a word. Stop and surface the
gap if any file is missing or contradicts the request.

1. **`AGENTS.md`** — your behavioral contract. Always.
2. **`.ai/memory/constitution.md`** — project identity, stack, scope
   boundaries, and the Quality Gate. The spec must live inside this
   project's stated scope; if the requirement pushes past it, that's a
   conversation to have *before* drafting (it may itself warrant an
   ADR or a constitution update via `update-brain`).
3. **`.ai/memory/reference-index.md`** — existing integrations. A PRD
   that invents a payment provider the project doesn't use, or ignores
   one it already has, is wrong on arrival.
4. **`.ai/memory/adr-log.md`** — past architectural decisions. The
   spec must not silently contradict a standing decision; if it needs
   to, that contradiction is a headline question for the developer.
5. **Existing specs under `.ai/specs/`** — to catch overlap. If a
   sibling spec already owns part of this requirement, say so before
   creating a duplicate.
6. **The code and its change history** — read the modules the
   requirement plausibly touches, plus `git log` and the closed-plan
   summaries in `.ai/memory/archive/plans/`. The history tells you
   what has already been tried and why; tools serve discovery here,
   not bulk content delivery (`AGENTS.md` §3).

If these reads reveal a conflict between the request and recorded
project facts, **flag it before producing artifacts** (see "Asking the
Human").

## Inputs

`specification` accepts the requirement from one of these sources:

- **Chat** — the developer describes it directly. The default.
- **A referenced file** — the developer points at a document in the
  repo (a brief, a notes file, an exported ticket). Read it.
- **A tracker ticket (Jira, Linear, …)** — *not* handled by this skill
  on its own. JAIBA models tracker access as a **knowledge skill**: a
  separate skill that teaches the agent how to fetch a ticket and
  declares that it should fire when `specification:define` runs with a
  ticket reference in the prompt. If such a knowledge skill is present,
  it will trigger and supply the ticket content; if it isn't, ask the
  developer to paste the ticket text. Don't invent a tracker
  integration that isn't there (`AGENTS.md` §5.3).

## Artifacts at a Glance

| File | Produced by | Lives in | Until |
|---|---|---|---|
| `.ai/specs/<spec-slug>/PRD.md` | `define` | spec folder | `archive` |
| `.ai/specs/<spec-slug>/user-stories.md` | `define`, updated as stories close | spec folder | `archive` |
| `.ai/memory/archive/specs/<YYYY-MM-DD>-<spec-slug>.md` | `archive` | long-term memory | permanent |

Templates live in `assets/`. **Use them verbatim** — the shared
structure is what keeps specs legible across the project's life.

| Asset | When |
|---|---|
| `assets/prd-template.md` | `define` |
| `assets/user-stories-template.md` | `define` |
| `assets/spec-archive-template.md` | `archive` |

Note the `brainstorm` row is absent on purpose: brainstorm writes
**nothing** to disk (see its reference). Its output is a landed
requirement that `define` consumes, in the same conversation.

## Slugs, prefixes, and story IDs

Two identifiers, don't confuse them:

- **Spec slug** — the kebab-case folder name under `.ai/specs/` and
  the archive filename stem. E.g. `oauth-authentication`. Derived from
  the requirement, lowercase, hyphenated.
- **Story prefix** — a short UPPERCASE token (≈3–6 chars) used for
  story IDs. E.g. `OAUTH`. Chosen at `define`, confirmed with the
  developer, and recorded in `PRD.md` frontmatter (`prefix:`). It must
  be **unique across specs**, because plans reference stories by these
  IDs and collisions would make the references ambiguous.

User stories are numbered `<PREFIX>-NNN`, incrementing and never
reused: `OAUTH-001`, `OAUTH-002`, … A story's number is permanent even
if the story is later dropped — gaps are fine, renumbering is not.

## Relationship with `planning`

`specification` and `planning` are two halves of one loop:

- **Spec → plan.** A `planning` plan implements one or more stories
  from an active spec. The plan declares which stories it covers
  (`stories:` in its frontmatter), and `planning:define` reads the PRD
  and the stories' acceptance criteria — under TDD, the happy/sad
  paths become the tests.
- **Plan → spec.** When `planning:summarize` closes a plan, it marks
  the covered stories `[x]` in `user-stories.md`. When that closes the
  *last* open story, summarize points the developer at
  `specification:archive`.
- **Out-of-spec work that impacts the spec.** Sometimes a plan must do
  something the spec didn't foresee — typically a bug fix needed for
  the PRD to actually hold. The framework's answer is a **retroactive
  corrective story**: add a new `<PREFIX>-NNN` story to
  `user-stories.md` describing the correction, so the spec stays the
  single source of truth for "everything it took to satisfy the PRD".
  `define` mode handles adding such a story to an active spec; see its
  reference.

## Asking the Human

Same discipline as the rest of the framework. When a mode says "ask
the developer", prefer a structured questionnaire over a wall of prose
(use `ask_user_input_v0` if available, otherwise chat):

- **One topic per question.** Don't bundle scope, users, and
  constraints into one prompt.
- **Closed options when the answer space is closed** (2–4 mutually
  exclusive choices); plain chat for open-ended rationale.
- **Never punt doubts into the artifact.** A PRD with
  `[NEEDS CLARIFICATION]` blocks is a failure — the artifact is the
  *answer*, not a list of pending questions. Resolve first, write
  second.
- **`define` does not finish while questions remain.** Approval comes
  after clarity, not before.

## Hand-off

The modes chain within a single requirement, and the skill hands off
to its neighbors at the edges:

```
(ask: "let's spec this")
        │
        ▼
   brainstorm ──→ define ──→  [ planning implements the stories ]  ──→ archive ──→ update-brain
  (conversational)  │                                                    │
                    └── approval gate                       (proposes ADRs / knowledge to promote)
```

| The developer now wants… | Route to |
|---|---|
| To start building a story | `planning` (`planning:define`) |
| To just ask about the spec, read-only | `ask` |
| A small contained change, no plan | `fast` |
| To apply the ADRs/knowledge an archive proposed | `update-brain` |

Two transitions deserve emphasis:

- **brainstorm → define is in-conversation.** Brainstorm persists
  nothing, so its result is only alive in the current session. If the
  developer is ready after brainstorming, continue straight into
  `define` — don't end the conversation expecting the brainstorm to be
  on disk somewhere.
- **define → planning is the approval boundary.** `define` ends when
  the developer approves the PRD and stories. From there, *building* is
  `planning`'s job. `specification` does not write source code.

## Language

Per `AGENTS.md` §3.5, the split is deliberate and matters here:

- **This skill's source** (SKILL.md, references, templates) — English.
- **`PRD.md` and `user-stories.md`** live under `.ai/specs/`
  (mid-term) → write them in the **language the developer is using**
  in the session.
- **The archive document** lives under `.ai/memory/` (long-term) →
  write it in **English**, always — even when the PRD and stories it
  summarizes were in another language. Translate the essence; don't
  copy-paste the Spanish PRD into a memory artifact.

## Common failure modes

- **Drafting before reading.** A PRD grounded in the prompt's
  assumptions instead of the code and brain produces phantom
  requirements. Load context first.
- **Skipping the approval pause in `define`.** Writing the files is
  not the end — the developer's "approved" is. Until then the spec is
  a draft.
- **Writing code.** The temptation is real once the stories are clear.
  Resist it: hand off to `planning`. Crossing this line erases the
  value of having a spec at all.
- **`[NEEDS CLARIFICATION]` in the PRD.** Forbidden. Ask in chat,
  resolve, then write.
- **Archiving an incomplete spec.** If stories are still unchecked,
  `archive` stops and asks. Don't bury open work.
- **Putting a non-English archive in `.ai/memory/`.** The long-term
  brain is English-only. The mid-term spec follows the developer's
  language; the archive does not.
