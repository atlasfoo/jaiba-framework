# Engram storage nature profile

Backend-specific filled profile (not the factory procedure) for the
`jaiba-engram-memory` adapter. Logical contract `jaiba-memory-surface`
**1.1.0**. Logical guarantees of 1.0.0 are unchanged
(`logical-guarantees-changed: no`). Archetype: `record-store`. Declared
physical protocol of this package: `jaiba-engram-storage/4` (`JAIBA4`).

The contrasted batch below observed `JAIBA3.` wires. Those rows are
historical evidence for the shared physical claims (one observation, one
wire line, truncation, topic cut, upsert, ack). They are not a JAIBA4
write trial and not a `patch` or `compact` trial. Do not relabel them.

`contrasted` means documentation and one finite verification batch were
compared. It is not conformance, not installation, and not activation.
No MEM criterion is declared delivered by this file. The chunk path
(`> 30,000` raw bytes) was subsequently exercised in the T-087 E2E trial
on the same JAIBA3 protocol.

```yaml
document-role: backend-specific-profile
profile-status: contrasted
contract-id: jaiba-memory-surface
contract-version: "1.1.0"
logical-guarantees-changed: no
archetype: record-store
procedure-provenance:
  locator: "/mnt/Storage/repos/jaiba-framework/skills/create-memory/references/storage-nature.md"
  revision: "SHA-256 5ebab6a40f737c344a524f75980716beb50b1b5362e45dd09abfbe89f4a7e200"
  resolved-at: "2026-10-31"
  method: "explicit current repository path"
```

`procedure-provenance` is generation-time history. It is not a
package-relative path, and it is not the procedure a later session must
open. This file does not persist `active-procedure-reference`. Each session
re-resolves the effective `create-memory` installation and reads that
installation's `references/storage-nature.md` before characterization or
re-derivation. It does not write the resolved path back into this profile,
the skill, the mapping, or the binding. A missing or ambiguous procedure
blocks re-derivation; it does not invite an invented profile, and it does
not block logical operations of an already-bound surface.

## Evidence

Durable raw evidence, outside this repository and outside Engram:

phase15r trial `efc16e3a-3764-4ae6-9454-4d9fd8bc7ac0`: `profiles/` for this contrasted batch, `e2e/` for the later T-087 chunk path.

That locator holds the predicted snapshots, native ACK/get text, and
byte comparisons in `receipts/`. It does not hold the specimen roots
`filesystem-root/` or `vault-root/`; those are separate local profiles
and do not certify Engram. It does not hold JAIBA4 wires.

Documentary source: Gentleman-Programming/engram tag `v3.6.0`
`internal/store/store.go`, fetched 2026-10-31, 539801 bytes, SHA-256
`2715b4adc0cf6681c6503ca313aa808e16e0b29a6c599a9a7ff902349182b4c9`.
That digest equals the phase14 capture of commit `ee1d5ade`. Local CLI
`engram 3.6.0` is environment identity only. Tool envelopes did not
name an MCP server version, so this file does not claim the running
server binary was hashed.

Effective `mem_*` schemas were inspected in this session on 2026-10-31
before any write. `mem_delete` was not in that callable catalog and is
not assumed.

Historical `#511`, `#519`, and `#520` were not re-read and were not
updated. The citation is the phase14 receipt files listed in
`receipts/historical-citation-manifest.json`. The 50001-byte probe was
not replayed.

## Assertions

| Id | Claim | Unit | State |
|---|---|---|---|
| A-unit | One observation held one `JAIBA3` line. Object `#533`, catalogue `#534`. | one native record | observed (this batch) |
| A-limit-doc | `MaxObservationLength = 50000`. `len(content)` is Go string bytes after `stripPrivateTags`, before the marker. | bytes | documented (`v3.6.0` `store.go`) |
| A-trunc | Over-limit content is cut to a UTF-8 prefix of at most 50000 bytes and the marker `... [truncated]` is appended, so the stored body can exceed 50000. `#520`: 50001 ASCII bytes submitted, retrieved body 50015, overflow byte absent. | bytes | documented; historical citation only. Not replayed. |
| A-norm | `stripPrivateTags` replaces `(?is)<private>…</private>` with `[REDACTED]`, then `strings.TrimSpace` on the whole string. `#511` call-3: edge whitespace removed, interior CRLF/Unicode kept. `#511` call-5: private block observed as redacted; exact transform not established. | content string | documented; historical citation only |
| A-topic | `normalizeTopicKey` trims, lowercases, collapses whitespace to `-`, and cuts at 120. This batch sent 54-character keys; both `Topic:` lines matched exactly. The 120 cut was not probed. | characters of the normalized Go string | documented; 54-character round-trip observed |
| A-upsert | Same project+scope+topic_key updates in place. Not re-tested this batch (two distinct keys). | native key | documented |
| A-ack | `mem_save` ACK omitted scope and topic_key. `mem_get_observation(id)` is not project-filtered and rendered exactly one `Project:` and one `Scope:` line on both gets. | lines | observed (this batch) |
| A-rev | `mem_update` schema requires `expected_project` (owner check). No revision parameter. `mem_update` was not called. | n/a | documented |
| A-cas / A-txn / A-delete | CAS, multi-record transactions, `mem_delete` | n/a | absent / not-assumed |
| A-sug | `judgment_required` is advisory. Object save: false. Catalogue save: true (`rel-9560fd440ac3ffcb`, candidate `#533` named in the ACK). The save still returned `#534` and the readback matched. `mem_judge` was not called. Candidates were not read. `#520`'s ACK also had `judgment_required` true and still returned an id; cited, not replayed. `#519` appears only as a candidate name in that historical ACK, not as a dedupe result. | ACK field | observed non-blocking on this catalogue save; not a lock |
| A-limit-sample | Wires of 612 and 780 ASCII characters, `truncated: false`, `limit_bytes: 50000`. | ACK `original_bytes` | observed sample, not a maximum |
| A-limit-cap | Direct path at most 30000 raw UTF-8 snapshot bytes. | raw snapshot bytes | choice, not a measured maximum |
| A-bytes | Object snapshot 403 bytes, SHA-256 `1a93f6f4f8bb53ee33fbd5b7862505cab401dc8e08d79fcc47c42cd68c2a1602`, exact match. Catalogue snapshot 531 bytes, SHA-256 `1da207848ab1b393f2fbf1335adf6a34c14a4efedd63774f9aaa676ec1c5690b`, exact match. The literal `<private>not-a-secret</private>` is inside the object snapshot JSON and absent from the wire. | raw UTF-8 snapshot bytes; wire ASCII characters | observed |

## Operating choices

- **Threshold:** direct path for logical snapshots `<= 30,000` raw UTF-8
  bytes. Above it, conditional chunking. A choice, not a measured maximum.
  This profile batch was the direct path only; the chunk path was subsequently
  exercised in T-087.
- **Index:** one owned catalogue observation per `(namespace, project_id)`,
  because native enumeration is unavailable. Full-text search is never the
  catalogue. That gap is an operating choice of this profile, not a new
  numbered observation beyond the batch that stored the catalogue as its
  own record (A-unit).
- **Cost, this batch:** 4 MCP calls for the write order (save object, get
  object, save catalogue, get catalogue), plus one prior `mem_current_project`.
  Object wire 612 ASCII characters; catalogue wire 780. Chunked objects
  were not measured in this profile batch (measured in T-087). Journal
  costs were not measured in this batch; unmeasured stays `unknown`.
- **Interruption and orphan protection:** object first, catalogue last. Both
  readbacks matched, so this batch did not stop between them. No second logical
  object was minted. Because A-upsert updates in place on topic_key matches,
  retries and uncatalogued creates probe topic_key before saving; matching
  sha256 adopts the orphan, while a differing digest stops with a mismatch
  rather than overwriting via upsert.

## Derived controls (JAIBA4)

Derivation uses the sufficient rows below plus contract **1.1.0** for
archetype `record-store`. These controls are not new observations from
phase15r. Each names the gap, the assertion it rests on, and the cost.
None is justified by the absence of CAS alone. The 30,000-byte cap remains
a chosen threshold (A-limit-cap), not a measured maximum; chunking still
cites the documented cut (A-limit-doc, A-trunc) and the verification gap
that a truncated or redacted body cannot be published intact (A-norm).

| Control | Gap | Realization | Cost |
|---|---|---|---|
| Owned catalogue | No native enumeration was available to the batch; search is not a catalogue (operating choice, resting on A-unit). | One `catalog` observation per `(namespace, project_id)`, key `jaiba/v4/<ns16>/cat/<proj_sha24>`. | One extra record and its readback on every catalogue mutation. Not atomic with the object write (A-cas / A-txn absent). |
| Chunk plus chunked-object | A-limit-doc / A-trunc: over-limit bodies are not published intact. A-limit-cap is the chosen direct threshold, not the gap by itself. | Payloads `> 30,000` raw bytes split into `chunk` slices plus one `chunked-object` manifest. JAIBA4 wires only. | One record per slice, plus the manifest. Unmeasured beyond the single T-087 sample. |
| Executive journal (`exec-base`, `exec-delta`) | Archetype `record-store` follows A-unit (discrete observations, not a document tree). Contract 1.1.0 then requires a stored journal. A full-object `update` is not `patch`. The classification is derivation, not a product-name guess and not a new probe. | `patch` appends one `exec-delta` (`jaiba/v4/<ns16>/del/…`). The base stays. A monolith is an implicit base at `seq` 0. Materialization is the helper, deterministic in the base plus ordered deltas. | O(delta): one delta record. Not measured in phase15r. |
| `context-head` | The journal pre-check needs one head per executive context without rewriting the project catalogue or other objects. | One `context-head` at `jaiba/v4/<ns16>/ctx/<sha24>`. A `patch` updates that object's slot only. A missing slot is `seq` 0, not absence. | One head record per patch, not one catalogue rewrite. Delta plus head is two records, not a transaction (A-txn absent). |
| Stdlib helper `scripts/jaiba_engram.py` | The only observed backend access is MCP. A-ack: save acknowledgements omit scope and topic key, so the agent must read back. Transport characterization probed alternatives: local CLI (`engram save`, `engram search`) lacks numeric observation retrieval (`engram get <id>` absent), emits update warnings to stdout/stderr, and lacks readback verification; HTTP (`engram serve`) requires a background daemon and port management. Therefore, MCP `agent-relay` is the verified, native transport mode where `batch-prepare` emits tool arguments and `batch-verify` verifies readback receipts. | Python 3 standard library only. Subcommands `encode`, `decode`, `delta`, `materialize`, `render`, `binding-path`, `cost`, `batch-prepare`, `batch-verify`. The script does not open the backend. `binding-path` prints a path and creates nothing. | Local process plus the MCP calls the agent relays. Bytes transit the model. `cost` leaves unmeasured byte counts `unknown`. |

Session re-resolution of the factory procedure can invalidate a derived
claim if the relevant procedure revision or contract version changed and
cannot be identified. It does not delete the observed rows above. It does
not authorize writing an active procedure path into this file.

## Sufficient and blocked

Sufficient for derivation: A-unit, A-limit-doc, A-trunc (as a documented
cut plus the historical `#520` citation, not as a new probe), A-norm
(documented plus the historical `#511` citation; this batch shows only
that the `JAIBA3` wire round-trips), A-topic (documented 120-character
cut; observed only for 54-character keys), A-upsert (documented only),
A-ack, A-rev (owner check only), A-sug (non-blocking on this save),
A-unit (discrete observation; the catalogue record is that unit).

The JAIBA4 wire prefix, `jaiba/v4/` keys, executive journal, context-head,
and helper are derived controls in the table above. They are not sufficient
observations. Depending on them as if phase15r had stored `JAIBA4.` lines
or executed `patch` is not allowed.

Blocked: crash atomicity, CAS, history substituting snapshots, journal
delta-plus-head atomicity, any JAIBA4 write measurement, and any claim
from historical `JAIBA1` / `JAIBA2`.

## Non-claims

- This profile is not conformance, installation, or activation.
- A passing sample is not a maximum; a readback is not crash atomicity.
- Search is not a complete catalogue; absent CAS is not distributed exclusion.
- Historical `JAIBA1` / `JAIBA2` records were not used as evidence or reinterpreted.
- The contrasted `JAIBA3.` wires were not relabeled `JAIBA4.` and were not migrated by this profile.
- `#511` / `#519` / `#520` were cited from local receipt files and were not re-read.
- Filesystem and vault profiles in the same evidence directory do not certify Engram.
- No MEM criterion is declared delivered here.
- `procedure-provenance` is not a live procedure pointer. There is no `active-procedure-reference` to follow.
