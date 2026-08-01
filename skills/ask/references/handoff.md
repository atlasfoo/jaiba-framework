# `ask`: handing off to action

`ask` answers; it never executes. The skill's boundary is the moment
the developer stops asking and starts asking you to *act*. Getting this
boundary right is the whole job: cross it too eagerly and you make an
unwanted edit; refuse to cross it and the developer has to repeat
themselves in a new turn. This reference is about reading that moment
and handing off cleanly.

## Why hand off at all — the shared-session payoff

The reason `ask` exists *next to* the action lanes, rather than each
skill orienting from scratch, is that they share one session. When the
developer asks first and acts second, everything `ask` read — the plan,
the PRD, the relevant code, the decision history — is already in
context. The receiving skill (`conduct`, `fast`,
`jaiba-init:update-brain`) doesn't re-investigate; it inherits.

So the hand-off is not "start over in another skill". It's "carry this
understanding into execution". Make that explicit when you route:
*"I already have the plan and PRD context; a 'continue' takes us
straight into conduct's execute phase."*

## Reading the shift: question vs. action

The signal is **intent**, not vocabulary. The same words can be either,
depending on what the developer wants to happen next. This is exactly
the framework routing rule — continuation → `execute`, question →
`ask`, change → `fast` — applied from inside the question lane.

**Still a question (stay in `ask`):**
- Interrogatives: "why…?", "what…?", "how…?", "is this
  covered?", "what's left…?".
- Exploratory framing: "explain", "walk me through", "compare the
  options".
- Hypotheticals: "if we changed X, what would break?" — analysis, not a
  request to change X.

**Now an action (hand off):**
- Imperatives that mutate state: "do…", "add…", "change…",
  "rename…", "bump the version".
- Continuation cues against an approved plan: "continue", "next",
  "advance", "go", "proceed".
- Work-shaping requests: "let's plan this", "we need a feature
  that…", "help me spec this out".
- A direct "yes, do it" / "ok, go" answering an offer you just made.

When a single message carries both — *"why does it validate like that? and also fix it"* — answer the question as `ask`, **then** route the action.
Never fold the change silently into the answer; the developer asked for
an explanation *and* a fix, and they're owed both, in that order.

## Routing table

| Developer's intent | Owner | Notes |
|---|---|---|
| Advance the approved, active plan | `conduct` — `execute` phase | Only if `.ai/work/plan.md` exists *and* is approved *and* the message is a continuation cue. If no plan is active, a continuation cue is meaningless — ask what they mean. |
| Spec / design / plan new work | `conduct` — chain entry | "let's plan this", a fuzzy requirement to shape (`propose`), or work too big for `fast`. The chain's triage decides the depth (design vs. spec — PRD only when warranted). |
| Small, contained change now | `fast` | `fast` runs the shared triage; if the change is bigger than it looks, `fast` itself escalates into the conduct chain (or, with a plan active, offers fold-as-phase / park-and-replan). Don't pre-judge size in `ask` beyond a rough offer. |
| Reconcile / update the brain | `jaiba-init:update-brain` | For drift you surfaced while answering. Propose it; don't edit memory from `ask`. |

`ask`, like `fast`, is a pure routing lane — the developer never
invokes any of these by command except `/conduct [phase]`, which
remains the one explicit override when routing misfires or a phase
must be forced. If the developer's intent is clear, route; don't tell
them to type a command.

## How to hand off

1. **Confirm the shift is real.** If you're inferring action from an
   ambiguous message, don't — default to `ask` and ask (`AGENTS.md`
   §2.6). Cheap question vs. unwanted edit.
2. **Name the receiving lane and why.** *"This is a small, contained
   change → `fast`."* The developer should know which mode they're
   entering and can veto it.
3. **State what carries over.** The plan/PRD/code you already read.
   This is the value of having asked first — make it visible.
4. **Then proceed under that skill's rules.** Once handed off, the
   receiving skill owns the discipline: conduct's `execute`
   phase checks the worktree and approval; `fast` triages blast
   radius; `jaiba-init:update-brain` proposes before patching. `ask`'s
   read-only
   guarantee ends where the action skill's contract begins — and the
   developer crossed that line deliberately.

## Don't over- or under-trigger

- **Over-trigger (acting on a question):** the most damaging failure.
  "could we upgrade requests to v5?" is a *question about
  feasibility*, not a request to bump it. Answer the feasibility (blast
  radius, breaking changes), then offer the route. Don't bump the
  version.
- **Under-trigger (re-asking on a clear action):** the developer says
  "go ahead, continue" with an approved plan active — that's the
  conduct's `execute` phase, not an invitation to re-explain the
  plan. Hand off and let `execute` run.
- **The offer is not the action.** Ending an answer with *"want me to
  apply that as a quick fix?"* is still `ask`. You execute only when
  the developer accepts. Offering ≠ doing.

## Worked example — question, then accepted action

1. 👤 *"why does the itinerary listing make so many queries?"*
2. `ask`: locate the view, read it, identify the N+1 in the
   collaborator loop (`itineraries/views.py:58`). Explain in 3 lines.
   Offer: *"Fixable with `select_related` — one file. Want me to apply
   it now, or add it to the plan?"* — then wait. (Still `ask`.)
3. 👤 *"yes, apply it now"* → that's the shift, and it's a small
   contained change → `fast`, carrying the located view and the
   diagnosis. `fast` triages (one file, `inline`), applies the change,
   runs the Quality Gate.

The developer got the explanation *and* the fix — but the fix happened
under `fast`'s contract, only after they asked for it.
