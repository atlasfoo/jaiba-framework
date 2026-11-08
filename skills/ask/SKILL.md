---
name: ask
description: >-
  Implicit read-only Q&A lane for questions about code, active work, or decisions; not user-invocable. Triggers on interrogative/exploratory requests ("why…?", "what's left?", "explain…", "is this covered?"). Never mutates JAIBA-owned data or persists JAIBA bindings; independent host-required bookkeeping is not JAIBA evidence. Continuations route to conduct:execute, new work to conduct, small changes to fast. Never executes changes or runs the Quality Gate.
version: 3.3.0
author: atlasfoo<iscomejia15@outlook.com>
user-invocable: false
requires:
  - git
tags:
  - jaiba
  - workflows
  - jaiba-workflows
  - ask-mode
---

# Ask Skill

The read-only lane of the JAIBA framework. `ask` answers questions —
about the codebase, the active work, or the recorded decisions —
without changing anything. It is the sanctioned place for the
developer to *think out loud* with the agent before committing to a
change.

Two properties define it:

1. **It is strictly read-only.** `ask` reads, searches, and explains.
   It never edits code, never writes to `.ai/`, never runs the Quality
   Gate to mutate state. This is what makes it safe to route into
   reflexively — the developer can ask anything without risking an
   accidental edit.
2. **It orients cold.** `ask` is meant to be usable with no prior
   conversation. A bare "what's left in the plan?" must work on the
   first message of a session. So `ask` orients itself from the
   repository — it does not assume it already knows what the active
   work is.

And one transition defines its boundary: when the developer shifts from
*asking* to *acting*, `ask` hands off to an action lane rather than
doing the work itself. The context it already gathered carries over —
that's the payoff of asking first.

## Invocation: implicit only

`ask` is **not user-invocable** — there is no `/ask` command. The
frontmatter declares `user-invocable: false` (on host agents that
support the field; elsewhere, this section and the `description:` are
the contract): the routing rule is the only way in. Whenever the
developer's message is a **question** — interrogative or exploratory,
wanting understanding rather than change — the host agent routes it
here. The sibling lanes: a continuation cue routes to the
conduct's `execute` phase, a change request routes to `fast`
(which triages it, escalating big work into the conduct chain).
Only `conduct` keeps an explicit override (`/conduct
[phase]`); `ask` and `fast` are pure routing lanes.

## Brain Discovery

`ask` can be installed per-project (`.claude/skills/`,
`.agents/skills/`) or **globally** (e.g. `~/.claude/skills/`), shared
across every repository you work in. Resolve memory through the effective
`create-memory` installation's `references/resolution.md` and
`references/memory-surface-contract.md` (`jaiba-memory-surface` contract version **1.1.0**), never relative to this skill's installation.
The built-in filesystem surface maps to the selected checkout; external
surfaces use their resolved standard binding `v2` (`~/.jaiba/memory/bindings/<sha256(canonical-work-root)>.yaml`, with legacy fallback to `~/.jaiba/memory/<host>/...` when present) and owned catalogue and need not have
local `.ai/` files or an `AGENTS.md` marker.

Orienting cold (see `references/orientation.md`) includes resolving the
current project's memory surface. Resolve the effective `create-memory`
installation's `references/resolution.md` and
`references/memory-surface-contract.md` (contract version `1.1.0`). On filesystem, resolve its
supported concept-bundle or legacy layout. On an external surface, require
a valid binding (`v2` locator), readable owned catalogue, exact project/context scope and
required full reads; a marker, probe, search result or empty catalogue alone
is not authoritative.

Follow the deterministic rendering path (`MSV-008`):
`binding` → read context/project catalogue → exact logical addresses/IDs → invoke package script `render` subcommand (or read materialized content directly in `document-tree`).
Strictly prohibit using full-text `search` (`mem_search`) to locate or display project artifacts or decisions; full-text search is only for exploratory discovery when the concept address is completely unknown.

`ask` is read-only for JAIBA-owned data: it must not
persist a JAIBA binding/namespace change or perform JAIBA adapter or memory
operations that mutate owned data. Ordinary host-required memory/session
bookkeeping remains independent, is not JAIBA evidence, and is not used as
a JAIBA read source.

- **No authoritative brain** — say so plainly when the filesystem has no
  resolved brain or an authoritative external catalogue confirms absence.
  If an external binding, catalogue, or required read is unavailable,
  ambiguous, or permission-denied, report that failure instead; do not
  call it an empty brain or route to bootstrap as though absence were proven.
  Code questions still work from source. For a plan or PRD, report no
  active work only after authoritative scoped enumeration confirms the
  executive catalogue is empty. For decisions, report missing constitutive
  memory only after the corresponding authoritative catalogue/read proves
  absence. Offer `jaiba-init` only for confirmed absence, never for an
  unavailable/ambiguous/permission-denied surface; `ask` never initializes
  or instruments anything. If the global contract is missing, name
  `jaiba-configure` as prerequisite, but do not run it.
- **Incomplete or malformed view** — distinguish missing concepts/artifacts
  established by authoritative full reads from unreadable, partial, stale,
  truncated or incomplete catalogue/read results. The latter are failures,
  not absence; explain what could not be verified and stop claims that
  depend on it. This applies to both filesystem layouts and external
  surfaces.

## What `ask` answers

Four domains, each grounded in the repository — never in memory from a
prior session or pre-training (`AGENTS.md` §2.1):

| Domain | Typical questions | Primary sources |
|---|---|---|
| **Code** | "what does this endpoint do?", "explain this module", "where is X handled?", "why does this break?" | The source files, their tests, `git log`/`git blame` for the *why-historical*. |
| **Active plan** | "what tasks are left?", "why does the plan do X first?", "is this already in the plan?" | Filesystem: `.ai/work/plan.md`, `tasks.md`, `walkthrough.md`. External: deterministic path via binding `v2` → exact executive context catalogue → exact logical IDs (`plan`, `tasks`, `walkthrough`) → package script `render` subcommand (or direct read in `document-tree`). No search. |
| **Active PRD** | "what does the PRD cover?", "which criteria are still unmet?", "what's out of scope?" | Filesystem: `.ai/work/PRD.md` (exists only at `spec` depth). External: deterministic path via binding `v2` → exact executive context catalogue → exact logical ID (`prd`) → package script `render` subcommand (or direct read in `document-tree`), when present. No search. |
| **Decisions** | "why did we decide to use Z?", "what alternatives did we reject?", "what happened in the last piece of work?" | Filesystem: `decision` via `.ai/memory/index.md` or legacy `.ai/memory/adr-log.md`, `.ai/memory/log/`, then `walkthrough.md`. External: deterministic path via binding `v2` → exact constitutive catalogue → exact logical IDs of decisions/log entries → package script `render` subcommand (or direct read in `document-tree`), plus resolved executive context for walkthrough. No search. |

A question can span domains ("does the plan cover criterion AUTH-002
from the PRD?") — read what the question needs from each, no more.

## Read what the question needs — and no more

`ask` is the lightweight lane. Unlike `conduct` and `fast`, it has
**no fixed precondition reads**. Reading the whole brain to answer
"what does this endpoint do?" would be wasteful (`AGENTS.md` §3.2). Let
the question drive the reads:

- **Pure code question** → go straight to the relevant source; you may
  not need the brain at all.
- **Plan / PRD / decision question** → read the corresponding artifacts
  (table above). Filesystem requires the actual selected files. External
  memory requires following the deterministic path (`MSV-008`): resolve binding
  `v2` (`~/.jaiba/memory/bindings/<sha256(canonical-work-root)>.yaml`, with legacy fallback to `~/.jaiba/memory/<host>/...` when present), complete enumeration of the exact owned catalogue scope, exact logical addresses/IDs, and invoke the adapter package script's `render` subcommand (or read materialized content directly on `document-tree`). Strictly prohibit full-text search (`mem_search`) to locate or display project artifacts or decisions; search is restricted to exploratory discovery when the concept address is completely unknown. Search previews, summaries and snippets are not authoritative content. Respect relation targets and
  unresolved-relation findings rather than inventing links. Cite external
  facts by stable logical address and available revision/receipt evidence,
  not a transient record ID or a local `.ai/` path. If the needed catalogue,
  read, relation target or provenance is partial/unavailable, state that
  limitation and do not claim absence or completeness.

The one cross-cutting rule: **ground every claim in something you
actually read.** If you didn't open it, don't assert it.

For how to orient when you don't yet know what's active — whether a
plan or PRD exists at all — read `references/orientation.md`.

## Answering well

- **Snippets, not dumps** (`AGENTS.md` §3.3). Quote the minimal lines,
  reference by `path:line`, use a small diff to illustrate. Never paste
  whole files into chat.
- **Say when something is missing or empty.** On filesystem, an exact
  selected file's absence may establish absence within that layout. On an
  external surface, only authoritative complete enumeration or exact
  `not-found` in the fully resolved readable owned scope establishes
  absence; partial views, failures and search misses do not (`AGENTS.md`
  §1, last line). Never invent an artifact.
- **Surface drift, don't patch it.** If, while answering, you notice
  the brain contradicts the code (the plan references a field the model
  renamed, the PRD assumes a flow the code dropped), point out the
  specific contradiction. Then *propose* `jaiba-init:update-brain` —
  `ask` never rewrites memory itself (`AGENTS.md` §5).
- **Distinguish fact from inference.** "The handler validates the email
  here (`auth/views.py:42`)" is a fact you read. "This probably fails
  when the token is expired" is an inference — mark it as one.
- **Offer the next step, don't take it.** A good answer often ends with
  a pointer: *"if you want, I can make that quick fix"* or *"this is
  big enough to design first"*. Offer — then wait. Suggesting is
  read-only; executing is not.

## When the question becomes an action

This is the boundary of the skill. `ask` does not execute changes — the
moment the developer stops asking and starts asking you to *act*, route
to the lane that owns that action. The session is shared, so
everything `ask` just read (the plan, the PRD, the code) is already in
context for the receiving skill — no re-investigation needed.

Quick routing (the framework routing rule, seen from `ask`):

| The developer now wants… | Route to |
|---|---|
| Advance the approved, active plan (cue: "continue", "next", "go") | `conduct` — `execute` phase |
| Spec, design, or plan new work ("let's plan this", "we need a feature that…", "help me think this through") | `conduct` — chain entry (`propose` or `spec`, per triage) |
| A small, contained change now ("quick change", "bump the version", "quick fix") | `fast` |
| Reconcile the brain with reality ("update the constitution", "record this decision") | `jaiba-init:update-brain` |

For the nuances — how to tell a question from an action cue, what to
carry across the hand-off, and how to avoid both over- and
under-triggering against conduct's `execute` phase and
`fast` — read `references/handoff.md`.

## Triggering: question vs. action

`ask` shares its trigger surface with the action lanes, so the
distinction is **intent**, not keywords:

- **Interrogative / exploratory → `ask`.** "why…?", "what…?",
  "how does … work?", "explain…", "is this covered?",
  "what's left…?". The developer wants understanding.
- **Imperative / continuation → action lane.** "continue", "do…",
  "add…", "bump the version", "let's plan this". The developer wants
  a change.

When a message mixes both ("why does the plan do X first? and also
bump the version"), answer the question first as `ask`, then route the
action — don't silently do the change while answering.

When genuinely ambiguous, default to `ask` and ask the developer what
they want. Answering a question you could have skipped costs a
paragraph; executing a change they only wanted explained costs an
unwanted edit (`AGENTS.md` §2.6).

## Language

Per `AGENTS.md` §3.5: this skill and all framework source are English.
Answers in chat follow the language the developer is writing in. `ask`
writes nothing into artifacts, so the artifact-language rule never
applies here.

## Common failure modes

- **Answering the plan/PRD from memory.** The repository is the
  source of truth (`AGENTS.md` §2.1). If you didn't open `plan.md`
  this session, you don't know what's in it. Read, then answer.
- **Reading the whole brain for a one-file question.** `ask` is the
  cheap lane — keep it cheap. Let the question scope the reads.
- **Sliding into execution.** The developer asks "why does this fail?"
  and you *fix* it. That's `fast`, not `ask`. Explain the
  cause, then offer to fix it — and wait.
- **Patching drift you spotted.** Noticing the brain is stale is an
  `ask` outcome; rewriting it is not. Propose
  `jaiba-init:update-brain`.
- **Dumping files.** "Explain this module" is not an invitation to
  paste 300 lines. Summarize, quote the load-bearing parts, link by
  line.
- **Inventing what isn't there.** No active plan established by a complete
  filesystem check or authoritative external enumeration? Say so, scoped
  to that checkout/context. On external access failure, report the failure;
  don't reconstruct a hypothetical plan or claim absence.
- **Using full-text search to locate known artifacts.** Searching with `mem_search`
  to find `plan`, `prd`, or decisions violates deterministic orientation. Always
  follow `binding` → catalogue → exact ID → `render`.
