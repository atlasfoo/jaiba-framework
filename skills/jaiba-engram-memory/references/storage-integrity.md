# Storage integrity: `jaiba-engram-storage/3` (`JAIBA3`)

Physical protocol of this adapter. Logical operations and guarantees stay at
contract **1.0.0**. Profile facts and thresholds: [storage nature](storage-nature.md).
Operation recipes: [Engram mapping](engram-mapping.md). The local validator
`evals/fixtures/run_jaiba3_static.py` computes these rules on synthetic bytes;
it is not backend evidence.

## 1. Snapshot and wire line

A logical object revision is one JSON snapshot, serialized once as UTF-8 with
`json.dumps(obj, ensure_ascii=False, separators=(",", ":"))` (or any standard
serializer; the **stored bytes are retained**, never re-serialized for
comparison). Its wire form is a single ASCII line:

```text
JAIBA3.<sha256_hex>.<base64_rfc4648>
```

- `sha256_hex`: 64 lowercase hex digits over the raw snapshot bytes.
- `base64_rfc4648`: standard padded base64 of those bytes (single encoding, no
  nested Base64). It contains no `<`, `>`, whitespace or newline.
- The observation `content` is exactly this line: immune to `TrimSpace`, to
  `<private>` to `[REDACTED]` replacement, to CRLF/Unicode changes and to
  header framing differences (9 vs 10 line reads).

Decode fails closed on: edge or inner whitespace, `<`/`>`/`[REDACTED]`, a prefix
other than `JAIBA3.` (including `JAIBA1.`/`JAIBA2.`, never decoded or relabeled),
malformed digest, invalid or non-canonical base64, sha256 mismatch, a
`... [truncated]` suffix, or `truncation.truncated == true` in the ACK/read.

## 2. Record kinds

| Kind | Holds | Direct path |
|---|---|---|
| `object` | One logical object snapshot (address, revision, content, metadata, relations). | raw `<= 30,000` bytes |
| `catalog` | Per `(namespace, project_id)`: identity, aliases, contexts, `close_index`, `entries` (`address` -> `{obs_id, topic_key, state: live\|retired, revision, sha256}`). | always one observation |
| `chunk` | Immutable raw slice `<= 30,000` bytes of an oversized snapshot (wire of the slice itself, digest over the slice). | only when snapshot `> 30,000` |
| `chunked-object` | Main observation: `logical_sha256`, `logical_bytes`, ordered `chunks: [{index, obs_id, topic_key, bytes, sha256}]`. | only when chunked |

There is no root, journal, descriptor page, allocation page or publication
manifest. Retired objects stay in `entries` as `retired`; logical retirement
never needs physical delete.

## 3. Keys

Deterministic, `<= 60` characters (far below Engram's silent 120-char cut):

- `jaiba/v3/<ns16>/cat/<proj_sha24>`
- `jaiba/v3/<ns16>/obj/<addr_sha24>`
- `jaiba/v3/<ns16>/chk/<ver_sha20>/<idx4>`

`ns16` is the namespace token; `*_shaN` are the first N hex digits of SHA-256 over
the logical project id, the full logical address, or the logical snapshot digest.

## 4. Verified read

Every `mem_get_observation(id)` is verified before use:

1. Exactly one `JAIBA3.` line, one `Project:` line and one `Scope:` line.
2. `Project:` equals the bound backend project and `Scope:` equals `project`
   (the `id` read is not project-filtered; the outer `project` argument is
   request context only).
3. Decode per section 1; for objects, check the logical address in the snapshot
   against the catalogue entry; for chunked objects, concatenate slices in index
   order and compare each slice's `bytes`/`sha256` and the total
   `logical_bytes`/`logical_sha256`.
4. Compare exact bytes with the retained snapshot for post-write readback.

`judgment_required`/`Suggestion:` lines, own or foreign, are advisory metadata.
They never enter verification, never block, and are never answered with
`mem_judge`/`mem_judge_many`; candidates are not read.

## 5. Write order and reconciliation (single writer)

1. Encode the snapshot; choose direct or chunked by the 30,000-byte threshold.
2. Save/update object (or chunks, then chunked-object):
   - When the `obs_id` is already in the catalogue, use
     `mem_update(id, content, expected_project)` for in-place revisions.
   - For an object not yet in the catalogue (new create or retry of an
     interrupted attempt), **probe the deterministic `topic_key` first** (e.g.
     via `mem_search(topic_key)`) before calling `mem_save`. Because `mem_save`
     with an existing `topic_key` performs an in-place upsert (`A-upsert`),
     saving blindly would overwrite an uncatalogued orphan from an interrupted
     prior write without comparing bytes.
   - If an existing observation is found for the key: read it back
     (`mem_get_observation(id)`), verify framing and decode the snapshot. If
     its address and `sha256` match the intended payload, adopt the existing
     `obs_id` directly into the catalogue without rewriting. If the existing
     observation has a different digest, owner, address, or revision, stop
     immediately with a mismatch conflict (`mismatch-stop`); never overwrite it.
   - If no existing observation is found for that topic key, save using
     `mem_save` with `capture_prompt:false`, `type:"manual"`, `scope:"project"`
     and the deterministic `topic_key`.
3. Read the observation back; verify (section 4) and compare exact bytes.
4. Save/update catalogue with the new entry; read back and verify.
5. Never call `mem_save` for narrative notes during surface operations.

Interruption points: after 2 (orphan object), after 3, after 4 (stale catalogue).
Retry uses the same address and key. On retry, the pre-save probe finds the
orphan; if its address and sha256 match, it is adopted into the catalogue (no
second object and no upsert); a different owner, address, revision or digest stops
with a mismatch before any write. A previous catalogue version remains the last
guaranteed state until step 4 verifies.

## 6. Closure, logs and retirement

- `append-log`: immutable log object keyed by close ID. Before calling
  `mem_save`, probe the deterministic close ID topic key. If an observation
  already exists: read back and verify its digest. The same close ID and same
  digest is idempotent (returns existing observation ID); the same ID with a
  different payload stops with a conflict before writing. Never perform a blind
  `mem_save` upsert over an existing close ID.
- `archive` then `clear-work`: verify the closing entry first, enumerate the
  context's executive objects from the catalogue, recheck revisions, mark only
  that context's entries `retired`, update catalogue, verify. Other contexts and
  ordinary memory are untouched.

## 7. Limits

`MaxObservationLength = 50,000` is a documented limit; `30,000` raw / about
`40,072` wire bytes is the chosen threshold. Direct records beyond the threshold
and chunks beyond it fail closed. Never walk sizes upward to probe the limit.
