# `conduct:spec`

Turn a clear requirement into the approved contract for execution. Two
internal steps — **define** (PRD, only at `spec` depth) and **design**
(`plan.md`, always) — closing with the **human approval gate**. End
state: the resolved executive context holds a full `plan` (and `prd`
when depth demanded it), grounded in the codebase, with the developer's
explicit approval persisted and verified by full readback. Names such as
`plan.md` below are logical artifact shorthand per `SKILL.md § Executive
addressing and persistence`, not unconditional local paths.

One plan per **change**, not per story: the unit of work is the
requirement that triaged into the chain, however many acceptance
criteria it carries. This phase writes no source code and no tasks —
`tasks` decomposes the approved design.

## Preconditions

- Triage has run (`references/triage.md`) and returned `design` or
  `spec` depth. If it returned `inline`, this work belongs to `fast`.
- No active `plan` in the selected context, established by complete
  catalogue/exact authoritative reads, not search or a local file check.
  If one exists, stop and ask:
  fold this into the active plan (via `fast`'s plan-adjustment path),
  finish and close the active work first, or explicitly park it.
  Never silently overwrite an active plan.
- Full context loaded (`SKILL.md § Context Loading`), including the
  landed requirement if `propose` ran in this conversation.
- Binding v2, required capabilities, declared `limits`, archetype, and
  single executive writer verified (`SKILL.md § Brain Discovery and
  Validation`). Apply `create` for a new base and `patch` for every later
  splice when `executive-journal` is realized; the `1.0.x` path is a full
  `update` with `efficiency-warning: full-update-without-patch`. Never
  upsert over existing work or write a local shadow of an external artifact.

## Analysis before either depth

Run `references/subagents.md § Pre-invocation toolchain check`, then
**dispatch `code-analyst` and `business-analyst`** for the requirement's
code survey and memory contrast at both `design` and `spec` depth. Launch
independent read-only work before awaiting either, within host capacity.
Reuse valid reports from `propose`; request scoped follow-ups for changed
requirements or stale facts. Consume both reports before writing artifacts,
resolve their contradictions, and record their provenance in Sources
consulted. Conduct retains routing, design judgment, and artifact writing;
it does not duplicate their full surveys. An actual blocked role uses the
same inline analysis with its named fallback reason recorded.

## Step 1 — define (PRD; `spec` depth only)

At `design` depth, **skip this step entirely** — no PRD, no
apologies; the plan's Objective section carries the why. At `spec`
depth:

1. **Consume the analyst reports.** The code survey covers modules,
   models, endpoints, and tests the criteria plausibly involve; the memory
   contrast covers scope, decisions, and integrations. Request targeted
   follow-ups for gaps. The PRD's "what exists today" must be true.
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
   constitutive `log-entry` objects for prefix collisions — criteria IDs are
   referenced from tasks and the final summary, so they must stay
   unambiguous.
5. **Create the context's `prd`** from `assets/prd-template.md`. This
   first write is `create` — the base, not a `patch`. Size it to the
   unchunked budget before that write (see **Limits and draft revisions**).
   One to two screens when the budget allows: problem, goals/non-goals,
   users, proposed solution,
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

When a native plan client applies, follow
`references/native-plan-client.md` before deciding the how.

1. **Use the current analyst reports** (shared with define when it ran)
   and decide the *how*: approach, boundaries, integration points, what
   is explicitly out. Request only the follow-ups needed to decide.
2. **Clarify remaining design-level questions** the same way — ask,
   resolve, then write.
3. **Create the context's `plan`** from `assets/plan-template.md`.
   Follow `references/ticket-link.md` when creating or amending. The
   first write is `create` (the base). Size it to the same unchunked
   budget. Later draft corrections are `patch`, not a second full write:
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

1. **Resolve the concept, never a guessed path or title.** Request the
   needed type (`architecture`, `convention`, `quality-gate`, `scope`,
   `sub-unit`, `decision`, `reference`) from the resolved constitutive
   catalogue, consume all pages, select its exact logical address and
   `render` it. Do not search to display or to verify a citation.
   Ambiguous matches require clarification. Analyst reports
   retain the scope, address and revision provenance of cited sources.
2. **Serialize a verifiable citation for the selected surface.**
   - **Filesystem only:** resolve bundle concepts through the index, or
     legacy concepts through the preserved flat document/entry mapping.
     Use file-relative Markdown from the artifact: e.g.
     `[Stripe](../memory/references/stripe.md)` in a bundle or
     `[Stripe (reference-index.md)](../memory/reference-index.md)` in
     legacy. Section names belong in labels, not guessed link targets.
     No absolute/repo-rooted path or bare section citation.
   - **External:** include the complete logical address (namespace,
     project ID, constitutive category, logical ID) and source revision
     in the citation/relations. A direct-read locator returned by the
     adapter may accompany it, but never invent a URI, use a bare record
     ID, or turn it into a `../memory/` link. Executive cross-references
     additionally identify the selected context ID. Preserve the surface's
     relation representation and unknown metadata for lossless round trips.
3. **Verify by exact full read before emitting.** A target's presence in
   search, an inaccessible object or truncated preview does not verify a
   citation. Report failures as failures, not missing concepts. The
   template's Sources consulted examples illustrate filesystem syntax;
   external citations use addresses without changing section/schema shape.

### A citation that doesn't resolve is surfaced, never emitted

This carries the same weight as the `[MISSING]` discipline
(`AGENTS.md` §5.4), and binds both directions — writing a citation
here, in `tasks`, or in `summarize`, and reading one back in a later
phase or in `ask`.

**When a citation would point at a brain concept that does not exist —
wrong logical ID, wrong scope, a `type:` never created, or (filesystem)
a flat file that isn't there — stop and tell the human.** Name the artifact, the citation as
written, and the concept it fails to reach. Then, and only then:

- the concept exists at a verified different locator ⇒ fix the citation and
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

## Limits and draft revisions

`MSV-017`. Before the first `create` of `prd` or `plan`, apply the limits
recorded at Brain Discovery. When lossless chunking is unsupported or
unverified, or the direct payload limit is the budget that applies, the
draft must fit that unchunked budget — documented maximum, or the
operating cap the binding already declares, each named with its unit.
Keep every required template section and, at spec depth, the fenced
criteria schema. Shrink prose and examples; do not drop the schema to
make the write fit. If the intended object would still exceed, stop with
`limit-exceeded` and do not mutate. Never truncate, summarize away a
field, or retry a smaller silent subset. Unknown limits are not a guessed
cap and not permission to truncate. Chunking that the binding declares
as lossless may carry an object above the direct unit; it does not waive
`limit-exceeded` when reassembly is unverified.

While materialized `status` is `draft`, iterative corrections are
`patch` ops, not a rewrite of the base:

| Change | Op |
|---|---|
| Prose section body | `replace-section` |
| New sibling section | `append-section` |
| Text added inside a section, including plan amendments | `append-to-section` |
| One frontmatter key other than reopening `status` | `set-frontmatter` |
| New criterion | `add-criterion` |
| Criterion body while still `draft` | `update-criterion` |
| Drop a criterion while still `draft` | `remove-criterion` |

Pass the `expected-head` from the last verified `render`. One request
is one delta on `record-store`, or one surgical document edit on
`document-tree`. Do not `update` the whole `prd` or `plan` when the
capability is realized. A refused op fails the whole patch; nothing is
partially applied.

On a `1.0.x` adapter, do not send `patch`. Apply those same ops locally,
enforce the same refusals, then `update` the complete object and record
`efficiency-warning: full-update-without-patch`. A 1.1 surface that
should realize `patch` and does not is `missing-capability`, not this path.

## The approval gate

Stop. Present the full design (and PRD, if produced) from a deterministic
`render`, identify their context/addresses, revisions, and heads, and ask
for explicit approval. They remain drafts until the developer says
`"approved"` / `"go ahead"` / `"looks good"`. Re-read and compare those
heads before `set-frontmatter` with `key: status` and `value: approved`
on each object being approved. That op preserves every other frontmatter
key and the body. Obtain the patch receipt and `render` each approved
object back; the materialized `status` must be `approved`. Approval is
persisted in the selected context, not merely a chat claim, local cache,
or backend tag detached from the artifact. A changed head, partial write,
or failed verification blocks handoff; reconcile and seek approval again
if the design changed. Do not transition into `tasks` in this phase or
write source code.

If the developer amends while `status` is still `draft`, apply the draft
ops above and re-ask. Once `status` is not `draft`, `remove-criterion`
and `update-criterion` are forbidden: a present ID fails `conflict`, and
a missing ID or unspliceable criteria block fails `invalid-object`. Do
not `set-frontmatter` `status` back to `draft` to reopen permanence —
that attempt is `conflict`. A corrective criterion after approval is
`add-criterion` with the next ID, not an edit of an existing one.
`replace-section` must not change criteria-fence bytes once frozen.

## Worked example (TripNest)

*"Let users co-edit itineraries with roles"* — triage: `spec` depth
(new capability, new actors).

1. Run the pre-invocation check and dispatch `code-analyst` and
   `business-analyst` concurrently. Consume both reports before
   defining or designing: the code report confirms `Itinerary` has
   `created_by` and no collaborator model; the memory report confirms
   the scope, decisions, and django-guardian reference. Record their
   provenance in Sources consulted.
2. Define (filesystem example): the `reference` concept for django-guardian resolves, so
   the PRD's Dependencies cite
   `[django-guardian](../memory/references/django-guardian.md)`. One
   clarification: "owner" maps to `created_by`? → yes, role concept.
   Prefix `ITIN`. PRD written; schema carries `ITIN-001`
   (invite by email, happy + already-invited/no-permission sad paths),
   `ITIN-002` (editor adds activity), `ITIN-003` (reader is
   read-only).
3. Design: plan.md — invitations + django-guardian object
   permissions, roles as `CharField` choices; out: real-time editing,
   conflict merge.
4. Gate: developer approves → next phase is `tasks`.

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
- **Rewriting `prd` or `plan` on every draft comment.** After the base
  exists, `replace-section` / criterion ops. A full `update` is the
  `1.0.x` warning path only.
- **Drafting past the declared limit, then truncating.** Size first.
  `limit-exceeded` stops the write.
- **Removing a criterion after approval.** Permanence already latched.
  `add-criterion` for a new ID, or stop and ask.
