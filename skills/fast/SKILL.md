---
name: fast
description: >-
  Implicit direct-execution lane of the JAIBA framework for small, well-scoped, low-risk changes that don't justify entering the conduct chain. Not user-invocable — the routing rule triggers it whenever the developer asks for a quick, concrete change made now rather than planned. Trigger on phrases like "quick change", "make a quick adjustment", "update package X", "bump the version of Y", "small fix", "rename this", "quick fix", "just bump", "small change", "tweak this". Also trigger when the developer requests a change NOT contemplated by an active plan (e.g. "add a validation to the endpoint that was not in the plan"). Runs the shared triage (`conduct/references/triage.md`) with default and floor `inline`: atomic, low-blast-radius edits execute on the spot; anything that triages `design` or deeper is surfaced and routed into the `conduct` chain — with an active plan, offering to fold the work in as a new phase or park-and-replan, never silently building a second plan.
version: 3.0.0
author: atlasfoo<iscomejia15@outlook.com>
user-invocable: false
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
work doesn't pay the overhead of the full `conduct` chain.

Two things make `fast` safe rather than reckless:

1. **It triages before it acts.** The skill first estimates the blast
   radius of the change using the framework's shared triage. If the
   work turns out to be larger than `inline`, it *refuses* to edit and
   routes the developer into the `conduct` chain — better to hand
   off early than to half-apply a change that needed a design.
2. **It keeps the brain honest.** When the change is an unplanned
   adjustment to an *active* plan, `fast` records it into the
   executive artifacts in `.ai/work/` — but only after the developer
   confirms the change is correct, so the plan never drifts ahead of
   reality.

## Invocation: implicit only

`fast` is **not user-invocable** — there is no `/fast` command. The
frontmatter declares `user-invocable: false` (on host agents that
support the field; elsewhere, this section and the `description:` are
the contract): the routing rule is the only way in. Whenever the
developer's message is a **change request** — small on its face, or
out-of-band relative to an active plan — the host agent routes it
here. The two sibling lanes are `ask` (questions, also implicit) and
`conduct` (`execute` for continuation cues; also the only lane
that keeps an explicit `/conduct` override).

Being implicit changes nothing about discipline: triage still runs
first, and `fast` still refuses work that is bigger than it looks.

## The one rule: triage first

Before reading or writing anything else, decide whether this change is
`inline` at all. The blast-radius → depth logic is **shared with
`conduct`** and lives in one place: the `conduct` skill's
`references/triage.md` (installed alongside this skill). Read it when
sizing a change. `fast` consumes it with these parameters:

| Parameter | Value | Meaning |
|---|---|---|
| Default | `inline` | assume contained; escalate only on evidence |
| Floor | `inline` | `fast` may conclude "this is `design`/`spec` work" and hand off — it never produces executive artifacts of its own |

In short, a change stays `inline` when all roughly hold: contained
footprint (~1–3 files), no contract/API/schema change consumed beyond
the change site, no migration ripple, verifiable atomically against
the Quality Gate. Any of the `design` or `spec` signals in the shared
triage pushes the work out of `fast`. **Investigate scope before
touching code** — a few surgical reads / greps, per the triage's
"estimate the blast radius cheaply" steps.

If the change triages past `inline`, **stop and hand off** — see
"Refusing gracefully" below. When in doubt, surface your estimate and
ask the developer; don't silently over- or under-scope
(`AGENTS.md` §2.6).

## Universal preconditions

> **Brain check first.** `fast` can be installed per-project or
> **globally** (e.g. `~/.claude/skills/`), shared across every
> repository. Either way, "the brain" means `.ai/` and `AGENTS.md` at
> the root of *this* project — where `.git/` lives — never a path
> relative to this skill's own installation location.
>
> If `AGENTS.md` is missing/empty/not JAIBA's (neither the minimal
> marker pointing at the global JAIBA contract nor a legacy full
> protocol), or
> `.ai/memory/` is incomplete (neither concept bundle at `index.md` nor
> legacy flat at `constitution.md`), this project isn't (fully)
> JAIBA-instrumented. `fast` doesn't block on this — small, atomic
> changes are still in scope — but: fall back to whatever verification
> commands the repo itself defines for the Phase Gate (in the concept
> bundle, the `quality-gate` concept; in legacy flat, `constitution.md
> §6`; see `jaiba-contract.md §1` if unsure which) — README, CI config,
> or failing those, the package manager's own scripts (`package.json`,
> `Makefile`, `justfile`, …). Treat the change as free-standing (skip
> "plan adjustment" entirely), and mention `jaiba-init` once, in the
> closing recap, as an opportunity rather than a blocker.

Context loaded depends on execution context — detect which applies (see
"Two contexts" below) before reading.

**Free-standing** (no active plan or change unrelated to it):
1. **`AGENTS.md`** — behavioral contract.
2. **Phase Gate commands and TDD mode flag:**
   - Concept bundle (when `.ai/memory/index.md` exists): the `quality-gate` concept
   - Legacy flat (when `constitution.md` exists, no `index.md`): `constitution.md §6`
   Read the applicable section only; skip the rest of your brain.
3. **External integrations the change touches:**
   - Concept bundle: `reference` concepts, mapped through `.ai/memory/index.md`
   - Legacy flat: `.ai/memory/reference-index.md`
   Skip entirely if the change touches no indexed integrations.
   
   Use `jaiba-contract.md §1` (Brain Map) to determine your brain layout.

**Plan adjustment** (`.ai/work/plan.md` exists and the change falls
within its scope):
1. **`AGENTS.md`** — behavioral contract.
2. **`.ai/work/plan.md`** and **`tasks.md`** — plan context and
   Phase Gate commands (already embedded in `tasks.md § Gate Commands`).

> For plan adjustments, the brain is not re-read. Gate commands and TDD
> posture are available in the work files (`tasks.md`).

Skip nothing within your applicable context — a "trivial" change
against the wrong assumptions isn't trivial.

## Two contexts

`fast` behaves slightly differently depending on whether it's
free-standing or adjusting a live plan. Detect which one applies:

- **Free-standing** — no `.ai/work/plan.md` exists, **or** one
  exists but the requested change is unrelated to its scope. Example:
  *"bump requests to 2.32"* with no plan active. The change stands on
  its own.

- **Plan adjustment** — `.ai/work/plan.md` exists, is approved/
  executing, **and** the requested change falls inside or adjacent to
  the plan's scope but wasn't contemplated by it. Example, mid-plan:
  *"add a validation to the endpoint that was not in the plan"*.

If a plan is active and you're unsure whether the change belongs to
it, ask — the recording behavior differs and you don't want to either
pollute an unrelated plan or silently expand its approved scope.

## Flow

1. **Triage.** (Shared triage, default/floor `inline` — see above.)
   If the change is not `inline`, refuse and route: no active plan →
   "Refusing gracefully" below; active plan → the **big out-of-band
   change** procedure in `references/plan-adjustment.md`. Stop here.
2. **Determine context.** Free-standing vs. plan adjustment (check
   whether `.ai/work/plan.md` exists and the change is in scope).
3. **Read preconditions** per context (see "Universal preconditions"
   above). Gate commands come from `tasks.md § Gate Commands` for plan
   adjustments, and from the brain (either `quality-gate` concept or
   `constitution.md §6` per layout) for free-standing changes.
4. **For a plan adjustment, check the worktree.** A dirty worktree is
   *expected* if you're mid-phase — read `tasks.md` / `walkthrough.md`
   to confirm the dirt is the in-progress phase, not a surprise from
   another session. If it looks unexpected, stop and ask (same
   discipline as `conduct`'s `execute` phase).
5. **Execute atomically** (`AGENTS.md` §2.5). One logical change. If
   it breaks something unrelated, stop and surface it — do not stack
   fixes.
   - **Tests / TDD.** Honor the Quality Gate after the change. For a
     *behavioral* change with TDD `enabled`, add or adjust the test
     that covers it. Purely non-behavioral changes (dependency bump,
     rename, comment, formatting) don't need a new test. If the change
     would require building substantial new test scaffolding, that's a
     signal it wasn't `fast` work — reconsider triage.
6. **Run the Phase Gate.** For plan adjustments use the commands from
   `tasks.md § Gate Commands`; for free-standing changes use the Phase
   Gate commands from the brain (`quality-gate` concept or `constitution.md §6`
   per layout). If it fails and the fix isn't itself atomic, stop and surface it.
7. **Record, per context:**
   - **Free-standing:** write nothing to `.ai/work/`. The change
     plus git history is the record; give the developer a one-line
     recap in chat. (Executive artifacts belong to `conduct`;
     creating an orphan `walkthrough.md` with no plan would be cleaned
     up by nothing.)
   - **Plan adjustment:** execute first, then **ask the developer to
     confirm the change is correct**. Only on confirmation, update the
     work artifacts (`tasks.md`, `plan.md`, `walkthrough.md`). The
     full procedure is in `references/plan-adjustment.md`.
8. **Suggest a commit, don't run it.** Propose a conventional-commit
   message (`fix`, `chore`, `refactor`, `perf`, `docs`, …) inferred
   from the change. Run git only if the developer asks (`AGENTS.md`
   restrictions; same policy as `conduct`).

## Refusing gracefully

Refusing is a feature, not a failure — it's how `fast` stays safe.
When triage says the work is past `inline` and **no plan is active**:

1. **Don't apply a partial change.** Leave the worktree as you found
   it.
2. **Explain the blast radius concretely.** Name what you found: how
   many files, which contracts change, what migration is implied. A
   developer can't trust "this is too complex" — they can trust "this
   touches 14 call sites and changes the `Client.request` signature".
3. **Route into the `conduct` chain.** The triage depth carries
   over (`design`: plan + tasks, no PRD; `spec`: PRD first), and so
   does the blast-radius evidence you just gathered — the chain's
   `spec` phase starts from it instead of re-investigating. Offer a
   one-line sketch of what the design would need to cover. Example:
   > This change breaks the `Client.request` signature in 14 places and
   > requires a config migration — that's `design`-depth work, not a
   > quick change. Shall we design it properly? I'll carry over what I
   > found.

When triage says the work is past `inline` and **a plan is active**,
don't just refuse — follow the big out-of-band procedure in
`references/plan-adjustment.md`: surface the size, then offer to fold
the work into the plan as a new phase or to park-and-replan. Never
create a second plan silently.

## Asking the human

Same discipline as `conduct`: one topic per question, closed
options when the answer space is closed, plain chat for open
questions. Never guess business rules or invent conventions
(`AGENTS.md` §2.6). The two moments `fast` most often needs the human:

- **Borderline triage** — the change is right at the `inline`/`design`
  boundary. Surface your blast-radius estimate and let the developer
  decide.
- **Plan-adjustment confirmation** — after executing, before writing
  to the work artifacts.

## Language

Per `AGENTS.md` §3.5: this skill and all framework source are English.
Anything `fast` writes **into** work artifacts (`walkthrough.md`
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
  `fast` writes nothing to `.ai/work/`.
- **Building a second plan around out-of-band work.** With a plan
  active, big out-of-band work has exactly two honest exits — fold it
  in as a phase, or park-and-replan — both chosen by the developer,
  in the open. A parallel plan silently forked next to the active one
  is never an option.
- **Running the Quality Gate "later".** A `fast` change is done when
  the gate is green, not when the edit is saved.
