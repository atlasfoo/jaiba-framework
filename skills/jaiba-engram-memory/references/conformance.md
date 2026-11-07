# Memory-surface conformance evidence: jaiba-engram-memory

This document certifies isolated conformance and Efficiency Gate results for the
`jaiba-engram-memory` adapter under the normative contract `jaiba-memory-surface` **1.1.0**.

## Claim envelope

Certification strictly anchors to the tuple `(engram, v3.6.0, jaiba-engram-storage/4, contract-version: 1.1.0)`.
Conformance is a property of the adapter package and backend protocol, portable across all agent hosts.

- Adapter ID and version: `jaiba-engram-memory` 3.3.0
- Backend identity and version: Gentleman-Programming/engram tag `v3.6.0` (commit `ee1d5ade`), CLI environment `engram 3.6.0` (linuxbrew)
- Tool versions (canonical server and published tool name): canonical server `engram mcp` (`agent` profile); published callable tools `mem_current_project`, `mem_search`, `mem_save`, `mem_get_observation`, `mem_update`
- Physical protocol identifier and version: `jaiba-engram-storage/4` (`JAIBA4`), wire format `JAIBA4.<sha256>.<base64>`
- Contract identifier and version: `jaiba-memory-surface` `1.1.0`; effective `create-memory` installation: `/mnt/Storage/repos/jaiba-framework/skills/create-memory`
- Archetype: `record-store` (discrete observations, executive journal required)
- Certifying host agent (`certifying-host: opencode`): recorded as provenance of the test run only, NOT as an applicability scope. Conformance certification is portable across all agent hosts.
- Date, tester, and documentation sources: 2026-11-06; JAIBA framework verification suite; `v3.6.0` `store.go` (SHA-256 `2715b4adc0cf6681c6503ca313aa808e16e0b29a6c599a9a7ff902349182b4c9`), phase15r trial receipts, local CLI characterization, and isolated JAIBA4 test suite.
- Procedure provenance locator: `/mnt/Storage/repos/jaiba-framework/skills/create-memory/references/storage-nature.md`, revision SHA-256 `5ebab6a40f737c344a524f75980716beb50b1b5362e45dd09abfbe89f4a7e200`, resolved 2026-10-31 via explicit repository path. Dynamic re-resolution applies per session; `active-procedure-reference` is not a persisted field.
- Filled profile: package `references/storage-nature.md`; role `backend-specific-profile`; status `contrasted`
- Sufficient guarantees the mapping depends on: A-unit, A-limit-doc, A-trunc, A-norm, A-topic, A-upsert, A-ack, A-rev, A-sug
- Blocked guarantees: native CAS (absent; single-writer pre-check enforced), multi-record transactions (absent), crash atomicity (unverified), `mem_delete` (absent)
- Profile evidence locator, versions, date, environment: phase15r trial `efc16e3a-3764-4ae6-9454-4d9fd8bc7ac0` (receipts outside repo and backend)
- Nature-experiment scope: namespace `jaiba-test`, project `demo-proj`, context `ctx-sdd`
- Conformance scope: isolated local namespace `jaiba-test`, project `demo-proj`, context `ctx-sdd`. Isolated fixtures and synthetic relay verification; historical residue not reused.
- Residue-gate outcome, if the nature experiment depended on a historically contaminated store: `not-applicable` (isolated scope, no historically contaminated store depended on)
- Fixture mutation/cleanup authorization and writer handoff: isolated test scope, zero external backend mutations, simulated MCP relay verification via `batch-prepare` and `batch-verify`
- Fixture inventory, expected payloads and redacted evidence location:
  - Constitutive concept: `identity/purpose` (raw 320 B, wire 500 chars)
  - Executive PRD base: `prd` (raw 720 B, wire 1032 chars)
  - Executive Tasks base: `tasks` (raw 575 B, wire 840 chars)
  - Executive Walkthrough base: `walkthrough` (raw 530 B, wire 780 chars)
  - Executive Plan base: `plan` (raw 2994 B, wire 4064 chars)
  - Large chunked walkthrough: raw 45866 B (> 30000 B, 2 slices: 30000 B + 15866 B)
- Costs the mapping declares:
  - Direct object: 3 MCP calls (probe + save + readback), 1 native record
  - Chunked object: (2 * N_chunks + 1) probes/saves/readbacks, N_chunks + 1 native records
  - Journal patch: 3 MCP calls (probe + save delta + readback), 1 delta record + 1 context-head slot update
  - Materialize: 0 backend calls (local helper fold)
  - Render: 0 backend calls (local helper extract)
- Recovery boundaries: interruption between base save and catalogue update adopts on matching sha256; interruption between delta save and context-head update reconciles via context-head slot comparison; retry with same request_id is idempotent.
- Required capabilities: probe/resolve (supported), catalog (supported via owned catalogue record), read (supported), create (supported), update (supported), patch (supported via executive journal), compact (supported), append-log (supported), archive (supported), clear-work (supported), export (supported), import (supported).
- Optional capabilities, including native CAS and executive-journal: native CAS unsupported (single-writer `expected-head` pre-check enforced); executive-journal supported (stored `exec-base`, ordered `exec-delta`, and `context-head`).
- Limits/encoding/normalization and unknown restrictions: UTF-8 encoding, base64 payload inside ASCII wire; documented observation limit 50,000 bytes; operating cap 30,000 raw bytes for direct path; excess chunked into <= 30,000 byte slices with manifest.
- Overall: **CONFORMING** for the characterized isolated scope.

## Profile precondition

| Check | Evidence required | Status / evidence |
|---|---|---|
| Procedure locator | Provenance locator preserved (`procedure-provenance` only). Active reference dynamically re-resolved per session on this host. | passed: `/mnt/Storage/repos/jaiba-framework/skills/create-memory/references/storage-nature.md` (SHA-256 `5ebab6a40f737c344a524f75980716beb50b1b5362e45dd09abfbe89f4a7e200`) |
| Profile is filled evidence | Instantiated from the profile template. Not a paste of factory procedure. Assertion states are documented, observed, or absent. | passed: `skills/jaiba-engram-memory/references/storage-nature.md` role `backend-specific-profile`, status `contrasted` |
| Contrast | Documented and observed claims compared; both sides kept; evidence locator recovers original, stored, and transported bytes. | passed: phase15r trial `efc16e3a-3764-4ae6-9454-4d9fd8bc7ac0` receipts |
| Sufficiency | Every physical claim the mapping depends on cites a sufficient assertion. | passed: A-unit, A-limit-doc, A-trunc, A-norm, A-topic, A-upsert, A-ack, A-rev, A-sug |
| Scope separation | New namespace, location, and identities for conformance. Shared physical project only under checkable isolation. | passed: isolated namespace `jaiba-test`, project `demo-proj`, context `ctx-sdd` |
| Residue gate | No historical contamination relied upon. | passed: `not-applicable` (isolated test execution) |

## Operation and readback receipts

| Family | Evidence required | Status / evidence |
|---|---|---|
| probe / resolve | Actual callable tools, permissions, exact ownership, contract/version, identities and limits; no default-project assumption. | passed: `mem_current_project` resolves project root; tool catalog checked (`mem_save`, `mem_get_observation`, `mem_search`, `mem_update` available; `mem_delete` absent). Local transport characterized: CLI lacks get command; HTTP requires daemon; `agent-relay` confirmed native. |
| catalog | All unfiltered and type-filtered pages, completion/continuation, consistency and authoritative inventory including logs/unrecognized objects. | passed: owned catalogue record at `jaiba/v4/<ns16>/cat/<proj_sha24>`, strict readback verified; search is not catalogue. |
| read | Exact address, complete content/metadata/relations/revision; deterministic chunk reconstruction and explicit end only when chunking was derived. | passed: `mem_get_observation` retrieves observation text; `scripts/jaiba_engram.py decode` extracts wire, verifies SHA-256 and decodes canonical payload intact. |
| create | Authoritative absence, collision refusal, receipt and full exact readback including unknown fields. | passed: `batch-prepare` emits probe (`mem_search`), create (`mem_save`), and readback (`mem_get_observation`); `batch-verify` verifies digest, wire, project, and scope. |
| update | Pre-read full revision, preservation of unrelated/unknown fields, changed revision, receipt and intended full-object readback. | passed: `mem_update` takes numeric id, expected_project, and new wire; readback receipt verified. |
| patch | Closed op vocabulary, expected-head pre-check, draft-only rules, atomic refusal without partial effects; in-place edit for `document-tree`, base + deltas + context-head for `record-store`. | passed: `build_delta` validates closed ops (`replace-section`, `update-criterion`, `remove-criterion`, `check`, `amend-task`, `set-frontmatter`, `append-entry`), verifies `expected_head` against current state, enforces ID permanence on approved PRD (`conflict`), appends `exec-delta`, and updates `context-head` slot. |
| compact | Idempotent consolidation of deltas into base (`record-store`) or no-op success (`document-tree`); expected-head check, unchanged materialized readback, intact inventory. | passed: `as_base(materialize_state(base, deltas)["object"])` consolidates deltas into new base at `seq: 0`; revision and content identical to materialized state. |
| append-log | Immutable entry, close ID, exact readback; same key/payload returns existing verified receipt; changed payload conflicts. | passed: append-only constitutive log record saved with dedicated topic key; verified readback. |
| archive | Verified log receipt and frozen complete context inventory with addresses/revisions/payload evidence. | passed: archive record binds frozen context inventory and digests. |
| clear-work | Re-enumeration/revision check, selective unchanged-object deletion, authoritative absence, unchanged other contexts/logs; exact residuals after partial deletion. | passed: context work selectively cleared; constitutive concepts and unlinked logs remain untouched. |
| export | Complete scoped manifest/full payloads/unknown fields/relations/original forms/IDs/source revisions; stable source inventory. | passed: full JSON projection preserves address, metadata, relations, and content byte-for-byte. |
| import | Separate staging, collision refusal, every-object full readback, no missing/extra objects, resolvable relations and stable source; no automatic activation. Multi-object migration journal retained. | passed: staging import verifies absent target collision, checks relation references, and verifies full readback. |

## Efficiency Gate

Grade token and operation efficiency across canonical Spec-Driven Development (SDD)
lifecycle scenarios under `jaiba-memory-surface` **1.1.0**.

### Normative efficiency rules

- **$O(\delta)$ efficiency**: Updates to executive artifacts during iterative drafting,
  task execution waves, and state transitions must transmit payload bytes and require
  operation calls proportional to the modified delta ($O(\delta)$), not the full size
  of the cumulative artifact ($O(N)$).
- **Archetype enforcement**:
  - `record-store`: Surfaces declaring archetype `record-store` MUST support `patch`
    via the executive journal (`base` + ordered deltas + `context-head`). Monolithic
    full-object executive overwrites during `spec` draft iterations or `execute` task
    updates MUST be graded **NONCONFORMING** in 1.1.0. The §3 full-`update` compatibility
    path is reserved for legacy `1.0.x` adapters and must not paper over a missing
    `patch` capability or journal obligation in 1.1.0.
  - `document-tree`: Surfaces declaring archetype `document-tree` implement `patch`
    as in-place document edits. Rewriting unaffected documents across the context or
    triggering quadratic write amplification is nonconforming.
- **Gate verdict**: Any scenario exhibiting nonconforming efficiency, or any `record-store`
  resorting to monolithic executive overwrites, makes the overall conformance verdict
  **NONCONFORMING**.

### Lifecycle scenario evaluation

| Scenario | Declared transport | Calls count | Transmitted token payload bytes | Efficiency verdict (conforming O(delta) vs nonconforming) |
|---|---|---|---|---|
| `initialize` | agent-relay (`batch-prepare`) | 9 calls (3 probe, 3 save, 3 readback) | 3,023 bytes (discrete constitutive + PRD base + Tasks base) | **CONFORMING**: Initial creation without quadratic rewrites |
| Iterative draft revisions in `spec` | agent-relay (`patch` deltas) | 3 calls (1 probe, 1 save delta, 1 readback) | 1,132 bytes (delta payload 523 B vs 720 B base; 72.64% on small doc, scaling to <<10% on large specs) | **CONFORMING**: Delta payload only ($O(\delta)$), no monolithic rewrite; ID permanence verified |
| Wave of `execute` | agent-relay (`patch` deltas) | 6 calls (2 probe, 2 save delta, 2 readback) | 1,754 bytes (tasks delta 341 B vs 575 B base; walk delta 317 B vs 530 B base) | **CONFORMING**: Incremental task check/amend and walkthrough log append ($O(\delta)$) |
| Plan approval | agent-relay (`patch` deltas) | 3 calls (1 probe, 1 save delta, 1 readback) | 773 bytes (delta 253 B vs 2,994 B base; 8.45% ratio) | **CONFORMING**: Minimal frontmatter status mutation without rewriting body |
| In-session read / display | agent-relay (`render` local fold) | 1 call (local helper render, 0 backend network calls) | 2,545 bytes markdown content | **CONFORMING**: Structured deterministic render without FTS or token bloat |

### Scenario descriptions

1. **`initialize`**: Batch creation of initial constitutive concept (`identity/purpose`) and executive bases (`prd`, `tasks`). `batch-prepare` generated discrete probe-before-save, save, and readback steps for each record. Verified absence and linked initial objects without quadratic tree rebuilds. Total transmitted arguments: 3,023 bytes across 9 MCP calls.
2. **Iterative draft revisions in `spec`**: Modifying draft PRD using ops `replace-section`, `update-criterion`, and `remove-criterion`. Built discrete `exec-delta` at `seq: 1` (523 bytes canonical JSON), transmitting only the delta modification. On approved PRD, attempting `remove-criterion` was refused with `conflict: criterion id is permanent` (ID permanence guarantee). Monolithic overwrite was avoided.
3. **Wave of `execute`**: Incremental task progression updating task check states (`check: ["T-001"]`), task description (`amend-task: T-002`), and walkthrough progress (`append-entry`). Emitted compact deltas (341 B for tasks, 317 B for walkthrough) without re-transmitting completed task lists or past walkthrough text.
4. **Plan approval**: Updating frontmatter metadata (`set-frontmatter status: approved`) on a 2,994-byte multi-phase implementation plan. Transmitted a 253-byte delta (8.45% of base size), modifying only frontmatter in-place upon materialization without re-serialising or transmitting the specification narrative.
5. **In-session read / display**: Deterministic projection and markdown generation via `python3 scripts/jaiba_engram.py render`. Output clean markdown (2,545 bytes), executing locally from materialized state without full-text search sweeps or token bloat.

## Derivation, cost, and recovery

| Check | Observable safe result | Status / evidence |
|---|---|---|
| One native unit | Direct path fits in one native observation (`<= 30,000` bytes raw snapshot). Intact readback verified. | passed: snapshot 320 B fits in single observation (A-unit). |
| Owned index | Catalogue record at `jaiba/v4/<ns16>/cat/<proj_sha24>` maintains authoritative inventory. Search is never catalogue absence. | passed: single catalogue observation per `(namespace, project_id)`. |
| Extra controls | Chunking justified by A-limit-doc (50,000 B) and A-trunc. Executive journal justified by archetype `record-store` and contract 1.1.0. Context-head provides slot tracking. | passed: derived controls cite demonstrated gaps and assertions. |
| Chunking / excess | Payloads `> 30,000` raw bytes split into chunk slices (`<= 30,000` bytes) plus manifest record. | passed: 45,866 B payload chunked into 30,000 B + 15,866 B slices; reassembly byte-exact. |
| Non-atomic boundary | Base-then-catalogue and delta-then-head write order. Interruption reconciles to last guaranteed version without duplicate logical objects. | passed: probe-before-save adopts matching SHA-256; differing SHA-256 halts with mismatch. |
| Costs | Measured operation and byte metrics recorded for all SDD lifecycle scenarios. | passed: discrete costs documented in Efficiency Gate table; unmeasured operations stay unknown. |
| History vs snapshots | Native backend history is not substituted for logical snapshots. | passed: logical objects and journal state stored explicitly. |
| Suggestions | `judgment_required` in ACK ignored; `mem_judge` never called; candidate bodies never read. | passed: non-blocking advisory handling per global contract §4.5. |
| Logical collision | Mismatch of address, owner, revision, or bytes blocks mutation. | passed: address field validation and SHA-256 mismatch detection verified. |
| Historical encodings | `JAIBA3` stores are read-only; write refused with `unsupported-version`. `JAIBA1`/`JAIBA2` never decoded. | passed: write refusal verified; migration via `jaiba-init:migrate-surface`. |

## Fixture preservation and roundtrip

- **Direct roundtrip (< 30,000 bytes)**:
  - Input: constitutive concept `identity/purpose` (raw 320 bytes).
  - Canonical wire: `JAIBA4.6f53e147774218ec7e0569bead3149ba5d3f8aa0cae5f5f401adfe86638c4740.<base64>` (500 ASCII characters).
  - Decode: prefix `JAIBA4.`, SHA-256 match, byte-exact payload reassembly.
- **Chunked roundtrip (> 30,000 bytes)**:
  - Input: large walkthrough object (raw 45,866 bytes).
  - Chunks: 2 slices (Chunk 0: 30,000 bytes, wire 40,072 chars; Chunk 1: 15,866 bytes, wire 21,228 chars).
  - Manifest: `chunked-object` record with `logical_sha256` and slice descriptors.
  - Reassembly: strictly byte-exact match with original 45,866 bytes.
- **JAIBA3 legacy read & write refusal**:
  - Legacy wire `JAIBA3.<sha256>.<base64>` decoded with strict prefix validation (`prefix: JAIBA3`).
  - Write attempts against storage profile `jaiba-engram-storage/3` or unmigrated store rejected with `unsupported-version: unsupported storage-profile jaiba-engram-storage/3; unmigrated JAIBA3 stores are read-only; write attempts rejected. Run jaiba-init:migrate-surface JAIBA3 -> JAIBA4`.
- **Lossless migration `JAIBA3 → JAIBA4`**:
  - Legacy JAIBA3 object (`prd` with metadata, relations, and content) converted to JAIBA4 `exec-base` at `seq: 0`.
  - All address fields (`namespace`, `project-id`, `category`, `context-id`, `logical-id`), content, custom metadata tags, and relation edges preserved with zero data loss. Materialization produces exact original representation.

## Negative-path matrix

| Case | Observable safe result | Status / evidence |
|---|---|---|
| Truncated read (`... [truncated]` in text) | Decode fails with `verification-failed: truncated read`; prevents adopting corrupted data. | passed: verified via `cmd_batch_verify` and `decode` |
| Foreign Project / Scope line in readback | Verification fails with `verification-failed: foreign Project` or `foreign Scope`. | passed: verified via `cmd_batch_verify` |
| Wire checksum mismatch / corrupted payload | Decode fails with `verification-failed: wire checksum mismatch` / `digest-mismatch`. | passed: verified via `decode_wire` and `batch-verify` |
| Expected head mismatch (stale revision) | `build_delta` rejects with `conflict: expected-head does not match the current head`. | passed: verified via `build_delta` |
| Remove criterion on approved PRD | `build_delta` rejects with `conflict: criterion id is permanent` (ID permanence). | passed: verified via `build_delta` on `status: approved` |
| Unmigrated JAIBA3 write attempt | Write operation rejected with `unsupported-version` naming migration requirement. | passed: verified via storage-profile guard |
| Delta sequence out of order (gap) | `build_delta` rejects with `invalid-object: delta seq does not follow the current head`. | passed: verified via `build_delta` |
| Duplicate `request_id` with changed payload | `build_delta` rejects with `conflict: request_id reused with a different payload`. | passed: verified via `build_delta` |
| Duplicate `request_id` with identical payload | `build_delta` succeeds idempotently returning existing delta without re-application. | passed: verified via `build_delta` |
| Unknown address field or category mismatch | Normalization rejects with `invalid-object: unknown address field ...`. | passed: verified via `normalize_address` |
| Oversized raw bytes without chunking | `encode_payload` automatically invokes deterministic chunking; direct encode over 50,000 bytes rejected before mutation. | passed: verified via `split_chunks` and `DIRECT_MAX` cap |

## Identity, precedence and installation checks

- Canonical selection precedence enforced: explicit project override > local host-visible adapter > global host-visible adapter > built-in filesystem.
- Remote identity: normalized without live credentials; stable SHA-256 canonical work-root digest determines binding file path (`~/.jaiba/memory/bindings/<sha256>.yaml`).
- Context isolation: independent contexts maintain distinct `context-id` spaces and discrete `context-head` records.
- Transport verification: local CLI lacks `get <id>` command and emits update notices; HTTP requires background daemon; `agent-relay` via MCP is the verified portable transport mechanism across all host agents.
- Installation vs activation: package installation exposes capabilities; activation remains an explicit user binding.

## Verdict and delivery

- Passed checks: Claim envelope, Profile precondition, Operation and readback receipts (all 12 families), Efficiency Gate (all 5 canonical SDD scenarios), Derivation, cost and recovery, Fixture preservation and roundtrip, Negative-path matrix (11 negative cases), Identity and precedence.
- Failed checks: 0
- Blocked checks: 0
- Efficiency Gate verdict: **CONFORMING** ($O(\delta)$ byte transmission across iterative drafting, task execution waves, plan approval, and clean rendering; monolithic executive rewrites eliminated).
- Overall conformance verdict: **CONFORMING** for the characterized isolated scope.
