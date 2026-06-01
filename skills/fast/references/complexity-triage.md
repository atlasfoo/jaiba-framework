# `fast`: complexity triage

The most important thing `fast` does is decide whether a change
belongs to `fast` at all. Get this right and everything else is easy;
get it wrong and you either pay planning overhead on a typo, or you
half-apply a breaking change that needed a plan.

The judgment is about **blast radius**, not about how the request was
phrased. "Just bump requests to v5" is one short sentence and possibly
a hundred edits across contracts. "Rename this private helper" is a
long-winded request and a one-file change. Estimate the work, not the
prose.

## Estimate the blast radius cheaply

Before deciding, do a few **surgical** reads/searches — enough to
size the change, not to do it. Tools serve discovery here, not bulk
content delivery (`AGENTS.md` §3.4).

1. **Find the change site(s).** Grep for the symbol, file, dependency,
   or config you'd modify.
2. **Count the call sites / dependents.** For a dependency or a public
   symbol, how many places consume it? A handful is `fast`; dozens is
   `planning`.
3. **Check for contract impact.** Would the change alter a function
   signature, an API shape, a serialized format, a DB schema, or a
   public type that other code or other services rely on?
4. **Check for migration / breaking-change ripple.** For dependency
   upgrades, skim the changelog or the breaking-change notes for the
   target version. Breaking changes that touch your call sites turn a
   bump into a project.
5. **Check verifiability.** Can you confirm the change is correct in a
   single focused pass with the Quality Gate, or would you need new
   test scaffolding and several rounds?

## Decision

**`fast`-eligible** when *all* roughly hold:

- Contained footprint — on the order of 1–3 files.
- No change to contracts/APIs/schemas consumed beyond the change site.
- No data or schema migration with downstream impact.
- Any dependency change is non-breaking, or its breaking changes don't
  reach your code.
- Verifiable atomically against the Quality Gate.

**Route to `planning`** when *any* hold:

- Many files or many lines.
- Changes a signature, interface, serialized format, schema, or public
  type that others depend on.
- Requires a migration that ripples.
- Is a dependency upgrade whose breaking changes cascade through the
  code.
- Would need phase decomposition, reversible checkpoints, or several
  verification rounds.

**Borderline** — right at the line: surface your estimate and let the
developer choose (`AGENTS.md` §2.6). Human-in-the-loop beats a coin
flip.

## How to refuse

When the change is too big, refuse *before* editing and be concrete
(see `SKILL.md` → "Refusing gracefully"). The value of the refusal is
the evidence: name the file count, the changed contract, the implied
migration. Then recommend `planning define`.

## Worked example — `requests` v5 (a refusal)

> 👤 *"/fast update the requests package to version 5"*

Triage steps:

1. Locate usage: grep `import requests` / `requests.` across the repo.
2. Count: 23 call sites across 9 modules, plus a custom
   `requests.Session` subclass in the HTTP layer.
3. Contract impact: v5 (hypothetically) drops the legacy
   `Session.request(**kwargs)` shape the subclass overrides → the
   subclass and its 6 callers change.
4. Migration ripple: the retry/adapter configuration moves to a new
   API → config touched in two settings modules.
5. Verifiability: needs new tests around the adapter behavior, several
   rounds.

Conclusion: **refuse**. Reply with the concrete blast radius and route
to planning:

> `requests` v5 touches 9 modules (23 usages), breaks the signature of
> your `Session` subclass, and moves the adapters/retries config to a
> new API. That requires phases and staged verification — this is
> `planning` work, not `fast`. Shall we build a plan with `planning define`?

## Worked example — `requests` patch bump (accepted)

> 👤 *"/fast bump requests from 2.31 to 2.32"*

Triage: changelog shows no breaking changes affecting your call sites;
only the manifest pin changes. Footprint: one file
(`pyproject.toml` / `requirements.txt`). → **`fast`-eligible.** Bump,
run the Quality Gate, suggest `chore(deps): bump requests to 2.32`.

## Worked example — unplanned validation (accepted, plan adjustment)

> 👤 (mid-plan) *"add an email validation to the invitation endpoint,
> it was not in the plan"*

Triage: one serializer/handler, one new test. Contained. →
**`fast`-eligible**, and a **plan adjustment** because it lands inside
the active plan's scope. Execute, then follow
`references/plan-adjustment.md` to record it after the developer
confirms.
