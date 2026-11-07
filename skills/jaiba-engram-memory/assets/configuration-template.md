# Inactive Engram routing example

Illustrative identifiers and locators only. **Not an activated binding**,
live project, backend schema, or conformance evidence. Copying this template
activates nothing. Resolve the effective `create-memory` contract and
resolution (contract **1.1.0**) before completing any value. Selecting this
adapter requires an explicit host binding.

Standard path, and the only standard write path:

`~/.jaiba/memory/bindings/<sha256(canonical-work-root)>.yaml`

The digest is SHA-256 of the UTF-8 canonical work root: the absolute
resolved directory, separators normalized to `/`, no trailing `/` unless the
path is exactly `/`. 64 lowercase hex characters, no prefix. The filename
stem must equal `work-root.sha256`. The path is shared by every agent
runtime of this user for that work root. Host identity is not a directory
and not a file key. Do not write a record under a per-agent subdirectory of
`~/.jaiba/memory/`. Do not put host identity in the filename. Compute the
path with `python3 -B scripts/jaiba_engram.py binding-path --work-root <abs>`;
that subcommand creates nothing.

```yaml
binding-format-version: "2"
# Host that last completed routing readback. Provenance, not a key.
last-verified-by: "<host-that-last-completed-routing-readback>"
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
  adapter-id: jaiba-engram-memory
  adapter-version: "3.3.0"
  category: memory-surface
  archetype: record-store
  confirmed-candidate-ids: []
  storage-profile: "jaiba-engram-storage/4"
  namespace: "jaiba/v4/<ns16>/"
  catalogue-locator: "<human-verified-catalogue-observation-id>"
  registry-locator: "<sanitized-exact-project-registry-locator>"
backend:
  project: "<existing-authorized-Engram-project>"
  scope: project
  catalogue-topic-key: "jaiba/v4/<ns16>/cat/<proj_sha24>"
project:
  project-id: "<stable-JAIBA-project-id-not-backend-project-label>"
  identity:
    kind: git-remote
    host: "code.example"
    path: "Group/App"
executive:
  context-id: "<confirmed-stable-context-for-this-work-root>"
  context-locator: "<context-id-verified-in-catalogue>"
provenance:
  consolidated-from: []
```

Do not add an installation path, `active-procedure-reference`,
`procedure-provenance`, `conformance-status`, or a certifying host to this
record. Procedure provenance stays in the package. Each session resolves
its own compatible `create-memory` and does not write that path back.

For local remotes or root fallback, use the canonical `local-remote`,
`git-root`, or `workspace-root` identity with a non-secret machine
discriminator and a normalized absolute path; label fallbacks nonportable.
Store no raw credential-bearing remote. The known formula lock is the
canonical string `/srv/checkouts/App`, digest
`4c0e89ce280a2f213662e9e260df1380403db27e2096fedba7db3bc5c530ec63`. Do not
hash a trailing slash or a `file://` URI.

Only identifiers, sanitized locators, versions, and routing provenance
belong in the file: no catalogue dumps, bodies, summaries, receipts, journal
bodies, raw tool results, passwords, or tokens. Authentication stays in the
existing host mechanism. A session-only selection uses the same routing
fields in session state and must not be described as this file.

Recompute selection precedence and verify origin and ownership before reuse.
A valid file at the standard path is reused by every agent for that
canonical root, including when `last-verified-by` names a different runtime.
Do not ask again for `project-id` or `context-id`. Still run the
non-destructive readiness preflight. The catalogue locator requires a full
`Project:` / `Scope:` and digest check; numeric ID lookup is not
project-filtered. Search may suggest human-verified candidates but cannot
prove catalogue absence or allocate a namespace. An unknown backend project
is not registered by this adapter. Logical lookup uses the catalogue's exact
IDs, never a topic upsert or fuzzy search. Trial IDs are not defaults.

Require `storage-profile: jaiba-engram-storage/4`, `archetype: record-store`,
and namespace `jaiba/v4/<ns16>/` before mutation. A record that still names
`jaiba-engram-storage/3` or `jaiba/v3/` is an unmigrated store: reads may
use legacy decode; writes are `unsupported-version` until explicit
`jaiba-init:migrate-surface JAIBA3 → JAIBA4`. Any other profile blocks as
`unsupported-version`. No sniffing and no fallback.

Read back any authorized routing write before claiming persistence. If
machine configuration is unavailable, obtain explicit consent for the same
validated session-only binding or stop. Do not claim it was saved, mint a
fresh context on retry, write a host-keyed substitute, or create an `.ai/`
cache. Existing memory still requires authority resolution and any
migration or activation approval. Branch or session changes alone do not
change the context. A different `last-verified-by` is not a writer handoff
and is not a lock. `.atl/tool-layout.md` remains local.
