# Engram storage nature profile

Backend-specific filled profile (not the factory procedure) for the
`jaiba-engram-memory` adapter. Logical contract `jaiba-memory-surface`
**1.0.0**, unchanged. Physical protocol `jaiba-engram-storage/3` (`JAIBA3`).

```yaml
document-role: backend-specific-profile
profile-status: incomplete   # documented + effects from upstream source; operational batch pending (T-086/T-087)
contract-id: jaiba-memory-surface
contract-version: "1.0.0"
logical-guarantees-changed: no
factory-procedure-locator: "<resolved effective create-memory installation>/references/storage-nature.md"
active-procedure-reference: null   # fill only after re-resolution on the current host
```

## Evidence

Upstream `gentleman-programming/engram` `internal/store/store.go` and
`internal/mcp/mcp.go` (main), read through Context7 on 2026-10-28, plus the
effective `mem_*` schemas of the host. Prior trial observations (#511,
#519, #520) are historical inputs to T-086, not evidence reused here.
Raw evidence for a contrasted profile lives outside the repository and
outside Engram (`~/.local/state/jaiba/trials/memory-surfaces/`).

## Assertions

| Id | Claim | State |
|---|---|---|
| A-unit | One observation = one native record (title, content, project, scope, topic_key, type). | documented |
| A-limit-doc | `content` limit `MaxObservationLength = 50,000` (bytes of the stored string; excess is cut with suffix `... [truncated]`). | documented |
| A-trunc | Over-limit saves truncate silently and flag `truncated`. | documented |
| A-norm | Content is trimmed (`TrimSpace`); `<private>…</private>` is replaced with `[REDACTED]`. | documented |
| A-topic | `topic_key` is normalized and cut at 120 chars; saves with the same project+scope+topic_key upsert. | documented |
| A-upsert | Topic saves are upserts, not exclusive create. | documented |
| A-enum | No native catalogue enumeration with completion; search is discovery only. | documented (schema) |
| A-rev | `mem_update(id, expected_project)` checks owner atomically; no revision CAS. | documented |
| A-cas / A-txn / A-delete | CAS, multi-record transactions, `mem_delete` | absent / not-assumed |
| A-ack | `mem_save` ACK omits scope and topic_key; `mem_get_observation(id)` is not project-filtered and renders `Project:` / `Scope:`. | documented |
| A-sug | Own and foreign `judgment_required` suggestions are native effects. | documented; advisory, not a lock |

## Operating choices

- **Threshold:** direct path for logical snapshots `<= 30,000` raw UTF-8
  bytes (wire about 40,072 bytes, under 80% of the documented limit plus
  header). Above it, conditional chunking. A choice, not a measured maximum.
- **Index:** one owned catalogue observation per `(namespace, project_id)`,
  because native enumeration is unavailable. Full-text search is never the
  catalogue.
- **Cost:** 4 MCP calls per write (save/update object, read object, save/update
  catalogue, read catalogue). Chunked objects add `K` save+read pairs.
- **Interruption:** object/chunks first, catalogue last; a crash leaves an
  orphan object (adopted by address on retry) or a stale catalogue (reconciled
  by readback). No second logical object is minted.

## Sufficient and blocked

Sufficient for derivation: A-unit, A-limit-doc, A-trunc, A-norm, A-topic,
A-upsert, A-ack, A-rev (owner check only). Blocked: crash atomicity, CAS,
history substituting snapshots, any claim from historical `JAIBA1`/`JAIBA2`.

## Non-claims

- This profile is not conformance, installation, or activation.
- A passing sample is not a maximum; a readback is not crash atomicity.
- Search is not a complete catalogue; absent CAS is not distributed exclusion.
- Historical `JAIBA1`/`JAIBA2` records were not used as evidence or reinterpreted.
