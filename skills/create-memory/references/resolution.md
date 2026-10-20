# Memory surface resolution and bindings

This reference specifies selection and identity for the
[logical memory surface contract](memory-surface-contract.md),
`jaiba-memory-surface` **1.0.0**. Resolve this reference and its sibling
contract from the effective `create-memory` installation, not from a
backend's alternative copy. It is a declarative workflow, not a resolver
runtime or permission to install tools, migrate memory, or change authority.
The [binding template](../assets/binding-template.md) records only routing
metadata; it is not a brain.

## 1. Discover, select, then validate

Discovery considers only skills visible to the **current host agent**.
A repository checkout, another host's installation, a package on disk, or
an entry in a previous tool inventory does not establish availability.
An external adapter declares category `memory-surface`, a stable adapter
ID, adapter version, supported contract/version, requirements, and the
capabilities, limits and operation mappings required by the contract.
An ID identifies an adapter, not a project, namespace, or tool server.
Filesystem is the built-in surface, with no installation requirement.

Use this precedence, highest first:

1. Explicit project `AGENTS.md` field `jaiba-memory-surface: filesystem`
   or `jaiba-memory-surface: <external-adapter-id>`.
2. Installed project-local memory-surface skill visible to this host.
3. Installed global memory-surface skill visible to this host.
4. Built-in filesystem surface.

The override is selection data, not executable instructions. Validate its
value against the built-in name or an exact declared ID. Duplicate or
conflicting override declarations are ambiguous; do not choose by line
order. An explicit external ID may identify a visible local or global
adapter; an invisible, unknown, or unavailable selected ID is an error.

At each installed level, collapse copies with the **same ID** using host
installation resolution; for the same ID at local and global levels,
local wins even when global has a newer version. Multiple unresolved
copies of one ID at the same level need explicit disambiguation. Multiple
**different IDs** at the winning level require explicit human selection,
not alphabetical order, version order, popularity, tool readiness, or the
first skill discovered. Do not select from a lower level to escape that
ambiguity. A confirmed binding can remember that explicit selection for
the same candidate set; a changed set must be presented for confirmation.

A saved binding is not a fifth precedence level. Recompute precedence on
each resolution. A new explicit override always wins over a remembered
choice, but does **not** approve migration or a switch between populated
stores. A new higher-priority installed candidate requires revalidation
and any necessary authority decision before writes. A previously selected
adapter that disappears or fails remains an unresolved/failed selection,
not a reason to silently use filesystem or another adapter. Explicitly
resolve or replace that binding with the human.

After selecting, validate actual callable tools and permissions using
the adapter's declared requirements and non-destructive probes. File
presence and `.atl/tool-layout.md` are discovery evidence, not a successful
tool call. Probe the selected contract/version, exact ownership scope,
complete catalogue and full reads; establish the required mutation,
revision, receipt, archive and portability guarantees before advertising
a mutable surface. Do not create test memory merely to probe without
authorization. Report unverified capabilities honestly and block dependent
operations. Missing requirements, failed probes, unavailable services,
permissions and unsupported versions are failures, **not absence**.

### Selection examples

| Visible state | Result |
|---|---|
| Override `filesystem`; local adapter `team-store` | Filesystem selected; no automatic export/import. |
| Override `team-store`; only its global skill visible | Global `team-store`, after real tool validation. |
| Override `team-store`; skill or required tool missing | Stop with selected-adapter failure; no fallback. |
| Local `team-store` v1; global same ID v2 | Local v1; incompatible contract blocks use, not fallback to v2. |
| Local `team-store`; global `personal-store` | Local `team-store`; existing data still needs authority checks. |
| Local `alpha` and `beta` | Ask which ID; retain the confirmed choice in the binding. |
| No adapters or override, no failed prior binding | Built-in filesystem. |
| Saved `alpha`; new override `beta` | Select `beta`, then resolve data authority before activation. |

## 2. Work root and project identity

First establish the exact work root from local Git metadata: the checkout
or worktree root, not its common Git directory. If there is no Git root,
use the absolute host workspace root. Multiple workspace roots or an
unknown root require a human choice. Do not infer a project from the
current directory's basename, a sibling folder, a branch, or a tool's
default project.

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

Use an unambiguous structured representation such as
`{kind: git-remote, host: code.example, path: Group/App}` rather than a
concatenated basename. Local remotes use
`{kind: local-remote, host-id: <host>, path: <absolute-path>}`.
These are routing identifiers, not connection URLs.

If no origin exists, use the normalized absolute Git work root as a
fallback candidate; without Git, use the host workspace root. Represent
it with kind `git-root` or `workspace-root`, host ID and absolute path.
Canonicalize only what local metadata establishes; unresolved symlinks,
case folding or path aliases are not evidence of equivalence. A fallback
is nonportable and must be visibly labeled as such.

The candidate is looked up by exact identity in the selected surface's
JAIBA project registry. The binding retains the stable resolved
`project-id` and sanitized candidate, not a display-name guess. A complete
authoritative registry lookup can establish an unknown identity; fuzzy
search cannot. No match requires explicit association with an existing
project or authorization for `jaiba-init` to create one. Multiple matches
are an identity conflict. Do not create a second brain to bypass it.

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
| No origin; checkout moves from `/srv/a` to `/srv/b` | New fallback candidate; explicit association required. |
| Two roots named `App` | Never merge by basename. |

Even when a changed origin already names another registered project,
reconcile the old binding explicitly before switching. A moved root or
changed origin must not inherit a former binding by heuristic. Clones
with the same normalized remote may resolve the same constitutive project,
but that fact does not select their executive context.

## 3. Executive contexts

Resolve constitutive memory at `(namespace, project-id, constitutive)`.
Resolve executive memory at `(namespace, project-id, executive, context-id)`.
The context ID is a stable opaque identifier persisted **per work root**,
independent of branch, session, model or terminal. A new branch in the
same checkout does not automatically create or select a context.

By default, clones and Git worktrees share the resolved constitutive
project and have **independent executive contexts**. On first association
with an external surface, confirm creating a fresh context or explicitly
selecting an existing one. Preserve the resulting ID in the binding.
Never choose the latest plan, a matching branch name, the first search
result or another checkout's context because it appears active.

To resume elsewhere, the human explicitly selects the existing context
after an authoritative context lookup. Verify namespace/project ownership
and establish the single executive writer handoff before writes; two
roots bound to the same context do not grant concurrent writer rights.
Context-ID collisions or multiple possible contexts block selection.
Switching contexts retains the old work; it is not clear-work permission.

Filesystem keeps `.ai/work/` **per checkout**, with its existing executive
filenames and layout unchanged. Its logical context denotes that checkout's
work, not a new context directory beneath `.ai/`. Selecting a context from
another machine does not magically expose its local files; that needs an
explicit supported transfer, not a path rewrite. See the effective
`create-memory` filesystem reference for its physical mapping.

## 4. Machine binding persistence

Store machine routing configuration beneath `~/.jaiba/memory/`, keyed by
the current host-agent identity and normalized absolute work root. Host
identity here distinguishes agents/installations; local-path project
identities additionally need a machine discriminator. These are locators,
not credentials. An implementation may use encoded keys or nested files,
but exact key comparison must retain the full root and host identity;
basename keys are insufficient.

A binding records only identifiers, sanitized locators and versions:
adapter/contract, namespace, stable project/context IDs, sanitized origin
or fallback, registry locator, and any confirmed candidate selection.
It must contain **no memory payload**, concept summaries, executive work,
receipts containing payloads, raw tool responses, passwords, tokens or
credential-bearing endpoints. A backend locator must be safe to disclose;
authentication stays in the host's existing credential mechanism. This is
not an `.ai/` mirror, shared project configuration, or synchronization layer.

Validate an existing binding against current precedence, root, origin,
adapter version and exact registry ownership before reuse. A stale or
invalid record is not proof that a project is absent. Readback of a safely
written binding must match the intended routing fields before claiming
persistence. Do not overwrite a malformed or conflicting record blindly;
retain it for explicit reconciliation without exposing sensitive values.

If machine configuration is inaccessible or unwritable, report that fact
and offer an **explicit session-only binding** with the same selection and
identity checks. Say that the choice will not survive the session; do not
claim it was saved, write a substitute under `.ai/`, or silently mint a
different context each time. If the human does not accept session-only
operation, stop. A later durable binding needs confirmed association to
the same project/context rather than automatic recreation.

## 5. Existing data and instrumentation

Selection is not activation. Before using an external surface for a root
with existing `.ai/` memory/work, present either an approved migration
under contract §8 or an explicit filesystem exception (normally the
`filesystem` override). Preserve both supported filesystem brain layouts;
both concept and legacy entry layouts present is itself ambiguous.
Do not silently ignore local work, migrate merely to read it, or dual-write.

If filesystem and external scopes are both populated, obtain an explicit
authority and collision decision. Inventory both completely, identify
project/context/address collisions, and keep the source authoritative
until a staged transfer is verified and activation approved. Neither
newer timestamps, a saved binding nor override text authorizes overwrite,
merge, retirement or cleanup. Surface failure while checking either side
does not prove that side empty. Follow the effective `create-memory`
interchange reference and contract §8; this reference performs no migration.

External instrumentation requires a valid resolved binding **and a real,
readable constitutive catalogue** in the selected owned project scope.
A binding file, successful probe, AGENTS marker, search hit or empty
catalogue alone is not instrumentation. Verify the catalogue and required
constitutive entry concepts by full reads; an empty confirmed scope routes
to authorized `jaiba-init`, whereas access failure blocks work. External
mode may omit project `AGENTS.md` and `.ai/` entirely. Do not create a local
`.ai/` cache or marker as proof of external instrumentation.

`.atl/tool-layout.md` always remains local at the work root, regardless of
surface or context. It is machine/toolchain evidence, never constitutive
or executive memory and never relocated into an external catalogue.

## 6. Unavailability, confirmed fallback and resumption

Preserve the last verified selection, authority and project/context identity
when a probe, catalogue, read or mutation fails. Distinguish unavailable tools
or backend, permission denial, incomplete data, unsupported capability and
unknown mutation outcome from authoritative absence. None authorizes init of
an empty brain, a new context, a lower-priority adapter or a local `.ai/` cache.
Draft/unverified adapters (including `jaiba-engram-memory`) remain unselectable
until required operational conformance is established; an outage is no waiver.

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
