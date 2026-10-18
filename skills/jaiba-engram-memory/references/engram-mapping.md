# Engram operation mapping

Adapter `jaiba-engram-memory` **3.2.0**; canonical contract
`jaiba-memory-surface` **1.0.0**, resolved through the effective `create-memory`
installation. This is a declarative mapping with **scoped execution evidence,
not complete mutable-surface certification**.
Read the completed [Storage integrity and publication](storage-integrity.md)
protocol 1 alongside this mapping for all storage operations. It specifies
encoding, computation, record roles, traversal, publication and recovery;
T-009 demonstrated the scoped results below, not universal operating limits.

## Contents

1. Evidence and real tool boundary
2. Ownership, identities and bootstrap
3. Representation and catalogue
4. Revisions, serialization and receipts
5. Operation recipes
6. Limits, failures and validation

## 1. Evidence and real tool boundary

On **2026-10-17**, the implementing OpenCode child independently discovered
the complete `engram` tool catalogue (19 tools, no remaining discovery page)
and inspected the schemas below. A non-destructive call
`mem_current_project({directory: "/mnt/Storage/repos/jaiba-framework"})`
returned project `jaiba-framework`, source `git_remote`, and the same absolute
project path. This proves child-local discovery/connectivity only, not
ownership, complete reads, mutable capability or adapter activation. No backend
binary/version identifier was returned. Reinspect schemas on each host/version.

A separately authorized read-only `mem_get_observation({id:24,
project:"jaiba-framework"})` inspected exactly one ordinary host session-summary
record to establish the actual response shape, not to adopt it into this
surface. Its result contained full summary text and server-rendered `Project`,
`Scope`, `Revisions` and other footer metadata, but **no native `topic_key`**.
The outer `project` field is request context, not physical-owner evidence.
No candidate records were read and no mutation was needed for that check.
This historical response profile does not describe every subsequent record:
the later T-009 owned reads rendered native **`Topic`**, checked against the
expected envelope key on every owned read. Apply the response-profile rules
in §2; neither assume Topic is always absent nor invent it for older output.

Current docs: Context7 `resolve-library-id("Engram", …)` selected
`/gentleman-programming/engram`, then `query-docs` covered observation MCP,
project/scope/topic keys, full reads, update/delete ownership and bounded search.
Sources returned: upstream `docs/ARCHITECTURE.md`, `docs/PLUGINS.md`,
`internal/store/store.go`, `internal/mcp/mcp.go` at
`https://github.com/gentleman-programming/engram` (main, no immutable version
reported). Docs describe an admin/deferred `mem_delete`; **it is not exposed
in this child's complete catalogue**. Do not call it or assume admin access.
Local callable schemas govern this mapping; disputed/new schema semantics
block the affected path pending verification, not a guessed call.

| Actual callable | Inspected arguments and use |
|---|---|
| `mem_current_project` | Optional `directory` or alias `cwd`; supply the established work root. Detection is a candidate, not authorization. |
| `mem_list_projects` | No arguments; optional backend-project discovery, never a logical JAIBA registry. |
| `mem_context` | Optional `project`, `scope`, `compact`, `max_bytes` (default 16384 bytes, clamped at 65536). Recent bounded context only. |
| `mem_search` | Required `query`; optional `project`, `scope`, `limit` (default 10, max 20), `match_mode` (`all`/`any`), `response_format` (`compact`), `type`, `all_projects`. No catalogue pagination cursor. Use explicit project/scope, never `all_projects:true` for authoritative resolution. |
| `mem_get_observation` | Required numeric `id`; optional `project`, `include_history`, `history_cursor`. Project is response context, **not an ownership filter**. History is bounded to 50 prior snapshots with explicit continuation; not catalogue pagination. |
| `mem_save` | Required `title`; use `content`, `project`, `scope:"project"`, `topic_key`, `type:"manual"`, **`capture_prompt:false`**. `content` is required unless alias `observation` is supplied; use `content` only. Optional `session_id` must already be authoritative. Explicit project must have known backing; invented names fail. |
| `mem_update` | Required `id`, **`expected_project`**; optional `content`, `title`, `scope`, `topic_key`, `type`, or literal `find`+`replace` (not with content). Use full content replacement after pre-read, never blind textual patches. The atomic owner check is not revision CAS or namespace enforcement. |

`mem_save` additionally accepts `project_choice_reason` and `recovery_token`
only for the server's actual ambiguous-project recovery flow. Use them only
after the human chooses one of that error's offered projects; never fabricate
recovery tokens, sessions, registrations or a project to bypass validation.
Topic saves are **upserts** within backend project+scope and may deduplicate;
they are not create-if-absent. A returned numeric ID must always be read back
and checked. ACKs and docs are not preservation evidence.

Other exposed tools (session/prompt bookkeeping, pin/review, judge/compare,
passive capture and doctor) are not adapter storage primitives. In particular,
native Engram relation judgments do not replace lossless logical relations or
authorize changes to ordinary observations. If save returns judgment candidates,
do not follow candidate IDs into unrelated memory as part of this adapter;
surface unresolved side effects and stop dependent operations as necessary.

### Executed scoped evidence — 2026-10-17

T-009 execution session: `ses_eb2b1144fffeId1ERTDOS6Bd4y`. Evidence bundle label:
`jaiba-memory-surfaces/531ae94b-393e-4e4f-a3f1-0055642782d3`; source labels:
`report.md`, `independent-audit.json`, `audit-evidence.py`, `source-hashes.json`
and `live-receipts.json`. These are retained external run artifacts, not
package-relative dependencies or shipped receipts. This refresh read the report
and independent audit; conduct inspected runner/audit source, reran the audit
PASS and independently confirmed root 30 by MCP. It made no new backend calls.

The authorized scope was backend project `jaiba-framework`, exclusive namespace
`jaiba-memory/v1/test-531ae94b-393e-4e4f-a3f1-0055642782d3/`, one synthetic logical
project and contexts A/B/empty, with explicit single-writer handoff. These are
historical test identifiers, **not default routing or activation configuration**.

| Executed target | Scoped observed result |
|---|---|
| Full object and computation | 57127 canonical bytes reconstructed from five chunks, three descriptor pages and manifest 50; exact byte/value equality including nested unknown fields, ordered relations, Unicode/CRLF and raw source. Numeric token spelling retained in raw representation; strict canonicalizer vectors also passed. |
| Complete managed catalogue | Four publications, each two shards; registry/close/allocation collection counts, digests, explicit ends and root rechecks passed. Malformed missing-type object and unlinked log retained. Final inventory: four addresses, three live and one retired. |
| Immutable update/publication | Updated object 57197 canonical bytes, manifest 81; old manifest 50 and its original full payload still exact. All four journals verified; replay accounts for all 132 created records. |
| Append/archive/retirement | Immutable log manifest 106, 2381 canonical bytes; identical close/payload reused it without a save, different payload conflicted. Verified log/frozen inventory preceded retirement of context-A plan only. Context-B tasks, malformed constitutive object, log and prior payloads retained. |
| Ordinary-memory witness | Outside-prefix sentinel 31's full returned value, including footer/revisions/duplicates, matched before/after; not catalogued or rewritten. |
| Final publication | Root 30 logical revision 13, live publication 167, pending null; audit replay PASS and separate conduct direct-read confirmation. No unknown writes or pending root operation reported. |

The trial made **2019 actual Engram calls**: 132 saves, 276 updates, 1244 reads,
366 host judgments and one project probe. Judgments concerned only authorized
IDs/current-run receipts, with no unknown candidate follow-up or body mutation.
There were no backend errors in the successful run. **135 physical namespace
records remain**: 30, 32, 33 and 41–172; 132 were created by this run. Earlier
truncated probe 32 and malformed placeholder 33 were excluded, not published as
valid payloads. No physical cleanup was attempted; sentinel 31 is outside scope.

Independent replay verified actual recorded calls, not a simulated happy path.
Corrupt-revision preflight and captured-data negative checks rejected stale
root, duplicate address, truncated wire, cycles/gaps/hidden pages, new/changed
work and lost save IDs **locally**. They do not demonstrate native denied reads,
network/lost-ID/root-update recovery, backend owner-guard failures or ACL isolation.
Interrupted multi-object retirement, full export/import/activation, all executive
templates and installed workflow integration were not exercised. These gaps
keep global status **draft/unverified**, not the whole PRD or backend certified.

## 2. Ownership, identities and bootstrap

Reserve one human-confirmed exclusive topic prefix
`jaiba-memory/v1/<namespace-token>/` inside an **already authorized Engram
project**, always with `scope: project`. The namespace token is collision-free
and stable, not a repository basename. Global skill installation never means
Engram `scope: global`. Ordinary memory stays outside this prefix.

The machine binding independently records backend project, namespace prefix,
exact root observation locator, stable JAIBA project-id, sanitized identity
candidate and executive context-id. A backend project may contain several
JAIBA projects; its label is not the logical project-id. The registry maps
exact canonical identity candidates/confirmed aliases to stable project IDs,
and lists contexts. Follow canonical origin normalization, nonportable root
fallback and explicit alias/rename authority; do not infer identity from titles.

**Owned physical record predicate**, checked after every ID read and before
any authoritative interpretation or write:

- Returned **server-rendered physical `Project` and `Scope`** equal the
  authorized backend project and `project`. Use the known response structure,
  not matching strings inside the stored body or the outer request-context
  project. Ambiguous body/footer boundaries or missing physical owner/scope
  block verification; content-only ownership is insufficient.
- Decoded transport envelope declares adapter/format version, exact namespace,
  backend project, record kind, exact record key and registry identity. Object
  records additionally match the full requested logical address (category/context
  included). Verify these against the trusted locator's expected envelope, not
  merely a self-asserted ownership marker.
- The exact locator is bound by the trusted registry/catalogue, with its
  expected record key and version/evidence; the root instead needs the explicit
  human-verified binding. Similar title, a search hit, an envelope alone or a
  numeric ID alone proves none of these.

This is **application-enforced namespace ownership**, anchored in physical
project/scope and a trusted exact locator chain, not a native namespace ACL.
Native topic keys are write-routing parameters: retain the submitted key and
acknowledgement/returned ID as routing evidence. For the T-009 **Topic-present**
profile, also require returned server-rendered `Topic` to equal the expected
allocated envelope/locator key; a mismatch or unexpected omission blocks use.
For an independently established **Topic-omitting** profile such as historical
read 24, verify the envelope key against the trusted registry/catalogue but
**do not claim it proves the native topic key**. Physical Project/Scope and the
trusted locator/envelope guards remain mandatory in both profiles. Do not
silently downgrade a Topic-present profile on a missing field; revalidate the
response framing/profile and completeness or stop. Neither profile makes
topic search/upsert an authoritative logical lookup.

Allocate each physical record's reserved routing key with a fresh UUID from an
actually available generator under the exclusive prefix; persist the intended
key in its envelope and owned publication/staging evidence. Serialize allocation
and check against all known allocated keys/locators, including staging and
retired records. Payloads, catalogue shards and publication manifests receive
distinct immutable version keys. Only mutable root/journal records keep their
allocated key and are updated by bound **ID**, not by topic upsert. Their
creation-time fingerprints are historical; verify their current exact wire
against captured prior/intended revision evidence under the storage protocol.
Never relax immutable child-locator fingerprint checks for mutable records.
UUID collision resistance is not proof of native uniqueness or CAS.
The namespace must be independently allocated exclusively to these writers;
if ordinary/external writers may use it, allocation or backend normalization
can collide, or the trusted locator chain cannot be established, block mutation
and report the missing guarantee. Safe encoding/normalization and collision
checks follow the storage protocol; T-009 demonstrated its tested allocation
and roundtrip, not unrestricted key normalization or universal collision safety.

Never use `mem_save` as a retry lookup for an existing key or as an ownership
test: its upsert may already mutate the wrong record before readback. Reconcile
known returned IDs by direct reads. If an outcome loses the ID and the trusted
publication/journal cannot recover it, stop with an unknown outcome for explicit
reconciliation; bounded search cannot prove safe retry or absence. Neither
native topic-key equality nor search-based enumeration is required for logical
lookup: only the complete owned catalogue supplies the address-to-ID mapping.

Registry/catalogue infrastructure is not a new OKF type or concept. Its root
has namespace/backend ownership, and its children have explicit registry and
project/context associations. Logical objects retain their contract addresses:
`(namespace, project-id, category, context-id?, logical-id)`.

### Root acquisition (no search-based absence)

1. Prefer a previously confirmed **exact numeric root ID** plus registry ID
   and expected namespace/backend ownership and root record key in routing
   configuration. Directly read and verify it. A changed/missing/inaccessible root blocks reuse; do not
   find a replacement by title or bootstrap an empty brain.
2. Without a root binding, bounded `mem_search` may show candidates in the
   authorized project/scope. Full-read each proposed candidate and ask the human
   to confirm the exact root and ownership. Search cannot prove uniqueness,
   absence or complete root discovery, even with an exact-looking topic query.
3. No verifiable candidate means **unresolved root**, not `not-found`. Ask the
   namespace owner for its exact locator. Only explicit authorization to
   provision a new exclusive namespace, with an independently established
   collision-free allocation, permits `jaiba-init` to bootstrap a root.
   Search returning zero is not that allocation evidence. Otherwise stop.
4. Under serialized namespace ownership, save the authorized new empty root
   with its exact reserved key, `scope:"project"`, `capture_prompt:false` and
   authorized backend project. Full-read/verify the returned physical record,
   then persist its exact locator by verified binding readback. This creates
   routing infrastructure, not an instrumented brain or backend project.

No registration hack, backend session-start side effect, fuzzy title choice,
or implicit filesystem fallback is part of bootstrap.

## 3. Representation and catalogue

Use a versioned, lossless transport envelope in observation `content`. Backend
`type:"manual"` classifies transport only; **OKF type belongs inside the full
logical object**, not a coerced Engram type. Preserve all twelve constitutive
types (`index`, `project`, `architecture`, `purpose`, `scope`, `sub-unit`,
`quality-gate`, `convention`, `decision`, `reference`, `snippet`, `log-entry`)
and executive `prd`, `plan`, `tasks`, `walkthrough`. Unknown/missing types remain
in unfiltered inventory with findings, not silently discarded or recast.

Each object envelope retains its address, type as found, complete metadata
(including nested unknown keys), full body, relations with original forms and
unknown relation metadata, original source/layout representation, and source
revision provenance. No executive template or legacy document becomes a summary.
Internal relations target logical addresses; physical IDs are replaceable
locators. Preserve/report unresolved/external links without inventing targets.
Legacy absent frontmatter/raw documents and deterministic entry mappings survive
interchange unchanged. Do not force filesystem legacy→bundle conversion.

The registry references a **complete authoritative managed catalogue** of
published logical addresses, physical version locators, types, lifecycle state
and full revision evidence, including unlinked logs and malformed objects.
Its registry inventory includes all identity aliases, projects and contexts,
including empty contexts. An unregistered save is staging, never published
logical memory. Every adapter writer must publish through this catalogue;
uncontrolled writers invalidate completeness and block mutation/cleanup.

`catalog(scope,type?)` follows the bound root and every referenced page/shard,
validates ownership and versions, consumes explicit continuation to an explicit
end, and checks declared entry counts/uniqueness. Filter types only after
complete unfiltered traversal. Return page continuation and `complete:false`
until every page is verified; expose malformed entries instead of omitting them.
No search, recent context, index Markdown links or top-k result can replace this.
Traverse retirement tombstones as catalogue infrastructure for completeness
and retry checks, but exclude retired addresses from the active logical object
inventory. They are not new work or new OKF concepts. Preserve their recovery
evidence separately; an export declares any included retirement/history records.
Before accepting completeness, re-read the root/publication revision under
serialized access. A changed root, dangling page, duplicate logical ID,
unreadable/truncated record or missing termination invalidates the result.

The completed [storage protocol](storage-integrity.md) specifies sharded
catalogues, reversible encoding, chunk reconstruction, staged version manifests
and publication/recovery. Follow its exact locator, page/count/digest and root
recheck rules rather than inventing a second layout here. T-009 demonstrated
the scoped multi-page/large-content roundtrip above. Validate applicable host,
computation and tested bounds before reuse; block dependent operations without
that evidence. This demonstration does not cover arbitrary size/depth or hosts.
All storage roles (registry, catalogue, payload versions, chunks and staging
journals) remain under the exclusive prefix with explicit role ownership.

## 4. Revisions, serialization and receipts

No exposed tool offers revision CAS, native locks, atomic multi-record
transactions or catalogue snapshots. `expected_project` protects only physical
project ownership. Establish an actual single-writer handoff for each executive
context and serialize constitutive writes, logs and **shared catalogue/root
publication across contexts**. If external writers cannot be excluded, block
mutations. Pre-read/write/readback is not atomic exclusion.

Revision evidence covers the **entire** decoded logical object, including
unknown metadata, body, relations and preserved original representation. Use
the storage protocol's token-preserving canonical `C(value)`, exact byte counts,
computed SHA-256 and complete intended-versus-observed byte/value comparison.
Map key order is canonicalized; array order, numeric token distinctions and
string bytes remain significant. Do not normalize body whitespace/Unicode/newlines.
Use actually available, verified computation tools; no invented digest,
timestamp, preview or revision counter alone establishes integrity. Retain
root/publication revision evidence too. Source revisions remain provenance,
not target write tokens. Protocol availability is not computation verification.

Every mutation result identifies contract/version, adapter/binding, operation,
full scope/address, stable request ID, verified prior revision/absence,
result revision and **full intended-versus-observed readback** evidence.
Archive evidence also binds close ID, exact immutable log address/revision and
the frozen executive inventory with full payload evidence. Receipts may be
workflow documents/tool results, not machine routing data. Report completed,
failed, unknown and residual objects separately on interruption. An ACK without
successful readback is an unverified outcome, never permission to clear work.

## 5. Operation recipes

These are logical workflows, not new tool names. Every recipe first checks
canonical selection/dependencies, exact ownership, authorization, permissions,
limits and writer discipline. All saves use explicit backend project,
`scope:"project"`, reserved exact topic key and `capture_prompt:false`.
All ID updates use `expected_project:<authorized-backend-project>` after full
physical and logical ownership checks. No operation edits ordinary memory.

### probe / resolve

1. Rediscover this agent's schemas and call `mem_current_project(directory)`.
   If needed use `mem_list_projects` or the actual ambiguity recovery flow
   for a human-authorized backend project, never infer logical identity.
2. Acquire/verify the exact registry root as above. Enumerate the full registry
   to resolve exact canonical identity/alias; zero matches requires explicit
   association or authorized init, multiple matches are a conflict.
3. Verify the bound stable context in the registry, not the latest plan.
   Confirm creation or existing-context resume/handoff before writes.
4. Report selected contract, binding, ownership, availability, capabilities,
   visibility/permissions, limits and consistency model. Full-read required
   constitutive entry concepts before declaring instrumentation. An empty
   confirmed catalogue routes to authorized init; a failed read is not empty.

### catalog / read

1. Traverse all authoritative catalogue pages for exact project/category/context
   as in §3; return completion/revision evidence and optional exact type filter.
2. Resolve an address to its published physical version locator. An address
   missing from a fully verified catalogue, or explicitly retired there, can
   return scoped logical `not-found`; an unavailable locator for a live entry
   is an integrity/access error, **not** logical absence.
3. Call `mem_get_observation({id, project:<backend-project>})`, verify physical
   owner despite the project argument, envelope and complete version. Follow
   the integrity manifest through all chunks to its explicit end when needed.
4. Return the complete decoded object and revision with `complete:true` only
   after exact reconstruction and verification. Unknown response format,
   omitted ownership, truncation or missing chunks blocks authoritative use.

### create / update

1. Authorize the category writer and fully enumerate/read the scope. Create
   requires authoritative logical absence; an existing or retired/reserved ID
   is a collision, not permission to reuse. Update requires a live full object
   and matching pre-read revision; it never implicitly upserts absence.
   Reject ordinary update/retirement of constitutive `log-entry` objects;
   immutable history is changed only by appending a separately identified entry.
2. Preserve all unmodified/unknown fields. Follow the storage protocol's
   journal/allocation sequence before staging any new physical payload version
   using `mem_save` with a unique reserved request/version key. Because save can
   upsert/dedupe, verify the returned ID, physical project/scope and entire
   intended envelope/payload, including its allocated record key. Record the
   submitted native topic key as write-routing evidence; independently verify
   native Topic when the established response profile exposes it, under §2.
   An ID colliding with another allocated record is a conflict;
   stop publication and report any possible write effects. Stable request IDs
   identify reconciliation; retry through known physical locators, not blind saves.
3. Follow [integrity publication](storage-integrity.md). Retain the prior live version; full-read
   and verify every staged record before publishing its locator. Re-read the
   prior object and catalogue/root evidence immediately before publication;
   divergence is a conflict. Stage immutable replacement shards and publication
   manifest, then publish only by updating the exact owned root's live pointer
   via `mem_update({id, expected_project, content:<whole-new-wire>})`, retaining
   its pending journal until verification. Never edit live shards in place.
4. Full-read the publication and the resolved logical object. Compare all
   intended fields and retained unknowns, then return the verified receipt.
   Failed publication/readback leaves old work intact or outcome unknown; stop
   dependent writes. Reconcile exact root/staging IDs before retry, never
   overwrite a historical version to make a mismatch disappear.

### append-log

1. Allocate/preserve a stable close/change ID **before** the first attempt.
   Enumerate all constitutive log entries; the close-ID index/catalogue must
   establish exact uniqueness, including logs unlinked from the brain index.
2. Existing same close ID and identical full payload: full-read/verify it and
   return the existing address/revision receipt without another save. Same ID
   with different payload is `conflict`; no edit of the historical entry.
3. Otherwise create a new `log-entry` using the create protocol, recording
   close ID, context and frozen inventory evidence. Read back fully before
   reporting verified append. Corrections are new IDs/entries, never updates
   or deletes. Unknown append outcomes require exact reconciliation first.

### archive / clear-work (logical retirement)

1. Conduct verifies closed work and cleanup approval; completely enumerate the
   exact context, read every object and freeze addresses/revisions/full payload
   evidence. Unexpected/unknown objects block cleanup, not invite omission.
2. Append the closing immutable log idempotently. Directly full-read it and
   verify the close ID, inventory evidence, full payload and resulting revision.
   Return archive receipt bound to that inventory. On failure retain all work.
3. Re-enumerate the context and re-read every inventory revision immediately
   before retirement, under serialization. Any new, unexpected or changed
   object blocks cleanup despite the existing archive. Previously verified
   retirement markers from this same close ID are retry evidence, not new work.
4. Retire **only** the unchanged known executive addresses in the authoritative
   catalogue through the same journaled immutable-publication/root-update
   workflow, not an in-place shard update. Each logical
   tombstone retains address, previous locator/revision and archive/close ID.
   Do not mutate payload versions or logs. This removes work from the active
   logical surface while retaining physical observations/history for recovery;
   it is not physical erasure. `mem_delete` is unavailable and not needed.
5. Read back catalogue publication and re-enumerate: each retired address must
   resolve to explicit retirement/scoped logical absence. Verify no new work,
   other contexts, ordinary memories or constitutive logs were retired. Report
   exact completed/failed/unknown/residual inventory on partial outcomes; retry
   only unchanged residuals against the same verified archive. Never bulk-purge
   a namespace, backend project, category, search results or host session.

### export / import boundary

Export composes complete catalogue + full reads with the canonical interchange
manifest: preserve every logical ID, original form, metadata, relation, log
close ID and source revision. Name all included/excluded contexts; an inaccessible
context is not empty. Recheck the full source inventory/revisions after capture.
An incomplete export cannot authorize migration or source cleanup.

Import composes authorized create into a separately identified **staging** target
with a migration/request ID; reject collisions and preserve source provenance,
not source physical IDs as target identities. Record any explicit approved
project/context remapping. Verify every staged object, full target inventory,
relations and unchanged source before explicit human-approved activation.
Keep source authoritative/intact through verification; no automatic binding
switch, dual writing, source retirement or merge. Full migration/journal and
activation workflow implementation belongs to the later migration task, not
this initial adapter or a claim of executed portability.

## 6. Limits, failures and validation

Transport follows protocol 1's exact `JAIBA1.<base64(C(envelope))>` wire,
canonical logical values, reversible raw-byte representation and chunk/page
rules. T-009's independent audit established these **largest successfully
read-back wire sizes in bytes**, not backend maxima or portable safe caps:

| Record role | Observed wire bytes |
|---|---:|
| Payload chunk | 22963 |
| Journal | 8467 |
| Root | 2075 |
| Descriptor page | 7483 |
| Object manifest | 2811 |
| Allocation page | 5899 |
| Catalogue shard | 5379 |
| Publication manifest | 5259 |

Use `independent-audit.json` for corrected per-role sizes; `live-summary.json`
had a response-size sampling bug. Application request JSON serialization and
returned-value sizes were audited separately; **actual MCP/network overhead
and backend binary version remain unknown**. No absolute observation/request/
response/page maximum is certified. Exact tested Unicode/source preservation
does not establish all possible text transformations or hidden-field visibility.
Revalidate applicable evidence for the active host/schema; block affected writes
without a tested computation/budget profile or return `limit-exceeded` before
mutation. Never derive safe thresholds from search/context budgets. No
truncation, summarization, unknown-field dropping or guessed limits are acceptable.

Map actual server errors to canonical outcomes without claiming undocumented
error shapes. Permission-denied, hidden/partial pages, unavailable versions,
unresolved root, stale catalogue, truncated reads and unknown write outcomes
are not absence. On partial publication stop cleanup, retain known prior and
staged locators, report exact effects and reconcile by direct reads. Do not
retry as a fresh create or silently select filesystem/another backend.

Schema discovery and historical read 24 are distinct from the executed T-009
owned-scope evidence in §1. Scoped ownership/readback, complete traversal,
create/update, log retry/conflict and single-object retirement passed there;
native error recovery, interrupted residual retirement and export/import/
workflow integration remain unverified. T-008 fixtures and static gates are
not additional live evidence. Revalidate after tool/backend/adapter/contract
changes; the package remains **draft/unverified** until every required path
is validated. No installation, consumer activation or real project migration
was performed by the trial or this evidence refresh.

Optional coordination is reserved under a **different** exclusive namespace,
with a consumer-supplied coordination-id and separately verified permissions.
It is not implemented, not one of the sixteen OKF types, not a project ID as
mission identity, and not permission for cross-project memory mutation.
