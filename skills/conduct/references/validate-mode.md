# `conduct:validate`

Prove the work is done — not "tasks checked" but *gate green and
acceptance criteria demonstrably met*. End state: the Plan gate has
passed, every criterion in the PRD schema is verified
delivered-or-not with evidence, criteria statuses are flipped, and
the work is cleared (or blocked) for `summarize`.

## Preconditions

1. `.ai/work/plan.md` exists and is approved.
2. Every task in `.ai/work/tasks.md` is checked. Unchecked tasks ⇒
   surface the gap and offer: finish them first, move them to a new
   plan, or drop them (recorded in the summary). Never silently
   validate incomplete work.

## Step 1 — the Plan gate

Run the **Plan gate** commands from `tasks.md § Gate Commands` — the
heavyweight tier: full test suite, coverage, build, security scan. It
runs **once**, here, not at phase boundaries.

**On failure:** list every failing check concisely and ask what
corrective action to take. Fixes route back to `execute` (as new
`T-NNN` tasks if non-trivial). The developer may explicitly waive a
check with a documented reason — waivers are recorded in the summary,
never assumed.

## Step 2 — criterion-by-criterion verification (spec depth)

If a `PRD.md` exists, parse its `criteria:` YAML block and verify
each criterion independently:

- **Primary path — the `verify` subagent.** Run the pre-invocation
  check from `references/subagents.md § Pre-invocation toolchain
  check` first: `verify` installed in the host's agents folder, its
  `requires:` tools present per `.atl/tool-layout.md`. Green ⇒ hand it
  the parsed schema, the `covers:` mapping from `tasks.md`, and the
  project's test/run commands (its input contract). It exercises each
  Given/When/Then — happy and sad — against the real behavior and
  returns a per-criterion verdict: **met / not met / not verifiable**,
  with evidence. Any gap in the check ⇒ surface it (name the missing
  agent or tool) and take the fallback — never let the gap emerge as a
  late failure.
- **Fallback — manual verification.** No subagent (or the check came
  up red) ⇒ do the same work yourself, criterion by criterion: locate the test(s) covering each
  Given/When/Then (the `covers:` fields in `tasks.md` say where to
  look) and/or exercise the behavior directly. Don't downgrade the
  standard because the tooling is absent — a criterion whose sad path
  you couldn't exercise is **not verifiable**, not "probably fine".

Report the verdict table to the developer. Then:

- **All met** → flip each criterion's `status: open` →
  `status: delivered` in the PRD schema. This is the only writer of
  that field.
- **Any not met** → back to `execute` with the gap named (usually new
  corrective tasks, sometimes a corrective criterion). Don't flip
  anything for partially delivered criteria.

At `design` depth (no PRD) this step reduces to: walk
`plan.md § Scope (In)` item by item and confirm each deliverable
exists and behaves; the gate plus that walk is the whole verdict.

## Step 3 — clear for close

When the gate is green and every criterion is delivered (or its
waiver documented):

> "Validation passed: gate green, N/N criteria delivered. Ready to
> close — shall I summarize and archive?"

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
  (`references/subagents.md`), never as a late failure. Fall back to
  manual.
- **Treating `verify`'s report as the flip.** The subagent reports;
  the developer sees the verdict table; only then does this phase
  flip `status: delivered` — and only for fully met criteria.
