# Historical surface consumer rehearsal evidence (T-021)

## What was actually exercised

The historical executor model read the shipped sources recorded in the
immutable source profile, then performed a bounded **executor-as-consumer
synthetic rehearsal** of conduct's six phases,
ask and fast. Developer turns and approvals in the recordings are scripted
fixtures, not human approval of any real project artifact. The current user's
approval authorized T-021 and scratch evaluation only.

Original scratch index: `fixtures/surface-rehearsal/index.json`.
Recorded follow-up: `/tmp/opencode/jaiba-memory-surfaces/phase4-t021/model-SBRbQzcS`.
The initial run and named dispatch attempts remain at `model-Ht4DnTfq` in the
same scratch parent. The follow-up tightened verified citations and stable
append request identity, reusing the observed host blocker, not new child access.
The three immutable recorded journals contain **592 events**: full logical input/output objects,
actual model-authored decisions, simulated transport requests/results, mutation
receipts, and real command results. Their source fingerprints describe the
sources observed at recording time; they do **not** assert those sources are
current. `fixtures/surface-rehearsal/reviewed-source-drift.json` records exact
recorded/current pairs for four reviewed later changes: filesystem mapping in
T-023 and recovery guidance in T-024, with the unchanged
source set, and immutable raw hashes for the index and all three journal files.
The source-profile hash is SHA-256 over canonical compact JSON encoding of the
decoded UTF-8 source text (the `surface_rehearsal.digest` convention); no
normalization is applied. Unknown future drift fails the freshness regression.

`capture_rehearsal.py` packages the actual journals losslessly as a
content-addressed DAG; `$blob` entries are references into `blobs`, not summaries
or truncated reads. `capture_rehearsal.load(path)` verifies and expands them.
Tests do not overwrite recordings. The recordings remain historical protocol
evidence. Recapture requires a new source-guided rehearsal; merely regenerating
expected results is not new model evidence. No fresh LLM run is claimed here.

| Workflow | Actual protocol/action evidence | Assertions |
|---|---|---|
| propose | Clarification and landed requirement; zero executive artifacts | `test_propose_and_refusal_have_zero_artifact_mutations` |
| spec | Spec-depth triage, full PRD + plan drafts, refusal, explicit synthetic revision approval + complete readbacks | `test_full_artifact_schemas_approval_and_gate_provenance` |
| tasks | Original GREET-001 happy/sad YAML fences (JSON inside), load/dependency/covers schema, full gate/convention read and copied command/address/revision, walkthrough | Same test; parsed with stdlib `json` |
| execute | Source-only low task; real named-tier dispatch refusal, inline fallback, actual source diff/test, divergent walkthrough readback stops checkbox/gate, explicit reconciliation | `test_execute_divergence_stops_before_gate_or_checkbox`, `test_actual_dispatch_failure_is_not_child_backend_evidence` |
| validate | Full source criteria + covers; real Plan gate; actual verify dispatch unavailable; separately injected actor permission-denied => not verifiable/no delivered write; restored permission + inline direct read/test => verified status update | `test_validate_failure_and_recovery_use_full_criteria_not_ack` |
| ask | Exact selected context + revisions, grounded answer, read-only trace; read failure reports failure, no other-context/path fallback | `test_ask_read_only_exact_context_and_failure_without_fallback` |
| fast | Actual private helper/test change, red/green tests, refusal => no executive writes; confirmation => conduct handoff, stale revision conflict, renewed approval preserves human annotation | `test_fast_actual_code_test_confirmation_handoff_conflict` |
| summarize | Presented English payload/inventory, refusal, confirmation, append/full-read/archive/clear; same-ID retry, different-payload conflict, changed inventory stops cleanup; other context/ordinary witness intact | `test_summarize_external_order_idempotency_and_isolation` |
| filesystem | Full executive bodies remain in `.ai/work/`, bundle index vs raw legacy documents retained without migration; real helper prepare, prepared-payload presentation/confirmation, archive and idempotent retry; `.gitignore` preserved | `test_filesystem_helper_keeps_both_layouts_full_artifacts_and_retry` |

All stages ran on **bundle, legacy and external** fixtures. External used no
local `.ai/` or `AGENTS.md` marker, no path archive command and no mirror. The
generic fake vault records the complete address tuple, ownership, unknown
metadata, relations, full bodies, revisions, paginated catalogues, context and
receipts. It is deliberately a **bounded simulated transport**, not a new
production JAIBA backend or a conforming selectable adapter. Export/import and
full adapter certification are not exercised.

## Actual child capability limit

Four real named dispatch attempts (`business-analyst`, `code-analyst`,
`executor-low`, `verify`) returned the host error:

> `Subagent depth limit reached (1). Increase "experimental.subagent_depth" to allow nested subagents.`

No child/job identity was returned and no child started or made partial writes.
The suggested host configuration change was **not** performed. Reports use
the documented role-local inline fallback, not a substituted generic agent.
The role-local permission fault is a **separate simulated actor operation**;
it is not described as an actual child's backend call. The original dispatch
attempts are in the invoking session's tool transcript; journal reports retain
their exact error, roles and state. The source-only executor needed no backend
access: **not required**, never inheritance verified.

Fresh child/backend inheritance remains untested here. Ordinary host Engram
bookkeeping is independent and provides **no** adapter evidence. No live
Engram assay, general model-compliance certification, Phase6 acceptance or
real PRD delivery is claimed. The simulated adapter is independent of Engram.

## Repeatable checks

From the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 skills/conduct/evals/test_workflow_rehearsal.py
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 skills/conduct/evals/test_surface_regressions.py
```

The first command checks historical source profiles against the reviewed drift
manifest (unchanged sources must still match; changed sources must match their
exact reviewed current hash) and replays the **recorded decisions/actions**,
without a runtime model API or fresh child dispatch. A static current-source
migration guard asserts the effective init staging/readback/approval/source
retention requirements and draft nonselectability; it is not behavior or adapter
conformance certification. Replays are not new LLM compliance evidence.
It prints its new exclusive scratch root and leaves evidence there. The
rehearsal uses the Python standard library only; fenced blocks are JSON.
No package install is performed. The earlier three primitive tests remain, honestly labeled as helper
and toy-store tests, not consumer evidence.

All fixture/test runtime writes are below
`/tmp/opencode/jaiba-memory-surfaces/phase4-t021/`; recorded fixture generation
is the sole explicit versioned output. No actual project `.ai/`/`.atl`, machine
binding, global install or production backend is written. Legacy eval IDs and
entries are retained; `filesystem_scoped_eval_ids` explicitly limits old path
expectations to filesystem and retains their selected supported layout.

## Reused helper evidence and caller audit

The previously independently passing **126 archive command assertions** at
`/tmp/opencode/jaiba-memory-surfaces/phase4-t018/run-xccxspv2` remain valid;
their source is `/tmp/opencode/jaiba-memory-surfaces/phase4-t018/test_archive.py`.
They cover interruptions, partial cleanup/retry, readback failure, changed
inventories, unexpected files/directories/symlinks, exact Unicode/space-bearing
identity, scope mismatch and safe rejection of old one-slug calls. T-021 did
not modify `archive.sh`, and did not repeat or rebrand those 126 assertions.
The new recordings add real helper calls with full workflow artifacts and
model presentation/confirmation decisions in each filesystem layout.

Read-only caller audit found no executable stale single-slug callers outside
evals. Current executable calls are the reviewed summarize prepare/archive
examples and eval harnesses, all with explicit project/context and filesystem +
serialization attestations. `create-memory/references/filesystem-surface.md`
and `interchange.md` still describe the helper's former narrower guarantees;
these are documentation reconciliation candidates outside T-021 ownership,
not permission to edit those files here.

## Barrier decision

At recording time, the temporary Phase3 consumer block had been removed from
the two contract copies while draft/nonconforming adapter restrictions and the
then-current migration barrier remained. Current migration guidance is now
defined by init's explicit `migrate-surface` procedure; historical recordings do
not exercise that procedure or authorize a populated-store switch, import,
merge or retirement.
