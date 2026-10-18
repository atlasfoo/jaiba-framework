# JAIBA neutral memory interchange manifest

> Declarative template only. Populate from a complete, verified source
> inventory. This file does not perform export, import, migration, or
> authority activation.

## Contract and source

- Contract identifier/version: `[identifier]` / `[version]`
- Source binding: `[binding]`
- Namespace: `[explicit JAIBA-owned namespace]`
- Project ID: `[stable project identity]`
- Selected scope: `[categories and contexts included; contexts are separately inventoried]`
- Source representation/adapter: `[filesystem bundle | filesystem legacy | external binding/adapter and representation]`
- Target representation/adapter: `[selected destination binding/adapter and representation]`
- Source root locator(s): `[explicit roots; locator is not project identity]`
- Source revision/inventory evidence: `[method, coverage, evidence]`
- Enumeration status: `[complete | incomplete]`
- Limits and consistency: `[declared details]`

## Context inventory

List every context in the selected executive scope, including contexts with
zero objects. Category is recorded per object below, not as one
manifest-wide category.

| Context ID | Source representation/locator | Destination root/adapter | Inventory status |
|---|---|---|---|
| `[stable context identity]` | `[source context locator]` | `[distinct target root/adapter]` | `[complete | incomplete | empty, verified]` |

Constitutive scope is separately identified by namespace and project and has
no executive context ID.

## Exclusions and completeness

- Inaccessible or excluded roots: `[none | list each root and reason]`
- Unreadable, truncated, malformed, or unknown objects: `[none | exact findings]`
- Completeness statement: `[complete only when all in-scope roots and objects were fully read]`

## Layout restoration

- Original source representation and restoration evidence: `[binding-specific representation, markers, paths or external adapter form]`
- Bundle index/path mapping, if applicable: `[complete mapping]`
- Legacy raw documents and deterministic section/entry mapping, if applicable: `[complete mapping; preserve absent frontmatter and source bytes/content]`
- Separate executive context roots: `[one explicit root per context; do not collapse contexts]`

## Complete object inventory

For every object include the full content and complete metadata; do not use
summaries in place of payloads.

| Namespace | Project ID | Category | Context ID | Logical ID | Type as found | Source locator | Revision evidence | Payload / metadata / relations record |
|---|---|---|---|---|
| `[namespace]` | `[project-id]` | `[constitutive | executive]` | `[context-id or not applicable]` | `[stable logical-id]` | `[type or missing; preserve historical missing-type entries]` | `[path or adapter locator]` | `[complete-object revision evidence]` | `[reference to complete embedded object record]` |

Each complete object record includes:

- full original content and representation;
- all metadata, including unknown fields and any original frontmatter;
- relation source/targets, complete metadata, original representations,
  and explicit unresolved/external status;
- source revision and locator, plus deterministic identity-to-locator mapping;
- for an archive: stable close ID, closing log logical address and revision,
  and the complete executive inventory's logical addresses and revisions.

## Staging and verification record

- Destination project/context mapping: `[explicit approved mapping]`
- Destination roots: `[distinct selected roots]`
- Collision report: `[none | exact conflicts; never merge silently]`
- Target readback and complete inventory comparison: `[evidence or not performed]`
- Internal relation resolution and file-relative links: `[evidence or findings]`
- Source stability recheck: `[evidence or findings]`
- Verification outcome: `[verified | incomplete | failed | not performed]`
- Human activation approval: `[not granted | approval reference and scope]`
- Source retention/retirement: `[source retained; any retirement requires separate explicit decision]`
