# Storage integrity: `jaiba-engram-storage/4` (`JAIBA4`)

Physical protocol of this adapter. Logical operations stay at contract
**1.1.0**. Archetype is `record-store`. Profile facts and thresholds:
[storage nature](storage-nature.md). Operation recipes, including `patch`
and `compact`: [Engram mapping](engram-mapping.md). The codec is
`scripts/jaiba_engram.py` (stdlib, `agent-relay`). It does not call Engram.
`evals/fixtures/run_jaiba3_static.py` still checks the legacy wire on
synthetic bytes; it is not a JAIBA4 trial and not backend evidence.

## 1. Snapshot and wire line

A record payload is JSON, serialized once as UTF-8. New payloads use
`json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)`.
**Stored bytes are retained** and never re-serialized for comparison.
`--raw` wraps retained bytes without parsing. The wire form is a single
ASCII line:

```text
JAIBA4.<sha256_hex>.<base64_rfc4648>
```

- `sha256_hex`: 64 lowercase hex digits over the raw payload bytes.
- `base64_rfc4648`: standard padded base64 of those bytes (single encoding,
  no nested Base64). It contains no `<`, `>`, whitespace, or newline.
- The observation `content` is exactly this line: immune to `TrimSpace`, to
  `<private>` → `[REDACTED]` replacement, to CRLF/Unicode changes, and to
  header framing differences (9 vs 10 line reads).

### Strict decode (`JAIBA4.`)

Fail closed on: edge or inner whitespace, `<` / `>` / `[REDACTED]`, a prefix
other than `JAIBA4.` (except the legacy read below), malformed digest,
invalid or non-canonical base64, sha256 mismatch, a `... [truncated]`
suffix, or `truncation.truncated == true` in the ACK/read. A successful
decode returns the exact payload bytes. It does not re-serialize them.

`JAIBA1.` and `JAIBA2.` are `unsupported-version`. Never decode them, never
relabel them, never migrate them.

### Legacy read-only decode (`JAIBA3.`)

`decode` also accepts exactly one `JAIBA3.` line under the same fail-closed
checks and reports prefix `JAIBA3`. That acceptance is a **read**. It is not
permission to relabel the line `JAIBA4.`, to adopt it as a JAIBA4 revision,
or to write. A read that contains both prefixes, or any `JAIBA` line that is
neither prefix, fails. See §8 for the store-level write refusal.

## 2. Record kinds

| Kind | Holds | Direct path |
|---|---|---|
| `object` | One logical object snapshot (address, revision, content, metadata, relations). Catalogue lists this kind, not the journal rows below. | raw `<= 30,000` bytes |
| `catalog` | Per `(namespace, project_id)`: identity, aliases, contexts, `close_index`, `entries` (`address` → `{obs_id, topic_key, state: live\|retired, revision, sha256}`). | always one observation |
| `chunk` | Immutable raw slice `<= 30,000` bytes of an oversized payload (wire of the slice, digest over the slice). | only when payload `> 30,000` |
| `chunked-object` | Manifest: `logical_sha256`, `logical_bytes`, ordered `chunks: [{index, obs_id, topic_key, bytes, sha256}]`. | only when chunked; the manifest itself must fit the direct cap |
| `exec-base` | Complete executive logical object used as the journal base (address, type, content, metadata, relations, `base_revision`). A monolithic object is an implicit base at `seq` 0. Not a catalogue type. | raw `<= 30,000`, else chunked |
| `exec-delta` | One accepted `patch`: target address, contiguous `seq` starting at 1, `request_id`, ops in order. Not a logical object. `catalog` does not list it. | one new record per patch; chunked only if that delta exceeds the cap |
| `context-head` | One record per executive context. Slots keyed by address hold `seq`, `chain_digest`, and the materialized logical revision. No full content, no other context. Not a logical object and not a second catalogue. | one observation; chunked only if the head record itself exceeds the cap |

There is no root, descriptor page, allocation page, or publication manifest.
Retired logical objects stay in `entries` as `retired`. Logical retirement
never needs physical delete. Retired deltas are excluded from
materialization; they are not history unless a separate history capability
is declared. This binding does not declare that.

## 3. Keys

Deterministic, `<= 60` characters (below Engram's silent 120-character cut).
`ns16` is 16 lowercase hex digits. Digests are SHA-256 hex; the key keeps a
prefix of that digest so the whole key fits.

| Kind | Key | Digest input |
|---|---|---|
| `cat` | `jaiba/v4/<ns16>/cat/<proj_sha24>` | UTF-8 project id, first 24 hex |
| `obj` | `jaiba/v4/<ns16>/obj/<addr_sha24>` | address canonical text, first 24 hex |
| `chk` | `jaiba/v4/<ns16>/chk/<ver_sha20>/<idx4>` | logical payload digest, first 20 hex, plus a 4-digit index |
| `ctx` | `jaiba/v4/<ns16>/ctx/<ctx_sha24>` | context canonical text, first 24 hex |
| `base` | `jaiba/v4/<ns16>/base/<addr_sha22>` | address canonical text, first 22 hex |
| `del` | `jaiba/v4/<ns16>/del/<addr_sha18>/<seq4>` | address canonical text, first 18 hex, plus a 4-digit `seq` (`1..9999`) |

Address canonical text (UTF-8, `\n` endings, one trailing newline), fields
escaped so each value is one line (`\` → `\\`, U+000A → `\n`, U+000D → `\r`):

```text
namespace <namespace>
project-id <project-id>
category <category>
context-id <context-id-or-empty>
logical-id <logical-id>
```

Context canonical text is `namespace`, `project-id`, and `context-id` in
that form. Constitutive addresses omit `context-id` in the logical address
but still emit an empty `context-id` line in this key input, matching the
helper. Do not invent a shorter digest. A key over 60 characters is
`limit-exceeded` before the write.

Legacy keys `jaiba/v3/<ns16>/{cat,obj,chk}/…` are readable under §8. New
writes do not use them.

## 4. Verified read

Every `mem_get_observation(id)` is verified before use:

1. Exactly one `JAIBA4.` or legacy `JAIBA3.` line, one `Project:` line, and
   one `Scope:` line.
2. `Project:` equals the bound backend project and `Scope:` equals `project`
   (the `id` read is not project-filtered; the outer `project` argument is
   request context only).
3. Decode per §1. A `JAIBA3.` prefix is a legacy read: do not relabel it and
   do not continue into a mutation (§8).
4. For a direct object, check the logical address in the snapshot against
   the catalogue entry. For a chunked object, concatenate slices in index
   order and compare each slice's `bytes`/`sha256` and the total
   `logical_bytes`/`logical_sha256`.
5. For an executive object, `read` is not the base alone. Load the
   `exec-base` (or the monolithic object as an implicit base at `seq` 0),
   the active `exec-delta` records in sequence order, and the `context-head`
   slot when one exists. Materialize with `scripts/jaiba_engram.py
   materialize`. The result must be one determined object. A gap, a
   duplicate `seq`, an address mismatch, an unapplicable op, or a head that
   disagrees with the chain so the object is not determined fails
   `invalid-object` and returns no object. Do not prefer the longer chain,
   the head, or the base.
6. Compare exact bytes with the retained snapshot for post-write readback.
   A journal readback compares the materialized object and the new head
   slot, not an acknowledgement.

A missing `context-head` slot on a readable base is the implicit head
(`seq` 0, chain digest of that base with an empty delta list). It does not
mean the object is absent. `catalog` does not list `exec-delta` or
`context-head`. A head slot whose address is not in the catalogue is an
inconsistent journal, not a catalogue entry to adopt.

`judgment_required` / `Suggestion:` lines, own or foreign, are advisory
metadata. They never enter verification, never block, and are never
answered with `mem_judge` / `mem_judge_many`. Candidates are not read.

Logical revision is the SHA-256 of the canonical projection of the
**materialized** logical object (address, type, content, metadata,
relations). `expected-head` is `seq` plus `chain_digest` of the journal
chain wrapper. They are not the same token. Compaction may change the head
and leave the logical revision unchanged.

## 5. Write order and reconciliation (single writer)

Constitutive creates, non-journal updates, and append-log still use the
object-then-catalogue order. `patch` and `compact` do not (§6).

1. Encode the snapshot with the helper (`encode`). Choose direct or chunked
   by the 30,000-byte threshold. New wires are `JAIBA4.` only.
2. Save or update the object (or chunks, then the chunked-object):
   - When the `obs_id` is already in the catalogue, use
     `mem_update(id, content, expected_project)` for in-place revisions.
   - For an object not yet in the catalogue, **probe the deterministic
     `topic_key` first** before `mem_save`. `mem_save` with an existing
     `topic_key` upserts in place (`A-upsert`); a blind save would overwrite
     an uncatalogued orphan without comparing bytes.
   - If an observation exists for the key: read it back, verify framing, and
     decode. Matching address and `sha256` adopts that `obs_id` without
     rewriting. A different digest, owner, address, or revision stops
     (`conflict`); never overwrite it.
   - If none exists, `mem_save` with `capture_prompt:false`, `type:"manual"`,
     `scope:"project"`, and the deterministic `topic_key`.
3. Read the observation back; verify (§4) and compare exact bytes.
4. Save or update the catalogue with the new entry; read back and verify.
5. Never call `mem_save` for narrative notes during surface operations.

`batch-prepare` emits those tool arguments and does not perform them. The
agent relays the calls. `batch-verify` compares the reads the agent
supplies. Bytes transit the model. That is `agent-relay`, not direct I/O.

Interruption points: after step 2 (orphan object), after step 3, after
step 4 (stale catalogue). Retry uses the same address and key. The pre-save
probe adopts a matching orphan and stops on a mismatch. A previous catalogue
version remains the last guaranteed state until step 4 verifies. No native
CAS is claimed.

## 6. Splicing: `patch` and `compact`

Both operations are executive-only, single-writer, and prepared by
`scripts/jaiba_engram.py`. `expected-head` (`seq` plus `chain_digest`) is a
pre-check. Comparing it is not CAS. A missing head field is
`invalid-object`. A well-formed head that does not match is `conflict`, and
nothing is written. Without the single-writer discipline, block mutation.

### `patch` — one delta and one head slot, O(delta)

1. Read the base and the active deltas; materialize. A missing head slot is
   `seq` 0, not `not-found`. An absent object is `not-found`. `patch` does
   not create.
2. `delta` validates the closed ops against the materialized object,
   including draft-only `update-criterion` and `remove-criterion`. A refusal
   writes nothing and has no partial op effects. The same `request_id` and
   the same canonical ops return the existing delta (idempotent). The same
   id with a different payload is `conflict`.
3. Persist **exactly one** new `exec-delta` at
   `jaiba/v4/<ns16>/del/<addr_sha18>/<seq4>` (`seq` = current + 1). If that
   record exceeds 30,000 raw bytes, chunk **the delta**, not the base.
4. Update that object's slot in the context `context-head`
   (`jaiba/v4/<ns16>/ctx/<ctx_sha24>`). The first patch may create the head
   record. Other slots are preserved. The project catalogue is not rewritten.
   Other contexts and other executive bodies are not rewritten.
5. Read both records back (§4) and materialize. The caller receives the
   materialized object, never the delta.

Cost is the delta record plus the head record, proportional to the patch,
not to the cumulative artifact. Two records are not one transaction. If the
delta is stored and the head update is unknown, stop. Reconcile by exact
reads. Do not append a second delta for the same `request_id`. If the head
and the chain cannot be materialized together, `read` fails
`invalid-object`; do not repair by dropping one of them.

Rewriting the base, or rewriting the catalogue, on every `patch` is
`update`, not this capability, and is nonconforming for this archetype.

### Deterministic materialization

`materialize` is a pure function of the current base and the active deltas
in sequence order (`seq` 1, 2, … with no gaps). Same inputs yield the same
canonical object and the same head. Ops splice; they do not reflow
Markdown, reorder unrelated YAML, or rewrite relations. `render` prints the
materialized `content` only. Callers that need the object use `materialize`,
not `render`.

Chain digest input is the executive-journal wrapper (`jaiba-journal-chain/1`,
base revision, then each delta's canonical form). The helper applies the
binding's SHA-256 fingerprint to that input. Do not shorten it. Logical
revision remains the fingerprint of the materialized object.

### `compact`

Optional. Never implied by `read` or `patch`.

- Pre-check `expected-head`. Mismatch is `conflict`; nothing is retired.
- No active deltas (`seq` 0, including an implicit base): success, **write
  nothing**, retire nothing, return the existing head.
- Otherwise the new base is the materialized object, byte for byte at the
  logical level (same metadata, content, relations, and logical revision).
  Write that base at the `base` key. Update the context-head slot to `seq`
  0 and the chain digest of that new base with an empty delta list. Retire
  the active deltas so a later `materialize` does not apply them. Retired
  deltas stay out of `catalog`.
- Read back the new base and the head. Logical revision is unchanged;
  `expected-head` is not. The caller must refresh the head.

`compact` is not archive and not `clear-work`. It does not append a log.

## 7. Closure, logs, and retirement

- `append-log`: immutable log object keyed by close ID. Probe that topic key
  before `mem_save`. Same close ID and same digest is idempotent. Same ID
  with a different payload stops before writing. Never blind-upsert a close
  ID. This path still updates the catalogue; it is not `patch`.
- `archive` then `clear-work`: verify the closing entry first. Enumerate the
  context's executive objects from the catalogue, recheck revisions, and
  bind each journaled object's base, active deltas, and the context
  `context-head`. Mark only that context's logical entries `retired`, retire
  the bound journal records with them, update the catalogue, and verify.
  Journal records are not unexpected objects to ignore and not extra types
  to catalogue. Other contexts, ordinary memory, and the verified
  constitutive log are untouched. If journal residuals cannot be enumerated,
  the outcome is `partial` or unknown; do not report a clean clear.

## 8. Legacy JAIBA3 stores

An unmigrated store is one whose binding says `jaiba-engram-storage/3`,
whose namespace is `jaiba/v3/<ns16>/`, or whose verified wires use the
`JAIBA3.` prefix.

- Reads use the legacy decode in §1. Report the prefix. Do not relabel.
- Any mutation — `create`, `update`, `append-log`, `patch`, `compact`,
  `clear-work`, or import into that store — is refused **before** encode or
  any `mem_save` / `mem_update`. The code is `unsupported-version`. The
  result requires explicit `jaiba-init:migrate-surface JAIBA3 → JAIBA4`.
- Do not write `JAIBA4.` bytes under a `jaiba/v3/` key. Do not rewrite a
  `JAIBA3.` line in place. A `JAIBA3.` line found under `jaiba/v4/` is not
  adopted and is not converted on read.
- Migration itself is the `jaiba-init` procedure, not a write this section
  authorizes. It copies retained snapshot bytes onto `jaiba/v4/<ns16>/…`
  as `JAIBA4.` wires, keeps history (close IDs and retired entries), and
  converts each monolithic executive object to an implicit `exec-base` at
  `seq` 0 with no invented deltas. The binding profile changes only at
  explicit activation. Until then the source stays read-only.

## 9. Limits

`MaxObservationLength = 50,000` is a documented limit, cited from the
nature profile, not re-probed. `30,000` raw bytes (about `40,072` wire
bytes for a `JAIBA4.` line: 7 + 64 + 1 + base64) is the chosen operating
cap. Direct records beyond the cap, and chunks beyond it, fail closed.
Never walk sizes upward to probe the limit. A delta or a head that exceeds
the cap is chunked as that record, or refused `limit-exceeded` if the
chunked-object manifest itself cannot fit. It is never a reason to rewrite
the executive base as a monolith.
