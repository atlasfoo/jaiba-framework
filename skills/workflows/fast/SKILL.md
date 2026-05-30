---
name: fast
description: Direct-execution workflow inside the JAIBA framework for small, well-scoped, low-risk changes that don't justify a full plan. Use this skill whenever the developer wants a quick, concrete change made now rather than planned. Trigger on explicit calls like "fast" / "/fast", and on phrases like "cambio rápido", "haz un ajuste rápido", "actualiza el paquete X", "sube la versión de Y", "pequeño fix", "renombra esto", "quick fix", "just bump", "small change", "tweak this". Also trigger when the developer asks for an adjustment NOT contemplated by an active plan (e.g. "agrega una validación al endpoint que no estaba en el plan", "add a quick check here"). This skill competes with `planning`: prefer `fast` for atomic, low-blast-radius edits, and defer to `planning` for anything that touches many files, changes public contracts, needs a migration, or warrants phase decomposition — `fast` itself will refuse over-large work and hand it to `planning`.
version: 1.0.0
author: atlasfoo<iscomejia15@outlook.com>
requires:
  - git
tags:
  - jaiba
  - workflows
  - jaiba-workflows
  - fast-mode
---

# Fast Skill

Direct execution of a small, well-scoped, low-risk change — without
writing a plan first. This is the sanctioned exception to the "no
blind coding" rule (`AGENTS.md` §2.3), and it exists so that trivial
work doesn't pay the overhead of the full `planning` cycle.

Two things make `fast` safe rather than reckless:

1. **It triages before it acts.** The skill first estimates the blast
   radius of the change. If the work turns out to be larger than a
   `fast` change should be, it *refuses* and routes the developer to
   `planning` — better to hand off early than to half-apply a change
   that needed a plan.
2. **It keeps the brain honest.** When the change is an unplanned
   adjustment to an *active* plan, `fast` records it into the session
   artifacts — but only after the developer confirms the change is
   correct, so the plan never drifts ahead of reality.

## The one rule: triage first

Before reading or writing anything else, decide whether this change is
`fast`-eligible at all. **Investigate scope before touching code** —
a few surgical reads / greps to estimate how far the change reaches.

Quick guardrails (guidelines, not hard limits — surface borderline
cases to the developer instead of deciding alone):

| `fast`-eligible | Route to `planning` instead |
|---|---|
| ~1–3 files, contained blast radius | Many files / many lines |
| No change to public contracts or APIs consumed elsewhere | Changes interfaces, signatures, schemas others depend on |
| No data/schema migration that ripples | Needs a migration with downstream impact |
| Dependency bump with no/contained breaking changes | Dependency upgrade whose breaking changes cascade through the code |
| Completable and verifiable in a single focused pass | Needs phase decomposition or reversible checkpoints |

If the change fails any right-column test, **stop and hand off** — see
"Refusing gracefully" below. When in doubt, ask the developer; don't
silently over- or under-scope (`AGENTS.md` §2.6).

For the full heuristics, the `requests`-v5-style worked example, and
how to estimate blast radius cheaply, read
`references/complexity-triage.md`.

## Universal preconditions

Once you've judged the change plausibly `fast`-eligible, do these
reads before executing (skip nothing — a "trivial" change against the
wrong assumptions isn't trivial):

1. **`AGENTS.md`** — your behavioral contract. Always.
2. **`.ai/memory/constitution.md`** — the **Quality Gate** (§6) and
   the **TDD mode** flag (§7). You still honor the gate for a one-line
   change.
3. **`.ai/memory/reference-index.md`** — only the entries the change
   touches (e.g. the dependency you're bumping). Don't invent
   integrations; if the change needs one that isn't indexed, surface
   the gap (`AGENTS.md` §5.3).
4. **`.ai/session/`** — check whether a plan is active. This decides
   the execution context (next section).

## Two contexts

`fast` behaves slightly differently depending on whether it's
free-standing or adjusting a live plan. Detect which one applies:

- **Free-standing** — no `.ai/session/plan.md` exists, **or** one
  exists but the requested change is unrelated to its scope. Example:
  `/fast actualiza requests a la 2.32`. The change stands on its own.

- **Plan adjustment** — `.ai/session/plan.md` exists, is approved/
  executing, **and** the requested change falls inside or adjacent to
  the plan's scope but wasn't contemplated by it. Example, mid-plan:
  *"agrega una validación al endpoint que no estaba en el plan"*.

If a plan is active and you're unsure whether the change belongs to
it, ask — the recording behavior differs and you don't want to either
pollute an unrelated plan or silently expand its approved scope.

## Flow

1. **Triage.** (See above / `references/complexity-triage.md`.) If not
   `fast`-eligible, refuse and route to `planning`. Stop here.
2. **Read preconditions.** Quality Gate, TDD mode, relevant
   reference-index entries, session state.
3. **Determine context.** Free-standing vs. plan adjustment.
4. **For a plan adjustment, check the worktree.** A dirty worktree is
   *expected* if you're mid-phase — read `tasks.md` / `walkthrough.md`
   to confirm the dirt is the in-progress phase, not a surprise from
   another session. If it looks unexpected, stop and ask
   (`planning:execute` discipline).
5. **Execute atomically** (`AGENTS.md` §2.5). One logical change. If
   it breaks something unrelated, stop and surface it — do not stack
   fixes.
   - **Tests / TDD.** Honor the Quality Gate after the change. For a
     *behavioral* change with TDD `enabled`, add or adjust the test
     that covers it. Purely non-behavioral changes (dependency bump,
     rename, comment, formatting) don't need a new test. If the change
     would require building substantial new test scaffolding, that's a
     signal it wasn't `fast` work — reconsider triage.
6. **Run the Quality Gate.** Use the commands from the project
   scriptfile or `README.md` (constitution §6). If it fails and the
   fix isn't itself atomic, stop and surface it.
7. **Record, per context:**
   - **Free-standing:** write nothing to `.ai/session/`. The change
     plus git history is the record; give the developer a one-line
     recap in chat. (Session artifacts belong to `planning`; creating
     an orphan `walkthrough.md` with no plan would be cleaned up by
     nothing.)
   - **Plan adjustment:** execute first, then **ask the developer to
     confirm the change is correct**. Only on confirmation, update the
     session artifacts (`tasks.md`, `plan.md`, `walkthrough.md`). The
     full procedure is in `references/plan-adjustment.md`.
8. **Suggest a commit, don't run it.** Propose a conventional-commit
   message (`fix`, `chore`, `refactor`, `perf`, `docs`, …) inferred
   from the change. Run git only if the developer asks (`AGENTS.md`
   restrictions; same policy as `planning`).

## Refusing gracefully

Refusing is a feature, not a failure — it's how `fast` stays safe.
When triage says the work is too big:

1. **Don't apply a partial change.** Leave the worktree as you found
   it.
2. **Explain the blast radius concretely.** Name what you found: how
   many files, which contracts change, what migration is implied. A
   developer can't trust "this is too complex" — they can trust "this
   touches 14 call sites and changes the `Client.request` signature".
3. **Route to `planning`.** Recommend `planning define`, and offer a
   one-line sketch of what the plan would need to cover. Example:
   > Este cambio rompe la firma de `Client.request` en 14 lugares y
   > necesita una migración de config. Es trabajo de `planning`, no de
   > `fast`. ¿Armamos un plan con `planning define`?

## Asking the human

Same discipline as `planning`: one topic per question, closed options
when the answer space is closed, plain chat for open questions. Never
guess business rules or invent conventions (`AGENTS.md` §2.6). The two
moments `fast` most often needs the human:

- **Borderline triage** — the change is right at the `fast`/`planning`
  boundary. Surface your blast-radius estimate and let the developer
  decide.
- **Plan-adjustment confirmation** — after executing, before writing
  to the session artifacts.

## Language

Per `AGENTS.md` §3.5: this skill and all framework source are English.
Anything `fast` writes **into** session artifacts (`walkthrough.md`
notes, `plan.md` amendments) follows the language the developer is
using in the session.

## Common failure modes

- **Skipping triage and discovering the size mid-change.** Estimate
  the blast radius *first*. The expensive mistake is a half-applied
  breaking change.
- **Treating "small request" as "small change".** "Just bump
  requests to v5" is one sentence and potentially a hundred edits.
  Investigate, don't assume.
- **Updating plan artifacts before the developer confirms.** For a
  plan adjustment, the confirmation gates the write — that's what
  keeps the plan from drifting ahead of approved reality.
- **Orphaning a `walkthrough.md` on a free-standing change.** Free
  `fast` writes nothing to `.ai/session/`.
- **Running the Quality Gate "later".** A `fast` change is done when
  the gate is green, not when the edit is saved.
