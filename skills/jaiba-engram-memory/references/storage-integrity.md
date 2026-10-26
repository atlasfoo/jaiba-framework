# Storage integrity and publication

Declarative storage protocol **2**, adapter `jaiba-engram-memory` 3.2.0,
contract `jaiba-memory-surface` 1.0.0. Read `engram-mapping.md` for authority,
binding and ownership, and the effective `create-memory` contract/interchange
references for logical semantics. This reference specifies storage, not a new
runtime SDK, installation, migration implementation or activation permission.
It covers MEM-005, MEM-008, MEM-009 and MEM-011; **full conformance remains unverified**.
Scoped executed T009 **profile-1 historical** evidence is recorded in §8; it
does not certify profile 2 or supply its computation/size evidence. Profile 2
remains draft/unverified; T-035 stays blocked until T-040 and any required
approval for a concrete binding transition. This is not logical contract v2.

## Contents

1. Evidence, prerequisites and measured bounds
2. Exact bytes and executable computation profile
3. Wire records and bounded structures
4. Complete catalogue and exact object read
5. Staging, publication and preserving the previous version
6. Retry, immutable close and logical retirement
7. Evidence and portability boundary
8. Historical profile-1 execution evidence
9. Transfer staging and cross-surface recovery

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

Serialize each complete logical object and each control envelope **once** as
ordinary JSON using an existing standard tool, then encode that output as UTF-8
without BOM. Retain the complete resulting byte snapshot `B` before dispatch,
including any serializer-produced whitespace/newline. Record tool/version and
options. No canonical key order, tagged tree, token-aware parser, normalization,
custom serializer/codec or cross-serializer equality is required or allowed as
a substitute. Different standard serializations may yield different revisions;
the chosen snapshot, not a regenerated serialization, defines this revision.
Each new write/revision gets its own snapshot. Reuse the original snapshot for
an identical retry; never reserialize data to justify a readback difference.

Preserve unknown metadata/types, missing versus null, ordered relations and
unknown relation fields without coercion. Preserve Unicode and CR/LF content
exactly; no normalization or replacement characters. Retain original source
bytes separately with declared media type/encoding and standard base64, including
non-UTF-8 or non-JSON sources (YAML tags/aliases/duplicate keys, for example).
Opaque extensions remain opaque; unknown required extensions block use.

Declare the effective standard parser/serializer's numeric limits **before**
structured use. Control counts, offsets, revisions and numeric IDs must be exact
non-negative integers within the intersection of all effective tools' supported
ranges; exceeding it blocks the operation, never rounding or string coercion.
For binary64-only tools this range is at most `0..9007199254740991`; a wider
range requires demonstrated exact support throughout. Reject duplicate keys,
NaN/Infinity, invalid UTF-8 and lone surrogates in profile-2 JSON. Use standard
parser facilities for strict validation (including duplicate-key rejection),
not a new parser. If those facilities are unavailable, block structured use.
Do not assume a parser's default last-key-wins behavior is safe.

Apply the exact non-negative integer validator only to the protocol fields
named above, by their schema roles, not recursively to every number in an
external tool result or receipt. External telemetry such as
`elapsed_from_intent_seconds: 177.250265`, or any other non-protocol float on a
receipt, is not a control count, offset, revision or numeric ID: it must not
fail that validator or be rounded/coerced into a protocol counter. Its presence
does not invalidate an otherwise intact record. Protocol integer checks and
the separate lossless-representation rules for logical/source values remain
unchanged.

Unsupported precision, significant numeric lexemes (such as `1.00`, `1e0` or
`-0`) and non-JSON values must remain in a declared opaque byte representation,
or unsafe structured edits/imports must stop. A parsed projection is not the
lossless authority for those values. Preserve original source bytes **before**
parsing; do not first round/coerce a value and then snapshot the lossy result.
If standard tooling cannot establish exact structured representability, keep
the affected source/extension opaque or block its structured use. No token-aware
inspection is a prerequisite for retaining the entire source opaquely.
Restore numeric spelling from preserved source bytes, never reconstituted parser
tokens. Unchanged opaque source and
extensions are copied exactly; if an authorized edit cannot preserve their
meaning and restoration mapping, block it rather than silently desynchronize
structured fields and source. This does not add an alternate typed-tree codec.

The following are standard workflow computations, **not new MCP methods or
helpers**. Capability evidence must record actual tools, options and results;
historical profile-1 execution is not profile-2 evidence.

| Computation | Exact input → output/check |
|---|---|
| Snapshot | Complete logical/control value → one standard JSON UTF-8 byte snapshot; retain all bytes and verify that strict standard parsing preserves supported fields/types. Parsing validates structure, not byte equality. |
| Fingerprint | Bytes `B` → `n=len(B)` and lowercase hex SHA-256 of all `B`. No ellipsis or estimated counts. |
| Encode | Bytes → standard RFC 4648 base64, padded, no whitespace/newlines. Decode strictly and require re-encoding equality. |
| Split | `B` and tested positive byte budget → contiguous slices with zero-based indexes and offsets; concatenate and byte-compare to `B`. Base64 expansion and envelope/request overhead are included in budget calculation. |
| Verify | Retrieved wire → exact wire comparison, strict base64 decode and standard JSON validation; compare FULL recovered bytes to the retained intended snapshot, length and digest. Never parse/reserialize as an equality test. |
| Allocate | Available UUID generator → stable request/version/record tokens, checked against the full known allocation inventory. Never regenerate on retry. |

For wire fingerprints, `wire_bytes` is `len(W)`, where `W` is the retained
complete ASCII `JAIBA2.<base64>` payload line (prefix included), compared to
the verified wire snapshot extracted under §3. It is not `len(B)` of the decoded
JSON snapshot and excludes MCP headers/footers. `truncation.original_bytes` is
external response metadata, **not the wire length**; never substitute it for
`len(W)` or use it to establish complete readback. Truncation still blocks
verification when complete wire bytes are unavailable.

For example, with a verified Python standard library tool, `len(B)`,
`hashlib.sha256(B).hexdigest()`, `base64.b64encode(B)` and
`base64.b64decode(text, validate=True)` implement the byte primitives;
`B == observed_B` performs comparison. Standard JSON facilities provide JSON
serialization/validation within their declared limits; there is no additional
canonicalization algorithm to implement. Full snapshots may be retained as
verified referenced artifacts/pages in existing journal/receipt workflows, not
machine routing data. Hashes alone cannot recover them. Unavailable original
operation snapshots block uncertain-write recovery; regenerated bytes are not
replacement evidence.
The model must not manually encode large values or calculate fingerprints.

### Point commands and profile-2 measured caps

For a retained snapshot file `snapshot.json`, these point invocations compute
its byte length, SHA-256 and standard-base64 representation from the bytes
already retained (they do not regenerate or normalize the snapshot):

```sh
python3 -c 'import base64,hashlib,pathlib; b=pathlib.Path("snapshot.json").read_bytes(); print("bytes",len(b)); print("sha256",hashlib.sha256(b).hexdigest()); print("base64",base64.b64encode(b).decode("ascii"))'
sha256sum snapshot.json
base64 -w 0 < snapshot.json
```

GNU `base64` wraps at 76 columns unless `-w 0` disables wrapping. Check the same
bytes with `base64 -d` when decoding a retained base64 value,
then compare the recovered file byte-for-byte with the snapshot; `sha256sum`
checks the file digest independently. These commands calculate evidence only,
not a complete record/wire or publication implementation. Do not use
`crypto.subtle`, an MCP client, a codec, a writer, a full-cycle harness, or a
maximum-search campaign.

The following profile-2 caps are conservative class-specific limits derived
only from already measured anchors. Margin is zero headroom above each anchor:
the cap equals the measured size, with no rounding or increase. A specimen is
in-cap only when its computed length is less than or equal to its own class cap.
Unknown classes or unavailable size evidence are not-in-cap; report them rather
than guessing. These are not backend maxima and do not authorize searching for
larger maxima.

| Profile-2 specimen class | Measured anchor and cap (bytes) |
|---|---:|
| Root JSON snapshot | 656 |
| Root wire | 883 |
| Journal JSON | 2304 |
| Journal wire | 3079 |
| Retained object | 1087 |
| Local fixture A | 876 |
| Local fixture B | 1146 |

The historical 57127-byte figure is profile-1 evidence only, not a profile-2
cap.

## 3. Wire records and bounded structures

### Profile boundary and confirmed transitions

The effective binding must explicitly declare `jaiba-engram-storage/2`, its
exact root/registry/namespace/backend project and fingerprint/number-tool profile.
Check that declaration, every locator's `storage_profile`, the `JAIBA2.` prefix
and envelope `format` agree **before** authoritative use. Missing, mixed,
unknown or incompatible profiles/locators/bindings block the operation as
`unsupported-version` (or `invalid-object` for malformed records); there is no
fallback decoder or profile inference from the decoded shape. Apply this to
all roles, including root, pending journal, history and staging references.

`JAIBA1.<base64(C(envelope))>` / `jaiba-engram-storage/1` is a distinct historical
profile. Never decode it as profile-2 JSON, relabel it, rewrite it in place or
automatically migrate it. Its existing bytes and evidence keep their original
meaning; this document supplies no new profile-1 writer or compatibility decoder.
A profile-1 source requires an independently supported, explicitly selected
legacy reader/exporter; otherwise export/transition is blocked. Retaining opaque
legacy source bytes is preservation, not verified interpretation or conformance.
Legacy physical references may occur only as explicitly labeled opaque
provenance, never as traversable profile-2 storage locators.

Any transition needs specific human approval of the **concrete** source and
destination storage profiles, bindings, physical namespace/root allocation and
logical address/restoration/remap table before transition writes. Follow §9 and
the neutral transfer barriers, with an isolated profile-2 target and source
authority retained. Activation requires its separate confirmed binding change,
precedence re-resolution and full readback; document correction, installation,
a version-looking namespace prefix or profile-1 evidence authorizes none of
these. Logical contract `1.0.0` and logical object identities do not change merely
because storage is profile 2. Do not broaden ownership to change routing assets
or a live binding here; an undeclared binding stays blocked pending approval.

### Standard wire and role schemas

Observation `content` is exactly one line with no surrounding whitespace:

```text
JAIBA2.<base64(UTF8-JSON-envelope-snapshot)>
```

The outer encoding protects all punctuation/Unicode/newlines and synthetic
redaction-like text from text-specific transforms, but is **not encryption**
and does not promise immunity to truncation/redaction. Verify exact wire equality
after every write and on reads; no Markdown wrapper, appended prose or tolerated
prefix/suffix. A backend transform of this representation fails verification.

That single stored line is not the surrounding MCP tool response. Extract
exactly one complete line beginning `JAIBA2.` by that prefix within the
established response framing, never by a fixed line position or total line
count. Extract server-rendered physical fields by the labels `Project:`,
`Scope:` and, when present, `Topic:`; do not use strings inside decoded content
or the outer request-context project as physical metadata. Headers/footers may
vary: a 9-line response and a 10-line response are both acceptable when the
labeled wire and required physical fields match and complete verification
passes. Neither 9 nor 10 lines is required. Missing wire or required physical
fields, duplicate labeled wire/fields (even identical), or ambiguous framing
block verification; never choose the first/last match. This permits neither
wrapping nor suffixing stored content, nor stripping whitespace from the wire
to make it match. Conditional Topic absence follows the response-profile rule
below, not a line-count test.

Every envelope is an object with these required fields:

```text
format: "jaiba-engram-storage/2"
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

A **locator** is `{storage_profile, id, record_key, kind, version_id,
wire_bytes, wire_sha256}`, where `storage_profile` is `jaiba-engram-storage/2`.
Every reference carries these expected values; roots/journals are mutable and
their current exact revision is captured separately, never inferred from ID.
For each read validate server-rendered physical `Project:` and `Scope: project`,
then expected envelope/locator and complete wire. Use the mapping's trusted
human-bound root or verified parent chain. Self-declared ownership is not enough.
Ambiguous content/footer framing blocks verification regardless of line count.
Native topic is not
returned by the response shape previously inspected in T006: retain submitted
key/ACK as routing evidence, **do not claim native topic was checked**. If a
host returns `Topic:`, extract it by label and check it too, under the mapping's
established response-profile rules. Absence is not proof that native topic was
checked. Never search unrelated IDs for recovery.

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
| `payload-chunk` | `object_version`, `index`, `offset`, `bytes`, `sha256`, `data_base64`. Data is one contiguous slice of the complete logical-object JSON UTF-8 snapshot. |
| `descriptor-page` | `collection_id`, `page_index`, `entries`, `next` locator or explicit null, `entry_count`, `remaining_count`. Entries are ordered chunk descriptors or other declared collection entries; no mixed collection kinds. |
| `object-manifest` | `object_version`, `logical_address`, `logical_bytes`, `logical_sha256`, `chunk_count`, `descriptors_head` locator, `descriptor_page_count`, `complete:true`, encoding profile identifier. Descriptor entries bind each chunk locator plus index/offset/bytes/digest. |
| `catalogue-shard` | `generation`, `index`, `entries`, `entry_count`, `remaining_count`, `next` locator or null. Each entry has full address, type-as-found/findings, lifecycle (`live`/`retired`), logical revision, immutable object-manifest locator. Retired entries additionally carry tombstone evidence below. |
| `publication-manifest` | `generation`, `previous` publication locator or null, `catalogue_head`, `shard_count`, total/live/retired entry counts, `inventory_fingerprint_method`, `inventory_bytes`, `inventory_sha256`, registry collection head/counts, close-index collection head/counts, allocation head/counts, `request_id`, `complete:true`. Every collection also declares its own method/byte length/digest under §4. |
| `allocation-page` | Immutable linked page of allocated keys/known IDs/roles/versions and attempt states, plus explicit next/null and counts. Retain staging, superseded, failed and retired records, not just active payloads. |
| `journal` | `journal_revision`, stable request/version/close IDs, prior publication/root evidence, intended object/inventory fingerprints, phase, append-only event-page head/counts and exact known ID receipts/unknown attempts. Never put an unbounded receipt array in this record. |
| `root` | `root_revision`, exact registry identity, `live` publication locator or null only for explicitly authorized empty bootstrap, `pending` journal locator or null. Prior live publication remains reachable through immutable `previous` links. |

Registry descriptor collections retain all projects, canonical aliases and
contexts, including empty contexts. Close-index entries bind project/context,
close ID, immutable log address/revision and frozen inventory evidence. Large
frozen inventories use immutable descriptor pages, not a giant log metadata
array. Their evidence is part of the complete log object. Collections declare
their entry kind, head locator, page count, total count and digest over the
exact collection snapshot defined in §4. Empty collections use head null and
zero counts; their snapshot is the empty byte sequence with its computed digest.

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
   Require full byte count/digest and strict standard JSON validation of the
   full address/type/metadata/content/relations and original representation.
   For mutation verification compare every reconstructed byte to the original
   intended object snapshot, not a parsed/reserialized equivalent. Each control
   record likewise compares to its own retained full envelope/wire snapshot.
5. Re-read the root and require the captured exact revision/wire still matches.
   Return traversal evidence: root/publication revisions, every page/locator,
   declared/observed counts, unique-address count, explicit terminal nulls,
   inventory digest and `complete:true`. Until then return `complete:false`
   and verified continuation, never absence. A changed root restarts/reconciles;
   a hidden page, denied read, omitted bytes or count mismatch fails closed.

For each inventory/registry/close/allocation collection, declare fingerprint
method `sha256-page-json-bytes/2`: concatenate the **complete decoded envelope
JSON snapshots** of its pages/shards in head-to-next traversal order, with no
separator or reserialization. Retain that full concatenation and the ordered
page locators/byte lengths in operation snapshot evidence; each immutable page
also retains its own original bytes. The digest covers every field, including
entry order, lifecycle/revisions/locators/tombstones and next/count fields.
Record total concatenated byte length alongside the digest. Page boundaries
are the declared lengths, not a custom parser. The concatenation is a byte
sequence for hashing/comparison, not another JSON document to parse. Verify page
bytes individually and the full reconstructed collection against the retained intended snapshot
on publication/readback; parsing only checks structure/counts/addresses. No
canonical address sort or key-order normalization is involved. A differently
ordered or paginated new inventory is a new snapshot/revision, not an equal
retry. Frozen inventories retain their original ordered snapshots as well.
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
   revisions. Serialize once and retain each complete intended byte snapshot,
   length and SHA-256, including new controls/collections as they are built. Allocate
   stable request, version and record keys once. Preserve original unknown
   fields and source forms. A retired/reserved address is not createable.
2. Create/verify a request journal and bind it through `root.pending` while
   leaving `root.live` unchanged. Read/compare the exact root immediately before
   each ID-based update; increment its revision and verify exact post-read.
   Initial journal creation itself needs retained tool receipts; unknown ID
   during this bootstrap blocks progress pending explicit reconciliation.
3. Before each save record the intended key, complete intended snapshot/wire
   (or verified durable snapshot reference), byte length, SHA-256 and
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

Retries use the same request/version/close IDs and original intended snapshots,
lengths and fingerprints. Snapshot loss blocks recovery, not a new serialization.
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

## 7. Evidence and portability boundary

The following remain operational obligations for profile 2, with fixtures
deferred to T-040; this documentation change runs none. Section 8 records only
historical profile-1 results, not transferable profile-2 conformance:

- A complete object larger than the measured individual-record operating bound,
  with adversarial escaping/Unicode/newlines, nested unknown metadata/relations
  and original raw representation; reconstruct all chunks and byte-compare the
  entire original JSON UTF-8 snapshot. Exercise truncation/transformation failures too.
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
exclusions. Import follows §9's separately staged mapping and init's explicit
approval workflow before activation, retaining source authority. This is
declarative guidance, not an executed migration, binding switch, merge, dual
writer or cleanup.

## 8. Historical profile-1 scoped T009 execution evidence — 2026-10-17

Everything in this section concerns `JAIBA1` / `jaiba-engram-storage/1` and
its historical canonicalizer, not the new JSON profile. Preserve its meaning,
byte counts, digests and evidence unchanged. No historical artifacts or backend
data were accessed for this profile-2 correction; the following is the retained
prior account, not a claim that this correction replayed or read those artifacts.

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

## 9. Transfer staging and cross-surface recovery

This is the physical mapping for the neutral transfer profile, not a native
Engram transaction/import/export API. Use only the known `mem_get_observation`,
`mem_save` and guarded `mem_update` operations from `engram-mapping.md`; schema
discovery and applicable computation/size/owner-profile evidence remain required.
Do not infer new tool names, CAS, locks or multi-record atomic publication.
No transfer/activation execution evidence is added by this section.

### Stable namespace, roles and journals

Init's external migration journal records one stable transaction ID and the
explicitly authorized **physical staging prefix**, backend project, registry
identity, intended root record key and logical address/remap table before
provisioning. The root numeric ID is initially unknown: capture the returned
ID in the external receipt before another effect, then fully read/verify and
bind it. Never invent a preallocated numeric ID.
Record source and destination storage profiles and exact approved bindings in
the external journal, including every address/restoration mapping and approval
reference (§3). A profile mismatch blocks before provisioning; no implicit
profile-1 read/migration is supplied by these profile-2 recipes.
The prefix is a storage allocation, not a new portable logical namespace or
project ID. Envelope `namespace`/`backend_project`/`registry_id` identify the
physical chain but prove nothing alone: require physical owner verification
and the trusted locator/registry chain. The approved registry/binding maps that
physical scope to the preserved logical scope. `address` and catalogue logical
addresses retain the source namespace/project/context/logical-id unless
explicitly remapped. Check both independently. Never silently rewrite logical
identity to match a backend project name or staging prefix.

Keep the same staging prefix/root for this transaction, wholly outside all
effective consumer bindings. Independently establish exclusive allocation;
search cannot prove it absent. Bootstrap a verified empty root only with
explicit authorization, retaining intent, full intended wire and numeric-ID
receipt externally before there is any backend journal. Unknown bootstrap
save IDs stop the transfer. No backend project/session registration hack.

Use **profile-2 roles from §3** rather than a parallel import store:

| Transfer evidence | Existing physical realization |
|---|---|
| Pending transfer | Owned `journal` bound through the staging root's `pending`; external migration journal binds its exact locator/current revision to the stable transaction, manifest revision and per-operation request IDs. |
| Large journal intents/receipts | Immutable `descriptor-page` event collections under §3's count/digest/end rules. Entries retain transaction/manifest revision, full address, phase, request/version/key, complete intended wire/payload artifact reference, prior absence/revision, known returned ID, result/evidence and unknown status. Verify any referenced external bytes before reuse; a hash alone cannot reconstruct an uncertain update. |
| Full neutral objects | `payload-chunk` → `descriptor-page` → immutable `object-manifest`, retaining all logical fields, opaque extensions and raw representation. Backend `type:manual` is transport, not a replacement for type as found. |
| Candidate inventory and registry | Immutable `catalogue-shard` and registry descriptor collections, including project/alias and empty-context inventory. Preserve close IDs/index and declare history/tombstone scope; imported log payloads stay immutable, not new summarize events. |
| Every physical attempt | `allocation-page` collections plus journal event receipts, including failed/staged/superseded allocations. Root/journal bootstrap and allocation-page self IDs use external/journal receipts, not circular invented references. |
| Verified whole staging generation | One immutable `publication-manifest` referencing all complete collections. The exact owned root publishes it only after full candidate verification; it remains a non-effective staging root until init verifies binding activation. |

The backend journal handles storage recovery; it never replaces the external
cross-surface journal that must survive source/target outages. Record intent
durably before **each** mutation, not after a batch. After each returned ID,
persist/verify its receipt before another save. All save keys remain independently
allocated under the one staging prefix (§2/§5), not address-derived upserts.
Journals themselves obey tested bounded encoding/page rules; oversized evidence
requires verified referenced pages/artifacts or blocks before dispatch.

### Whole-candidate verification and publication

1. Keep source read-only and authoritative. Export uses §4's full traversal and
   reconstruction plus neutral snapshot readback, with no source-side pending
   journal or writes. Capture/recheck source root, registry, complete inventory
   and every full logical revision, not just object count or recent context.
   Preserve source snapshots as source evidence. Serialize each neutral manifest
   or payload once using its declared standard representation, retain all bytes
   and compare its full artifact readback/length/SHA-256. Neutral interchange
   is not an Engram storage envelope and gains no new canonicalization rule.
   Already-opaque raw payloads are copied byte-for-byte, not parsed or converted
   to JSON; their complete original bytes are the expected artifact snapshot.
2. Apply §5's allocation/journal sequence to all imported objects under the
   same migration transaction. Leave `root.live` at its verified empty baseline
   during the first import; on an explicitly reconciled refreshed candidate,
   retain the prior verified staging publication. Every new payload, page and
   manifest is immutable and journaled. Each target logical object is serialized
   once as its own profile-2 snapshot; preserve exact opaque source bytes and
   provenance independently, without coercing them through the target parser.
   No per-object live generations while the candidate inventory is partial.
   No in-place live catalogue edits.
3. Reconstruct **every** candidate object and compare FULL bytes against its
   original intended target JSON snapshot, length and digest. Separately validate
   complete neutral values, unknown fields/extensions, ordered relations and
   opaque original bytes against the approved source/restoration mapping;
   never use cross-serializer byte equality or parse/reserialize for readback.
   Traverse the candidate publication directly through its trusted journal
   locator even while it is not live. Check all counts/digests/ends, no duplicate
   addresses/locators, exact registry/context equality and close-ID uniqueness;
   internal targets resolve after approved remaps. Source-unresolved links
   remain explicitly unresolved. Source versions are retained provenance;
   target wire/object/publication revisions are independently computed evidence.
4. Recheck full source and staged target/registry evidence under actual shared
   writer serialization. Only a complete verified candidate may pass §5's exact
   old-root comparison and `mem_update({id, expected_project, content})` live
   pointer update, retaining pending until full root/publication/object readback
   verifies the result. This is one guarded record update, **not atomic CAS**
   or an authority switch. Unknown root updates follow §6, never automatic
   rollback. Finish backend journal/pending cleanup without repeating import.
5. External journal `staging-verified` additionally requires all neutral barrier
   checks. Init separately obtains activation approval for that manifest
   revision, immediately repeats both inventories/revision checks, changes only
   approved routing, re-resolves precedence and reads back the complete selected
   surface. Only this verified binding change can become `active-verified`.
   Retain source, snapshot, all known staging/previous versions and journals.

### Resume, invalidation and exact residuals

On interruption reopen **both journals for the same transaction**, establish
ownership/writer handoff and read the exact root/pending/publication chain.
Partition each planned logical object and physical attempt into never attempted,
known matching staged, verified published, failed-no-effect, conflicting or
unknown. Full-read known IDs and compare exact intended wire and request/key/
version, not just logical content; verify their trusted journal lineage.
Reuse matching records without `mem_save`, including historical logs/close
index entries. Candidate already published by this request means verify/reuse,
not repeat create or append. Different payload under the same request conflicts.

For uncertain root/journal updates, retain full old and intended new wire and
directly compare owned readback: old permits continuation under serialization,
intended new permits verification; any other value blocks dependent operations.
For an attempted save without a recoverable numeric ID, **stop** for exact-request
reconciliation. Do not upsert the same topic, allocate a fresh UUID/namespace,
search unrelated memory or use bounded absence as a retry test. Only proven
never-attempted or conclusively reconciled no-effect attempts may proceed.

If source or staging changed, invalidate dependent barrier/activation evidence
and retain the last verified state, exact effects and prior snapshot revisions.
A reconciled new snapshot revision keeps the transaction and staging namespace;
changed intended payloads receive explicitly journaled new child request/version
IDs, never reuse an old request for different bytes. Preserve old immutable
records and require renewed scope/remap approval where affected; a source change
does not itself authorize additional writes. Report completed/failed/unknown/
residual logical addresses and all known physical allocations separately.
Abandonment/activation implies no delete, namespace purge, source retirement,
dual-write or fallback; cleanup requires separate exact-scope authorization.
