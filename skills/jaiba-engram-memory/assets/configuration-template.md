# Inactive Engram routing example

Illustrative identifiers/locators only; **not an activated binding**, live
project, backend schema or conformance evidence. Resolve the effective
`create-memory` contract/resolution before completing any value. This draft
adapter is not selectable as a certified mutable surface.

```yaml
binding-format-version: "1"
host-agent-id: "<exact-host-agent-installation-id>"
machine-id: "<non-secret-machine-discriminator>"
work-root: "<normalized-absolute-work-root>"
contract:
  id: jaiba-memory-surface
  version: "1.0.0"
surface:
  adapter-id: jaiba-engram-memory
  adapter-version: "3.2.0"
  installation-locator: "<effective-host-visible-installation>"
  confirmed-candidate-ids: []
  storage-profile: "jaiba-engram-storage/3"
  namespace: "jaiba/v3/<ns16>/"
  catalogue-locator: "<human-verified-catalogue-observation-id>"
backend:
  project: "<existing-authorized-Engram-project>"
  scope: project
  catalogue-topic-key: "jaiba/v3/<ns16>/cat/<proj_sha24>"
project:
  project-id: "<stable-JAIBA-project-id-not-backend-project-label>"
  identity:
    kind: git-remote
    host: "code.example"
    path: "Group/App"
executive:
  context-id: "<confirmed-stable-context-for-this-work-root>"
  context-locator: "<context-id-verified-in-catalogue>"
```

For local remotes or root fallback, use the canonical `local-remote`,
`git-root` or `workspace-root` identity with host-id and normalized absolute
path; label fallbacks nonportable. Store no raw credential-bearing remote.

The eventual verified routing record belongs under `~/.jaiba/memory/`, keyed
by **full host-agent identity and absolute work root**, not a basename, `.ai/`
or a committed project file. Only IDs, sanitized locators and versions belong
there: no catalogue dumps, bodies, summaries, receipts, raw tool results,
passwords or tokens. Authentication stays in the existing host mechanism.

Recompute selection precedence and verify origin and ownership before reuse.
The catalogue locator requires a full `Project:`/`Scope:` and digest check;
numeric ID lookup is not project-filtered. Search may suggest human-verified
candidates but cannot prove catalogue absence or allocate a namespace. An
unknown backend project is not registered by this adapter. Logical lookup uses
the catalogue's exact IDs, never a topic upsert or fuzzy search. Trial IDs are
not defaults.

Read back any authorized routing write before claiming persistence. If machine
configuration is unavailable, obtain explicit consent for the same validated
session-only binding or stop. Do not claim it was saved, mint a fresh context
on retry or create an `.ai/` cache. Existing memory still requires authority
resolution and any migration/activation approval. Branch/session changes alone
do not change the context. `.atl/tool-layout.md` remains local.
