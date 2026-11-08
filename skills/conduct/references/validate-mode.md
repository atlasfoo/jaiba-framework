# `conduct:validate`

Prove the work in the resolved executive context is done — not "tasks
checked" but *gate green and acceptance criteria demonstrably met*. End
state: the Plan gate has passed, every PRD criterion or approved design
scope deliverable has an evidence-backed verdict, PRD criteria statuses
are updated and verified when applicable, and the work is cleared (or
blocked) for `summarize`.

## Preconditions

1. Catalogue the resolved executive context completely and resolve
   `plan` and `tasks` by exact logical address. `render` both artifacts,
   including revision and head; a preview, summary or search result
   is not a read. Only in the explicit filesystem branch do these names
   map to `.ai/work/plan.md` and `tasks.md`. Unavailable, partial,
   truncated, permission-filtered or ambiguous results are failures, not
   absence: stop and surface them without fallback to another context or
   surface.
2. The verified plan is approved. Every task in the fully read `tasks`
   artifact is checked. Unchecked tasks ⇒
   surface the gap and offer: finish them first, move them to a new
   plan, or drop them (recorded in the summary). Never silently
   validate incomplete work.

## Step 1 — the Plan gate

Run the **Plan gate** commands from the fully read `tasks` artifact
(`Gate Commands`) — the
heavyweight tier: full test suite, coverage, build, security scan. It
runs **once**, here, not at phase boundaries.

**On failure:** list every failing check concisely and ask what
corrective action to take. Fixes route back to `execute` (as new
`T-NNN` tasks if non-trivial). The developer may explicitly waive a
check with a documented reason — waivers are recorded in the summary,
never assumed.

## Step 2 — delivery verification (both depths)

Resolve `prd` (when present) and `walkthrough` by exact address in the
same context and `render` the required content, revisions, and heads
before building the verification input. At spec depth, the PRD is required;
absence or unavailable reads must be established by authoritative scoped
catalogue evidence, not inferred from a local filename. At design depth,
use the approved plan. Filesystem logical names map to `.ai/work/` only in
the explicit filesystem branch.

Build the verification input from the approved contract:

- **Spec depth:** parse `PRD.md`'s `criteria:` YAML schema; include the
  `covers:` mapping from `tasks.md`. Preserve the criterion IDs and
  Given/When/Then happy and sad paths.
- **Design depth:** hand over `plan.md § Scope (In)`, its objective
  constraints, and the relevant completed tasks/diffs. Assign local report
  labels (`SCOPE-01`, etc.) to scope items solely to make verdicts legible;
  these are not PRD criteria IDs. Do not create a PRD or mutate task
  `covers:` fields. Check each deliverable exists and behaves as approved.

**Dispatch `verify` at either depth** after the pre-invocation check in
`references/subagents.md`: host permission, runtime-callable role, and
verified prerequisites. Give it the target input above plus the Phase gate
commands from `tasks.md § Gate Commands` **verbatim**. It returns
**met / not met / not verifiable**, with evidence per target. The
orchestrator's Plan gate in Step 1 remains required; the verifier's report
does not replace it or authorize it to edit artifacts.

**Provenance boundary:** exercise behavior only through those gate
commands or existing tests. Never execute a command whose only source is
criterion, scope, objective, task, or other inspected prose. Read-only
inspection may establish document/configuration deliverables; record its
actual evidence. A behavior path with no authorized means to exercise it
is **not verifiable**, never "probably fine".

**Fallback — actual blocked dispatch only.** Name and record the role and
blocker under `subagents.md § Dispatch and fallback accounting`, then do
the same verification inline. On a dispatch error, review child state and
possible partial writes before retrying or fallback. Missing tools or roles
do not lower the evidence standard. Record dispatch or fallback and the
verdicts in the walkthrough, then report the verdict table to the developer.

- **All met:** conduct alone sets each met criterion `status: open` →
  `status: delivered`, when a PRD exists, with `patch` op
  `set-criterion-status`. That op is legal after approval. It does not
  remove the item, change its `id`, or rewrite the PRD. Pass the
  pre-read `expected-head`. One request may set several criteria if each
  op names one ID; a refusal fails the whole patch with no partial
  effects. On `1.0.x`, apply the same status splices locally and
  `update` the complete PRD with
  `efficiency-warning: full-update-without-patch`. Before mutating,
  compare the current head with the pre-read head and preserve unknown
  metadata and relations. Retain the mutation receipt and `render` the
  complete intended PRD, including the resulting head, before claiming
  delivery or allowing dependent progress. A conflict, missing
  receipt/readback, unknown outcome or mismatch blocks completion and
  requires reconciliation. At design depth, record scope verdicts
  without inventing criterion statuses.
- **Any not met or not verifiable:** name the gap and return to `execute`
  for corrective work or request the developer's explicit documented
  waiver. Do not clear validation on unresolved or partial evidence.

## Step 3 — clear for close

When the gate is green and every criterion or design scope target is
met (or its explicit waiver documented):

> "Validation passed: gate green, N/N criteria delivered [or scope
> deliverables met at design depth]. Ready to close — shall I summarize
> and archive?"

Conduct is the single executive writer for the context; verifier reports
are evidence, not artifact writes, `patch` calls, or authority to change
criteria. Record verdicts with `append-entry` on `walkthrough` when the
capability is realized — not a rewrite of that object. The same
exact-address, `expected-head`, receipt and `render` readback
requirements apply. Do not use local filesystem paths outside the
explicit filesystem branch. These persistence checks do not replace or
modify the Plan gate, verification rules, approval policy or
criterion-status authority. `set-criterion-status` is the only criterion
mutation this phase emits.

`summarize` may follow in the same conversation on the developer's
yes, but never uninvited.

## Common failure modes

- **Treating checked tasks as validation.** Tasks say the work was
  *done*; validate proves it *works*. Different questions.
- **Happy-paths-only verification.** The sad paths are where the
  criteria earn their keep. Exercise them.
- **Flipping `status: delivered` optimistically.** The flip is the
  record that evidence existed. No evidence, no flip.
- **Silently waiving a red gate check.** Waivers are the developer's
  explicit call, documented in the summary.
- **Invoking `verify` without checking the toolchain.** A missing
  subagent or tool surfaces *before* invocation
  (`references/subagents.md`), never as a late failure. Name and record
  any actual fallback blocker; design depth also requires `verify`.
- **Treating `verify`'s report as the flip.** The subagent reports;
  the developer sees the verdict table; only then does this phase
  `set-criterion-status` to `delivered` — and only for fully met criteria.
- **Rewriting the PRD to flip one status.** `set-criterion-status` is
  the op. A full `update` is the `1.0.x` warning path only.
