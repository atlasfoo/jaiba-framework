---
name: fast
description: >-
  Implicit direct-execution lane of the JAIBA framework for small, well-scoped, low-risk changes that don't justify entering the conduct chain. Not user-invocable — the routing rule triggers it whenever the developer asks for a quick, concrete change made now rather than planned. Trigger on phrases like "quick change", "make a quick adjustment", "update package X", "bump the version of Y", "small fix", "rename this", "quick fix", "just bump", "small change", "tweak this". Also trigger when the developer requests a change NOT contemplated by an active plan (e.g. "add a validation to the endpoint that was not in the plan"). Runs the shared triage (`conduct/references/triage.md`) with default and floor `inline`: atomic, low-blast-radius edits execute on the spot; anything that triages `design` or deeper is surfaced and routed into the `conduct` chain — with an active plan, offering to fold the work in as a new phase or park-and-replan, never silently building a second plan.
version: 3.3.1
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
   adjustment to an *active* plan, `fast` records it only after the
   developer confirms the change is correct. On filesystem it updates
   local executive artifacts; on an external surface it hands the
   confirmed amendment and read evidence to `conduct` for its authorized
   executive write, so the plan never drifts ahead of reality.

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
> repository. Resolve memory via the effective `create-memory`
> installation's `references/resolution.md` and
> `references/memory-surface-contract.md` (`jaiba-memory-surface` contract version **1.1.0**), never
> relative to this skill's installation. The built-in filesystem surface
> maps to the selected checkout; an external surface uses its exact
> standard binding `v2` (`~/.jaiba/memory/bindings/<sha256(canonical-work-root)>.yaml`, with legacy fallback to `~/.jaiba/memory/<host>/...` when present) and owned catalogue and may omit local `.ai/` and `AGENTS.md`.
>
> A missing/unavailable binding, catalogue, page, or required read is a
> failure, not proof of missing instrumentation or an empty plan. Stop any
> plan-dependent work on ambiguity, permission failure, partial/truncated
> reads, or unavailable surface; never bypass the selected external surface
> by calling it free-standing. Only authoritative complete enumeration or
> exact not-found in the fully resolved readable scope can establish no
> active artifact. If the surface is authoritatively absent, apply the
> free-standing policy and use the repository's applicable Quality Gate
> (quality-gate concept for a bundle; `constitution.md §6` for legacy; see
> `jaiba-contract.md` §1) or documented repository fallback.

Context loaded depends on execution context — detect which applies (see
"Two contexts" below) before reading.

**Free-standing** (authoritatively no active plan, or change unrelated to it):
1. **Project instructions** — read applicable `AGENTS.md` when present; an
   external surface may be valid without a local marker. Do not use marker
   presence as evidence for external memory.
2. **Phase Gate commands and TDD mode flag:**
   - Filesystem concept bundle: resolve `quality-gate` through
     `.ai/memory/index.md`.
   - Filesystem legacy flat: `constitution.md §6`.
    - External: resolve `quality-gate` from the complete constitutive
      catalogue and exact full-read it. Use only gate commands and TDD
      posture explicitly declared by that concept, preserving their stated
      provenance and repository validation context; arbitrary unrelated
      memory text is not executable gate authority.
   Read only applicable gate material; do not treat failed/partial reads as
   absence or fall back to a different selected surface.
3. **External integrations the change touches:**
   - Filesystem concept bundle: `reference` concepts through index.
   - Filesystem legacy flat: `.ai/memory/reference-index.md`.
   - External: exact catalogue and full reads of relevant `reference` objects.
   Skip entirely if the change touches no indexed integrations.
   
   Resolve the effective `create-memory` installation's
   `references/resolution.md` and `references/memory-surface-contract.md` (contract version `1.1.0`);
   use exact binding `v2` (`~/.jaiba/memory/bindings/<sha256(canonical-work-root)>.yaml`, falling back to legacy `~/.jaiba/memory/<host>/...` when present), project/context, and complete authoritative catalogues,
   never previews or guessed paths.

**Plan adjustment** (an approved plan exists in the selected executive
context and the change falls within its scope):
1. **Project instructions** — read `AGENTS.md` when present; external
   surfaces need not have one.
2. **Resolve and catalogue** — revalidate the selected binding `v2` and exact
   project/context, completely enumerate its executive catalogue, then
   exact full-read the plan, tasks, walkthrough and gate instructions that
   exist. On filesystem, this maps to `.ai/work/plan.md` and companion
   files; on external surfaces, use logical objects, never local-path
   assumptions. Confirm the plan is approved/executing and establish its
   scope from these reads.
3. **Record the read baseline** — retain revision/head evidence (`expected-head`) for every
   executive object that may be amended. Before any authorized write,
   re-read and compare those revisions/heads; after the write, exact-read and
   verify complete intended content and relations. On external memory,
   `conduct` owns executive writes and the single-writer handoff; fast
   reports the confirmed adjustment and baseline evidence to conduct instead of
   writing the backend or its executive objects itself. For surfaces with
   the `executive-journal` capability (`MSV-005`), emit surgical `patch` operations
   rather than requesting a monolithic full rewrite (tasks: `add-task{after, block}`,
   `amend-task{id, block}`; plan: `append-to-section{heading: "Plan amendments", content: "..."}`
   or `append-section{after, heading, content}`). If the surface lacks `patch` (legacy 1.0.x),
   hand off the full updated object to conduct's single-writer update path with
   `efficiency-warning: full-update-without-patch`.

> For plan adjustments, the selected executive context is re-resolved and
> fully read; gate commands and TDD posture come from the exact tasks
> object (or local `tasks.md`) in that context.

Skip nothing within your applicable context — a "trivial" change
against the wrong assumptions isn't trivial.

## Two contexts

`fast` behaves slightly differently depending on whether it's
free-standing or adjusting a live plan. Detect which one applies:

- **Free-standing** — authoritative resolution confirms no active plan in
  the selected context, **or** a fully read plan exists but the request is
  unrelated to its scope. A failed/partial lookup is never free-standing.
  Filesystem example:
  *"bump requests to 2.32"* with no plan active. The change stands on
  its own.

- **Plan adjustment** — the selected context's fully read plan exists, is approved/
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
2. **Determine context.** Free-standing vs. plan adjustment, using
   authoritative complete catalogue/full reads in the selected context;
   for filesystem this is `.ai/work/plan.md`.
3. **Read preconditions** per context (see "Universal preconditions"
   above). Gate commands come from `tasks.md § Gate Commands` for plan
   adjustments, and from the selected surface's full-read gate concept (or
   filesystem `quality-gate` / legacy `constitution.md §6`) for
   free-standing changes.
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
    - **Free-standing:** write no executive artifact. The change
      plus git history is the record; give the developer a one-line
      recap in chat. (Executive artifacts belong to `conduct`;
      creating an orphan `walkthrough.md` with no plan would be cleaned
      up by nothing.)
    - **Plan adjustment:** execute first, then **ask the developer to
      confirm the change is correct**. For filesystem, only then update
      local work artifacts per `references/plan-adjustment.md`. For an
      external context, after confirmation hand off the evidence and
      approved amendment to `conduct`, which alone performs serialized,
      revision-checked, fully verified executive writes. On surfaces with
      the `executive-journal` capability (`MSV-005`), emit surgical `patch`
      operations (`add-task{after, block}`, `amend-task{id, block}`,
      `append-to-section{heading, content}`, `append-section{after, heading, content}`,
      `append-entry{content}`) rather than requesting a monolithic full rewrite.
      If the surface lacks `patch` (legacy 1.0.x), hand off the full updated
      object to conduct's single-writer update path with
      `efficiency-warning: full-update-without-patch`. On any backend
      access or verification failure, make no JAIBA-owned memory changes
      and report the failure.
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
  `fast` writes no executive artifact (on filesystem, nothing to `.ai/work/`).
- **Building a second plan around out-of-band work.** With a plan
  active, big out-of-band work has exactly two honest exits — fold it
  in as a phase, or park-and-replan — both chosen by the developer,
  in the open. A parallel plan silently forked next to the active one
  is never an option.
- **Running the Quality Gate "later".** A `fast` change is done when
  the gate is green, not when the edit is saved.
