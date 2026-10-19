# `ask`: cold-start orientation

`ask` is meant to answer on the **first message of a session**, with no
prior conversation to lean on. "what's left in the plan?" has to work even
when you don't yet know whether a plan exists, what its slug is, or
whether the work carries a PRD. Orientation is how you find out,
cheaply, before you answer.

The guiding rule: **orient only as far as the question requires.** A
pure code question needs almost no orientation. A plan or PRD question
needs you to locate the active artifact first. Don't read the whole
brain reflexively (`AGENTS.md` §3.2).

## Step 1 — classify the question

Decide which domain(s) the question touches. This tells you what to
look for.

Three rows below touch constitutive memory. First resolve the effective
`create-memory` installation and follow its `references/resolution.md` and
`references/memory-surface-contract.md`; do not assume filesystem or discover a
surface from this skill's location. For filesystem, apply the dual-layout
rule in `jaiba-contract.md` §1 and use the appropriate column below. For
an external surface, use its exact binding, owned catalogue and full reads
as the authoritative source; search previews are discovery only. The
`type:` vocabulary is the closed set in `jaiba-init/references/okf-pattern.md`.

| Question is about… | Filesystem: concept bundle | Filesystem: legacy flat | External surface |
|---|---|---|---|
| A piece of code, a symbol, a behavior | Locate source. No brain read unless the *why* is historical. | Same. | Same; external memory is not a source-code substitute. |
| "The plan" (tasks left, ordering, scope) | `.ai/work/` executive artifacts. | Same; `.ai/work/` is separate from constitutive layout. | Resolve exact executive context; completely enumerate its owned catalogue, then full-read the plan/tasks/walkthrough objects that exist. |
| "The PRD" / "the spec" (coverage, criteria, scope) | `.ai/work/PRD.md` when present. | Same. | Exact executive context catalogue/full read of PRD object when present; verify linked logical objects as needed. |
| A past decision ("why did we…") | `decision` by type via `.ai/memory/index.md`. | `.ai/memory/adr-log.md`. | Complete constitutive catalogue and full-read matching decision objects. |
| Closed, past work ("what did we ship last week?") | `.ai/memory/log/` entries. | Same. | Complete constitutive catalogue and full reads of relevant `log-entry` objects. |
| The project in general (stack, conventions) | Relevant `project`, `architecture`, or `convention` concept via index. | `.ai/memory/constitution.md`. | Complete constitutive catalogue and full reads of relevant concepts. |

Either branch, a decision question that needs the tactical *why* behind
a still-open call also reads `walkthrough.md`, not just the standing
decision.

## Step 2 — resolve and locate the active artifact

For filesystem, use the selected checkout's physical paths below after
resolving the supported layout. For an external surface, resolve the exact
binding, project ID and executive context through the canonical references
above. Enumerate the complete owned executive catalogue for that context
(consume all pages and confirm completion/consistency); then exact-read the
full logical objects needed for this question. Preserve relation targets
and revision/receipt evidence for citations. A search result or preview may
help discover candidates but cannot prove completeness or absence. If
binding, catalogue, page, exact read, or required relation is unavailable,
ambiguous, partial, truncated, or permission-denied, report the failure and
stop; none is evidence that the context or artifact is empty. `ask` must
not persist JAIBA bindings, alter JAIBA namespace/ownership, or perform
JAIBA adapter/memory operations that mutate JAIBA-owned data. Ordinary
host-required memory/session bookkeeping remains independent and is not
JAIBA evidence or a source for JAIBA reads.

### Active plan

On the filesystem surface, active work lives in `.ai/work/`. Check, in order:

1. **`.ai/work/plan.md` exists?** If yes, that *is* the active plan —
   there is only ever one. Read its frontmatter for the slug, the
   depth, and whether a local PRD exists (`prd:`). Read `tasks.md` for
   progress and `walkthrough.md` for what already happened.
2. **No `plan.md`?** There is no active plan in this checkout. Say so: *"There is no
   active plan in `.ai/work/`."* Don't reconstruct one from a summary or
   from git. If a `<slug>-summary.md` is present, the work was finished
   but not yet archived — mention that, it's the honest answer.

> **Legacy layout.** If the project still has `.ai/session/` and/or
> `.ai/specs/` instead of `.ai/work/`, it predates the unified layout.
> Answer from the files that exist, note the drift, and suggest
> `jaiba-doctor` — don't migrate anything from `ask`.

On an external surface, use the authoritative full catalogue and exact
reads described above. The unique logical `plan` object in the selected
context is the active plan; read its related `tasks` and `walkthrough`
objects as needed. Report an absent plan only after complete authoritative
enumeration (or exact not-found in that fully resolved readable scope),
never from a search miss. Check the plan's declared PRD relation/logical ID;
read its full content and needed criteria relations. Cite stable logical
addresses and available revision/receipt evidence, not local `.ai/` paths
or ephemeral backend record IDs. Ambiguous duplicates or unresolved
relations block confident claims; surface them as such.

### Active PRD

On filesystem, the PRD, when it exists, is an executive artifact next to the plan:

1. **`.ai/work/PRD.md` exists?** Read it — its acceptance criteria
   schema (`<PREFIX>-NNN`, happy/sad) is what "coverage" questions are
   really about. Cross-check `plan.md § Covered criteria` and the
   `covers:` fields in `tasks.md` when the question is "is this
   covered?".
2. **No `PRD.md` but a plan exists?** The work is at `design` depth —
   deliberately no PRD. Say so; the plan's Objective carries the why.
3. **Neither?** There is no active work in this checkout. For *past* work, the
    `.ai/memory/log/` entries are the record.

On an external surface, report no PRD only when a complete catalogue/read
of the exact context and the plan's full relation data establishes that no
PRD is present. A partial catalogue or failed read is not a no-PRD result.

## Step 3 — answer from what you read

Once oriented, answer per the SKILL.md rules: grounded in the files you
opened, snippets not dumps, facts distinguished from inferences. If
orientation itself surfaced a contradiction (the plan cites a criterion
that isn't in the PRD; the PRD assumes a model the code renamed),
that *is* part of the answer — surface it, and propose
`jaiba-init:update-brain` if reconciliation is warranted.

## What orientation is *not*

- **Not a full precondition sweep.** `conduct` and `fast` read the
  constitution, reference-index, and work state every time because
  they're about to act. `ask` isn't acting — read only what the
  question needs.
- **Not a license to assume.** "Active plan" means *the file exists and
  you read it*, not "there's probably a plan". If `plan.md` is absent,
  the answer is "there is no active plan", full stop.

## Worked example — cold "what's left in the plan?"

First message of the session. No context.

1. Classify: it's a **plan** question.
2. Locate: `.ai/work/plan.md` exists → slug
   `collaborative-itineraries-base-model`, `depth: spec`, local
   `PRD.md`. Read `tasks.md`.
3. `tasks.md` shows Phase 1 fully checked, Phase 2 has 2 of 4 tasks
   left (T-007 invitation email integration, T-008 its test), Phase 3
   untouched.
4. Answer: name the two open Phase-2 tasks and the pending Phase 3, in
   2–4 lines, referencing `tasks.md`. Offer: *"say 'continue' and we
   pick it up from T-007"* — then wait. Offering is read-only;
   advancing the plan is conduct's `execute` phase, not
   `ask`.

## Worked example — cold "does the PRD already cover account deletion?"

1. Classify: **PRD** question.
2. Locate: `.ai/work/PRD.md` exists (the plan's frontmatter also cites
   it). Read its acceptance criteria schema.
3. Search the criteria for an account-deletion behavior; check whether
   any `AUTH-NNN` criterion covers it and whether some task in
   `tasks.md` lists it under `covers:`.
4. Answer with the specific criterion (or its absence) and a `path`
   reference. If the criterion exists but the code clearly doesn't
   implement it yet, note the gap as an inference, not a fact —
   `tasks.md` says whether it's still pending.
