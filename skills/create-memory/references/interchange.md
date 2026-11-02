# Neutral surface-to-surface interchange

This document defines a portable, declarative interchange envelope between
any two compatible memory surfaces under the `jaiba-memory-surface` contract.
Either endpoint may use a filesystem or external backend representation;
each representation is declared by its binding/adapter, not assumed to be a
filesystem layout. It does not implement export/import or activate a new
authority. Consumers first resolve the effective
`create-memory` installation and its canonical `memory-surface-contract.md`;
cross-installation use must not assume sibling files were installed.

The transfer profile below completes the adapter mappings under contract
**1.0.0**, not a second contract or storage SDK. Resolve the effective
`jaiba-init` installation separately for `references/surface-migration.md`
and `assets/migration-journal-template.md`. Those own orchestration, approvals,
writer handoff and activation; this reference owns the shared interchange
fields and verification rules used by **both** endpoint mappings. Definitions
do not establish operational conformance or make a draft adapter selectable.

## Manifest contents

An interchange manifest is a complete inventory, not a summary. Use
`assets/interchange-template.md` as the human-readable envelope. A serialized
manifest must carry at least:

- contract identifier/version, source binding, namespace, stable project
  identity, selected scope with category/context inventory, source/target
  representation and adapter, and completeness status;
- every in-scope logical object, with full content, complete metadata
  (including unknown keys), type as found, relations, original relation and
  document representations, logical address, source locator, and source
  revision evidence;
- source inventory/traversal evidence, declared exclusions and inaccessible
  roots, limits, and enough representation-specific information to restore
  the source representation without rewriting it;
- for legacy objects, the complete raw source document and deterministic
  section/entry mapping, preserving absent frontmatter and unknown material.

For a resumable transfer, populate the template together with these explicit
records (embedded or referenced by exact verified artifact locator). They are
the same neutral format for filesystem and Engram, not backend-native exports:

| Record | Required transfer evidence |
|---|---|
| Manifest identity | Stable transaction ID, manifest ID/revision, contract/version, source and intended target binding/adapter/version, state/completeness, approved scope and approval references. |
| Registry inventory | Namespace, stable logical project IDs, sanitized identity candidates and approved aliases; every declared context, including empty ones, marked included or explicitly excluded with reason/approval. Record registry revisions and complete traversal evidence. Backend project/account keys are separate physical routing fields, never logical project IDs. |
| Address/restoration mapping | Each full source logical address → approved target address, source representation/locator → target representation/locator; stable logical ID retained. Include original filename/extension, raw byte encoding, bundle index paths or legacy document/view anchors, and distinct filesystem root per context. Record remaps explicitly, including namespace/project/context changes and their relation-target mapping. |
| Complete object | Full content, type as found, all metadata, relations with ordered targets/unknown fields/original forms, original raw representation and source revision. Preserve unknown optional envelope/object extensions as opaque lossless values; unknown required extensions block use, not silent downgrade. |
| History | Immutable historical payloads and stable close IDs with original log address/revision and frozen archive inventories when present. Preserve missing historical metadata as missing; do not fabricate close IDs or append new closure logs during import. Declare included histories/tombstones separately from the active object inventory. |
| Integrity/completion | Fingerprint method/version, exact coverage/normalization, byte counts/digests and complete payload comparison evidence, catalogue/registry counts and explicit traversal ends, findings/limits/exclusions. Include snapshot readback and source re-enumeration/revision evidence. |
| Target attempt/receipt | Journal transaction and per-object request IDs, exact intended payload/locator, proven prior absence, known effects/outcome, target revision and full readback evidence. Source revision remains provenance, never a target concurrency token. |

Preserve filename extensions and representation-specific unknown fields even
when the target has no native filenames/frontmatter. Preserve absent versus
null and raw non-JSON metadata without lossy coercion. The manifest's referenced
payloads must be fully accessible and integrity-verified; a digest, preview,
summary or expired attachment alone is not a complete object record. Transport
IDs/chunks and target receipts do not replace portable logical addresses.

Never replace content with summaries, omit unlinked log entries, coerce
unknown types, or treat omitted/inaccessible roots as empty. Historical
legacy entries with no type remain represented with original content and a
missing-type finding; absence of a modern type does not omit them or prevent
lossless preservation. An incomplete
manifest is explicitly incomplete and cannot authorize migration, cleanup,
or an assertion of full portability. Checkout paths are provenance/locators,
not portable project IDs.

The context inventory describes the declared registry, not merely contexts
having objects. An approved smaller scope needs its own complete manifest
revision and explicit limitations; retain the earlier incomplete result.
Resolve shared constitutive authority and excluded-context routing before any
switch. Scope expansion, alias/remap changes or a different target need renewed
approval and invalidate dependent verification; they are not retry defaults.

## Export and staging

Export only an exact, resolved ownership scope after complete enumeration and
full reads. Declare namespace and list all contexts in the selected scope,
including contexts with no objects; each object records its own category and
context. Preserve stable logical IDs and original source revision evidence.
Recheck source inventory and revisions after export; changes during
capture require reconciliation and a fresh verified export.

Import stages into separately identified destination roots. Keep the source
authoritative and intact. Preserve logical IDs, types, full content, unknown
metadata, relations, log close IDs, and original forms; any project/context
remapping must be explicit, approved, and recorded. Physical locators may
change, but logical relation targets must resolve in staging and ordinary
file-relative Markdown links must be serialized for the target layout.
Collisions are conflicts; never merge or overwrite silently.

Read back every staged object and compare complete payloads, metadata,
relations, and target inventory for missing or extra objects. Recheck source
revision evidence and repeat staging verification if the source changed.
Multi-hop transfer between physical protocols (`filesystem`, `JAIBA3`, and
`posix-file/1`) has verified lossless evidence under trial `6c90b698-39ba-441e-9c63-35ba9f9055c3`,
confirming fail-closed rejection of `digest-mismatch` (corrupt chunk) and
`symlink-root` (decoy target) before write.
Partial or unverified staging is not activation. Switching the effective
binding requires explicit human approval after complete verification; retain
the source through verified activation. Source retirement is a separate
explicit decision. No fallback or dual-write is implied.

## Transaction resume and activation barrier

Use init's durable, user-visible journal outside both catalogues and routing
storage. The approved snapshot is read-only after verification; a source
change creates a new manifest/snapshot revision in the **same transaction**,
retaining old evidence and invalidating dependent staging/activation checks.
Never mutate source memory to make export agree with a snapshot.
An explicitly reconciled changed payload gets a new journaled child request/
version ID under that same transaction; never repurpose an existing request
ID for different bytes. Preserve previous staged generations and collision
findings; replacement staging needs explicit authorization, not blind overwrite.

Journal phases are `preflight → snapshot-verified → staging-pending →
staging-verified → activation-pending → active-verified`; `blocked` and
`outcome-unknown` retain the last verified state. Each side effect has a stable
request ID and intent recorded **before** dispatch, then full verified receipt
or explicit failed/partial/unknown status. Adapter storage journals supplement,
not replace, this cross-surface journal.

| Resume observation | Required action in the original transaction |
|---|---|
| Exact owned staged result belongs to this request and matches the full intended payload | Verify/reuse its existing receipt and locator; no create or duplicate log append. Matching content alone does not prove request ownership. |
| Proven never attempted, or conclusively failed with exact absence/no side effect | Recheck ownership, scope, absence and all prior revisions before the journal-authorized attempt with the original request ID. |
| Known locator but readback missing, partial or different | Directly reconcile the exact intended/previous state; stop dependent writes. Do not overwrite partial data or issue a fresh request to hide it. |
| Save ID lost, routing outcome unknown or ownership unprovable | Keep unknown status and reconcile the exact request/binding using retained receipts and trusted locators. Search or a new UUID cannot establish nonexecution. No blind retry. |
| Already active by this request | Re-resolve actual routing, verify complete target inventory/revisions and entry concepts, then reuse activation evidence. Do not import again. |

Before activation, compare the complete target inventory and context registry
with the approved manifest after recorded remaps: no missing, extra, duplicate
or unexpected objects. Full-read **every** payload, metadata/extension/relation
and raw representation against its intended target value; verify source
lineage and independent target revisions. Reconstruct chunks to a verified
end. Internal targets must resolve; preserve external and source-unresolved
links with explicit findings. Link serialization changes require approved
mapping and retained original forms, not silent payload normalization.

Re-enumerate and recheck **all** source and staged target revisions, including
registry/aliases/empty contexts, after capture and immediately before the
confirmed binding change under actual writer serialization. A change invalidates
the barrier, not merely a count. Request new explicit human activation approval
for that verified manifest revision. After routing mutation, re-resolve actual
host precedence, read back routing/registry and the complete active surface,
and compare revisions again. A storage-root publication is not a binding switch.
Partial staging remains unpublished to consumers; activation failures pause
writers with exact effects recorded, without assumed rollback or fallback.

## Representation preservation

For filesystem bindings, both concept bundle and legacy flat layout remain
valid. Do not require conversion to interchange or restore either layout.
For every binding, record the source representation and adapter-specific
information needed to reconstruct it. Bundle inventory respects
`index.md` paths and includes all objects and `log/` entries. Legacy
inventory preserves `constitution.md`, `adr-log.md`, `reference-index.md`,
and `log/` as raw documents plus deterministic logical mappings; it does not
add frontmatter or rewrite those documents. A source containing both
`index.md` and `constitution.md` is ambiguous and blocks interchange until
resolved by a human.

Separate executive contexts remain separate. A selected scope may contain
multiple contexts, but inventory each individually and select distinct
destination roots/adapters for each; do not collapse plans or work
inventories into one `.ai/work/`. If a source root cannot be read, name it
as excluded and mark the manifest incomplete.

## Closure archives

An archive used for clear-work must be immutable and identify the verified
closing log by stable close ID, logical address and revision, together with
namespace/project/context, exact complete executive inventory (each object's
logical address and revision), and payload evidence. Read the log back by exact
identity before any clearing. Re-enumerate and verify that every known work
object is unchanged; new, unexpected, or changed objects block clearing.
Clear only those exact unchanged objects under serialized access and verify
the final state. Keep the archive and source evidence.

The existing filesystem-only `skills/conduct/scripts/archive.sh` now uses
explicit `prepare` and `archive` modes with project/context arguments and
filesystem/serialized-writer attestations. Prepare freezes a visible
`jaiba-close-v1` receipt in the summary: stable close ID, exact root/project/
context scope, summary-body fingerprint and presence/revisions of the four
executive files plus `.gitignore`. Archive checks that receipt and complete
payload, creates without overwrite or reuses an identical closing log, verifies
log readback, rechecks inventory/log before each selective deletion and reports
residual work on failure. It retains `.gitignore`; it rejects unexpected work,
changed payloads/inventory and unsafe roots. Retrying uses the frozen close,
not a newly derived date/ID.

These are scoped helper guarantees under caller-established serialization,
not native CAS, generic complete-surface conformance, or a migration receipt.
The helper neither exports/imports neutral manifests nor operates an external
surface, changes bindings, inventories multiple contexts or proves portable
logical identity/registry coverage. This definition does not invoke it or
claim that transfer/recovery/activation paths were operationally exercised.
