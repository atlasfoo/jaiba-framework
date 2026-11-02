# Engram mapping (JAIBA3)

Maps the logical surface (`jaiba-memory-surface` **1.0.0**) onto Engram's
existing MCP tools. Physical bytes, keys, verified reads and write order are in
[storage integrity](storage-integrity.md); profile facts in
[storage nature](storage-nature.md). This file is the tool mapping and the
per-operation recipes. Package status: `memory-surface`, conformance verified on
finite trial evidence (phase15r trial `efc16e3a-3764-4ae6-9454-4d9fd8bc7ac0`,
`profiles/` for T-086 and `e2e/` for T-087, outside this repository). This is not a claim of universal conformance across
all hosts or production scopes.

## Contents

1. Tool boundary
2. Ownership, binding and bootstrap
3. Catalogue, revisions and receipts
4. Operation recipes
5. Limits, failures and validation

## 1. Tool boundary

Inspect **this agent's** callable `mem_*` schemas on every host/version; parent
tools, documentation and `.atl` are not child capability evidence. Docs mention
an admin `mem_delete`: it is not assumed and never called.

| Callable | Use |
|---|---|
| `mem_current_project` | Optional `directory`/`cwd`; supply the work root. A candidate, not authorization. |
| `mem_save` | `title`, `content`, `project`, `scope:"project"`, `topic_key`, `type:"manual"`, `capture_prompt:false`. Topic saves are upserts; the ACK omits scope/topic_key; always read back by returned numeric `id`. `project_choice_reason`/`recovery_token` only for the server's real ambiguous-project flow after the human chooses. |
| `mem_get_observation` | Numeric `id`; not project-filtered. Verify `Project:`/`Scope:` on every read. `include_history` is not catalogue pagination. |
| `mem_update` | `id`, `expected_project`, full `content` replacement after pre-read; owner check is not revision CAS. |
| `mem_search`, `mem_context`, `mem_list_projects` | Discovery only; never the catalogue, never proof of absence. |

Never used by this adapter: `mem_judge`, `mem_judge_many`, `mem_compare`,
`mem_review`, passive capture, session/prompt bookkeeping, `mem_save` for
narrative notes, `all_projects:true` for resolution. Host bookkeeping stays
outside the reserved prefix.

## 2. Ownership, binding and bootstrap

Reserved prefix `jaiba/v3/<ns16>/` inside an **already authorized Engram
project**, always `scope: project`. `ns16` is a 16-hex token allocated once for
an exclusive namespace; ordinary memory stays outside it. Historical
`JAIBA1`/`JAIBA2` records, `jaiba-memory/v1/...` keys and protected resources
(`#420`, `477..485`, protected judgments) are excluded and never decoded.

The machine binding records: host agent, work root, adapter id/version,
`storage-profile: jaiba-engram-storage/3`, `ns16`, backend project, catalogue
locator (numeric observation id of the project catalogue), stable JAIBA
`project-id`, sanitized identity candidate and executive `context-id`. Backend
project labels are not the logical project id. Any other profile in the
binding blocks as `unsupported-version`; no sniffing, no fallback.

**Owned record predicate** after every id read: physical `Project`/`Scope` match
the binding; the decoded snapshot's kind, namespace, project id and (for objects)
logical address match what the catalogue promised. Similar titles, search hits or
a numeric id alone prove nothing. Mismatch means stop, never adopt.

**Catalogue acquisition (no search-based absence):**

1. Read the bound catalogue locator, verify per storage §4, check the declared
   project id. Changed, missing or inaccessible blocks reuse; no title lookup.
2. No locator: unresolved bootstrap, not `not-found`. Search may propose
   candidates for human confirmation only.
3. Only explicit authorization to provision a new exclusive namespace lets
   `jaiba-init` save the empty catalogue (key `jaiba/v3/<ns16>/cat/<sha24>`),
   read it back, then persist its locator by verified binding readback.

## 3. Catalogue, revisions and receipts

The catalogue (`kind: catalog`) holds identity, aliases, contexts, `close_index`
and `entries`. Complete enumeration = a verified read of the one catalogue plus
verified reads of listed objects; there is no pagination. Revisions are the
logical revision inside snapshots, incremented by this adapter under
single-writer discipline (no native CAS is claimed). A receipt records the
operation, address, new revision, observation ids, keys, byte lengths and
sha256 values, and the readback result.

Serialized writers: shared catalogue writes serialize even across independent
executive contexts. Uncontrolled concurrent writers block mutation.

## 4. Operation recipes

| Operation | Recipe |
|---|---|
| `probe` | Inspect schemas; `mem_current_project`; read-only. |
| `resolve` | Recompute selection (override, local, global, built-in filesystem); resolve identity via catalogue aliases; confirm context binding. A failed selected adapter never falls back or creates an empty brain. |
| `catalog` | Verified catalogue read; return entries for the exact address scope (live and retired states preserved). |
| `read` | Catalogue entry, then verified object (or chunked-object reassembly); exact full content, metadata, unknown fields and relations. |
| `create` | Absent from catalogue; probe deterministic topic_key before save to detect orphans from interrupted attempts; if orphan found, verify digest (match adopts, mismatch stops with conflict); only call mem_save if absent; then storage §5 order. |
| `update` | Pre-read, check expected revision, `mem_update(id, content, expected_project)`, readback, catalogue update. |
| `append-log` | Immutable log object keyed by close id; probe topic_key before save; readback existing to verify digest: idempotent on same digest, stops with conflict on different payload; never blind mem_save upsert. |
| `archive` | Verified closing entry first; no destructive step. |
| `clear-work` | After archive: frozen inventory of one context, revision recheck, mark only that context's entries `retired`, verify. |
| `export` / `import` | Neutral transfer per `create-memory` `interchange.md`; every object read verified; import never overwrites without explicit decision and never changes the source. |

`judgment_required` suggestions are logged as metadata in the receipt and
otherwise ignored.

## 5. Limits, failures and validation

Fail closed on: wrong `Project`/`Scope`, missing or duplicate wire/labels,
truncation, digest mismatch, foreign owner/address/revision, unsupported
profile, corrupt or missing chunk, unknown outcome of a write. An uncertain
write ACK gets one diagnosis and an id/digest-based reconcile; probe topic_key
before retry and never blind retry through `mem_save`.

Local validation: `python3 -B skills/jaiba-engram-memory/evals/fixtures/run_jaiba3_static.py <evidence-dir>`
checks wire, framing, truncation, censorship, chunk reassembly, ownership and
reconciliation on synthetic bytes. It is static and not operational conformance.
