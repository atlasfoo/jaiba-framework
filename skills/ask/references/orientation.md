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

| Question is about… | Orient by… |
|---|---|
| A piece of code, a symbol, a behavior | Locating it in source (grep / glob). No brain read needed unless the *why* is historical. |
| "The plan" (tasks left, ordering, scope) | Finding the active work in `.ai/work/`. |
| "The PRD" / "the spec" (coverage, criteria, scope) | `.ai/work/PRD.md` — it exists only when triage ran the chain at `spec` depth. |
| A past decision ("why did we…") | `.ai/memory/adr-log.md` (standing decisions), then `walkthrough.md` for tactical calls in flight. |
| Closed, past work ("what did we ship last week?") | `.ai/memory/log/` — append-only, one entry per closed piece of work, newest by date prefix. |
| The project in general (stack, conventions) | `.ai/memory/constitution.md`. |

## Step 2 — locate the active artifact

### Active plan

The active work lives in `.ai/work/`. Check, in order:

1. **`.ai/work/plan.md` exists?** If yes, that *is* the active plan —
   there is only ever one. Read its frontmatter for the slug, the
   depth, and whether a local PRD exists (`prd:`). Read `tasks.md` for
   progress and `walkthrough.md` for what already happened.
2. **No `plan.md`?** There is no active plan. Say so: *"There is no
   active plan in `.ai/work/`."* Don't reconstruct one from a summary or
   from git. If a `<slug>-summary.md` is present, the work was finished
   but not yet archived — mention that, it's the honest answer.

> **Legacy layout.** If the project still has `.ai/session/` and/or
> `.ai/specs/` instead of `.ai/work/`, it predates the unified layout.
> Answer from the files that exist, note the drift, and suggest
> `jaiba-doctor` — don't migrate anything from `ask`.

### Active PRD

The PRD, when it exists, is an executive artifact next to the plan:

1. **`.ai/work/PRD.md` exists?** Read it — its acceptance criteria
   schema (`<PREFIX>-NNN`, happy/sad) is what "coverage" questions are
   really about. Cross-check `plan.md § Covered criteria` and the
   `covers:` fields in `tasks.md` when the question is "is this
   covered?".
2. **No `PRD.md` but a plan exists?** The work is at `design` depth —
   deliberately no PRD. Say so; the plan's Objective carries the why.
3. **Neither?** There is no active work. For *past* work, the
   `.ai/memory/log/` entries are the record.

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
