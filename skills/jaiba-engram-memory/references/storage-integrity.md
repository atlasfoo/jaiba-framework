# Storage integrity and publication

Declarative storage protocol **1**, adapter `jaiba-engram-memory` 3.2.0,
contract `jaiba-memory-surface` 1.0.0. Read `engram-mapping.md` for authority,
binding and ownership, and the effective `create-memory` contract/interchange
references for logical semantics. This reference specifies storage, not a new
runtime SDK, installation, migration implementation or activation permission.
It covers MEM-005, MEM-008 and MEM-011; **full conformance remains unverified**.
Scoped executed T009 evidence is recorded in §8; it does not certify all paths.

## 1. Evidence, prerequisites and measured bounds

Historical T007 discovery: on 2026-10-17 the implementing child independently
inspected all 19 callable
Engram schemas and called only
`mem_current_project({directory:"/mnt/Storage/repos/jaiba-framework"})`.
It returned `jaiba-framework`, `git_remote`, and that absolute project path.
No adapter record was read or mutated. Backend/version, actual response
framing, text transformations, visibility and all storage limits remain
unverified by that discovery. T009 owns authorized live checks; see §8 for the
subsequent scoped results. This refresh performs no backend operations.

The inspected schemas expose `mem_save` (topic upsert), ID-based
`mem_get_observation` and `mem_update` with required `expected_project`.
They expose neither create-if-absent, CAS, catalogue pagination nor locks.
`mem_get_observation.project` is response context, not ownership filtering.
`mem_update.expected_project` atomically guards the physical owner only;
it is not a namespace, revision or content guard. Search has max 20 results
and no enumeration cursor. History continuation is not catalogue continuation.

Before affected writes, an authorized disposable test scope must establish a
capability record bound to host, callable schema, backend identity/version if
available, adapter/encoding version and test date. Record separately:

| Quantity | Required evidence; never infer from another row |
|---|---|
| Observation content | Accepted and exactly retrieved wire bytes, characters and encoded request bytes; rejection/truncation boundaries if measured. |
| Request/response | Full request including JSON escaping/metadata and full retrieved response including server framing; client/tool display bounds too. |
| Control records | Largest verified envelope, descriptor, shard, manifest, root and journal; maximum tested entries/depth and complete multi-page traversal. |
| Routing/metadata | Actual key normalization, key/title lengths, project/scope reporting, field visibility and deduplication/upsert behavior. |
| Transformations | Exact comparison of punctuation, whitespace, CRLF/LF, trailing newlines, Unicode including combining forms/non-BMP, escaping, long repetitions and sensitive-pattern-like **synthetic** text. Never test with secrets. |
| Computation | Available encoder/decoder, strict JSON parser, SHA-256, byte counter, byte comparator and UUID generator; versions and deterministic test vectors. |

Measure both raw candidate text and this ASCII transport; a server may trim,
redact, normalize, deduplicate or truncate `mem_save` content. A reported
`50000` maximum, if encountered, is not a verified byte budget, character
budget or successful readback. No numeric safe threshold is prescribed here.
An observed successful size is a tested operating bound, not proof of the
server's absolute maximum. Choose conservative bounds no larger than tested
successful sizes for **each** request/response role and reject larger requests
before sending. Unknown hidden/blank bounds cannot become a success flag.
Invalidate evidence after relevant host/schema/backend changes or a mismatch.

If computation, complete tool-result access, physical owner parsing, exclusive
namespace ownership or actual shared single-writer serialization is unavailable,
return `missing-capability`/`unavailable`; do not substitute model arithmetic,
invent hashes, summarize payloads or proceed with guessed limits. A display
preview is insufficient even when the backend stored the full value.

## 2. Exact bytes and executable computation profile

Logical revision input is the **whole** logical object, not just its body:
address, type as found (including missing/invalid-type representation), complete
metadata, full content, ordered relations and unknown relation fields, original
source/layout/raw-document representation and source revision provenance.
Unknown keys survive. Transport generation/request/physical IDs are outside the
logical object so storage retries do not change its logical fingerprint.

Define `C(value)` by this deterministic tagged JSON tree, serialized as compact
ASCII JSON without whitespace or a final newline:

- JSON null, booleans and strings become `["null"]`, `["bool",value]` and
  `["str",value]`. Strings are Unicode scalar sequences, never normalized.
- Integers become `["int","<base-10>"]` with no leading zeros or plus sign;
  zero is `0`. JSON decimal numbers become `["decimal","<original-token>"]`:
  retain their exact valid JSON numeric token, never parse through binary float.
- Arrays become `["array",[C-tree(item),...]]` preserving order.
- Objects become `["map",[[key,C-tree(value)],...]]`, sorted by the UTF-8
  bytes of the original keys. Duplicate JSON keys are invalid, not last-wins.
- For strings/keys, escape quote and backslash, encode controls as lowercase
  `\u00xx`, all non-ASCII BMP scalars as lowercase `\uxxxx`, and non-BMP
  scalars as UTF-16 surrogate-pair escapes. Do not escape `/` or printable ASCII.
  Reject lone surrogates. Absent and null fields remain different.

`C-tree` means the tagged tree before its one outer JSON serialization, not a
string containing serialized JSON. Integer/decimal token distinction and raw
number spelling are retained by a token-aware parser. Non-JSON metadata (for
example YAML tags, aliases or duplicate keys) requires a reversible typed/raw
representation in the logical object, not lossy JSON coercion. If unavailable,
block structured mutation and retain the exact raw source with findings.
Raw source bytes, including non-UTF-8 originals, use a declared base64 byte
field; they must never be decoded with replacement characters. Text content
retains exact Unicode scalars and CR/LF bytes; original raw bytes are also
retained when needed to restore the source form.

The following are workflow computations executed using an actually available
general-purpose tool (for example a verified Python/Node executable), **not
new MCP methods**. T009 must record the actual tool invocation and outputs.

| Computation | Exact input → output/check |
|---|---|
| Canonicalize | Strict token-aware logical/control value → ASCII `C(value)` bytes; decode the tagged tree and compare every original value/token. |
| Fingerprint | Bytes `B` → `n=len(B)` and lowercase hex SHA-256 of all `B`. No ellipsis or estimated counts. |
| Encode | Bytes → standard RFC 4648 base64, padded, no whitespace/newlines. Decode strictly and require re-encoding equality. |
| Split | `B` and tested positive byte budget → contiguous slices with zero-based indexes and offsets; concatenate and byte-compare to `B`. Base64 expansion and envelope/request overhead are included in budget calculation. |
| Verify | Retrieved ASCII wire → strict parse/decode; compare exact intended bytes, length, digest and decoded complete value. Byte equality, not digest alone, verifies intended readback. |
| Allocate | Available UUID generator → stable request/version/record tokens, checked against the full known allocation inventory. Never regenerate on retry. |

For example, with a verified Python standard library tool, `len(B)`,
`hashlib.sha256(B).hexdigest()`, `base64.b64encode(B)` and
`base64.b64decode(text, validate=True)` implement the byte primitives;
`B == observed_B` performs comparison. These alone do **not** implement the
tagged canonicalizer or token-preserving parser. Those computations must be
provided and verified in the authorized workflow before claiming capability.
The model must not manually encode large values or calculate fingerprints.

## 3. Wire records and bounded structures

Observation `content` is exactly one line with no surrounding whitespace:

```text
JAIBA1.<base64(C(envelope))>
```

The outer encoding protects all punctuation/Unicode/newlines and synthetic
redaction-like text from text-specific transforms, but is **not encryption**
and does not promise immunity to truncation/redaction. Verify exact wire equality
after every write and on reads; no Markdown wrapper, appended prose or tolerated
prefix/suffix. A backend transform of this representation fails verification.

Every envelope is an object with these required fields:

```text
format: "jaiba-engram-storage/1"
adapter: "jaiba-engram-memory"
contract: {id: "jaiba-memory-surface", version: "1.0.0"}
namespace: exact exclusive prefix
backend_project: authorized physical project
registry_id: stable registry identity
kind: root | journal | payload-chunk | object-manifest | descriptor-page |
      catalogue-shard | publication-manifest | allocation-page
record_key: exact allocated routing key
request_id: stable request/close operation identifier
version_id: immutable version identifier (root/journal use their own revisions)
address: complete logical address, or null for namespace infrastructure
body: role-specific complete value below
```

A **locator** is `{id, record_key, kind, version_id, wire_bytes, wire_sha256}`.
Every reference carries these expected values; roots/journals are mutable and
their current exact revision is captured separately, never inferred from ID.
For each read validate server-rendered physical `Project` and `Scope: project`,
then expected envelope/locator and complete wire. Use the mapping's trusted
human-bound root or verified parent chain. Self-declared ownership is not enough.
Ambiguous content/footer framing blocks verification. Native topic is not
returned by the response shape previously inspected in T006: retain submitted
key/ACK as routing evidence, **do not claim native topic was checked**. If a
host returns it, check it too. Never search unrelated IDs for recovery.

For mutable root/journal locators, the bound ID/key/kind establish identity;
their locator's creation-time wire fingerprint is historical, not a claim
that later content is unchanged. Each update retains the full old and intended
new wire/revision in the operation receipt, then verifies the current exact
wire against that evidence. A journal's newly verified revision is recorded
in the receipt before subsequent writes. Lost journal-update acknowledgement
requires direct comparison with those two exact values, just like a root
update; neither value or missing receipt means unknown/block. Do not weaken
immutable child-locator fingerprint checks to accommodate mutable records.

Role bodies (all counts are exact non-negative integers, all digests computed):

| Role | Required body fields and meaning |
|---|---|
| `payload-chunk` | `object_version`, `index`, `offset`, `bytes`, `sha256`, `data_base64`. Data is one contiguous slice of `C(logical-object)`. |
| `descriptor-page` | `collection_id`, `page_index`, `entries`, `next` locator or explicit null, `entry_count`, `remaining_count`. Entries are ordered chunk descriptors or other declared collection entries; no mixed collection kinds. |
| `object-manifest` | `object_version`, `logical_address`, `logical_bytes`, `logical_sha256`, `chunk_count`, `descriptors_head` locator, `descriptor_page_count`, `complete:true`, encoding profile identifier. Descriptor entries bind each chunk locator plus index/offset/bytes/digest. |
| `catalogue-shard` | `generation`, `index`, `entries`, `entry_count`, `remaining_count`, `next` locator or null. Each entry has full address, type-as-found/findings, lifecycle (`live`/`retired`), logical revision, immutable object-manifest locator. Retired entries additionally carry tombstone evidence below. |
| `publication-manifest` | `generation`, `previous` publication locator or null, `catalogue_head`, `shard_count`, total/live/retired entry counts, `inventory_sha256`, registry collection head/counts, close-index collection head/counts, allocation head/counts, `request_id`, `complete:true`. |
| `allocation-page` | Immutable linked page of allocated keys/known IDs/roles/versions and attempt states, plus explicit next/null and counts. Retain staging, superseded, failed and retired records, not just active payloads. |
| `journal` | `journal_revision`, stable request/version/close IDs, prior publication/root evidence, intended object/inventory fingerprints, phase, append-only event-page head/counts and exact known ID receipts/unknown attempts. Never put an unbounded receipt array in this record. |
| `root` | `root_revision`, exact registry identity, `live` publication locator or null only for explicitly authorized empty bootstrap, `pending` journal locator or null. Prior live publication remains reachable through immutable `previous` links. |

Registry descriptor collections retain all projects, canonical aliases and
contexts, including empty contexts. Close-index entries bind project/context,
close ID, immutable log address/revision and frozen inventory evidence. Large
frozen inventories use immutable descriptor pages, not a giant log metadata
array. Their evidence is part of the complete log object. Collections declare
their entry kind, head locator, page count, total count and digest over the
canonical ordered entries. Empty collections use head null and zero counts.

All paged collections use the same explicit linked-page/count rules. Build
pages tail-first so immutable locators are known before encoding predecessors.
An object manifest contains only a bounded head/count descriptor, not an
unbounded chunk list; publication manifests similarly do not list all shards.
Verify even one entry/locator fits the measured control-record bound. Oversized
individual metadata/control entries need a referenced immutable chunked value
with the same exact verification, or `limit-exceeded` before publication.
Never recursively invent an untested layout. Finite counts/depth and tool
budgets are disclosed; exceeding them is incomplete, not silent success.

## 4. Complete catalogue and exact object read

1. Under serialized access read/verify the bound root and capture its exact
   wire/revision and live publication locator. A pending operation is not a
   replacement live catalogue; resolve unknown publication outcomes first.
2. Read the immutable publication, then every registry, catalogue, close-index
   and allocation page to explicit null termination. Check generation,
   page indexes, decreasing remaining counts, declared counts/digests, unique
   locators/keys and no cycles, gaps or duplicate logical addresses. Retain
   retired addresses as permanent reservations, never reusable logical IDs.
3. Catalogue entries cover **all managed published objects**, including malformed
   objects, missing/unknown types, unlinked logs and all selected contexts.
   Validate entry structure and expose findings; unreadable/malformed transport
   entries block completeness rather than being skipped. Filter only after
   complete unfiltered traversal. Search/index links are never enumeration.
4. For an object follow its immutable manifest and all descriptor pages. Require
   exactly indexes `0..chunk_count-1`, contiguous offsets, matching lengths and
   locators, explicit end and matching page counts. Verify every chunk and
   concatenate decoded bytes in index order using the computation tool.
   Require full byte count/digest, strict canonical decode/re-encode equality,
   full address/type/metadata/content/relations and original representation.
   Compare full intended-versus-observed object when verifying a mutation.
5. Re-read the root and require the captured exact revision/wire still matches.
   Return traversal evidence: root/publication revisions, every page/locator,
   declared/observed counts, unique-address count, explicit terminal nulls,
   inventory digest and `complete:true`. Until then return `complete:false`
   and verified continuation, never absence. A changed root restarts/reconciles;
   a hidden page, denied read, omitted bytes or count mismatch fails closed.

The inventory digest covers the canonical ordered full catalogue entry list
(ordered by canonical address bytes), including lifecycle/revisions/locators
and tombstones. Registry/close/allocation collections have their own digests.
Complete enumeration describes this exclusively managed namespace; it does not
claim to discover arbitrary unpublished Engram records. Allocation evidence
accounts for known staging records separately. Unknown IDs remain unknown;
the absence of search results cannot complete an inventory or reconcile them.

## 5. Staging, publication and preserving the previous version

The namespace's real single writer serializes **all shared root/catalogue and
registry writes**, even across independent executive contexts. An explicit
handoff includes pending/unknown attempts and receipts. Read/write/readback is
not a lock. Without actual exclusion, block all mutations.

1. Verify authority, full inventory, current object/absence and prior exact
   revisions. Compute the complete intended value and fingerprints. Allocate
   stable request, version and record keys once. Preserve original unknown
   fields and source forms. A retired/reserved address is not createable.
2. Create/verify a request journal and bind it through `root.pending` while
   leaving `root.live` unchanged. Read/compare the exact root immediately before
   each ID-based update; increment its revision and verify exact post-read.
   Initial journal creation itself needs retained tool receipts; unknown ID
   during this bootstrap blocks progress pending explicit reconciliation.
3. Before each save record the intended key, full wire fingerprint and
   `attempting` event in the verified journal. All saves use authorized project,
   scope `project`, type `manual`, exact allocated topic and `capture_prompt:false`.
   Persist the returned numeric ID in the operation receipt **before another
   save/retry**, then record/verify it in the journal. Detect collisions against
   all known allocated IDs/keys, including retired/staged versions. Save is an
   upsert and may deduplicate: an ACK is not ownership or preservation proof.
4. Stage payload chunks, descriptor pages, then immutable object manifest.
   Full-read/verify every returned ID and exact intended wire/value. Do not
   mutate a prior payload or manifest. Build replacement catalogue shards and
   registry/close/allocation collections from the entire prior inventory plus
   only authorized changes; unchanged objects retain their exact revisions.
5. Stage and verify the immutable publication manifest last among live-data
   records. Its `previous` references the prior live publication. Include the
   request's known allocations/journal locator; journal event pages account
   for later control writes, with root/journal self locators in their trusted
   binding chain. Allocation pages do not recursively list their own unknown
   IDs: those receipts live in the journal. Verify the complete candidate
   traversal and full resulting object before exposing it.
6. Re-read prior live root/publication, touched object revisions and complete
   inventory. Require exact expected values. Publication is **one** bound root
   `mem_update({id, expected_project, content:<whole-new-wire>})` replacing only
   the live pointer/revision while retaining the pending journal. Do not mutate
   live shards in place. Pre-read comparison is application discipline, not CAS.
7. Read back the root, traverse the new publication and full-read the result.
   Only exact matching readback yields a verified receipt. Mark the journal
   verified, then clear pending with the same guarded root protocol. Keep
   journal/allocation evidence reachable from publication history; no physical
   delete or garbage collection is specified. Failure to clear pending is a
   recoverable administrative partial outcome, not permission to repeat writes.

Before the publication update, **every** failure leaves the prior live pointer
unchanged. During/after that update, failure may leave old or new live state:
report `unknown` until a direct exact root read establishes which. The old
immutable publication and payloads are always retained; do not promise the old
pointer is still active after an acknowledged or uncertain root update. Do not
blindly roll back a potentially newer root or rewrite history to hide mismatch.
Stop dependent writes/cleanup and explicitly reconcile any corrupt root using
the retained prior exact evidence under the namespace owner's authority.

## 6. Retry, immutable close and logical retirement

Retries use the same request/version/close IDs and intended fingerprints.
Read the exact root, pending journal, publication chain and known returned IDs:

- Published identical request/result: verify full object and return its existing
  receipt, no save. Same identifier with different payload is `conflict`.
- Known staged IDs: read/verify and reuse only exact matching owned versions;
  finish missing *never-attempted* records under the same journal.
- Attempted save without recoverable returned ID, including journal/control
  writes: **block and ask for explicit reconciliation**. Bounded search absence,
  a stable key or a fresh UUID cannot make retry safe. Record uncertainty before
  handing off; never call save again to discover whether it already succeeded.
- Unknown root update: direct read matching old exact root permits continuation
  only under established serialization; matching new intended root permits
  verification. Any other state is conflict/unknown, never automatic overwrite.

For append-log, traverse the full close index **and** constitutive inventory,
including unlinked/malformed log findings; require unique close ID and matching
full immutable payload. Existing identical close returns its verified log;
different content conflicts. Stage/publish one new log via §5 only after exact
absence. Never update an existing log to repair or deduplicate it.

Archive evidence binds namespace/project/context, close ID, verified log
address/revision, and frozen complete executive addresses/revisions/full payload
evidence. Before retirement re-enumerate and full-read the log and all residual
work. Changed/new/unknown objects block cleanup even with a valid archive.

A tombstone replaces only the selected live catalogue entry and permanently
retains address, former type, prior manifest/revision, close ID, immutable archive
locator/revision, frozen-inventory evidence and retirement request/generation.
It is infrastructure, not a new OKF object or physical deletion. Never delete
payloads, logs, allocation evidence, tombstones or old publications. Root history
and the current catalogue retain all tombstones for future reservation/retry.

Retirement batches each use §5. On retry partition the frozen inventory into
verified tombstones for this exact close/archive, unchanged live residuals and
changed/unexpected/unknown entries. Only unchanged residuals may be retired;
verify existing tombstones without replacing them. Different-close tombstones
conflict. Every batch republishes the whole consistent catalogue. Read back and
report exact completed/failed/unknown/residual sets; `clear-work` succeeds only
when all intended addresses are tombstoned and no outside address changed.
The immutable close must already be verified before the first retirement.

## 7. T009 evidence and portability boundary

Required authorized tests as specified at T007, **not run during T007**.
Section 8 distinguishes subsequent executed paths from remaining obligations:

- A complete object larger than the measured individual-record operating bound,
  with adversarial escaping/Unicode/newlines, nested unknown metadata/relations
  and original raw representation; reconstruct all chunks and byte-compare the
  entire canonical object. Exercise truncation/transformation failures too.
- Multiple catalogue shards and descriptor pages, explicit completion/counts,
  empty contexts, malformed logical objects and unlinked logs. Missing/hidden
  page, cycle, duplicate address and changing root must never report complete.
- Fail before/during publication and on lost save IDs/readback; retain the old
  version and block unknown retries. Test root owner guard separately from
  revision discipline; demonstrate actual shared-writer serialization.
- Repeat identical close with no duplicate log; changed payload conflicts.
  Interrupt retirement, then verify tombstones and retire only unchanged
  residuals. New work, changed work or unverifiable archive blocks cleanup.

Each result records actual tool calls, computed byte counts/digests, bound
locators, prior/result publication evidence and exact comparisons, with no
secrets. Static gates and schema discovery cannot certify these capabilities.

Export unwraps this storage into the canonical neutral interchange manifest;
physical chunk/shard IDs are representation/provenance, not portable logical
identities. Preserve complete logical values, source forms/revisions, relation
order and unknown fields; explicitly declare scope, histories/tombstones and
exclusions. Import remains separately staged and explicitly approved before
activation, retaining source authority. This reference implements neither the
Phase 5 migration workflow nor a binding switch, merge, dual writer or cleanup.

## 8. Scoped T009 execution evidence — 2026-10-17

Provenance: run `531ae94b-393e-4e4f-a3f1-0055642782d3`, executor session
`ses_eb2b1144fffeId1ERTDOS6Bd4y`; evidence artifacts `report.md` and
`independent-audit.json`. The audit independently replays actual recorded MCP
calls, not simulated backend happy paths. The parent reports replaying the
audit source with PASS and directly verifying root 30, revision 13,
live publication 167, `pending:null`. This documentation refresh reads those
artifacts only; it does not repeat their backend calls. Evidence labels/run ID
identify provenance, not an installed dependency on a scratch directory or
a shipped implementation driver.

The authorized synthetic namespace was
`jaiba-memory/v1/test-531ae94b-393e-4e4f-a3f1-0055642782d3/` in physical project
`jaiba-framework`. Explicit single-writer handoff was used: no native lock,
CAS, atomic revision guard or transaction is claimed. The trial made 2019
actual calls (132 saves, 276 updates, 1244 reads, 366 host judgments and one
project probe), with no backend errors in this run. The audit records 1242
full exact read checks and accounts for all 132 created records through
allocation/journal evidence. No installation, binding activation or real
project work closure occurred.

### Executed happy paths

- **Complete large-object roundtrip:** 57127 canonical bytes,
  SHA-256 `00a1275ebdb9abaa762f55507f3014aeb045bf30668ceae8591d3016024c2195`,
  five chunks (42–46), three descriptor pages (47–49), manifest 50. Full bytes
  and values compared equal, including unknown nested metadata, ordered
  relations, external/unresolved-link finding, combining/non-BMP Unicode,
  CRLF and original raw-source base64. Numeric spelling survived in explicit
  raw original representation; strict numeric, duplicate-key and lone-surrogate
  canonicalizer vectors were tested separately. This is not proof for every
  possible metadata/source representation.
- **Fragmented complete catalogue:** four root-last publications (67, 98, 130,
  167), each with two shards. Registry includes contexts A/B/empty; missing-type
  logical object and unlinked log are retained. Collection counts, digests,
  explicit ends and root rechecks passed. Final inventory: four addresses,
  three live and one retired. All four journals finish verified.
- **Immutable update:** new manifest 81 holds 57197 canonical bytes; old
  manifest 50 and its full original payload remain exact after publication.
- **Immutable log and retry:** manifest 106, close ID
  `cd3f654a-bcac-46a5-a5f0-8b9746a04f68`; identical complete payload reused the
  verified log without a retry save (allocation count 94 → 94), while changed
  payload conflicted.
- **Archive then selective retirement:** only context-A `plan.md` was
  tombstoned after full log/frozen-inventory verification. Context-B `tasks.md`,
  the malformed constitutive object, log and old/new physical payloads remain.
  Outside-prefix sentinel 31's complete returned value, including footer,
  revisions and duplicates, was identical before/after and never rewritten.
- **Current host ownership evidence:** native `Topic` was returned and checked
  against the envelope key on every owned read, alongside physical ownership.
  T006's omitted-topic response remains historical evidence, not a fixed schema
  assumption. Hosts without that field still follow §3's conditional rule.

### Observed per-role bounds, not universal maxima

The independent audit corrects `live-summary.json`'s response-size sampling bug
(it sampled a journal instead of the intended role). Values below are largest
successfully checked sizes **in bytes**, not certified backend limits. Columns
measure wire content, serialized application arguments, serialized returned
value, and server-result UTF-8 text respectively; they are separate quantities.

| Role | Wire | Application request JSON | Response-value JSON | Server-result UTF-8 |
|---|---:|---:|---:|---:|
| payload-chunk | 22963 | 23237 | 23374 | 23270 |
| journal | 8467 | 8527 | 8874 | 8770 |
| root | 2075 | 2134 | 2466 | 2362 |
| descriptor-page | 7483 | 7759 | 7897 | 7793 |
| object-manifest | 2811 | 3087 | 3225 | 3121 |
| allocation-page | 5899 | 6175 | 6313 | 6209 |
| catalogue-shard | 5379 | 5655 | 5793 | 5689 |
| publication-manifest | 5259 | 5540 | 5678 | 5574 |

Backend binary version, absolute size maxima and actual MCP/network overhead
remain unknown. Application JSON sizes are **not** measured transport sizes.
The prior raw probe (reported input length 51020) reported a 50000 limit and remained
truncated (record 32); it and malformed placeholder 33 were excluded from valid
published payloads. This does not establish a universal 50000-byte safe budget
or prove that arbitrary raw text avoids transformation. The trial retained
135 physical namespace records (30, 32, 33, 41–172), with no physical deletion.

### Negative checks and remaining unverified paths

A deliberately corrupted expected revision was rejected using actual payload
reads before publication; the actual root retained its prior live pointer.
Duplicate address, stale root, truncated wire, cycle/gap/missing/hidden page,
new/changed work and unknown save-ID rejection were **local simulations on
captured actual data**, not induced live backend errors or permission faults.

Actual outage/network failure, permission/hidden-response injection, atomic
owner-guard rejection, lost save ID and uncertain root-publication recovery
remain unverified. So does interrupted **multi-object** retirement/residual
retry: the executed selective retirement covered one object only. No native
CAS/lock guarantee follows from serialized successful operations. Full
export/import, migration/activation, all executive templates and installed
workflow-consumer integration remain later-phase obligations. These scoped
results advance evidence for MEM-005/008/011 but do not certify their complete
acceptance paths or weaken any protocol requirement above.
