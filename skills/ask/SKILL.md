---
name: ask
description: Read-only question-and-answer mode of the JAIBA framework. Use this skill whenever the developer asks a question instead of requesting a change — about the codebase, about the active plan (`.ai/session/plan.md`, `tasks.md`, `walkthrough.md`), or about the active spec (`.ai/specs/<name>/`) — and answer it cold, without relying on prior session context. Trigger on explicit calls like "ask" / "/ask", and IMPLICITLY on interrogative or exploratory messages even when the developer doesn't name the skill: "why does the plan do X before Y?", "what tasks are left?", "what does the auth spec cover?", "is this already in the plan?", "what does this endpoint do?", "explain this module", "why did we decide to use Z?", "what's left in the plan?", "why did we go with this approach?", "is this covered by the spec?", "walk me through this". This skill is strictly read-only: it reads, searches, and explains, but never edits code, writes session/brain artifacts, or runs the Quality Gate to change state. It deliberately yields to the action skills — when the developer stops asking and asks to *act*, route there instead: a continuation cue ("continue", "next", "go") belongs to `planning:execute`; "let's build a plan" / "planning define" to `planning`; "quick change", "bump the version of X", "quick fix" to `fast`. Because `ask` and the action skills share one session, the context gathered while answering carries straight into whichever skill executes the change.
version: 1.0.0
author: atlasfoo<iscomejia15@outlook.com>
requires:
  - git
tags:
  - jaiba
  - workflows
  - jaiba-workflows
  - ask-mode
---

# Ask Skill

The read-only mode of the JAIBA framework. `ask` answers questions —
about the codebase, the active plan, or the active spec — without
changing anything. It is the sanctioned place for the developer to
*think out loud* with the agent before committing to a change.

Two properties define it:

1. **It is strictly read-only.** `ask` reads, searches, and explains.
   It never edits code, never writes to `.ai/`, never runs the Quality
   Gate to mutate state. This is what makes it safe to invoke
   reflexively — the developer can ask anything without risking an
   accidental edit. (`AGENTS.md` sample: *"When in doubt, use `skill:
   ask` before executing."*)
2. **It orients cold.** `ask` is meant to be usable with no prior
   conversation. A bare "what's left in the plan?" must work on the
   first message of a session. So `ask` orients itself from the
   repository — it does not assume it already knows what the active
   plan or spec is.

And one transition defines its boundary: when the developer shifts from
*asking* to *acting*, `ask` hands off to an action skill rather than
doing the work itself. The context it already gathered carries over —
that's the payoff of asking first.

## What `ask` answers

Three domains, each grounded in the repository — never in memory from a
prior session or pre-training (`AGENTS.md` §2.1):

| Domain | Typical questions | Primary sources |
|---|---|---|
| **Code** | "what does this endpoint do?", "explain this module", "where is X handled?", "why does this break?" | The source files, their tests, `git log`/`git blame` for the *why-historical*. |
| **Active plan** | "what tasks are left?", "why does the plan do X first?", "is this already in the plan?" | `.ai/session/plan.md`, `tasks.md`, `walkthrough.md`. |
| **Active spec** | "what does the auth spec cover?", "is this story already closed?", "what's out of scope?" | `.ai/specs/<name>/PRD.md`, `user-stories.md`. |
| **Decisions** | "why did we decide to use Z?", "what alternatives did we reject?" | `.ai/memory/adr-log.md`, then `walkthrough.md` for tactical calls. |

A question can span domains ("does the plan cover the invitation story
from the spec?") — read what the question needs from each, no more.

## Read what the question needs — and no more

`ask` is the lightweight skill. Unlike `planning` and `fast`, it has
**no fixed precondition reads**. Reading the whole brain to answer
"what does this endpoint do?" would be wasteful (`AGENTS.md` §3.2). Let
the question drive the reads:

- **Pure code question** → go straight to the relevant source; you may
  not need the brain at all.
- **Plan / spec / decision question** → read the corresponding
  artifacts (table above). For these you *must* read the actual files
  — never answer "what's in the plan" from assumption.

The one cross-cutting rule: **ground every claim in something you
actually read.** If you didn't open it, don't assert it.

For how to orient when you don't yet know what's active — which plan,
which spec, whether either exists — read
`references/orientation.md`.

## Answering well

- **Snippets, not dumps** (`AGENTS.md` §3.3). Quote the minimal lines,
  reference by `path:line`, use a small diff to illustrate. Never paste
  whole files into chat.
- **Say when something is missing or empty.** If the developer asks
  about "the plan" and `.ai/session/plan.md` doesn't exist, say so
  plainly — don't invent one (`AGENTS.md` §1, last line).
- **Surface drift, don't patch it.** If, while answering, you notice
  the brain contradicts the code (the plan references a field the model
  renamed, the spec assumes a flow the code dropped), point out the
  specific contradiction. Then *propose* `update-brain` — `ask` never
  rewrites memory itself (`AGENTS.md` §5).
- **Distinguish fact from inference.** "The handler validates the email
  here (`auth/views.py:42`)" is a fact you read. "This probably fails
  when the token is expired" is an inference — mark it as one.
- **Offer the next step, don't take it.** A good answer often ends with
  a pointer: *"if you want, we can fix it with `fast`"* or *"this
  could use a plan"*. Offer — then wait. Suggesting is read-only; executing is
  not.

## When the question becomes an action

This is the boundary of the skill. `ask` does not execute changes — the
moment the developer stops asking and starts asking you to *act*, route
to the skill that owns that action. The session is shared, so
everything `ask` just read (the plan, the spec, the code) is already in
context for the receiving skill — no re-investigation needed.

Quick routing:

| The developer now wants… | Route to |
|---|---|
| Advance an approved, active plan (cue: "continue", "next", "go") | `planning:execute` |
| Build a new plan ("let's build a plan", "planning define") | `planning:define` |
| A small, contained change now ("quick change", "bump the version", "quick fix") | `fast` |
| Reconcile the brain with reality ("update the constitution", "record this decision") | `update-brain` |
| Formalize a requirement into a spec ("let's make a spec for this") | `specification` |

For the nuances — how to tell a question from an action cue, what to
carry across the hand-off, and how to avoid both over- and
under-triggering against `planning:execute` and `fast` — read
`references/handoff.md`.

## Triggering: question vs. action

`ask` shares its trigger surface with the action skills, so the
distinction is **intent**, not keywords:

- **Interrogative / exploratory → `ask`.** "why…?", "what…?",
  "how does … work?", "explain…", "is this covered?",
  "what's left…?". The developer wants understanding.
- **Imperative / continuation → action skill.** "continue", "do…",
  "add…", "bump the version", "let's build a plan". The developer wants
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

- **Answering the plan/spec from memory.** The repository is the
  source of truth (`AGENTS.md` §2.1). If you didn't open `plan.md`
  this session, you don't know what's in it. Read, then answer.
- **Reading the whole brain for a one-file question.** `ask` is the
  cheap skill — keep it cheap. Let the question scope the reads.
- **Sliding into execution.** The developer asks "why does this fail?"
  and you *fix* it. That's `fast`, not `ask`. Explain the
  cause, then offer to fix it — and wait.
- **Patching drift you spotted.** Noticing the brain is stale is an
  `ask` outcome; rewriting it is not. Propose `update-brain`.
- **Dumping files.** "Explain this module" is not an invitation to
  paste 300 lines. Summarize, quote the load-bearing parts, link by
  line.
- **Inventing what isn't there.** No active plan? Say "there is no
  active plan". Don't reconstruct a hypothetical one to be helpful.
