# `conduct:spec`

Turn a clear requirement into the approved contract for execution. Two
internal steps — **define** (PRD, only at `spec` depth) and **design**
(`plan.md`, always) — closing with the **human approval gate**. End
state: `.ai/work/plan.md` (and `.ai/work/PRD.md` when depth demanded
it) exists, is grounded in the codebase, and the developer has
**explicitly approved** the design.

One plan per **change**, not per story: the unit of work is the
requirement that triaged into the chain, however many acceptance
criteria it carries. This phase writes no source code and no tasks —
`tasks` decomposes the approved design.

## Preconditions

- Triage has run (`references/triage.md`) and returned `design` or
  `spec` depth. If it returned `inline`, this work belongs to `fast`.
- No active `plan.md` in `.ai/work/`. If one exists, stop and ask:
  fold this into the active plan (via `fast`'s plan-adjustment path),
  finish and close the active work first, or explicitly park it.
  Never silently overwrite an active plan.
- Full context loaded (`SKILL.md § Context Loading`), including the
  landed requirement if `propose` ran in this conversation.

## Step 1 — define (PRD; `spec` depth only)

At `design` depth, **skip this step entirely** — no PRD, no
apologies; the plan's Objective section carries the why. At `spec`
depth:

1. **Survey the code the requirement touches.** Not everything — the
   modules, models, and endpoints the criteria will plausibly involve,
   plus their tests. The PRD's "what exists today" must be true.
2. **Detect gaps and contradictions** between the requirement and
   reality: assumed models/endpoints/integrations that don't exist
   (gaps — fine, name them), conflicts with an existing model, a
   standing `decision` concept, or the `scope` concept
   (contradictions — headline questions).
3. **Clarify before writing — questionnaire mode.** One topic per
   question; closed options where the answer space is closed. Loop
   until nothing is pending. Never emit `[NEEDS CLARIFICATION]` into
   the artifact.
4. **Choose the criteria prefix.** A short UPPERCASE token (≈3–6
   chars) derived from the requirement, confirmed with the developer,
   recorded in `PRD.md` frontmatter (`prefix:`). Check recent
   `.ai/memory/log/` entries for prefix collisions — criteria IDs are
   referenced from tasks and the final summary, so they must stay
   unambiguous.
5. **Write `.ai/work/PRD.md`** from `assets/prd-template.md`. One to
   two screens: problem, goals/non-goals, users, proposed solution,
   scope, assumptions, dependencies (one `reference` concept per
   external surface, cited as a link per **Citing the brain** below;
   an integration with no `reference` concept yet is flagged
   "NEW — to be added" for `jaiba-init:update-brain`, not linked),
   success metrics — and the
   **acceptance criteria schema**: every criterion `<PREFIX>-NNN`,
   Given/When/Then, happy and sad paths, inside the fenced `yaml`
   block exactly as the template shows. That block is a machine
   contract: `validate` (and the `verify` subagent) will parse it to
   check delivery criterion by criterion, so keep it well-formed YAML
   — prose goes in the PRD sections, not inside the schema.

   Criteria IDs are permanent: incrementing, never reused or
   renumbered. A criterion added later (including a **corrective**
   one surfaced during execution — a fix that turned out to be
   necessary for the PRD to hold) takes the next number and a
   `corrective: true` mark, so the PRD stays the single source of
   truth for everything it took to deliver.

## Step 2 — design (`plan.md`, always)

1. **Survey the code** (if define ran, you've already done most of
   this) and decide the *how*: approach, boundaries, integration
   points, what is explicitly out.
2. **Clarify remaining design-level questions** the same way — ask,
   resolve, then write.
3. **Write `.ai/work/plan.md`** from `assets/plan-template.md`:
   - **Objective** — what and why, 2–4 sentences. At `design` depth
     this section carries the whole motivation (perf target,
     breaking-changes summary of the bump, refactor rationale).
   - **Covered criteria** — the `<PREFIX>-NNN` IDs this plan
     delivers, when a PRD exists. "None — design depth" otherwise.
   - **Scope in/out**, **Technical approach** (cite the
     `architecture` and `convention` concepts, the `reference`
     concepts for external surfaces, and any knowledge skills),
     **Discrepancies vs PRD** (only if deviating from the approved
     PRD), **Sources consulted** — every brain citation in these
     sections written as a link per **Citing the brain** below.
4. **Respect sub-unit boundaries.** If the design crosses a boundary
   declared by a `sub-unit` concept, or touches a `reference` concept
   of `kind: internal-contract`, say so explicitly in the approach and
   link it — that's exactly what reviewers need to see.

## Citing the brain

`spec` is the phase that writes most of the executive artifacts'
references to long-term memory, so it owns the citation shape. Three
steps, in order:

1. **Resolve the concept, never a path.** Ask for the `type:` you need
   — `architecture`, `convention`, `quality-gate`, `scope`,
   `sub-unit`, `decision`, `reference` — and let the layout tell you
   where it lives, per the dual-resolution rule (`AGENTS.md` §1). In a
   **concept bundle** (`.ai/memory/index.md` present) `index.md` maps
   the `type:` to its file. In the **legacy flat layout**
   (`constitution.md`, no `index.md`) the same concept is the matching
   section of the flat file — `quality-gate` and `convention` are
   `constitution.md` §6 and §7–§8, a `decision` is an `adr-log.md`
   entry, a `reference` a `reference-index.md` row. Both layouts are
   supported; never assume the bundle exists.
2. **Write the citation as a file-relative markdown link**, resolved
   from the artifact that carries it. `.ai/work/` sits beside
   `.ai/memory/`, so the prefix is `../memory/`:
   - bundle — `[identity/architecture.md](../memory/identity/architecture.md)`,
     `[Stripe](../memory/references/stripe.md)`,
     `[ADR-004 event bus](../memory/decisions/004-event-bus.md)`;
   - legacy flat — `[constitution.md](../memory/constitution.md)`,
     `[Stripe (reference-index.md)](../memory/reference-index.md)`.
     The link still navigates; the section name belongs in the label,
     never in the target.
   Never a bare section citation (`constitution.md §6`), never an
   absolute or repo-rooted path. `plan-template.md § Sources
   consulted` shows the shape it expects.
3. **Verify the target exists before you emit the link.** A citation
   is a claim about the brain, and an unverified claim is the thing
   the next rule forbids.

### A citation that doesn't resolve is surfaced, never emitted

This carries the same weight as the `[MISSING]` discipline
(`AGENTS.md` §5.4), and binds both directions — writing a citation
here, in `tasks`, or in `summarize`, and reading one back in a later
phase or in `ask`.

**When a citation would point at a brain concept that does not exist —
wrong slug, wrong path, a `type:` never created, a flat file that isn't
there — stop and tell the human.** Name the artifact, the citation as
written, and the concept it fails to reach. Then, and only then:

- the concept exists under another name or path ⇒ fix the link and
  continue;
- the concept genuinely does not exist yet ⇒ leave `[MISSING] <what
  was needed>` in the artifact where the reviewer will see it, and
  route the gap to `jaiba-init:update-brain` — `spec` never invents a
  concept to satisfy its own citation;
- reading an artifact whose citation is already dead ⇒ same surface,
  before acting on anything that citation was supposed to ground.

Never silently emit a dead link, never silently substitute a plausible
path, never silently drop the citation to make the artifact look
clean. A dead citation the human cannot see is worse than a visible
gap, because the next reader trusts it.

## The approval gate

Stop. Present the design (and PRD, if produced) and ask for explicit
approval. The artifacts are drafts until the developer says
`"approved"` / `"go ahead"` / `"looks good"` — only then set
`status: approved` in the frontmatter. Do not transition into `tasks`.
Do not write source code. If the developer amends, apply and re-ask.

## Worked example (TripNest)

*"Let users co-edit itineraries with roles"* — triage: `spec` depth
(new capability, new actors).

1. Define: survey `Itinerary` (has `created_by`, no collaborator
   model); the `reference` concept for django-guardian resolves, so
   the PRD's Dependencies cite
   `[django-guardian](../memory/references/django-guardian.md)`. One
   clarification: "owner" maps to `created_by`? → yes, role concept.
   Prefix `ITIN`. PRD written; schema carries `ITIN-001`
   (invite by email, happy + already-invited/no-permission sad paths),
   `ITIN-002` (editor adds activity), `ITIN-003` (reader is
   read-only).
2. Design: plan.md — invitations + django-guardian object
   permissions, roles as `CharField` choices; out: real-time editing,
   conflict merge.
3. Gate: developer approves → next phase is `tasks`.

Counter-example: *"update requests to v5"* — triage: `design`. No
PRD; plan.md's Objective summarizes the breaking changes and the
migration shape; criteria section reads "None — design depth"; "done"
is the gate plus the stated scope.

## Common failure modes

- **Writing a PRD at design depth.** Triage decided; don't
  over-formalize a bump into user-story fiction.
- **Writing without surveying.** A PRD or plan that misstates what
  exists today poisons everything downstream.
- **Happy-path-only criteria.** No sad paths ⇒ no failure tests ⇒
  brittle delivery. Push for the edges.
- **Prose inside the criteria schema.** The `yaml` block is parsed by
  `validate`. Malformed YAML there breaks criterion-by-criterion
  verification.
- **Citing a concept you never resolved.** A plausible-looking
  `../memory/references/<guess>.md` is a dead link with good posture.
  Resolve, then link — and surface what doesn't resolve.
- **Citing by section number.** `constitution.md §6` is not an
  address; in a bundle it resolves to nothing at all.
- **Drifting into implementation detail in the PRD.** The PRD says
  *what* and *why*; schemas and libraries belong to the design;
  decomposition belongs to `tasks`.
- **Skipping the approval pause.** `spec` ends at "approved", not at
  "files written".
