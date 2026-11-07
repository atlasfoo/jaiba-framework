# Filesystem surface binding

This reference binds the `jaiba-memory-surface` contract (version **1.1.0**)
to the existing JAIBA filesystem layouts. Under contract 1.1.0, the
filesystem surface is classified as archetype **`document-tree`** (one
editable Markdown document per object). It is declarative guidance, not an
importer, runtime, SDK, or filesystem synchronization service. Consumers must
resolve the effective `create-memory` installation and read its canonical
`memory-surface-contract.md`; they must not assume sibling skills are
co-installed.

## Resolution and ownership

The project root is the checkout currently selected by the host. Resolve
`.ai/memory/` before any operation:

| Evidence | Layout and action |
|---|---|
| `.ai/memory/index.md` and no `constitution.md` | Concept bundle; resolve concepts through the index and its declared paths. |
| `constitution.md` and no `index.md` | Supported legacy flat layout; retain the source documents and map their logical contents losslessly. |
| Both entry files | Ambiguous; block access, export, and mutation pending human resolution. |
| Neither entry file | No resolved brain; do not manufacture one or claim an empty brain. |

The filesystem binding owns only the selected project's `.ai/memory/` and,
for a specifically selected executive context, its `.ai/work/`. It does not
own `.atl/tool-layout.md`, `.ai/vendored/`, another checkout, or ordinary
files outside those scopes. A checkout path is a locator, not a portable
project identity; resolve and persist the stable project identity separately.
Filesystem state is local to this checkout: it does not imply clone
synchronization, remote availability, or coordination with other checkouts.

Constitutive objects reside under `.ai/memory/`. In the bundle, the index
catalogues concepts and their existing relative file paths determine the
physical locators. Include every declared concept and every `log/` entry in
the inventory, not just objects linked from a curated subset. Preserve each
complete document, frontmatter, unknown metadata, relations, and original
representation. Where the filesystem and selected tool can store a complete
object and its ownership in one file, that file is the payload unit; the
catalogue/index remains an independent logical completeness requirement. Do
not add per-file journals, chunks, or manifests unless a characterized native
limit or verification gap requires them.

For legacy brains, map `constitution.md`, `adr-log.md`,
`reference-index.md`, and each `log/` entry as logical objects without
rewriting the source. Preserve the raw documents and frontmatter exactly,
including the absence of frontmatter. Deterministically identify logical
sections/entries using their source document and stable section/entry
identity; retain original byte/content representation so export and restore
are lossless. Do not invent OKF metadata or split, normalize, or discard
unrecognized sections. A legacy document may contain multiple logical
concepts; treat the complete raw document as the single persisted source
object, and record section/concept views as mappings into it, not duplicate
independently writable identities. An authorized view update writes the
shared source document as one unit after revision verification, preserving
all other views. `adr-log.md` and historical `log/` entries are immutable;
corrections are new entries, not edits.

Executive objects belong only to one explicitly resolved `.ai/work/`
context: `PRD.md`, `plan.md`, `tasks.md`, and `walkthrough.md`, when present.
Do not merge multiple executive contexts into a single `.ai/work/` root.
Each requires a distinct selected destination root and preserved context ID.
Other work files are not silently treated as concepts.

Under the `document-tree` archetype, each executive object maps as-is to its
corresponding Markdown file. The `patch` operation on an executive address
`(namespace, project-id, executive, context-id, logical-id)` is realized
directly as targeted, surgical text edits on `.ai/work/<file>.md` (such as
toggling checklist items `[ ]` to `[x]`, inserting task blocks, splicing
sections, or appending walkthrough notes) without rewriting unrelated
sections of the document. All invariants from `executive-journal.md`
(including the draft-only rule for `update-criterion` / `remove-criterion`,
and ID permanence) are strictly enforced prior to editing. Deterministic
materialization on filesystem is trivial: the document itself is the
materialized canonical state, so no external delta chain or `context-head`
record is required or stored on disk. Invoking `compact` on an executive
document is a no-op success. The conduct helper
`skills/conduct/scripts/archive.sh` is filesystem-only: explicit `prepare`
freezes a visible summary receipt with close ID, root/project/context scope,
body fingerprint and known inventory revisions; explicit `archive` verifies
that receipt and the identical immutable log, then rechecks inventory/log
before selective clear and verifies deletions. It preserves `.gitignore`,
rejects unexpected work/unsafe roots/changed payloads, and retries the original
close with residual-state reporting. Caller attestations are not locks.
See `interchange.md` for its exact boundary: these scoped guarantees do not
make the helper a complete surface, neutral transfer engine, external adapter
or binding-activation mechanism.

## Physical and logical addressing

Keep the contract logical address (namespace, project ID, category,
context ID when executive, logical ID) separate from its physical path.
Paths are current locators only; renames and layout changes must not change
logical identity. Assign IDs deterministically on first inventory from the
resolved namespace, stable project ID, category, context ID if any, source
representation, and normalized relative locator (for legacy views, raw
document locator plus stable section/entry anchor). Persist the ID-to-locator
assignment in the authorized binding/surface registry when that registry is
part of the resolved binding, or carry it as export lineage when no such
registry exists. The mapping contains identity and locator evidence only,
not duplicate memory payloads; do not add required metadata to concepts or
create a mandatory hidden mirror.

A path-derived first assignment cannot alone survive rename. Detect renames
through an explicit old-to-new locator alias/remap approved by the owner.
Verify old identity and complete revision, retain the same logical ID, and
record both locators before accepting the new one. Without provable
continuity or approved remap, report a possible new object/collision and
block reassignment; never infer identity from similar title or content.
Serialize ordinary
Markdown links as file-relative links appropriate to the restored layout;
retain relation targets as logical identities and preserve original link
representations. Internal relations must resolve after staging, while
external links remain external. Report unresolved targets instead of
guessing.

The complete inventory includes malformed or unrecognized content, unknown
metadata, relations, full content, and source revision evidence. Unknown
types are findings, not grounds for omission or coercion. Historical legacy
documents and log entries without types remain fully inventoried with their
raw representation and a missing-type finding; do not require new frontmatter
or omit them for that reason. A filesystem
revision may be a deterministic fingerprint over the complete logical
object and declared source representation; document its coverage and
normalization. Recheck the full source inventory and revisions before
activation or destructive work. A changing or incompletely readable source
blocks a complete-export claim.

Multiple selected roots must remain independently addressable. If any
required root is inaccessible, explicitly exclude it and mark the result
incomplete; never present a partial inventory as complete. No operation
silently discovers or adopts similarly named directories.

## Operation-family mapping

These are semantic bindings, not commands or new consumer behavior:

| Contract family | Filesystem realization |
|---|---|
| `probe` / `resolve` | Inspect the selected root and layout markers, report exact paths, project/context identity, readable/writable scope, supported semantics and limits; dual markers are ambiguous. |
| `catalog` / `read` | Enumerate every in-scope file/logical object and retrieve full source content, metadata, relations and revision evidence; traversal completion and inaccessible paths are explicit. |
| `create` | Check exact logical address and physical destination for absence, refuse collisions, create only within owned roots, then read back and verify. |
| `update` | Re-read and compare the complete source revision, preserve unmodified and unknown data, write the authorized change, then verify complete readback. Historical log entries are immutable. |
| `append-log` | Add a new immutable log entry with stable idempotency/close identity; exact readback verifies it. Existing entries are not edited to correct them. |
| `archive` / `clear-work` | First verify the closing entry and frozen, exact executive inventory; re-enumerate and compare unchanged revisions before removing only those objects in that context. The prepare/archive helper realizes scoped filesystem closure, not generic surface or migration conformance. |
| `patch` | On executive address `(namespace, project-id, executive, context-id, logical-id)`, realize directly as targeted, surgical in-document text edits on `.ai/work/<file>.md` without rewriting unrelated sections; enforce `executive-journal.md` invariants (e.g. draft-only criteria, ID permanence), check pre-read revision, and verify full readback. |
| `compact` | No-op success; the filesystem document itself is always in the materialized state with zero external deltas on disk. |
| `export` / `import` | Use the neutral manifest in `interchange.md`; stage into separately selected roots, read back all objects, compare inventory/content/relations and source stability, then require explicit human approval before authority changes. |

No atomicity, crash durability, serialization, or history behavior is
asserted here for filesystem operations; those properties depend on the
selected filesystem, tools, and configuration and remain unknown until
documented or observed in a contrasted profile. A successful write/readback
only verifies that read's bytes. Rename or replacement of one file does not
establish a transaction across payload, index, history, or metadata, nor
crash durability. A read-revision-write-read sequence is not CAS or
distributed exclusion. Where the required guarantees are insufficient or
unknown, block the dependent mutation/cleanup route and reconcile; do not
generalize that block to unrelated filesystem operations. Mutations and
cleanup require established single-writer serialized access and full pre/post
verification; without both, block them regardless of whether filesystem
atomicity is characterized. Filesystem acknowledgment alone is not
verification.

Use native history instead of snapshots only when fidelity and retention are
verified for the required recovery window. Otherwise retain snapshot-based
recovery. A multi-object migration journal remains required; simplifying a
single-file payload does not remove it.
This reference supplies the transfer mapping below, not an executable importer
or consumer activation. Init's effective migration reference owns orchestration.

## Neutral export, staged restore and resume

Use `interchange.md`'s **same neutral transfer records** for either direction,
not a directory copy offered as a complete manifest. Resolve ownership before
reading a source root or creating a destination: approved absolute real roots,
their namespace/project/context assignment, and ID-to-locator lineage. Check
every traversed path component for symlinks/escape and verify readable complete
scope; do not follow a link into unowned storage. Unsafe, inaccessible or
unrepresentable paths block the affected complete-transfer claim.

### Export to a read-only snapshot

1. Resolve the layout and the entire declared project/context registry, including
   empty contexts and exclusions. Freeze actual writers across all selected
   roots and shared constitutive authority. Enumerate unfiltered in-scope files,
   including all bundle concepts, index and unlinked logs; findings cannot hide
   unknown/malformed objects. Inventory unexpected work separately and block
   until scope/disposition is resolved, rather than deleting or coercing it.
2. Persist existing logical-ID assignments in the approved snapshot lineage;
   do not rederive IDs from restored filenames. Capture full bytes/content,
   frontmatter/unknown metadata, relations and their original forms, filename
   extensions and layout paths. Legacy raw documents are single persisted
   objects with deterministic section views, never converted or split copies.
3. Compute revisions using a verified deterministic byte/structured-value
   profile. Record exact raw bytes/length/digest **and** a fingerprint of the
   complete logical object (address/type, all metadata, content, ordered
   relations/unknown fields and original representation). Declare encoding,
   key ordering and normalization; no newline/Unicode or metadata loss. A raw
   file hash alone does not cover separately mapped relations/identity. Registry,
   locator/view mappings and context inventories have independent full evidence.
4. Write snapshot/manifest only at the approved transaction-artifact location;
   read back all payloads and complete inventories, then re-enumerate/recheck
   the source and registry. Seal that snapshot revision read-only. Source changes
   invalidate freshness; recapture explicitly in the original transaction.
   No export writes to source memory or creates a hidden mirror.

### Import from the neutral snapshot

1. Verify the complete snapshot and journal, target ownership and writer handoff.
   Approve an absent, separately selected staging scope; inspect any existing
   destination completely without modifying it. Address/path/alias/close-ID
   collisions conflict, even with matching content, except exact journal-proven
   results of this same transaction. No merge, overwrite or implicit remap.
2. Record a stable destination root per executive context and each constitutive
   root/replica with its authority policy. Each context uses its own workspace's
   `.ai/work/{PRD.md,plan.md,tasks.md,walkthrough.md}`; preserve IDs and names,
   never collapse contexts or substitute context subdirectories. No automatic
   clone synchronization follows. Roots must stay outside effective authority
   until verified activation; reject overlapping source/staging roots.
   Import operates on materialized canonical objects: restoring an executive
   object writes the file directly in its materialized state, requiring no
   delta journal or context-head on disk. Prior monolithic objects restore
   identically as implicit bases with zero deltas.
3. Journal intent, exact target path, approved address map, full intended bytes/
   logical value and proven absence before each create. Use actually available
   no-overwrite filesystem facilities under serialization, not an assumed atomic
   multi-file rename/transaction. Restore bundle paths/index or original legacy
   raw documents, absent frontmatter and section mappings losslessly. Preserve
   extensions, unknown optional extensions and historic log/close payloads.
   Import copies history; it does not invoke work closure or create new logs.
4. Serialize ordinary relative links for the approved target layout, preserving
   original forms and logical targets in lineage. Compare against the explicitly
   intended target serialization as well as the original source representation.
   If path constraints would require rewriting immutable historical payloads or
   cannot retain raw legacy form, choose an approved compatible layout or block;
   do not rewrite history as a transfer side effect.
5. Fully read back each created file and reconstructed logical object, compute
   independent target revisions and journal verified receipts. Re-enumerate
   all target roots and registry for exact manifest equality, including empty
   contexts and no extra files. Keep transaction control artifacts out of concept
   inventories. Preserve ID-to-locator mappings as authorized registry/lineage,
   not required new concept metadata or a mandatory hidden payload store.

### Interrupted filesystem attempts

Reopen the original transaction and exact paths, not a newly named destination.
For a known create intent, a fully matching owned file may be reused **only**
with journal proof of the request and full payload/revision verification. An
absent path after a proven failed/no-effect attempt permits a journaled retry
after full absence/scope checks; an unattempted path may be created. A partial,
different or unexpectedly missing verified file is a conflict requiring explicit
reconciliation, never permission to truncate/overwrite. Unknown outcomes remain
unknown until exact path/registry/receipt checks establish their effects. Do not
reappend imported history or delete residual staging to conceal an interruption.

Before requesting binding activation, repeat interchange's complete source and
target/registry revision barrier under actual serialization and obtain explicit
approval for that manifest revision. Init re-resolves/readbacks routing and the
active inventory; filesystem creation or successful static checks alone cannot
mark `active-verified`. Retain source, read-only snapshot and journal; neither
activation nor retry authorizes source/staging cleanup or fallback.
