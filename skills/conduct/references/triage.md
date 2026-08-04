# Triage: blast radius → depth

The single triage of the JAIBA framework. Every change request — no
matter which skill received it — is sized here and mapped onto the
depth continuum:

```
inline ────────→ design ────────→ spec        (mission: reserved for
(no executive     (plan.md +       (PRD +       multi-component work,
 artifacts;        tasks.md,        plan.md +    future SPEC-06)
 fast lane)        no PRD)          tasks.md)
```

Two skills consume this reference, with different parameters:

| Consumer | Default | Floor | Meaning |
|---|---|---|---|
| `fast` | `inline` | `inline` | assume contained; escalate on evidence |
| `conduct` | `design` | `design` | never less than a design; deepen to `spec` on evidence |

**Default** is where you land when the evidence is unremarkable.
**Floor** is the minimum the consumer can produce — `fast` may
conclude "this is `design` work" and hand off; `conduct` never
concludes "this is `inline`" for work already accepted into the chain
(if a request reaches it and triages `inline`, route it to `fast`
instead of building ceremony around a typo).

The judgment is about **blast radius**, not about how the request was
phrased. "Just bump requests to v5" is one short sentence and possibly
a hundred edits across contracts; "rename this private helper" is a
long-winded request and a one-file change. Estimate the work, not the
prose.

## Estimate the blast radius cheaply

Before deciding, do a few **surgical** reads/searches — enough to size
the change, not to do it. Tools serve discovery here, not bulk content
delivery.

1. **Find the change site(s).** Grep for the symbol, file, dependency,
   or config you'd modify.
2. **Count call sites / dependents.** A handful is contained; dozens
   ripple.
3. **Check contract impact.** Function signatures, API shapes,
   serialized formats, DB schemas, public types — and internal
   cross-component contracts, recorded as `reference` concepts of
   `kind: internal-contract` (`references/<slug>.md` in a concept
   bundle, the matching `reference-index.md` §3 row in the legacy flat
   layout): a change that crosses a boundary declared by a `sub-unit`
   concept (`identity/units/<slug>.md`, or `constitution.md` §5.1 in
   the legacy flat layout) ripples by definition.
4. **Check migration / breaking-change ripple.** For dependency
   upgrades, skim the changelog for the target version.
5. **Check verifiability.** One focused pass against the Quality Gate,
   or new test scaffolding and several rounds?
6. **Check the *why*.** Is the motivation technical (bump, perf,
   refactor, fix) or a change in *what the product does* for someone?

## Decision

### `inline` — no executive artifacts (fast lane)

All roughly hold:

- Contained footprint, on the order of 1–3 files.
- No contract/API/schema change consumed beyond the change site.
- No migration ripple; any dependency change is non-breaking for
  this code.
- Verifiable atomically against the Quality Gate.

### `design` — plan.md + tasks.md, **no PRD**

Any of these push past `inline`:

- Many files or lines; needs phase decomposition and reversible
  checkpoints.
- Changes a contract, schema, or public type others depend on.
- Requires a migration that ripples, or a breaking dependency upgrade
  that cascades.

…**and** the motivation is technical — the *what the product does*
doesn't change. Canonical `design`-depth cases (explicitly **no
PRD**, whatever their size):

- **Critical library / framework bump** with cascading breaking
  changes.
- **Performance improvement** — behavior identical, resource profile
  better.
- **Contained refactor** — structure changes, product behavior
  doesn't.
- Infrastructure/tooling work with no user-facing story to tell.

Writing product prose for these produces fiction ("As a user, I want
requests v5…"); their "why" is one paragraph in `plan.md § Objective`,
their "done" is the gate plus the plan's stated scope.

### `spec` — PRD + plan.md + tasks.md

Any of these:

- The request changes **what the product does for someone** — new
  capability, changed behavior, new actor — so acceptance criteria
  are worth writing before design.
- Multi-faceted: several user-visible behaviors that must agree.
- Ambiguous enough that formalizing the *what/why* is how the
  ambiguity gets resolved (often arriving via `propose`).

### Borderline

Right at a line: surface your estimate — files touched, contracts hit,
migration implied — and let the developer choose. Human-in-the-loop
beats a coin flip.

## Escalating and de-escalating

- **`fast` finds `design`+ work:** refuse *before* editing, with the
  concrete evidence (file count, changed contract, implied migration),
  and route into the conduct chain. If a plan is already active,
  `fast`'s plan-adjustment reference governs whether the work folds
  into it instead.
- **`conduct` receives `inline` work:** don't build ceremony —
  route to `fast`.
- **Depth discovered wrong mid-flight** (a "design" change turns out
  to alter user-visible behavior): stop, surface, and add the missing
  artifact (a PRD can be added to `.ai/work/` at any point before
  `execute` resumes) rather than pretending the depth was right.

## Worked examples

- *"bump requests from 2.31 to 2.32"* — changelog clean, one manifest
  line → **inline** (fast).
- *"update requests to v5"* — 23 call sites, 9 modules, Session
  subclass signature breaks, adapter config moves → **design**: real
  phases and staged verification, but nothing product-visible. No PRD.
- *"make the itinerary list load faster"* — perf target, behavior
  unchanged → **design** (measurements belong in the plan, not a PRD).
- *"let users co-edit itineraries with roles"* — new capability, new
  actors, happy/sad paths worth agreeing on first → **spec**.
