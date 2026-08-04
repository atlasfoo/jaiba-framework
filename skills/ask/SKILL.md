---
name: ask
description: >-
  Implicit read-only Q&A lane of the JAIBA framework. Not user-invocable — the routing rule triggers it whenever the developer asks a question instead of requesting a change: about the codebase, the active work in `.ai/work/` (plan.md, tasks.md, walkthrough.md, PRD.md), or recorded decisions in `.ai/memory/`. Trigger on interrogative or exploratory messages like "why does the plan do X before Y?", "what tasks are left?", "what does the PRD cover?", "is this already in the plan?", "what does this endpoint do?", "explain this module", "why did we decide to use Z?", "walk me through this". Strictly read-only: it reads, searches, and explains, but never edits code, writes artifacts, or runs the Quality Gate to change state. It yields to the action lanes per the routing rule: a continuation cue ("continue", "next", "go") belongs to conduct's execute phase, new work to spec or plan enters the conduct chain, and a small contained change routes to fast.
version: 2.0.0
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
across every repository you work in. Either way, "the brain" means
`.ai/` and `AGENTS.md` at the root of the **current project** — where
`.git/` lives — never a path relative to this skill's own installation
location.

Orienting cold (see `references/orientation.md`) includes checking
whether this project is JAIBA-instrumented at all — `AGENTS.md` exists,
is non-empty, and is the JAIBA behavioral contract (or points to the
global JAIBA contract installed in the agent's config), and
`.ai/memory/` holds real content, not bare `[bracket]` templates. Two
outcomes:

- **Not instrumented at all** (no `.ai/`, or `AGENTS.md` missing/empty/
  not the JAIBA contract) — say so plainly. Code questions still work
  from the repository directly; plan/PRD/decision questions get "there
  is no active work — this project has no JAIBA brain yet." Offer
  `jaiba-init` (bootstrap) as the next step, then wait — `ask` doesn't
  instrument anything. If the *global* contract is also missing, name
  `jaiba-configure` as its machine-level prerequisite; still don't run
  either.
- **Partially instrumented** (`.ai/` exists but `.ai/memory/` is bare
  templates) — questions about active work still function (`.ai/work/`
  doesn't depend on the long-term brain); decision questions ("why did
  we choose X?") get "the ADR log hasn't been initialized yet." Offer
  `jaiba-init`, which resumes at its `update-brain:initialize` mode.

## What `ask` answers

Four domains, each grounded in the repository — never in memory from a
prior session or pre-training (`AGENTS.md` §2.1):

| Domain | Typical questions | Primary sources |
|---|---|---|
| **Code** | "what does this endpoint do?", "explain this module", "where is X handled?", "why does this break?" | The source files, their tests, `git log`/`git blame` for the *why-historical*. |
| **Active plan** | "what tasks are left?", "why does the plan do X first?", "is this already in the plan?" | `.ai/work/plan.md`, `tasks.md`, `walkthrough.md`. |
| **Active PRD** | "what does the PRD cover?", "which criteria are still unmet?", "what's out of scope?" | `.ai/work/PRD.md` (exists only at `spec` depth). |
| **Decisions** | "why did we decide to use Z?", "what alternatives did we reject?", "what happened in the last piece of work?" | The `decision` concept via `.ai/memory/index.md` (`.ai/memory/adr-log.md` in the legacy flat layout), `.ai/memory/log/` (closed work, chronological), then `walkthrough.md` for tactical calls in flight. |

A question can span domains ("does the plan cover criterion AUTH-002
from the PRD?") — read what the question needs from each, no more.

## Read what the question needs — and no more

`ask` is the lightweight lane. Unlike `conduct` and `fast`, it has
**no fixed precondition reads**. Reading the whole brain to answer
"what does this endpoint do?" would be wasteful (`AGENTS.md` §3.2). Let
the question drive the reads:

- **Pure code question** → go straight to the relevant source; you may
  not need the brain at all.
- **Plan / PRD / decision question** → read the corresponding
  artifacts (table above). For these you *must* read the actual files
  — never answer "what's in the plan" from assumption.

The one cross-cutting rule: **ground every claim in something you
actually read.** If you didn't open it, don't assert it.

For how to orient when you don't yet know what's active — whether a
plan or PRD exists at all — read `references/orientation.md`.

## Answering well

- **Snippets, not dumps** (`AGENTS.md` §3.3). Quote the minimal lines,
  reference by `path:line`, use a small diff to illustrate. Never paste
  whole files into chat.
- **Say when something is missing or empty.** If the developer asks
  about "the plan" and `.ai/work/plan.md` doesn't exist, say so
  plainly — don't invent one (`AGENTS.md` §1, last line).
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
- **Inventing what isn't there.** No active plan? Say "there is no
  active plan". Don't reconstruct a hypothetical one to be helpful.
