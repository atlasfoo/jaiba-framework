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
   standing ADR, or the constitution's scope (contradictions —
   headline questions).
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
   scope, assumptions, dependencies (cite `reference-index.md`; flag
   NEW integrations for `update-brain`), success metrics — and the
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
   - **Scope in/out**, **Technical approach** (cite constitution,
     reference-index, knowledge skills), **Discrepancies vs PRD**
     (only if deviating from the approved PRD), **Sources consulted**.
4. **Respect sub-unit boundaries.** If the design crosses a boundary
   from constitution §5.1 or touches an internal cross-component
   contract (reference-index §3), say so explicitly in the approach —
   that's exactly what reviewers need to see.

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
   model), reference-index (django-guardian present). One
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
- **Drifting into implementation detail in the PRD.** The PRD says
  *what* and *why*; schemas and libraries belong to the design;
  decomposition belongs to `tasks`.
- **Skipping the approval pause.** `spec` ends at "approved", not at
  "files written".
