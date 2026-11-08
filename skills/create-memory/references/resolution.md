# Memory surface resolution and bindings

This reference specifies selection and identity for the
[logical memory surface contract](memory-surface-contract.md),
`jaiba-memory-surface` **1.1.0**. It is additive over **1.0.0**: rules
below that are not amended remain in force, including how a `1.0.x`
adapter is still accepted by a 1.1 consumer. Resolve this reference and
its sibling contract from the effective `create-memory` installation,
not from a backend's alternative copy. It is a declarative workflow,
not a resolver runtime or permission to install tools, migrate memory,
or change authority. The [binding template](../assets/binding-template.md)
records only routing metadata; it is not a brain, a conformance record,
or a per-agent configuration.

Package conformance and session readiness are different claims.
Conformance is certified once, on the package. Readiness is this
session's non-destructive preflight. A binding is shared by canonical
work root across agent runtimes of this user. Neither claim is rewritten
because a different host is resolving.

## 1. Discover, select, then validate

Discovery considers only skills visible to the **current host agent**.
A repository checkout, another host's installation, a package on disk, or
an entry in a previous tool inventory does not establish availability.
An external adapter declares category `memory-surface`, a stable adapter
ID, adapter version, supported contract/version, requirements, and the
capabilities, limits and operation mappings required by the contract.
An ID identifies an adapter, not a project, namespace, or tool server.
Filesystem is the built-in surface, with no installation requirement.

### Step 0 — Binding-First

Before reading, listing, or testing `.ai/`, and before assuming a default
surface, establish the canonical work root `R` (§2). An unconfirmed root
is not hashed. Inspect:

`~/.jaiba/memory/bindings/<sha256(R)>.yaml`

That file is binding `v2`. Do not create it merely to test it. Do not open
`.ai/` to decide whether the file is worth opening.

**Valid v2 record.** It is the authoritative machine registration for this
checkout. It already names `surface.adapter-id`, `surface.namespace`,
`project.project-id` and `executive.context-id`. Project and context
identity are resolved in O(1) from those fields. Do not search the
backend, rank hits, scan the registry, or re-ask. Reuse them without
prompting, including when `last-verified-by` names another agent.

Precedence is subordinate to an explicit project override and to nothing
else. The only override is an `AGENTS.md` field
`jaiba-memory-surface: filesystem` or
`jaiba-memory-surface: <exact-adapter-id>`. If that field is absent, or
`AGENTS.md` does not exist (traceless), the binding governs
unconditionally. Do not apply the installed-skill list below, and do not
select built-in filesystem over it. A newly installed local skill is not
a higher-priority candidate that displaces the bound surface.

When the active surface — the binding's adapter, unless that explicit
field selected another — is external, do not test, list, or read `.ai/`
paths. Absence of those paths is expected, not evidence of an empty brain.

Still run session readiness on the active surface. A missing, failed, or
unavailable selected adapter blocks. It is not permission to use
filesystem or another adapter. An explicit override that names a different
surface selects that surface for this resolution; it does **not** approve
migration or a switch between populated stores.

**No v2 file.** Do not assume filesystem. Do not open `.ai/` until a step
below requires it. Absence of v2 is not absence of a project (§4 still
reads agreeing legacy records before this branch treats the root as
unbound).

1. Read `AGENTS.md`, if it exists, only as selection data. An explicit
   `jaiba-memory-surface:` field is a pin. No field is not a pin. A missing
   file is not a pin. Duplicate or conflicting declarations are ambiguous;
   do not choose by line order.
2. Before any fallback surface or new-project creation, resolve identity
   by the sanitized `git-remote` candidate from `origin` (§2). Look that
   candidate up by exact identity in the external surface's owned JAIBA
   project registry. The surface queried is the pin when the pin names an
   external adapter; otherwise the winning host-visible external adapter
   from the installed-skill list below. Ambiguous IDs at that level still
   need a human choice before the lookup. Filesystem has no external
   registry; do not invent one, and do not use filesystem to skip the
   lookup when an external surface can be queried.
3. An exact hit links that registered project. `jaiba-init` creates
   binding `v2` for this canonical root with the registry's stable
   `project-id` and a fresh per-root `executive.context-id` (the §3
   default), without search and without the ≤4-question questionnaire.
   Do not prompt. Do not pick another checkout's context. Search, titles,
   and basename ranking are not the lookup. A read-only consumer must not
   persist the binding, must not invent a filesystem brain, and must not
   declare the project absent because the local file is missing. It routes
   the link to `jaiba-init` and does not run the questionnaire.
4. Only an authoritative registry miss — not a permission error, a partial
   page, or a search miss — permits the rest of this branch. Multiple
   matches block. Do not create a second brain.
5. After that miss, a local `.ai/` directory is an unbound filesystem
   bootstrap or legacy repository. Check it only then. If there is also no
   `AGENTS.md` pin and no `.ai/` directory, the checkout is authoritatively
   uninstrumented. Do not manufacture memory. The ≤4-question questionnaire
   (`jaiba-init`, Issue #17 C3) runs only for that miss, and only in
   `jaiba-init`. It does not run because a binding file was absent on a
   machine that can still match `origin`.

The installed-skill list is not Step 0. It chooses which external surface
to query when no binding and no pin exist, and it is the selection order
only on the authoritative-miss path with no pin. It never outranks a valid
binding, and it never justifies reading `.ai/` first.

Use this precedence, highest first, only on that no-binding miss path:

1. Explicit project `AGENTS.md` field `jaiba-memory-surface: filesystem`
   or `jaiba-memory-surface: <external-adapter-id>`.
2. Installed project-local memory-surface skill visible to this host.
3. Installed global memory-surface skill visible to this host.
4. Built-in filesystem surface, and only when a local `.ai/` directory
   shows an unbound filesystem brain, or an explicit pin names
   `filesystem`. Do not select filesystem merely because nothing else
   matched.

The override is selection data, not executable instructions. Validate its
value against the built-in name or an exact declared ID. An explicit
external ID may identify a visible local or global adapter; an invisible,
unknown, or unavailable selected ID is an error. That error means this
host cannot see the selected adapter. It does not edit the package and
does not change a conformance status recorded on another copy. It does
not fall back.

At each installed level, collapse copies with the **same ID** using host
installation resolution; for the same ID at local and global levels,
local wins even when global has a newer version. Multiple unresolved
copies of one ID at the same level need explicit disambiguation. Multiple
**different IDs** at the winning level require explicit human selection,
not alphabetical order, version order, popularity, tool readiness, or the
first skill discovered. Do not select from a lower level to escape that
ambiguity. When no binding exists, a confirmed choice for that candidate
set is retained by writing v2 after the identity rules above, so every
agent runtime of this user sees the same choice. A changed set must be
presented for confirmation. Do not present it merely because another
agent is resolving.

A valid v2 binding is not a fifth level under the list above. It is Step
0. On each resolution, re-read only the explicit `AGENTS.md` override;
that field alone may select a different surface than the binding records.
Do not recompute installed-skill precedence over a binding that governs.
A new explicit override always wins over the bound surface, but does
**not** approve migration or a switch between populated stores. When no
binding exists, a new higher-priority installed candidate requires
revalidation and any necessary authority decision before writes. A
previously selected adapter that disappears or fails remains an
unresolved/failed selection, not a reason to silently use filesystem or
another adapter. Explicitly resolve or replace that binding with the
human.

After selecting, separate package conformance from session readiness
(below). Do not treat a readiness failure, a missing tool, or an
unreadable catalogue as absence, as an empty brain, or as a reason to
rewrite the package. An unsupported contract version is
`unsupported-version`, not a conformance re-run. File presence and
`.atl/tool-layout.md` are discovery evidence, not a successful tool
call. An `mcp:` row indexed there as unverified is not preflight
success.

### Package conformance

Package conformance is a property of the installed adapter package, not
of the host that happens to be resolving and not of the machine binding.
The built-in filesystem surface has no external package and no claim
envelope. An external package is selectable as a mutable surface only
when its recorded conformance status is verified **and** this session's
readiness preflight passes. A draft or unverified package stays
unselectable. Session readiness never upgrades that status.

The claim envelope certifies exactly these, together:

- backend identity and version
- tool versions, named by canonical server and published tool name
- physical protocol identifier and version
- contract identifier and version (`jaiba-memory-surface` and the
  declared `contract-version`)

The host that ran that certification is **provenance, not scope**. A
package certified on one agent remains certified for every other agent
that can select it. Do not re-run the conformance suite because the
resolving host changed. Do not edit package files, conformance status,
or procedure locators during resolution, preflight, binding reuse, or
legacy consolidation.

Persisted procedure identity is `procedure-provenance` only: the
generation-time locator, revision or digest, date, and resolution
method, kept as history. `active-procedure-reference` is not a
persisted field. Do not write it into the package, the profile, the
mapping, the conformance record, or the binding. If an older package
still contains it, ignore it. It is not the procedure to open, not a
compatibility key, and not authority. Do not rewrite the package to
delete it during resolution; removal belongs to generation or an
authorized upgrade, not to this workflow.

Each session resolves its own compatible `create-memory` and reads the
contract and this reference from that installation. Compatibility is
the contract that installation implements, not the skill's distribution
`version:` frontmatter and not a path stored in the package. Required
version is the package's declared `contract-version`, unless the claim
envelope names a higher minimum of the same contract. The resolved
installation must implement the same major and a minor greater than or
equal to that required minor. A different major, or a required minor
greater than this installation implements, is `unsupported-version`.
Acceptance is not symmetric with the contract's adapter rule: a 1.1
consumer may accept a `1.0.x` adapter, but a `create-memory` that
implements only 1.0.0 does not satisfy a package that requires 1.1.
Do not rewrite the package down to the older contract. If no
compatible installation is visible, or several remain ambiguous, stop.
Name the unresolved dependency. Do not open `procedure-provenance` as
if it still pointed at the procedure, and do not assume a sibling
directory.

### Canonical tool names

An external package declares MCP requirements as `requires:` entries of
the form `mcp:<server>` plus each required tool's name **as that server
publishes it**. The published name is the tool name a client calls on
that server. It is not a host exposure prefix, not a skill name, and
not an alias invented by an agent product.

Mapping a published name to the name this host exposes is session
preflight duty. It is never hardcoded in the package. Claude Code's
`mcp__engram__mem_save` is an exposure of server `engram`, tool
`mem_save`, on that host only. A package that lists the exposure as the
requirement has not declared the canonical tool. Resolution does not
repair that declaration and does not change conformance status. Stop
and name the package; upgrade or repair is a separate authorized
workflow.

This session may treat a host-exposed tool as the published tool only
when **this session's** tool catalogue shows that the exposure refers
to that server and published name. A remembered prefix table in the
package, a previous host's inventory, or a guessed `mcp__` spelling is
not that proof. If the alias cannot be proved, the tool is not visible.

### Session readiness

Readiness is a non-destructive preflight of the already selected
surface. It does not certify the package, invalidate it, or edit it.
Failure does not fall back to filesystem or to another adapter.

Run, in order, and stop at the first failure:

1. Resolve a compatible `create-memory` as above. Do not persist the
   path you resolved.
2. Confirm each required canonical tool is visible on **this** host,
   after the exposure mapping above. Filesystem declares no `mcp:`
   requirement; do not invent one. A required tool that is not visible
   is `missing-capability`. The result names this host-agent identity
   and the canonical tool (`mcp:<server>` plus the published tool
   name). It does not name a guessed exposure as the requirement. It
   does not set or clear the package's conformance status.
3. Probe the selected surface: contract/version, exact ownership,
   capabilities, limits, and permissions the contract's `probe` /
   `resolve` require. Do not create test memory. Probe success alone
   does not prove a complete read.
4. Read the exact catalogue of the bound scope. Search is not this
   read. An access failure, truncation, or incomplete page is not an
   empty brain and is not a conformance failure.

Other preflight failures use the contract's existing codes
(`unavailable`, `permission-denied`, `verification-failed`, and the
rest). They likewise leave package conformance unchanged. Do not
collapse every failure into `missing-capability`. Reserve that code,
here, for a required capability or canonical tool this host does not
expose, including a 1.1 `record-store` that lacks the executive journal
the contract already classifies that way.

A passed preflight means this session may operate the selected surface.
It is not a new certification and not permission to write while a
pending journal or unknown mutation blocks writes (§4).

### Selection examples

| Visible state | Result |
|---|---|
| Valid v2 binding; no `jaiba-memory-surface:` field, or no `AGENTS.md` | Binding governs. O(1) `project-id` and `context-id`. Do not read `.ai/`. Do not fall through to filesystem. |
| Valid v2 external binding; explicit override `filesystem` | Override selects filesystem. Not migration approval. Do not treat the override as a silent switch of populated stores. |
| Valid v2 binding for `alpha`; local skill `beta` newly visible | `alpha` still governs. A new local skill does not displace Step 0. |
| Override `filesystem`; local adapter `team-store`; no binding | Filesystem selected; no automatic export/import. |
| Override `team-store`; only its global skill visible | Global `team-store`, after real tool validation. |
| Override `team-store`; skill or required tool missing | Stop with selected-adapter failure; no fallback. |
| No binding; local `team-store` v1; global same ID v2 | Local v1 is the surface to query. Incompatible contract blocks use, not fallback to v2. |
| No binding; local `team-store`; global `personal-store` | Query local `team-store`. Existing data still needs authority checks. |
| No binding, no pin; local `alpha` and `beta` | Ask which ID before the registry lookup; do not pick by discovery order. |
| No binding; `origin` matches one registry project | Link and write v2. No search. No ≤4 questionnaire. Fresh per-root context. |
| No binding; `origin` not in the registry (authoritative miss) | Then pin / `.ai/` / uninstrumented. Questionnaire only in `jaiba-init`. |
| No binding, no pin, no `.ai/`, registry miss or no external surface to query | Authoritatively uninstrumented. Do not assume filesystem. |
| No adapters, no pin, no binding, no `.ai/` | Uninstrumented. Built-in filesystem is not a silent default. |
| Saved `alpha`; new override `beta` | Select `beta`, then resolve data authority before activation. |
| Verified package; this host sees the canonical tools and a compatible `create-memory` | Selectable. Do not re-run conformance or edit the package. |
| Verified package; a required MCP tool is not exposed here | `missing-capability` names this host and the canonical tool. Conformance status unchanged. No fallback. |
| Package requires a contract major this `create-memory` does not implement, or a higher minor | `unsupported-version`. Do not rewrite the package. |

## 2. Work root and project identity

First establish the exact work root from local Git metadata: the checkout
or worktree root, not its common Git directory. If there is no Git root,
use the absolute host workspace root. Multiple workspace roots or an
unknown root require a human choice. Do not infer a project from the
current directory's basename, a sibling folder, a branch, or a tool's
default project. Do not compute a binding path until this root is
established. An unconfirmed root is not hashed.

### Canonical work root

The canonical work root is the machine-local binding key. Surface
`binding-path` calculations and the global contract use this formula
and no other. This reference is that definition. Do not hash a URI, the
Git common directory, a relative path, a path with a trailing slash, or
a host-specific display name.

Given the established work root `R`:

1. Make `R` absolute. A relative path is not canonical. Do not accept a
   basename, a branch name, or a remote path in its place.
2. Resolve `.` and `..` and symbolic links to the local directory the
   filesystem opens for `R` (the POSIX `realpath` of that directory, or
   the host equivalent). This resolution is local. Do not contact a
   network, a Git host, or an SSH alias. If resolution fails, the path
   is not a directory, or two resolutions disagree, stop. Do not hash a
   partially resolved path and do not fall back to the unresolved
   spelling.
3. Normalize every native separator to `/`. Collapse repeated separators
   to one. Preserve a drive or volume prefix exactly as resolution
   returned it. Do not case-fold, Unicode-normalize, or percent-decode.
4. Remove a trailing `/` unless the path is exactly `/`.
5. The canonical string is that result. Encode it as UTF-8 with no BOM,
   no surrounding quotes, and no trailing newline. `sha256` is SHA-256
   of those bytes, written as 64 lowercase hexadecimal characters with
   no algorithm prefix.

The binding file name is that digest plus `.yaml`.

This canonicalization is only the binding key. It does not prove two
remotes are one project, does not collapse distinct Git worktrees, and
does not make paths equivalent across machines. Two checkouts whose
resolved directories differ are different work roots even when they
share a remote. Case folding remains not evidence of identity.

Known vector, formula lock only: the canonical string
`/srv/checkouts/App` hashes to
`4c0e89ce280a2f213662e9e260df1380403db27e2096fedba7db3bc5c530ec63`.
Do not hash `/srv/checkouts/App/` or `file:///srv/checkouts/App`.

For a Git project, use its configured `origin` as the preferred identity
candidate. Inspect metadata locally without fetching, contacting a host,
or printing secret-bearing remote URLs. Missing `origin` permits the
fallback below; malformed or ambiguous configured origins require
clarification, not silent fallback or selection of another remote. Never
persist the raw remote, credentials, userinfo, query parameters or fragment.

### Remote normalization

Normalization yields an identity candidate, not proof of ownership or
an instruction to connect to that address:

- Parse standard HTTPS/HTTP, SSH URL and SCP-style SSH forms. Remove
  transport syntax and userinfo; lowercase the DNS host. Retain the full
  namespace and repository path, including nested namespaces.
- Normalize path separators to `/`, repeated separators and trailing
  separators; remove one terminal `.git` suffix. Preserve path case:
  `/Team/App` and `/team/app` are not automatically equivalent. Preserve
  meaningful path encoding; do not decode an escaped separator into a
  different namespace or lowercase an entire URL.
- Drop standard transport-default ports from the candidate. Retain a
  non-default port as part of the host identity; different custom ports
  are not assumed to name the same service. If equivalence is uncertain,
  request a confirmed alias rather than guess.
- Omit query and fragment from the sanitized candidate, never store them.
  If they could affect repository selection, require confirmation of the
  sanitized identity before use. An unsupported or lossy parse blocks
  automatic association. Do not resolve SSH host aliases through network
  access or assume an alias is the public hostname.
- Local path and `file://` remotes use a normalized absolute local path,
  resolving a relative remote against its checkout root. Normalize `.`
  and `..` and native separators. Retain volume and case-sensitive path
  components; do not assume cross-machine or symlink equivalence. Include
  the local host identity for local-path identities; a nonlocal file
  authority or unclear path semantics needs explicit clarification.
  When that local path is on this machine, use the canonical work-root
  formula above so the identity path and the binding key do not diverge
  by spelling. That still does not make a different machine's path the
  same identity.

Use an unambiguous structured representation such as
`{kind: git-remote, host: code.example, path: Group/App}` rather than a
concatenated basename. Local remotes use
`{kind: local-remote, host-id: <host>, path: <absolute-path>}`.
These are routing identifiers, not connection URLs.

If no origin exists, use the canonical work root as a fallback candidate
when the root is a Git checkout; without Git, use the same canonical
form of the host workspace root. Represent it with kind `git-root` or
`workspace-root`, host ID and that canonical path. A fallback is
nonportable and must be visibly labeled as such. Unresolved symlinks,
case folding, or path aliases are not evidence that two fallback
identities are the same project. The binding key may still collapse two
spellings of one directory on this machine; that file sharing is not a
registry merge.

When a valid v2 binding exists for this canonical root, identification is
already finished. `project.project-id` and `executive.context-id` are the
identity. That read is O(1). Do not search the backend, rank titles, or
re-query the registry to confirm who the checkout is. Still run readiness.
An explicit `AGENTS.md` override may select a different surface; it does
not replace those IDs and does not approve a store switch.

When no local binding exists — a new machine, or a fresh clone — derive
the sanitized `git-remote` candidate from `origin`
(`{kind: git-remote, host, path}`, §2). Look that candidate up by exact
identity in the external surface's owned JAIBA project registry before
any fallback surface or new-project creation. Fuzzy search cannot
establish the hit. An exact hit links that project: `jaiba-init` writes
binding `v2` with the registry `project-id` and a fresh per-root
`context-id`, without search and without prompting. The ≤4-question
questionnaire does not run. A read-only consumer does not write the file
and does not fall back while that link is outstanding. Only an
authoritative miss — not a permission error, a partial page, or a search
miss — requires explicit association or authorization for `jaiba-init`
to create a project, and only then does the ≤4-question questionnaire
(C3) trigger. Multiple matches are an identity conflict. Do not create a
second brain to bypass it. The binding retains the stable resolved
`project-id` and sanitized candidate, not a display-name guess.

### Aliases, renames and identity examples

Aliases are human-confirmed exact mappings to a stable `project-id`,
recorded in the **surface project registry** under declared JAIBA
ownership. A machine binding may retain their identifiers, but is not
the authority for an alias. Adding or changing a registry association is
a constitutive identity change owned by `jaiba-init`, not an incidental
read or adapter installation side effect. Check collisions before adding
an alias; one identity must not silently map to two projects.

| Input/change | Interpretation |
|---|---|
| `git@code.example:Group/App.git` and `https://code.example/Group/App/` | Same sanitized host/path candidate, without a network request. |
| `ssh://git@code.example/Group//App.git` | Same candidate after separator normalization. |
| `https://code.example/Group/App.git` vs `https://other.example/Group/App.git` | Different hosts; same basename does not establish identity. |
| `Group/App` vs `group/app` on the same host | Distinct until explicitly confirmed as aliases. |
| SSH nickname `work-git:Group/App.git` vs `code.example/Group/App` | No assumed equivalence; confirm registry alias. |
| Local remote `../shared/App.git` from `/srv/checkouts/dev` | Local host plus `/srv/checkouts/shared/App`, not a hosted repository identity. |
| Origin changes from `Group/App` to `Platform/App` | Stop automatic reassociation; confirm rename/alias or a different project. |
| No origin; checkout moves from `/srv/a` to `/srv/b` | New fallback candidate and a new binding key; explicit association required. |
| Two roots named `App` | Never merge by basename. |
| `/srv/checkouts/App` and a symlink that resolves to it | Same binding file on this machine. Not, by itself, the same portable project identity. |

Even when a changed origin already names another registered project,
reconcile the old binding explicitly before switching. A moved root or
changed origin must not inherit a former binding by heuristic. Clones
with the same normalized remote may resolve the same constitutive project,
but that fact does not select their executive context. Distinct canonical
work roots keep distinct binding files.

## 3. Executive contexts

Resolve constitutive memory at `(namespace, project-id, constitutive)`.
Resolve executive memory at `(namespace, project-id, executive, context-id)`.
The context ID is a stable opaque identifier persisted **per canonical
work root**, independent of branch, session, model, terminal, or which
agent last verified the binding. A new branch in the same checkout does
not automatically create or select a context. A different agent opening
the same canonical root does not create one either.

By default, clones and Git worktrees share the resolved constitutive
project and have **independent executive contexts**. A `git-remote`
registry hit on a root with no binding does not ask: write a fresh
per-root `context-id` with the link. Do not prompt, and do not borrow
another checkout's context. An explicit human request to resume an
existing context is the only reason to select one, and it is not part of
that link. On any other first association, confirm creating a fresh
context or explicitly selecting an existing one. Preserve the resulting
ID in the shared v2 binding. Never choose the latest plan, a matching
branch name, the first search result, another checkout's context, or
another agent's private legacy file because it appears active.

To resume elsewhere, the human explicitly selects the existing context
after an authoritative context lookup. Verify namespace/project ownership
and establish the single executive writer handoff before writes; two
roots bound to the same context do not grant concurrent writer rights.
Context-ID collisions or multiple possible contexts block selection.
Switching contexts retains the old work; it is not clear-work permission.
This reference does not add a lock protocol. A different
`last-verified-by` is not a second writer and is not a reason to ask
again. An uncommitted journal or an unknown mutation outcome is the
write barrier in §4.

Filesystem keeps `.ai/work/` **per checkout**, with its existing executive
filenames and layout unchanged. Its logical context denotes that checkout's
work, not a new context directory beneath `.ai/`. Selecting a context from
another machine does not magically expose its local files; that needs an
explicit supported transfer, not a path rewrite. See the effective
`create-memory` filesystem reference for its physical mapping.

## 4. Machine binding persistence

Store the machine routing record at:

`~/.jaiba/memory/bindings/<sha256(canonical-work-root)>.yaml`

`~` is this user's home directory. The file is shared by every agent
runtime of this user for that canonical work root. It is not shared
across users. `host-agent-id` is **not** a directory, a file name, or a
lookup key. The only key is the canonical-work-root digest from §2.
`bindings` is a fixed directory name, not a host id. Do not write a new
record under `~/.jaiba/memory/<host-agent-id>/`.

These paths are locators, not credentials. Basename keys, branch names,
and host names are insufficient. An implementation does not choose a
different encoding for v2: the path above is the standard path. Exact
comparison uses the canonical string and the lowercase digest, not a
display path.

A binding records only identifiers, sanitized locators, versions, and
routing provenance:

- `binding-format-version: "2"`
- `last-verified-by`: the host-agent id that last completed a successful
  routing readback. Provenance, not a key.
- timestamps of creation and last verification
- `machine-id`: a non-secret machine discriminator for local-path
  project identities. Not a file key.
- work root: canonical path and its sha256
- sanitized remote identity candidate, or the labeled nonportable
  fallback
- surface selection: adapter id, adapter version, contract version,
  category `memory-surface`
- namespace, stable `project-id`, executive `context-id`
- sanitized registry and context locators, confirmed candidate ids, and
  an optional confirmed alias id
- consolidation provenance: legacy locators read, and which record was
  chosen if a human had to choose

It must contain **no memory payload**, concept summaries, executive work,
journal bodies, receipts containing payloads, raw tool responses,
passwords, tokens, or credential-bearing endpoints. It does not copy
`conformance-status`, a claim envelope, or `procedure-provenance`.
Those stay in the package. It does not store `active-procedure-reference`
or a host-specific installation path. A stored installation path would
make another agent treat a shared binding as stale. Each session
resolves its own visible installation. A backend locator must be safe to
disclose; authentication stays in the host's existing credential
mechanism. This is not an `.ai/` mirror, shared project configuration,
or synchronization layer.

`surface.category` in the binding is the adapter category
(`memory-surface`), not the logical memory category. Constitutive versus
executive remains the address category, not a second binding file.

### Read and reuse

On each resolution, after the canonical work root is known:

1. Compute the v2 path. Do not create the file merely to test it.
2. If that file exists, parse it and read it back against this session's
   canonical string and digest. A valid v2 record has
   `binding-format-version` `"2"`, a `work-root.canonical` equal to this
   session's canonical string, and a `work-root.sha256` equal both to
   the filename stem and to the digest of that string. Reuse its
   `project.project-id` and `executive.context-id` without asking,
   including when `last-verified-by` names a different agent. Identity
   is that O(1) read. Do not search the registry to re-identify the
   checkout. Re-read only an explicit `AGENTS.md` override (Step 0); do
   not recompute installed-skill precedence over a binding that governs.
   Still run readiness. When the active surface is external, do not test,
   list, or read `.ai/` paths. A valid v2 record is authoritative over
   legacy files. Do not re-open a legacy disagreement, and do not merge a
   later legacy file over it.
3. If the file exists but fails those checks, stop. Do not overwrite it
   from legacy, from this host's memory, or from a guess. Retain it for
   explicit reconciliation. Do not print secret-bearing values. Legacy
   files are not a silent fallback for a malformed v2 record.
4. If the file does not exist, read legacy locations for compatibility
   as specified under legacy read and consolidation. Do not treat
   absence of v2 as absence of a project. If no legacy record matches,
   this is not yet "uninstrumented": apply Step 0's no-binding branch.
   Derive the sanitized `git-remote` candidate and look it up before any
   filesystem fallback or new-project creation. An exact hit is a link,
   not a questionnaire. Only an authoritative miss, with no pin and no
   `.ai/` directory, is an authoritatively uninstrumented checkout.

Validate a reusable binding against the explicit `AGENTS.md` override,
root, origin, adapter identity, and exact registry ownership before
writes. Do not recompute installed-skill precedence over a valid v2
record; that list does not outrank Step 0. A stale or invalid record is
not proof that a project is absent. Another agent's verification is not
a skipped ownership check. Readback of a safely written binding must
match the intended routing fields before claiming persistence.
Routing-field comparison is semantic for quoting; the canonical path
and digest are exact strings.

After a successful readiness preflight, this host may update
`last-verified-by`, `last-verified-at`, and the adapter version it
actually read, without asking. That update is routing provenance. It
must itself be read back. It must not change `project-id`, `context-id`,
adapter id, namespace, or the identity candidate. Those changes require
the human decisions this reference already requires. Do not update them
because this host is new.

### Legacy read and consolidation

Legacy 1.0.0 records live under `~/.jaiba/memory/<host-agent-id>/`, or
an equivalent 1.0.0 encoding that keyed a record by host-agent identity
plus work root. They are compatibility inputs, not the standard path.

Enumerate only immediate child directories of `~/.jaiba/memory/` other
than `bindings`. Do not follow a symlink out of that directory. Do not
search the rest of the filesystem. Do not treat `bindings` as a host
id. Within each legacy directory, consider `*.yaml` records.

A legacy record matches this work root only when its stored work root,
passed through the §2 formula, equals this session's canonical string.
A filename stem equal to the digest is additional evidence, not a match
by itself. If the stem equals the digest and the body is missing, does
not canonicalize, or canonicalizes to a different path, stop. That
record is a conflict for this root. Do not adopt it, delete it, or
ignore it. A record with no comparable work root and a different
filename is not a match. Leave it unread as authority and do not delete
it.

If no legacy record matches, this root has no machine registration yet.
That is not permission to assume filesystem or to open the questionnaire.
Apply Step 0's no-binding branch: pin, then the sanitized `git-remote`
lookup, then `.ai/` only after an authoritative miss. An exact registry
hit writes v2 as that link, with a fresh per-root context and no
questionnaire. An authoritative miss follows the identity and context
rules, and only then may `jaiba-init` run C3. Do not also write a
host-keyed legacy file.

If one or more legacy records match and they agree on every blocking
field below, consolidate once:

- Write a v2 record at the standard path from those agreed routing
  fields.
- `last-verified-by` is the host performing consolidation, and only
  after readback succeeds.
- List every legacy locator in consolidation provenance. Locators are
  sanitized paths under `~/.jaiba/memory/`, not file bodies.
- Read the v2 file back. Every persisted routing field, the canonical
  path, and the digest must match the intended record. If readback
  fails, do not claim consolidation, do not delete or rewrite legacy
  files, and stop.
- Preserve each original legacy file byte for byte as backup and as
  the fallback used only when the v2 file is absent. Do not rewrite
  legacy files in place, rename them over v2, or delete them after
  success.

Blocking fields, compared after the identity normalization in §2:

- `project-id`
- `context-id`
- adapter id
- namespace
- sanitized identity candidate (`kind`, host or host-id, path, and any
  non-default port)
- contract major (`jaiba-memory-surface` major). A `1.x` record and a
  `2.x` record do not agree.

A missing `surface.category` on a 1.0 record is not a conflict with
`memory-surface`. Adapter-version skew, contract minor or patch skew
within the same major, timestamps, host ids, installation paths, and
`last-verified-by` are not blocking. Record those differences in
provenance. Do not ask solely because they differ. If adapter versions
disagree, the consolidated record uses the version this session
actually reads from the selected visible package. Contract version in
the new record is the version that package declares. Note the legacy
values in provenance; do not leave the binding on a stale minor when
the declaration was read. Built-in filesystem has no external package. Its consolidated
`contract.version` is the version the resolved `create-memory`
implements, and only when that major agrees with the legacy records.
A 1.1 session and legacy major `1` therefore record `1.1.0`, with the
legacy value kept in provenance. Do not bump a major. If an external
package was selected and this session cannot read its declaration, do
not invent a version and do not write v2. Do not consolidate ahead of
selection.

`confirmed-candidate-ids` is not a blocking field. If several non-empty
lists disagree, keep them in provenance and set the field to their
intersection when that intersection is non-empty. If the intersection
is empty, stop and ask which remembered candidate set remains in force.
Do not union them. An empty list beside a non-empty list keeps the
non-empty list.

If any blocking field differs across matching legacy records, stop.
Present the differing fields and the legacy locators. Require an
explicit human choice of one record, or an explicit new association.
Do not pick by host name, directory order, mtime, lexical order, which
agent is running, or which file was found first. Do not write v2 until
that choice is made. After the choice, consolidate from the chosen
record only, read it back, and preserve every legacy file, including
the ones not chosen. Record which locator was chosen. The next agent
reads v2 and does not ask again.

### Binding examples

| State | Result |
|---|---|
| Valid v2 file for this canonical root | Same file, same `project-id` and `context-id`, any agent. O(1). Do not ask. Do not search. Do not read `.ai/` when the active surface is external. |
| v2 absent; no matching legacy; `origin` matches one registry project | Link. Write v2. No search. No questionnaire. |
| v2 absent; one legacy file, or several that agree | Consolidate to the v2 path with readback. Leave every legacy file in place. |
| v2 absent; legacy files disagree on a blocking field (`project-id`, `context-id`, adapter, namespace, identity, or contract major) | Stop. Human choice. Do not pick by host order. |
| v2 valid, and a disagreeing legacy file also exists | v2 wins. Do not re-consolidate. |
| v2 present but digest or canonical path disagrees | Stop. Do not repair from legacy. |
| Pending journal or unknown mutation on the bound context | Block dependent writes. Do not change conformance or mint a context. |

### Pending journal and unknown mutation

A shared binding does not grant a write. Before any dependent write —
create, update, patch, append-log, archive, clear-work, import
activation, or a binding change that switches project, context, or
adapter — establish that no transaction is still open for this scope.

Block dependent writes when any of the following is true:

- The effective `jaiba-init` migration or recovery journal has an open
  transaction, an uncommitted effect, or an unknown outcome for this
  project or context. That journal is not the executive journal. See
  §6. This reference does not perform the migration.
- The executive journal for this context, when the selected surface
  provides `executive-journal`, has an uncommitted transaction: a base,
  delta, or head write whose receipt is missing, whose readback does
  not match, or whose outcome is unknown. Classify the outcome with
  `executive-journal.md`, including its retry rule. Do not invent a
  second journal model here. A `document-tree` edit with an unknown
  outcome is the same barrier; absence of a stored delta chain does
  not mean the write is known.
- Any mutation by any agent, including this one, has an unknown outcome
  for an address this write would touch, including shared constitutive
  data.

An unreadable journal is not an empty journal. If the check cannot be
completed, mutation state is unknown and dependent writes stay blocked.
Name the pending journal or mutation, the `context-id`, and the other
agent when its identity is known. That identity is not authority to
proceed. Do not mint a context, fall back, start a local `.ai/` cache,
or change package conformance because a write is blocked. The binding's
`project-id` and `context-id` stay as recorded.

Non-destructive preflight may still run. Consolidation that only copies
already agreed routing fields into a missing v2 file may still run: it
does not switch identity and it does not write memory. Do not
consolidate by choosing a context while a conflict or an unknown
mutation is unresolved.

A different `last-verified-by` with no pending journal and no unknown
outcome is ordinary reuse. It is not a lockout. Writes remain under the
contract's single-writer rules. This reference defines no distributed
lock.

### Unwritable machine configuration

If machine configuration is inaccessible or unwritable, report that fact
and offer an **explicit session-only binding** with the same selection,
identity, and pending-write checks. Say that the choice will not survive
the session and will not be visible to other agents. Do not claim it was
saved, write a substitute under `.ai/`, write a host-keyed legacy file,
or silently mint a different context each time. If the human does not
accept session-only operation, stop. A later durable binding needs
confirmed association to the same project and context rather than
automatic recreation. Session-only state uses the same routing fields
and must not be described as the v2 file.

## 5. Existing data and instrumentation

Selection is not activation. Step 0 does not inventory `.ai/` when a
valid binding declares an external surface: do not test, list, or read
those paths to discover the surface or to decide instrumentation. The
populated-store check below is not Step 0. It runs on an explicit
transition request, or on first association when no binding exists and,
after the `git-remote` registry lookup, a local `.ai/` directory is
present. Before using an external surface for a root with existing
`.ai/` memory/work in that case, present either an approved migration
under contract §8 or an explicit filesystem exception (normally the
`filesystem` override). Preserve both supported filesystem brain layouts;
both concept and legacy entry layouts present is itself ambiguous.
Do not silently ignore local work, migrate merely to read it, or dual-write.
A shared v2 binding is not that approval.

If filesystem and external scopes are both populated, obtain an explicit
authority and collision decision. Inventory both completely, identify
project/context/address collisions, and keep the source authoritative
until a staged transfer is verified and activation approved. Neither
newer timestamps, a saved binding, another agent's `last-verified-by`,
nor override text authorizes overwrite, merge, retirement or cleanup.
Surface failure while checking either side does not prove that side
empty. Follow the effective `create-memory` interchange reference and
contract §8; this reference performs no migration.

External instrumentation requires a valid resolved binding **and a real,
readable constitutive catalogue** in the selected owned project scope.
A binding file, successful probe, AGENTS marker, search hit or empty
catalogue alone is not instrumentation. Verify the catalogue and required
constitutive entry concepts by full reads; an empty confirmed scope routes
to authorized `jaiba-init`, whereas access failure blocks work. External
mode may omit project `AGENTS.md` and `.ai/` entirely. Do not create a local
`.ai/` cache or marker as proof of external instrumentation. Do not treat
a passed cross-agent preflight as instrumentation by itself.

`.atl/tool-layout.md` always remains local at the work root, regardless of
surface or context. It is machine/toolchain evidence, never constitutive
or executive memory and never relocated into an external catalogue.

## 6. Unavailability, confirmed fallback and resumption

Preserve the last verified selection, authority and project/context identity
when a probe, catalogue, read or mutation fails. Distinguish unavailable tools
or backend, permission denial, incomplete data, unsupported capability and
unknown mutation outcome from authoritative absence. None authorizes init of
an empty brain, a new context, a lower-priority adapter or a local `.ai/` cache.
Draft/unverified adapters remain unselectable until required operational
conformance is established; an outage is no waiver. A readiness failure does
not change package conformance. A pending journal does not invalidate the
v2 binding.

Offer the human **retry the selected source after restoration**, **stop and
retain pending work**, or **explicitly request fallback/recovery**. Retry means
non-destructive availability/exact-state checks first, not replay of a possibly
successful mutation. Freeze dependent execute/validate/closure progress and
init, registry and append-log writers across contexts sharing constitutive
data (and shared publication infrastructure). Establish pause acknowledgements;
an offline service does not prove other writers stopped. Record exact pending
request IDs, known receipts/locators, prior/intended revisions and residuals in
the owning workflow's recoverable evidence, never in routing-only bindings.
If that evidence cannot be durably retained, stop before further side effects.
Another agent resolving the same v2 binding observes that barrier by the
journal and unknown-outcome checks in §4. It does not clear the barrier by
being a different host.

Fallback is **not** a resolver branch. Resolve the effective `jaiba-init`
installation independently and use `references/surface-migration.md` and its
same durable migration/recovery journal. A new recovery request opens that
journal before effects; an interrupted transfer reopens its original transaction.
Require a complete verified neutral snapshot: full bodies/original forms,
metadata, relations, registry/aliases/all declared contexts, revision provenance
and closure/residual evidence, not search, recent context, summaries or hashes
without payloads. No complete snapshot means retry or stop, not empty replacement.

With the source reachable, normal migration requires its current full inventory
and revision barrier. With source freshness unverifiable, use only init's
explicit **stale-snapshot recovery** decision and later-write reconciliation;
never report it as a current-source-verified migration. Target staging and full
readback, separate activation consent and actual routing/active readback remain
mandatory. Use distinct filesystem roots per executive context. Retain source
and evidence, with no merge, purge, dual-write or automatic failback.

An edited override or saved/session binding cannot bypass this barrier. On
partial activation, freeze all affected roots until exact routing/registry and
request outcomes are reconciled; do not assume either store is safely writable.
After verified activation, update only approved routing fields and hand off one
authority. When the old backend returns, reconcile possible later writes with
the human before resuming any writer or proposing a separate transfer back.
Consolidation of a legacy binding is not activation and not that handoff.
