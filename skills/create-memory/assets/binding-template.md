# Machine memory binding template

This is an illustrative routing record, **not an activated configuration**
or an executable schema. Replace placeholders only after following
[resolution](../references/resolution.md) and the effective installation's
[surface contract](../references/memory-surface-contract.md), version
`1.1.0`. Resolve these references through the selected `create-memory`
installation; do not choose a backend-specific contract copy. A 1.0.0
record is a legacy input to consolidation, not this template.

Persist a completed record only at:

`~/.jaiba/memory/bindings/<sha256(canonical-work-root)>.yaml`

The digest is the resolution formula: SHA-256 of the UTF-8 canonical
work root, 64 lowercase hex characters, no prefix. The canonical string
is the absolute resolved directory, separators normalized to `/`, with
no trailing `/` unless the path is exactly `/`. The same formula is the
one surface `binding-path` calculations and the contract use. The
filename stem must equal `work-root.sha256`.

The path is shared by every agent runtime of this user for that work
root. `host-agent-id` is not a directory and not a file key. Do not
write `~/.jaiba/memory/<host-agent-id>/`. Do not copy this record into
project memory or commit a machine binding. A session-only selection
uses the same routing fields in session state and must not be described
as this file or as saved.

```yaml
binding-format-version: "2"
# Host that last completed routing readback. Provenance, not a key.
last-verified-by: "<host-agent-id>"
last-verified-at: "<UTC-timestamp>"
created-at: "<UTC-timestamp>"
# Non-secret discriminator for local-path identities. Not a path component.
machine-id: "<non-secret-machine-discriminator>"

work-root:
  canonical: "<absolute-resolved-path-separators-/-no-trailing-slash>"
  sha256: "<64-lowercase-hex-chars>"

contract:
  id: jaiba-memory-surface
  version: "1.1.0"
surface:
  adapter-id: "<filesystem-or-exact-visible-adapter-id>"
  adapter-version: "<version-actually-read>"
  # Adapter category, not constitutive/executive.
  category: memory-surface
  # Same-level candidate IDs at the confirmed selection.
  # Not a precedence tier. Re-confirm if this set changes.
  confirmed-candidate-ids: []
  namespace: "<exact-JAIBA-owned-namespace>"
  registry-locator: "<sanitized-exact-project-registry-locator>"

project:
  project-id: "<stable-registry-project-id>"
  # Choose ONE identity variant below; omit the other variant's fields.
  identity:
    kind: git-remote
    host: "code.example"
    path: "Group/App"
    # port: "<non-default-port-only-if-present>"
  # For local-remote, git-root, or workspace-root instead:
  # identity:
  #   kind: "<local-remote-or-git-root-or-workspace-root>"
  #   host-id: "<non-secret-machine-discriminator>"
  #   path: "<canonical-absolute-path>"
  # Optional exact registry alias identifier, never an invented mapping.
  # alias-id: "<confirmed-surface-registry-alias-id>"

executive:
  context-id: "<stable-context-id-for-this-work-root>"
  context-locator: "<sanitized-exact-context-locator>"

provenance:
  # Routing provenance only. Not a claim envelope.
  consolidated-from: []
  # chosen-legacy-locator: "<set-only-after-an-explicit-human-choice>"
```

Do not add `host-agent-id`, `active-procedure-reference`,
`procedure-provenance`, `conformance-status`, a certifying host, or an
installation path to this record. Procedure provenance stays in the
package claim envelope. Each session resolves its own compatible
`create-memory` and does not write that path back. The certifying host
of a package is provenance of that certification, not a constraint on
who may read this binding.

## Completion and reuse checks

- All angle-bracket values are placeholders, not usable identities. The
  example hostname and path are illustrative, not a default project.
  The known formula lock is the canonical string `/srv/checkouts/App`,
  digest `4c0e89ce280a2f213662e9e260df1380403db27e2096fedba7db3bc5c530ec63`.
  Do not hash a trailing slash or a `file://` URI.
- The v2 path is the only standard write path. A valid file there is
  reused by every agent for that canonical root, including when
  `last-verified-by` names a different runtime. Do not ask again for
  `project-id` or `context-id`. Recompute selection precedence and run
  the non-destructive readiness preflight anyway.
- Resolve explicit `AGENTS.md` override, local installation, global
  installation, then built-in filesystem. A remembered choice cannot
  override a new explicit selection or conceal a failed selected adapter.
- Package conformance certifies backend, tool version, physical
  protocol, and contract version. It is not stored here and is not
  redone because another host is resolving. Readiness failure
  (`missing-capability` names this host and the canonical `mcp:<server>`
  tool, or another contract error code) does not edit the package and
  does not change this record's project or context.
- Map `mcp:<server>` plus the published tool name to this host's
  exposure only during preflight. Do not record a host-prefixed alias
  such as `mcp__engram__mem_save` as a requirement in the package or
  in this file.
- Validate actual tools, supported contract and adapter versions, and
  exact namespace, project, and context ownership before writes. No
  unverified capability claim is stored as proof. A passed preflight
  may refresh `last-verified-by` and `last-verified-at` after readback.
  It must not switch adapter, project, context, namespace, or identity.
- Normalize remote identity without network access. Store no raw remote,
  userinfo, credentials, query, or fragment. The identity candidate must
  match a confirmed registry association, not a basename or fuzzy result.
- An origin change or moved fallback root needs explicit association.
  Alias authority remains in the surface registry, not this record.
  A new canonical directory is a new binding file.
- Keep context stable across branch, session, and agent changes. Use
  independent executive contexts for new work roots by default.
  Resuming an existing context on another root requires explicit
  selection and writer handoff. A different `last-verified-by` is not
  that handoff and is not a lock.
- Legacy records under `~/.jaiba/memory/<host-agent-id>/` are read for
  compatibility when the v2 file is absent. Consolidate only when
  blocking fields agree, or after an explicit human choice when
  `project-id`, `context-id`, adapter id, namespace, the sanitized
  identity candidate, or contract major disagree. Do not pick by host
  order. Read the new file back before claiming persistence. Leave
  every legacy file in place, unchanged. A malformed v2 file is not
  repaired from legacy. A valid v2 file is not rewritten because
  legacy files disagree.
- An open migration or recovery journal, an uncommitted executive
  journal, or an unknown mutation outcome blocks dependent writes until
  reconciled. It does not by itself invalidate this record or the
  package. An unreadable journal is not an empty one. This file stores
  no journal body.
- Existing populated stores require authority and collision resolution
  and, if transferring, verified migration plus explicit activation
  approval. Saving routing fields is not approval to switch authority.
- Store **identifiers, locators, versions, and routing provenance
  only**. No concepts, plans, summaries, catalogue dumps, mutation
  payloads, tool responses, or secrets. Sanitize locators before
  writing. Do not persist authentication material.
- Verify persistence by exact readback of the routing fields, the
  canonical path, and the digest. On inaccessible configuration, obtain
  explicit session-only consent or stop. Never claim a saved choice,
  write a host-keyed substitute, or create an `.ai/` cache. Do not
  persist a session-only record as if it were this file, or invent a
  new context on retry.
- A binding alone is not instrumentation: verify the real constitutive
  catalogue and entry concepts. Project `AGENTS.md` is optional
  externally. `.atl/tool-layout.md` stays local under every surface.
