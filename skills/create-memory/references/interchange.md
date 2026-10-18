# Neutral surface-to-surface interchange

This document defines a portable, declarative interchange envelope between
any two compatible memory surfaces under the `jaiba-memory-surface` contract.
Either endpoint may use a filesystem or external backend representation;
each representation is declared by its binding/adapter, not assumed to be a
filesystem layout. It does not implement export/import or activate a new
authority. Consumers first resolve the effective
`create-memory` installation and its canonical `memory-surface-contract.md`;
cross-installation use must not assume sibling files were installed.

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

Never replace content with summaries, omit unlinked log entries, coerce
unknown types, or treat omitted/inaccessible roots as empty. Historical
legacy entries with no type remain represented with original content and a
missing-type finding; absence of a modern type does not omit them or prevent
lossless preservation. An incomplete
manifest is explicitly incomplete and cannot authorize migration, cleanup,
or an assertion of full portability. Checkout paths are provenance/locators,
not portable project IDs.

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
Partial or unverified staging is not activation. Switching the effective
binding requires explicit human approval after complete verification; retain
the source through verified activation. Source retirement is a separate
explicit decision. No fallback or dual-write is implied.

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

The existing `skills/conduct/scripts/archive.sh` has narrower behavior: it
moves a summary file and removes known work files after script preconditions.
It does not itself provide the above immutable close identity, complete
inventory binding, verified readback, or stability guarantees. This
interchange definition neither changes nor invokes that script, and does not
claim that a compliant importer/runtime currently exists. Migration
implementation is reserved for Phase 5.
