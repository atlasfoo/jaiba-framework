# Filesystem surface binding

This reference binds the `jaiba-memory-surface` contract to the existing
JAIBA filesystem layouts. It is declarative guidance, not an importer,
runtime, SDK, or filesystem synchronization service. Consumers must resolve
the effective `create-memory` installation and read its canonical
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
representation.

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
Other work files are not silently treated as concepts. The conduct archive
script is a related existing operation, not a guarantee of this binding:
`skills/conduct/scripts/archive.sh` moves a `<slug>-summary.md` into
`log/` and removes four known executive files after its stated preconditions.
It does not implement the complete inventory, immutable receipt,
readback, revision-stability, or selective-clear guarantees of the surface
contract. Do not infer those guarantees from invoking or inspecting it.

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
| `archive` / `clear-work` | First verify the closing entry and frozen, exact executive inventory; re-enumerate and compare unchanged revisions before removing only those objects in that context. The current archive script does not establish this full contract by itself. |
| `export` / `import` | Use the neutral manifest in `interchange.md`; stage into separately selected roots, read back all objects, compare inventory/content/relations and source stability, then require explicit human approval before authority changes. |

File writes are not assumed atomic or serialized. Without an established
single-writer discipline and full pre/post verification, mutations and
cleanup are blocked. Filesystem acknowledgment alone is not verification.
No migration or consumer change is implemented by this reference; migration
implementation details are reserved for the approved later phase.
