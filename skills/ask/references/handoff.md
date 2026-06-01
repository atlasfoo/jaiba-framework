# `ask`: handing off to action

`ask` answers; it never executes. The skill's boundary is the moment
the developer stops asking and starts asking you to *act*. Getting this
boundary right is the whole job: cross it too eagerly and you make an
unwanted edit; refuse to cross it and the developer has to repeat
themselves in a new turn. This reference is about reading that moment
and handing off cleanly.

## Why hand off at all — the shared-session payoff

The reason `ask` exists *next to* the action skills, rather than each
skill orienting from scratch, is that they share one session. When the
developer asks first and acts second, everything `ask` read — the plan,
the spec, the relevant code, the decision history — is already in
context. The receiving skill (`planning`, `fast`, `update-brain`)
doesn't re-investigate; it inherits.

So the hand-off is not "start over in another skill". It's "carry this
understanding into execution". Make that explicit when you route:
*"I already have the plan and spec context; we continue this with
`planning:execute`."*

## Reading the shift: question vs. action

The signal is **intent**, not vocabulary. The same words can be either,
depending on what the developer wants to happen next.

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
- Explicit skill calls: "let's build a plan", "/fast …", "planning
  define".
- A direct "yes, do it" / "ok, go" answering an offer you just made.

When a single message carries both — *"why does it validate like that? and also fix it"* — answer the question as `ask`, **then** route the action.
Never fold the change silently into the answer; the developer asked for
an explanation *and* a fix, and they're owed both, in that order.

## Routing table

| Developer's intent | Owner | Notes |
|---|---|---|
| Advance an approved, active plan | `planning:execute` | Only if `plan.md` exists *and* is approved *and* the message is a continuation cue. If no plan is active, a continuation cue is meaningless — ask what they mean. |
| Build a new plan | `planning:define` | "armemos un plan", or work too big for `fast`. |
| Small, contained change now | `fast` | `fast` will triage; if it's bigger than it looks, `fast` itself routes to `planning`. Don't pre-judge size in `ask` beyond a rough offer. |
| Reconcile / update the brain | `update-brain` | For drift you surfaced while answering. Propose it; don't edit memory from `ask`. |
| Formalize a requirement | `specification` | "let's make a spec for this". |

## How to hand off

1. **Confirm the shift is real.** If you're inferring action from an
   ambiguous message, don't — default to `ask` and ask (`AGENTS.md`
   §2.6). Cheap question vs. unwanted edit.
2. **Name the receiving skill and why.** *"This is a small, contained
   change → `fast`."* The developer should know which mode they're
   entering and can veto it.
3. **State what carries over.** The plan/spec/code you already read.
   This is the value of having asked first — make it visible.
4. **Then proceed under that skill's rules.** Once handed off, the
   receiving skill owns the discipline: `planning:execute` checks
   `git status` and approval; `fast` triages blast radius;
   `update-brain` proposes before patching. `ask`'s read-only guarantee
   ends where the action skill's contract begins — and the developer
   crossed that line deliberately.

## Don't over- or under-trigger

- **Over-trigger (acting on a question):** the most damaging failure.
  "could we upgrade requests to v5?" is a *question about
  feasibility*, not "/fast bump it". Answer the feasibility (blast
  radius, breaking changes), then offer the route. Don't bump the
  version.
- **Under-trigger (re-asking on a clear action):** the developer says
  "go ahead, continue" with an approved plan active — that's
  `planning:execute`, not an invitation to re-explain the plan. Hand
  off and let `execute` run.
- **The offer is not the action.** Ending an answer with *"si quieres
  lo arreglamos con `fast`"* is still `ask`. You execute only when the
  developer accepts. Offering ≠ doing.

## Worked example — question, then accepted action

1. 👤 *"why does the itinerary listing make so many queries?"*
2. `ask`: locate the view, read it, identify the N+1 in the
   collaborator loop (`itineraries/views.py:58`). Explain in 3 lines.
   Offer: *"Fixable with `select_related`; do we do it with `fast` or
   add it to the plan?"* — then wait. (Still `ask`.)
3. 👤 *"do it with fast"* → that's the shift. Hand off to `fast`,
   carrying the located view and the diagnosis. `fast` triages
   (one file, contained), applies the change, runs the Quality Gate.

The developer got the explanation *and* the fix — but the fix happened
under `fast`'s contract, only after they asked for it.
