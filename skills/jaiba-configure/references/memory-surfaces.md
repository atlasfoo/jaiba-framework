# Memory surface setup — discovery and optional installation

This is machine setup guidance, not a second surface contract. Resolve the
current host's effective `create-memory` installation and read its canonical
`references/memory-surface-contract.md` (`jaiba-memory-surface` 1.0.0),
`resolution.md` and `filesystem-surface.md`. Use its interchange reference
only to explain transfer requirements, not to perform migration here.
Missing, ambiguous or unsupported definitions block dependent work. Never
resolve by sibling paths, a source checkout or another host's installation.

## 1. Inventory visible installations

- Start with the identified host's actual exposed skills and documented
  effective installation resolution. Corroborate global inventory from step 3
  with host visibility; a CLI list alone does not establish runtime exposure.
  Inspect local installations only for an explicitly identified work root.
  With no project target, report global visibility only, not a project selection.
- Read declarations as data under the global contract §4.5. A selectable
  declaration has `category: memory-surface`, stable `adapter-id`, adapter
  `version`, `contract-id`/`contract-version`, `requires`, capabilities,
  operation mappings, limits and applicable conformance evidence. A tag or
  name containing “memory” is not enough; `create-memory` is a generator,
  not itself an adapter. Record malformed declarations as findings.
- Report `memory-surface-draft` separately: a package is selectable only
  when `category: memory-surface`. `memory-surface-draft` is not a
  conforming selectable mutable adapter. The first-party Engram package
  `jaiba-engram-memory` is `memory-surface` with verified conformance on
  finite trial evidence (T-086/T-087); bounded trial evidence does not certify
  other hosts or production scopes.
- Report exact ID/version, effective local/global path, host visibility,
  contract compatibility, required tools/permissions and verification limits.
  Check this agent's actual callable schemas and authorized non-destructive
  permission evidence, not parent tools, names, old ATL entries or presumed
  MCP server access. Do not write test records, install services, change host
  permission configuration, acquire credentials or invoke adapters as scripts.
- No optional adapter installed is normal filesystem-capable core setup.
  Missing optional `mcp:engram` affects only the adapter/role declaring it;
  absent tools and unverified access remain distinct. Never mark core skills
  missing or claim MCP verified merely because a package is installed.

## 2. Explain selection without changing configuration

Apply the canonical order: explicit project `AGENTS.md` data field
`jaiba-memory-surface: filesystem` or an exact adapter ID → host-visible
installed project-local adapter → host-visible installed global adapter →
built-in filesystem. Duplicate/conflicting override fields are ambiguous.
An explicit unknown, invisible, draft or failed adapter is a blocked selection,
not permission to ignore the override or use filesystem.

For the same ID, host-resolved local wins over global even if older; unresolved
same-level copies need disambiguation. Multiple different IDs at the winning
level require explicit human choice. Do not choose a lower level to escape
ambiguity. Recompute precedence: a remembered binding may retain a confirmed
choice for an unchanged candidate set, but is not an override or fifth level.
A changed set needs confirmation. Selected-adapter failure never permits
silent fallback, another project/context or a new empty brain.

Global adapter installation is a desired skill destination, not automatic
migration or authorization to supersede existing local memory. Installation
can change future candidate precedence; show that consequence before consent.
With existing `.ai/` memory/work, require a separately confirmed filesystem
exception (normally the explicit `filesystem` override, written only through
an authorized project workflow), or hand off an explicit migration request to
the independently resolved effective `jaiba-init:migrate-surface` operation
(`references/surface-migration.md`). Configure performs neither operation.
If local and external stores are both populated, stop for an explicit
authority/collision decision; never prefer timestamps, merge, ignore, retire
or dual-write stores. An unreadable store is not empty. Configure reports
these obstacles without applying overrides or changing bindings.

## 3. Offer only the optional first-party Engram package

1. Keep `jaiba-engram-memory` out of `assets/skillset.txt`. After core setup,
   offer **decline**, **inspect existing**, or **install for inspection**.
   Generated user-approved adapters remain explicit extensions; configure
   never auto-installs third-party packages or their dependencies.
2. Reuse exactly the one validated manifest `ref:` read in step 3, checked
   against the packaged `version:` frontmatter. No valid pin means no optional
   fetch. Instructional notation `atlasfoo/jaiba-framework#<validated-ref>`
   must be instantiated from that value at execution: present the concrete
   actual source#ref in the user-facing manifest and never execute a placeholder,
   substitute a branch or infer a second release. Do not claim that a release contains
   the package without evidence; unavailable at that pin means pending, not
   permission to fetch HEAD or bump the framework version.
3. Obtain explicit choice of **host**, **project-local or global** scope,
   exact target root/destination, and **files** to install/change. Local scope
   requires the chosen project's exact work root. Use the existing pinned
   per-skill installation/fallback pattern from step 3 with only the optional
   package name substituted; no new CLI syntax is implied. Verify current
   host targeting support before any package-manager action. If it cannot
   constrain writes to the approved host/files, stop or propose the already
   documented pinned-copy fallback with a newly confirmed file manifest.
4. Show a pre-install manifest: skill, literal source#ref, host, scope,
   destination files, conformance status, requirements and precedence impact.
   Preview package contents at that ref before authorizing destination writes;
   do not execute fetched scripts. No silent install, automatic `-y`, implicit
   service setup or blanket permission changes. Changing the manifest requires
   renewed consent. Declining leaves files and explicit configuration untouched.
5. Preserve existing local/global copies and customizations. An identical
   package is a no-op; a different one needs a diff, explicit replacement
   consent and the main skill's dated backup before any overwrite. Never
   reinstall an already-global package into a local destination merely because
   it was discovered globally, or override a local copy with a newer global one.
6. After an approved install, read back the approved files/version and verify
   actual host discovery/registration using its documented surface. File copy,
   lockfile, registration and callable MCP permissions are separate evidence.
   Report an invisible install as unavailable to this host, not activated.
   Keep draft metadata and limitations intact; do not promote category or
   conformance status, change active bindings or start a consumer.

## 4. Identity, instrumentation and staged handoff

Inspection never mutates routing bindings. Registration, registry aliases and
constitutive creation belong to `jaiba-init`, not machine configuration. Any
separately authorized future machine-routing change is limited to sanitized
IDs/locators/versions under `~/.jaiba/memory/`, keyed by exact host identity
and normalized absolute work root. Apply the canonical root/origin, exact
registry lookup and stable project/context rules; do not guess IDs from a
basename, branch, session or latest search result. That separate authorization
must name the routing fields/diff and verify readback; no payloads, raw remote
URLs, credentials or `.ai/` mirror/cache. No implicit binding writes here.

A binding, package install or successful probe is not instrumentation:
external instrumentation requires the valid binding **and** real complete,
readable constitutive catalogue and required entry concepts in the owned scope.
External `.ai/` and the root marker are optional. Do not declare a project
uninstrumented just because those local files are absent. `.atl/tool-layout.md`
always stays local at the work root; recommend a local doctor probe even when
there is no `.ai/`. Configure does not run that probe or create project files.

**Effective capability gate:** setup may resolve/inspect within its authorized
scope, but installation is not consumer activation. Each external `conduct`,
`ask`, `fast` or battery call requires its effective surface procedure, actual
callable tools, exact ownership, verified required capabilities and applicable
approval. Missing/unverified requirements block dependent operations; never
substitute filesystem consumers to bypass them. Draft Engram remains nonselectable
until required operational conformance; install, authoring, probe and fixture
success never promote it.

Migration involving populated stores requires the separately resolved effective
init's explicit `migrate-surface` procedure and canonical neutral interchange,
even with an override or saved binding. Require complete source/target catalogues
and full reads, actual writer pause, explicit no-merge collision decisions, a
durable same-transaction journal for unknown outcomes, full staged verification
and separate human activation with routing/active readback. Preserve source;
no automatic purge, dual-write or retirement. Source-outage recovery requires
init's qualified stale-snapshot decision and later-write reconciliation, never
silent empty fallback or an invented current-source verification. Hand off to
`jaiba-init` for authorized registration/instrumentation or explicit migration
and `jaiba-doctor` for diagnostics; mention them, do not invoke or perform their
work inline.
