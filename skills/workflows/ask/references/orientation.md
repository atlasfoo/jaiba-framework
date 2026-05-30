# `ask`: cold-start orientation

`ask` is meant to answer on the **first message of a session**, with no
prior conversation to lean on. "¿qué falta en el plan?" has to work even
when you don't yet know whether a plan exists, what its slug is, or
which spec — if any — is active. Orientation is how you find out, cheaply,
before you answer.

The guiding rule: **orient only as far as the question requires.** A
pure code question needs almost no orientation. A plan or spec question
needs you to locate the active artifact first. Don't read the whole
brain reflexively (`AGENTS.md` §3.2).

## Step 1 — classify the question

Decide which domain(s) the question touches. This tells you what to
look for.

| Question is about… | Orient by… |
|---|---|
| A piece of code, a symbol, a behavior | Locating it in source (grep / glob). No brain read needed unless the *why* is historical. |
| "The plan" (tasks left, ordering, scope) | Finding the active plan in `.ai/session/`. |
| "The spec" (coverage, stories, scope) | Finding the active spec in `.ai/specs/`. |
| A past decision ("why did we…") | `.ai/memory/adr-log.md`, then `walkthrough.md`. |
| The project in general (stack, conventions) | `.ai/memory/constitution.md`. |

## Step 2 — locate the active artifact

### Active plan

The active plan lives in `.ai/session/`. Check, in order:

1. **`.ai/session/plan.md` exists?** If yes, that *is* the active plan —
   there is only ever one. Read its frontmatter for the slug and the
   spec it descends from (if any). Read `tasks.md` for progress and
   `walkthrough.md` for what already happened.
2. **No `plan.md`?** There is no active plan. Say so: *"No hay un plan
   activo en `.ai/session/`."* Don't reconstruct one from a summary or
   from git. If a `<slug>-summary.md` is present, the plan was finished
   but not yet cleaned up — mention that, it's the honest answer.

### Active spec

Specs live in `.ai/specs/<name>/`. Unlike the plan, there can be more
than one.

1. **Did the developer name the spec?** ("la spec de auth") → read
   `.ai/specs/<that-name>/PRD.md` and `user-stories.md`.
2. **They said "the spec" but didn't name it?**
   - Exactly one spec directory exists → that's the one. Read it.
   - Several exist → don't guess. List them and ask which.
   - The active plan's frontmatter cites a spec → prefer that one, but
     confirm if it's ambiguous.
3. **No `.ai/specs/` or it's empty?** Say there's no active spec.

## Step 3 — answer from what you read

Once oriented, answer per the SKILL.md rules: grounded in the files you
opened, snippets not dumps, facts distinguished from inferences. If
orientation itself surfaced a contradiction (the plan cites a spec
story that doesn't exist; the spec assumes a model the code renamed),
that *is* part of the answer — surface it, and propose `update-brain`
if reconciliation is warranted.

## What orientation is *not*

- **Not a full precondition sweep.** `planning` and `fast` read the
  constitution, reference-index, and session state every time because
  they're about to act. `ask` isn't acting — read only what the
  question needs.
- **Not a license to assume.** "Active plan" means *the file exists and
  you read it*, not "there's probably a plan". If `plan.md` is absent,
  the answer is "no hay plan activo", full stop.

## Worked example — cold "¿qué falta en el plan?"

First message of the session. No context.

1. Classify: it's a **plan** question.
2. Locate: `.ai/session/plan.md` exists → slug
   `itinerarios-colaborativos-modelo-base`, descends from spec
   `itinerarios-colaborativos`. Read `tasks.md`.
3. `tasks.md` shows Phase 1 fully checked, Phase 2 has 2 of 4 tasks
   left (invitation email integration, its test), Phase 3 untouched.
4. Answer: name the two open Phase-2 tasks and the pending Phase 3, in
   2–4 lines, referencing `tasks.md`. Offer: *"si quieres seguimos con
   `planning:execute`"* — then wait. Offering is read-only; advancing
   the plan is `execute`, not `ask`.

## Worked example — cold "¿la spec ya cubre el borrado de cuenta?"

1. Classify: **spec** question.
2. Locate: developer didn't name it. Two specs under `.ai/specs/`:
   `auth` and `itinerarios-colaborativos`. "Borrado de cuenta" points
   at `auth`, but two exist → confirm: *"¿La spec `auth`?"* before
   reading, rather than guessing.
3. On confirmation, read `auth/PRD.md` and `user-stories.md`, find
   whether an account-deletion story exists and its checkbox state.
4. Answer with the specific story (or its absence) and a `path`
   reference. If the story exists but the code clearly doesn't
   implement it, note the gap as an inference, not a fact.
