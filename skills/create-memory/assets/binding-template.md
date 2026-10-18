# Machine memory binding template

This is an illustrative routing record, **not an activated configuration**
or an executable schema. Replace placeholders only after following
[resolution](../references/resolution.md) and the effective installation's
[surface contract](../references/memory-surface-contract.md), version
`1.0.0`. Resolve these references through the selected `create-memory`
installation; do not choose a backend-specific contract copy.

Persist a completed record only beneath `~/.jaiba/memory/`, indexed by the
exact host-agent identity and absolute work root. File naming/encoding is
implementation-specific. Do not copy this record into project memory or
commit a machine binding. A session-only selection uses the same routing
fields in session state and must not be described as saved.

```yaml
binding-format-version: "1"
host-agent-id: "<stable-host-agent-installation-id>"
machine-id: "<non-secret-machine-discriminator>"
work-root: "<normalized-absolute-checkout-or-workspace-root>"

contract:
  id: jaiba-memory-surface
  version: "1.0.0"
surface:
  adapter-id: "<filesystem-or-exact-visible-adapter-id>"
  adapter-version: "<validated-version>"
  installation-locator: "<sanitized-visible-installation-locator-or-built-in>"
  # Identifiers of same-level candidates at the confirmed selection.
  # Not a new precedence tier; re-evaluate if this set changes.
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
  #   path: "<normalized-absolute-path>"
  # Optional exact registry alias identifier, never an invented mapping.
  # alias-id: "<confirmed-surface-registry-alias-id>"

executive:
  context-id: "<stable-context-id-for-this-work-root>"
  context-locator: "<sanitized-exact-context-locator>"
```

## Completion and reuse checks

- All angle-bracket values are placeholders, not usable identities. The
  example hostname/path are illustrative, not a default project.
- Resolve explicit `AGENTS.md` override, local installation, global
  installation, then built-in filesystem. A remembered choice cannot
  override a new explicit selection or conceal a failed selected adapter.
- Validate actual tools, supported contract/adapter versions and exact
  namespace/project/context ownership. No unverified capability claim is
  stored as proof; re-probe when resolving a session.
- Normalize remote identity without network access. Store no raw remote,
  userinfo, credentials, query or fragment. The identity candidate must
  match a confirmed registry association, not a basename or fuzzy result.
- An origin change or moved fallback root needs explicit association.
  Alias authority remains in the surface registry, not this record.
- Keep context stable across branch/session changes; use independent
  executive contexts for new work roots by default. Resuming an existing
  context elsewhere requires explicit selection and writer handoff.
- Existing populated stores require authority/collision resolution and,
  if transferring, verified migration plus explicit activation approval.
  Saving routing fields is not approval to switch authority.
- Store **identifiers, locators and versions only**. No concepts, plans,
  summaries, catalogue dumps, mutation payloads, tool responses or secrets.
  Sanitize locators before writing; do not persist authentication material.
- Verify persistence by exact readback. On inaccessible configuration,
  obtain explicit session-only consent or stop; never claim a saved choice
  or create an `.ai/` cache. Do not persist a `session-only` record as if it
  were durable, or invent a new context on retry.
- A binding alone is not instrumentation: verify the real constitutive
  catalogue and entry concepts. Project `AGENTS.md` is optional externally;
  `.atl/tool-layout.md` stays local under every surface.
