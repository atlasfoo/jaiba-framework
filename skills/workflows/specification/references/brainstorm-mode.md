# `specification:brainstorm`

Shape a fuzzy requirement into something concrete enough to formalize.
End state: a **landed requirement** — a shared, explicit understanding
of the problem, the users, the rough scope, and the open decisions —
held in the conversation, ready for `define` to turn into artifacts.

This mode is **purely conversational. It writes nothing to disk.** A
half-formed idea is volatile by nature; committing it to a file before
it has settled just creates an artifact that's wrong by the next
message. So brainstorm lives entirely in the chat, and its output flows
straight into `define` **within the same conversation**. If the session
ends, the brainstorm is gone — that's the intended trade-off. Tell the
developer this if they seem to expect a saved file.

## When this mode fits

Use brainstorm when the input is any of:

- **Vague** — "I want some kind of collaboration feature."
- **A solution in search of a problem** — "let's add websockets"
  (why? for whom? what breaks without it?).
- **Too big to be one spec** — it smells like three requirements
  wearing a trench coat.
- **In tension with the project** — it seems to contradict the
  constitution, an ADR, or what the code already does.

If the requirement is already clear, skip brainstorm and go to
`define`. Brainstorming a well-formed requirement just wastes the
developer's time.

## Flow

1. **Read the universal preconditions** (see `SKILL.md`). You can't
   help shape a requirement well without knowing the project's scope,
   stack, existing integrations, and prior decisions. The history
   especially matters here — a feature that was tried and reverted is
   worth knowing about before you re-propose it.
2. **Mirror back the core.** State, in one or two sentences, the
   problem you think the developer is describing — *the problem, not a
   solution*. Getting this wrong early is cheap to fix; getting it
   wrong silently is expensive. Confirm before going further.
3. **Probe the dimensions that matter.** Ask, one topic at a time, the
   questions that actually move the requirement from fuzzy to
   concrete. Typical axes:
   - **Users / actors** — who is this for? One role or several?
   - **The job to be done** — what can they *not* do today, and what
     would "done" let them do?
   - **Boundaries** — what's explicitly *not* part of this?
   - **Constraints** — performance, security, compliance, existing
     systems it must respect.
   - **Risks and unknowns** — what could make this much bigger than it
     looks? What hidden subsystem does it touch?
4. **Offer shapes, don't dictate one.** When there's a real fork
   (async vs real-time, build vs integrate, one role vs a role
   system), lay out the 2–3 viable shapes with their trade-offs and
   let the developer choose. Ground the options in what the code and
   `reference-index.md` already support — a shape that reuses an
   existing integration beats one that invents a new dependency.
5. **Split if it's too big.** If the requirement is clearly several
   specs, say so and help carve it at the joints. It's better to ship
   one well-defined spec than to define one sprawling, unbuildable
   one.
6. **Converge.** Brainstorm is done when the developer can answer:
   *who is this for, what problem does it solve, what's in and out, and
   what are the known unknowns.* At that point, summarize the landed
   requirement in a few crisp lines and offer to move to `define`.

## Hand-off to `define`

When the requirement has landed and the developer is ready:

> "I think we've got this shaped: **<one-line problem>**, for
> **<users>**, covering **<scope in>** but not **<scope out>**. Want me
> to write it up as a spec? (`specification define`)"

On a yes, continue **in the same conversation** into `define` — carry
everything you just established (it's all in context) rather than
asking the developer to repeat it. Do not expect the brainstorm to be
persisted; it isn't.

## Worked example (TripNest)

The developer opens with: *"I want users to be able to share their
trips somehow and maybe edit them together?"*

Steps in this mode:

1. Read constitution (TripNest: Django, travel planning), the
   `Itinerary` model and views, `reference-index.md` (notices
   `django-guardian` is already integrated for object permissions),
   and recent plan summaries (no prior collaboration work).
2. Mirror: *"So the core problem is that travelers can't plan a trip
   together inside TripNest today — they fall back to WhatsApp or
   Google Docs. Is that the pain?"* → developer confirms.
3. Probe, one at a time:
   - *Editing — real-time, or asynchronous is fine?* → async is fine
     for v1.
   - *Can anyone with the link edit, or are there roles?* → roles:
     owner / editor / reader.
   - *What happens when two people edit the same day at once?* →
     last-write-wins is acceptable for now; full conflict resolution
     is out.
4. Offer a shape: invitation-based collaboration reusing the existing
   `django-guardian` object permissions, rather than a new ACL layer.
   Developer agrees.
5. Not too big — one spec.
6. Converge: *"Landed: invitation-based async collaboration on
   itineraries with owner/editor/reader roles, last-write-wins,
   reusing django-guardian. Out: real-time editing, conflict merging.
   Want me to write the spec?"*

→ Developer says yes → continue into `define` in the same conversation.

## Common failure modes

- **Solutioning before the problem is clear.** "Let's use websockets"
  is an answer to a question nobody has stated yet. Pin the problem
  and the users first.
- **Writing a file.** Brainstorm persists nothing. The moment you
  reach for the templates, you've left brainstorm — that's `define`.
- **Interrogation instead of collaboration.** This is a dialogue, not
  a form. React to answers, follow the interesting threads, and offer
  your own read of the trade-offs — the developer brought you in to
  think *with* them.
- **Letting a three-headed requirement through.** If it won't fit in
  one coherent PRD, split it now, not after `define` has tangled it.
- **Forgetting the in-conversation hand-off.** Since nothing is saved,
  ending the chat after a great brainstorm loses it. Move into
  `define` while the context is live.
