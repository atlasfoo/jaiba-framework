# Engram mapping (contract 1.1.0, JAIBA4)

Maps the logical surface (`jaiba-memory-surface` **1.1.0**) onto Engram's
existing MCP tools. Archetype: `record-store`. Physical protocol:
`jaiba-engram-storage/4` (`JAIBA4`). Bytes, keys, verified reads, and write
order are in [storage integrity](storage-integrity.md); profile facts in
[storage nature](storage-nature.md). This file is the tool mapping and the
per-operation recipes.

Package status: `memory-surface`, conformance verified on finite trial
evidence for the physical properties the JAIBA3 trial measured (phase15r
`efc16e3a-3764-4ae6-9454-4d9fd8bc7ac0`, outside this repository). That trial
is not a JAIBA4 write trial and not a `patch` / `compact` trial. The journal
recipes below are the `record-store` realization. This is not a claim of
universal conformance across all hosts or production scopes.

Transport is **`agent-relay` only**. The stdlib helper
`scripts/jaiba_engram.py` (invoke `python3 -B scripts/jaiba_engram.py` from
the package directory) prepares payloads and canonical tool arguments, and
parses reads the agent obtained. It does not open Engram, spawn a backend
CLI, send HTTP, or write a binding file. Bytes transit the model. Do not
describe that as direct I/O.

## Contents

1. Tool boundary
2. Ownership, binding, and bootstrap
3. Catalogue, revisions, and receipts
4. Operation recipes
5. `patch` and `compact`
6. Unmigrated JAIBA3 stores and migration
7. Limits, failures, and validation

## 1. Tool boundary

Inspect **this agent's** callable `mem_*` schemas on every host/version.
Parent tools, documentation, and `.atl` are not child capability evidence.
`requires` declares `mcp:engram`, `python3`, and `git`. Published tool names
live in this mapping. Do not record a host-prefixed alias such as
`mcp__engram__mem_save` as a requirement. Docs mention an admin `mem_delete`:
it is not assumed and never called.

| Callable | Use |
|---|---|
| `mem_current_project` | Optional `directory`/`cwd`; supply the work root. A candidate, not authorization. |
| `mem_save` | `title`, `content`, `project`, `scope:"project"`, `topic_key`, `type:"manual"`, `capture_prompt:false`. Topic saves are upserts; the ACK omits scope/topic_key; always read back by returned numeric `id`. `project_choice_reason`/`recovery_token` only for the server's real ambiguous-project flow after the human chooses. |
| `mem_get_observation` | Numeric `id`; not project-filtered. Verify `Project:`/`Scope:` on every read. `include_history` is not catalogue pagination. |
| `mem_update` | `id`, `expected_project`, full `content` replacement after pre-read; owner check is not revision CAS. |
| `mem_search`, `mem_context`, `mem_list_projects` | Discovery only; never the catalogue, never proof of absence. A topic-key probe before save is a collision check, not absence proof. |

Helper subcommands, no aliases: `encode`, `decode`, `delta`, `materialize`,
`render`, `binding-path`, `cost`, `batch-prepare`, `batch-verify`. The first
seven never call the backend. `batch-prepare` emits `mem_search` /
`mem_save` / `mem_update` / `mem_get_observation` arguments.
`batch-verify` compares `{expected, observed}` and does not certify
conformance.

Never used by this adapter: `mem_judge`, `mem_judge_many`, `mem_compare`,
`mem_review`, passive capture, session/prompt bookkeeping, `mem_save` for
narrative notes, `all_projects:true` for resolution. Host bookkeeping stays
outside the reserved prefix.

## 2. Ownership, binding, and bootstrap

Reserved prefix `jaiba/v4/<ns16>/` inside an **already authorized Engram
project**, always `scope: project`. `ns16` is a 16-hex token allocated once
for an exclusive namespace; ordinary memory stays outside it. Keys: `cat`,
`obj`, `chk`, `ctx`, `base`, `del` as in storage integrity §3. Historical
`JAIBA1` / `JAIBA2` records, `jaiba-memory/v1/...` keys, and protected
resources (`#420`, `477..485`, protected judgments) are excluded and never
decoded. `jaiba/v3/<ns16>/` is the legacy read-only prefix (§6), not a
second writable namespace.

The machine binding is format `"2"` at
`~/.jaiba/memory/bindings/<sha256(canonical-work-root)>.yaml`. No
host-agent identity in the path or as a file key. `binding-path` prints
that path and creates nothing. The record holds: work root and its digest,
adapter id/version, `archetype: record-store`,
`storage-profile: jaiba-engram-storage/4`, namespace `jaiba/v4/<ns16>/`,
backend project, catalogue locator, stable JAIBA `project-id`, sanitized
identity candidate, and executive `context-id`. It does not hold
`active-procedure-reference`, an installation path, or payloads. Backend
project labels are not the logical project id.

A bound profile other than `jaiba-engram-storage/4` blocks mutation.
`jaiba-engram-storage/3` is the read-only legacy case in §6, still
`unsupported-version` for writes. Anything else is `unsupported-version`
with no sniffing and no fallback.

**Owned record predicate** after every id read: physical `Project` / `Scope`
match the binding; the decoded snapshot's kind, namespace, project id, and
(for objects) logical address match what the catalogue promised. Similar
titles, search hits, or a numeric id alone prove nothing. Mismatch means
stop, never adopt. A `JAIBA3.` prefix does not satisfy a JAIBA4 owned-write
predicate.

**Catalogue acquisition (no search-based absence):**

1. Read the bound catalogue locator, verify per storage §4, check the
   declared project id. Changed, missing, or inaccessible blocks reuse; no
   title lookup.
2. No locator: unresolved bootstrap, not `not-found`. Search may propose
   candidates for human confirmation only.
3. Only explicit authorization to provision a new exclusive namespace lets
   `jaiba-init` save the empty catalogue (key
   `jaiba/v4/<ns16>/cat/<sha24>`), read it back, then persist its locator
   by verified binding readback. Do not provision into `jaiba/v3/`.

## 3. Catalogue, revisions, and receipts

The catalogue (`kind: catalog`) holds identity, aliases, contexts,
`close_index`, and `entries`. Complete enumeration is a verified read of
that one catalogue plus verified reads of listed logical objects. There is
no pagination. `exec-delta` and `context-head` are not listed. A journaled
executive `read` still materializes base plus active deltas; catalogue
completeness is completeness of logical objects, not of journal bookkeeping.

Revisions are the logical revision inside the materialized snapshot,
incremented by this adapter under single-writer discipline (no native CAS
is claimed). `expected-head` is the journal pre-check (`seq` plus
`chain_digest`). Do not compare the two as one token. A receipt records the
operation, address, previous and resulting logical revision, observation
ids, keys, byte lengths, sha256 values, and the readback result. A `patch`
or `compact` receipt also records the previous and resulting head. Same
`request_id` and same canonical payload returns the existing verified
receipt and does not append a second delta.

Serialized writers: shared catalogue writes serialize even across
independent executive contexts. Uncontrolled concurrent writers block
mutation. Matching `expected-head` does not replace that discipline.

## 4. Operation recipes

On an unmigrated JAIBA3 store, `probe`, `resolve`, `catalog`, `read`, and
`export` may proceed as legacy reads (§6). Every mutation in this table is
refused before encode or any `mem_save` / `mem_update`.

| Operation | Recipe |
|---|---|
| `probe` | Inspect schemas; `mem_current_project`; helper `cost` is local. Read-only. |
| `resolve` | Recompute selection (override, local, global, built-in filesystem). Require profile `jaiba-engram-storage/4` to mutate. Resolve identity via catalogue aliases; confirm context binding. A failed selected adapter never falls back or creates an empty brain. |
| `catalog` | Verified catalogue read; return entries for the exact address scope (live and retired states preserved). Do not list deltas or the context head. |
| `read` | Catalogue entry, then verified object. Executive objects: load base and active deltas, `materialize`, return that object. A `JAIBA3.` prefix is a legacy read, not a write grant. |
| `create` | Absent from catalogue. `encode` a `JAIBA4.` payload. `batch-prepare` a save (probe, `mem_save`, readback) then the catalogue update. Matching orphan digest is adopted; a mismatch stops. |
| `update` | Pre-read, check expected logical revision, `batch-prepare` an update plus catalogue update, `batch-verify`. Not the journal path. Do not use this to simulate `patch`. |
| `append-log` | Immutable log object keyed by close id. Probe before save. Same digest is idempotent; a different payload conflicts. Never blind `mem_save` upsert. |
| `archive` | Verified closing entry first; no destructive step. Bind journal base, active deltas, and `context-head` into the frozen inventory. |
| `clear-work` | After archive: frozen inventory of one context, revision recheck, retire only that context's logical entries and their journal records, verify. |
| `export` / `import` | Neutral transfer per `create-memory` `interchange.md` on the **materialized** object. Journal lineage is optional metadata. Import of a monolith is an implicit base at `seq` 0. Import never overwrites without an explicit decision and never changes the source. |
| `patch` | §5. One `exec-delta` plus one context-head slot. |
| `compact` | §5. New base plus head when deltas exist; otherwise write nothing. |

`judgment_required` suggestions are logged as metadata in the receipt and
otherwise ignored.

## 5. `patch` and `compact`

Both use `scripts/jaiba_engram.py` in `agent-relay` mode. The agent runs
the helper locally, issues the emitted `mem_*` calls, and feeds the
observed reads back to `batch-verify`. The helper never performs those
calls. Stop before `delta` or `encode` when §6 applies.

Shared pre-read: catalogue entry, `exec-base` (or the monolithic object as
an implicit base), active `exec-delta` records in order, and the
`context-head` if a slot exists. Verify each read (storage §4). A missing
slot is `seq` 0, not absence. An absent logical object is `not-found`.

### `patch`

1. Build the `delta` request JSON: `base`, `deltas`, `ops`, `request_id`,
   `expected_head` (`seq` and `chain_digest`), `ns16`, and `context_head`
   when one was read. Archetype must be `record-store`.
2. Run `python3 -B scripts/jaiba_engram.py delta` on that JSON. Refusals
   are final: missing head is `invalid-object`; mismatched head, frozen
   criterion edit, or reused `request_id` with a different payload is
   `conflict`; nothing is written. `idempotent: true` returns the existing
   delta and does not append another. Do not call `mem_save` in that case.
3. On a new delta, `batch-prepare` a batch with `transport: agent-relay`,
   the bound `backend_project`, and `ns16`. Actions, in order:
   - `save` the `exec-delta` record (topic kind `del`, seq from the helper).
     The emitted steps probe the deterministic key, then `mem_save`, then
     `mem_get_observation`.
   - `update` the `context-head` when its observation id is known; `save`
     it only when this is the first slot and the probe finds no head.
     Topic kind `ctx`. One slot changes. Other slots are copied, not dropped.
4. Issue only those tool calls. Do not `mem_update` the base. Do not
   `mem_save` or `mem_update` the catalogue. Do not touch another context
   or another executive body.
5. `batch-verify` the readbacks against the helper's expected sha256 and
   wire. Then `materialize` and confirm the logical revision matches the
   receipt. The caller receives that object, not the delta.
6. `python3 -B scripts/jaiba_engram.py cost --operation patch` reports 2
   records and 5 calls for a direct delta. That is the helper's recipe
   figure, not a measured trial. The calls the agent issues are the
   `batch-prepare` steps: a save probes, an update does not. Pass `--bytes`
   and `--head-bytes` when they are known. Unmeasured transmitted bytes
   stay `unknown`. A delta over 30,000 raw bytes is the chunked delta
   path; it still does not rewrite the base. Two records are not one
   transaction. An unknown head write stops dependent work; reconcile by
   id and `request_id` before any retry.

O(delta) means the persisted payload is the delta plus the head record, not
a rewrite of the artifact. Grading a full-object executive overwrite as
`patch` is nonconforming.

### `compact`

1. Same pre-read. Run `materialize` on `{base, deltas}`. Compare the
   request `expected_head` to the materialized head before any encode.
   Mismatch is `conflict`; write nothing and retire nothing.
2. If `seq` is 0, return success with the existing head. Do not call
   `batch-prepare`. Do not retire anything. This includes an implicit base.
3. Otherwise encode the materialized object as an `exec-base`
   (`encode --topic-kind base --ns16 <ns16> --address <json>`). Run
   `materialize` again on that new base with `deltas: []` to obtain the
   post-compact head (`seq` 0, chain digest of the new base, logical
   revision unchanged). Upsert that slot into the context-head record
   locally; do not drop other slots.
4. `batch-prepare` two actions and no catalogue write: `update` the existing
   base observation in place (same observation id the catalogue already
   locates; a monolith already stored as that object is the implicit base
   and is updated in place, not copied to a second logical object), then
   `update` the context-head. Retire active delta observations so a later
   `materialize` does not apply them. Retirement is an adapter index fact,
   not a catalogue row and not `mem_delete`. If the base observation id is
   unknown, stop `invalid-object`; do not invent a second object and do not
   rewrite the catalogue to paper over it.
5. `batch-verify` both readbacks. Receipt: previous head, resulting head,
   unchanged logical revision, count of retired deltas. The caller must
   refresh `expected-head` even when `read` content is identical.
6. `cost --operation compact` reports 2 records and 4 calls when active
   deltas exist (update plus readback for base and head; no probe on the
   update path). A no-op reports the recipe note "writes nothing" and must
   not be billed as those writes. `compact` is not archive and is never
   implied by `read` or `patch`.

Same `request_id` rules as `patch` when the caller supplies one: same
payload is idempotent; a different payload conflicts. Do not compact
implicitly to make a retry look new.

## 6. Unmigrated JAIBA3 stores

A store is unmigrated when any of these hold: binding
`storage-profile: jaiba-engram-storage/3`, namespace `jaiba/v3/<ns16>/`,
or a verified wire prefix `JAIBA3.`.

- `decode` accepts the line and reports prefix `JAIBA3`. Never relabel it
  `JAIBA4`. `catalog` and `read` may return the recovered logical object.
- Any write attempt — `create`, `update`, `append-log`, `patch`, `compact`,
  `clear-work`, import into that store, `encode` aimed at a v3 key, or
  `batch-prepare` of a save/update — is refused **before** the helper emits
  a mutation and before `mem_save` / `mem_update`. Code:
  `unsupported-version`. Detail names the migration below. Do not dual-write
  JAIBA4 records into the v3 prefix.
- `JAIBA1.` and `JAIBA2.` stay undecoded. They are not a JAIBA3 store and
  not a migration source.

### Recipe: `jaiba-init:migrate-surface JAIBA3 → JAIBA4`

Not a helper subcommand and not an automatic side effect of `decode`.
Follow the effective `jaiba-init` `references/surface-migration.md`: one
transaction id, a journal outside both catalogues, writer pause, complete
inventories, staging, the verification barrier, and a separate activation
approval. This adapter's conversion, only inside the approved staging
target:

1. Read the source with legacy decode. Do not write `jaiba/v3/`. Source
   remains authoritative until `active-verified`.
2. Stage an exclusive namespace `jaiba/v4/<ns16>/`. Collisions are
   conflicts, not upserts. Leave the binding profile at
   `jaiba-engram-storage/3` until activation.
3. Copy each logical object by encoding the **retained** snapshot bytes as
   `JAIBA4.` (`encode --raw` when the bytes must not be re-serialized).
   Retain history: append-log close IDs, log payloads, and retired
   catalogue entries. Do not mint a second logical id.
4. Convert each monolithic executive object to an implicit base at
   **seq 0**: store it as `exec-base` under the `base` key, with no deltas.
   For each executive context receiving a converted base, create an initial
   `context-head` at `jaiba/v4/<ns16>/ctx/<ctx_sha24>` with a `seq: 0` slot
   whose chain digest is that base with an empty delta list, plus the
   materialized logical revision. Do not invent ops from git history, from
   Engram observation history, or from retired siblings. `read` of that
   base is the object. Logical revision is the fingerprint of that object.
5. After the barrier and a new explicit activation approval, switch the
   binding to `storage-profile: jaiba-engram-storage/4` and
   `namespace: jaiba/v4/<ns16>/`. Read the binding back. No dual-write.
   Source retirement is a later explicit decision, not this recipe's last
   step.

Until that activation, writers keep the §6 refusal.

## 7. Limits, failures, and validation

Fail closed on: wrong `Project` / `Scope`, missing or duplicate wire or
labels, truncation, digest mismatch, foreign owner/address/revision,
unsupported profile, corrupt or missing chunk, unknown outcome of a write,
head/chain disagreement, and a `JAIBA3` mutation. An uncertain write ACK
gets one diagnosis and an id/digest/`request_id` reconcile. Probe the topic
key before retry and never blind-retry through `mem_save`. A refused
`patch` has no partial op effects.

Local validation:

- `python3 -B skills/jaiba-engram-memory/evals/fixtures/run_jaiba3_static.py <evidence-dir>`
  checks the legacy wire, framing, truncation, censorship, chunk
  reassembly, ownership, and reconciliation on synthetic bytes. Static. Not
  operational conformance. Not a JAIBA4 trial.
- `python3 -B skills/jaiba-engram-memory/scripts/jaiba_engram.py` is the
  JAIBA4 codec. `encode` / `decode` / `delta` / `materialize` / `render` /
  `cost` are local. They do not certify a live Engram project.
