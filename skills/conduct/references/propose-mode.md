# `conduct:propose`

Shape a fuzzy requirement into something concrete enough to enter the
chain. End state: a **landed requirement** — a shared, explicit
understanding of the problem, the users, the rough scope, and the open
decisions — held in the conversation, ready for `spec` to formalize.

This phase is **purely conversational. It writes nothing to disk.** A
half-formed idea is volatile by nature; committing it to a file before
it has settled just creates an artifact that's wrong by the next
message. So propose lives entirely in the chat, and its output flows
straight into `spec` **within the same conversation**. If the session
ends, the proposal is gone — that's the intended trade-off. Tell the
developer this if they seem to expect a saved file.

## When this phase fits

- **Vague** — "I want some kind of collaboration feature."
- **A solution in search of a problem** — "let's add websockets"
  (why? for whom? what breaks without it?).
- **Too big to be one piece of work** — it smells like three
  requirements wearing a trench coat.
- **In tension with the project** — it seems to contradict the
  constitution, an ADR, or what the code already does.

If the requirement is already clear, skip propose and run triage →
`spec`. Brainstorming a well-formed requirement wastes the developer's
time.

## Flow

1. **Load the full context** (see `SKILL.md § Context Loading`). You
   can't shape a requirement well without the project's scope, stack,
   integrations, standing decisions, and what past `.ai/memory/log/`
   entries say was already tried.
2. **Mirror back the core.** State, in one or two sentences, the
   problem you think the developer is describing — *the problem, not a
   solution*. Confirm before going further.
3. **Probe the dimensions that matter**, one topic at a time:
   - **Users / actors** — who is this for?
   - **The job to be done** — what can't they do today?
   - **Boundaries** — what's explicitly *not* part of this?
   - **Constraints** — performance, security, compliance, existing
     systems it must respect.
   - **Risks and unknowns** — what could make this much bigger than
     it looks?
4. **Offer shapes, don't dictate one.** When there's a real fork
   (async vs real-time, build vs integrate), lay out 2–3 viable shapes
   with trade-offs and let the developer choose. Ground the options in
   what the code and `reference-index.md` already support.
5. **Split if it's too big.** Better one well-defined piece of work
   than one sprawling, unbuildable one.
6. **Converge and pre-triage.** Propose is done when the developer can
   answer: *who is this for, what problem does it solve, what's in and
   out, what are the known unknowns.* Summarize the landed requirement
   in a few crisp lines, note the depth triage suggests (a landed
   requirement that's purely technical may still be `design` depth —
   see `references/triage.md`), and offer to move into `spec`.

## Hand-off to `spec`

> "I think we've got this shaped: **<one-line problem>**, for
> **<users>**, covering **<scope in>** but not **<scope out>**. This
> looks like **<spec | design>** depth. Want me to formalize it?"

On a yes, continue **in the same conversation** into `spec` — carry
everything just established (it's all in context). Do not expect the
proposal to be persisted; it isn't.

## Common failure modes

- **Solutioning before the problem is clear.** "Let's use websockets"
  answers a question nobody has stated. Pin the problem and users
  first.
- **Writing a file.** Propose persists nothing. The moment you reach
  for a template, you've left propose — that's `spec`.
- **Interrogation instead of collaboration.** This is a dialogue, not
  a form. React to answers, follow the interesting threads, offer your
  own read of the trade-offs.
- **Letting a three-headed requirement through.** If it won't fit one
  coherent piece of work, split it now.
- **Forgetting the in-conversation hand-off.** Nothing is saved;
  continue into `spec` while the context is live.
