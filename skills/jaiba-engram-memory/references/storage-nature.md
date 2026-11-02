# Engram storage nature profile

Backend-specific filled profile (not the factory procedure) for the
`jaiba-engram-memory` adapter. Logical contract `jaiba-memory-surface`
**1.0.0**, unchanged. Physical protocol `jaiba-engram-storage/3` (`JAIBA3`).

`contrasted` means documentation and one finite verification batch were
compared. It is not conformance, not installation, and not activation.
No MEM criterion is declared delivered by this file. The chunk path
(`> 30,000` raw bytes) was subsequently exercised in the T-087 E2E trial.

```yaml
document-role: backend-specific-profile
profile-status: contrasted
contract-id: jaiba-memory-surface
contract-version: "1.0.0"
logical-guarantees-changed: no
factory-procedure-locator: "/mnt/Storage/repos/jaiba-framework/skills/create-memory/references/storage-nature.md"
factory-procedure-revision: "SHA-256 5ebab6a40f737c344a524f75980716beb50b1b5362e45dd09abfbe89f4a7e200"
factory-procedure-resolved-at: "2026-10-31"
factory-procedure-resolution-method: "explicit current repository path"
active-procedure-reference: "/mnt/Storage/repos/jaiba-framework/skills/create-memory/references/storage-nature.md"
```

## Evidence

Durable raw evidence, outside this repository and outside Engram:

phase15r trial `efc16e3a-3764-4ae6-9454-4d9fd8bc7ac0`: `profiles/` for this contrasted batch, `e2e/` for the later T-087 chunk path.

That locator holds the predicted snapshots, native ACK/get text, and
byte comparisons in `receipts/`. It does not hold the specimen roots
`filesystem-root/` or `vault-root/`; those are separate local profiles
and do not certify Engram.

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
  catalogue.
- **Cost, this batch:** 4 MCP calls for the write order (save object, get
  object, save catalogue, get catalogue), plus one prior `mem_current_project`.
  Object wire 612 ASCII characters; catalogue wire 780. Chunked objects
  were not measured in this profile batch (measured in T-087).
- **Interruption and orphan protection:** object first, catalogue last. Both
  readbacks matched, so this batch did not stop between them. No second logical
  object was minted. Because A-upsert updates in place on topic_key matches,
  retries and uncatalogued creates probe topic_key before saving; matching
  sha256 adopts the orphan, while a differing digest stops with a mismatch
  rather than overwriting via upsert.

## Sufficient and blocked

Sufficient for derivation: A-unit, A-limit-doc, A-trunc (as a documented
cut plus the historical `#520` citation, not as a new probe), A-norm
(documented plus the historical `#511` citation; this batch shows only
that the `JAIBA3` wire round-trips), A-topic (documented 120-character
cut; observed only for 54-character keys), A-upsert (documented only),
A-ack, A-rev (owner check only), A-sug (non-blocking on this save).

Blocked: crash atomicity, CAS, history substituting snapshots, and any claim
from historical `JAIBA1`/`JAIBA2`.

## Non-claims

- This profile is not conformance, installation, or activation.
- A passing sample is not a maximum; a readback is not crash atomicity.
- Search is not a complete catalogue; absent CAS is not distributed exclusion.
- Historical `JAIBA1`/`JAIBA2` records were not used as evidence or reinterpreted.
- `#511` / `#519` / `#520` were cited from local receipt files and were not re-read.
- Filesystem and vault profiles in the same evidence directory do not certify Engram.
- No MEM criterion is declared delivered here.
