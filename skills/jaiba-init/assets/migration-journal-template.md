# Surface migration journal — contract `jaiba-memory-surface` `1.1.0`

Finite recovery artifact for `jaiba-init:migrate-surface`, not an OKF concept,
binding file, memory mirror or synchronization service. Persist it automatically
at the transaction directory below. Do not ask the operator to invent or choose
a directory. Reference complete snapshot payloads without embedding credentials
or ordinary backend memory. Unfilled fields are pending, never evidence. Keep
this transaction ID and append attempt history on retry.

## Standard transaction directory

Create this directory before the first mutation. The only path is:

`~/.jaiba/migrations/<project-id>/<tx-id>/`

`<project-id>` is the stable registry project ID. `<tx-id>` is the transaction
ID assigned for this transfer and reused on every retry. Each must be one path
segment. If either is empty, ambiguous, or not a single segment (separator,
`..`, or empty), stop. Do not encode a substitute path, and do not ask for
another location. This directory is outside source and target catalogues,
`.ai/`, `.atl/` and `~/.jaiba/memory/`.

| File | Required | Holds |
|---|---|---|
| `journal.yaml` | yes | This journal: state, binding `v2` locators, cutover decisions, attempt history. No payloads. |
| `snapshot.json` | yes | Complete source snapshot for the approved scope. Full bodies, not summaries. |
| `staging-manifest.json` | yes | Staged target inventory, protocol-conversion rows, receipts and verification evidence. |

Additional payload parts, if one JSON file cannot hold the snapshot, stay inside
this same directory and are named by the procedure, never by the operator.
`snapshot.json` references them. A journal that cannot be written and read back
stops the transaction before mutation.

## `journal.yaml`

Contract version on the file is `1.1.0`. Routing locators are binding `v2`
only: `~/.jaiba/memory/bindings/<sha256(canonical-work-root)>.yaml`
(`binding-format-version: "2"`). The digest is the effective `resolution.md`
formula (SHA-256 of the UTF-8 canonical work root, 64 lowercase hex). No
`~/.jaiba/memory/<host-agent-id>/` path. No payloads, credentials, or receipts
that contain payloads.

```yaml
contract:
  id: jaiba-memory-surface
  version: "1.1.0"
transaction-id: "<stable-tx-id>"
created-at: "<UTC>"
coordinator: "<host-agent-id>"
journal:
  locator: "~/.jaiba/migrations/<project-id>/<tx-id>/journal.yaml"
  revision: "<journal-revision>"
  verified-readback: pending
snapshot:
  locator: "~/.jaiba/migrations/<project-id>/<tx-id>/snapshot.json"
  revision: pending
  sha256: pending
staging-manifest:
  locator: "~/.jaiba/migrations/<project-id>/<tx-id>/staging-manifest.json"
  revision: pending
  sha256: pending
current-state: preflight
# preflight | snapshot-verified | staging-pending | staging-verified |
# cutover-pending | activation-pending | active-verified |
# blocked | outcome-unknown
last-verified-state: pending
protocol:
  # JAIBA3-to-JAIBA4 | none
  conversion: none
  source-wire: pending          # JAIBA3 | JAIBA4 | filesystem | other
  target-wire: pending          # JAIBA4 | filesystem | other
  source-storage-profile: pending   # jaiba-engram-storage/3 when JAIBA3
  target-storage-profile: pending   # jaiba-engram-storage/4 only after activation
  source-namespace: pending     # jaiba/v3/<ns16> when JAIBA3
  target-namespace: pending     # jaiba/v4/<ns16> when JAIBA4
  context-heads: pending        # locators created at seq 0; none if conversion is none
  roundtrip: pending            # pending | verified | failed | not-applicable
cutover-gate:
  # Single questionnaire after staging-verified. Two decisions, one turn.
  presented-at: pending
  activation-decision:
    state: pending              # pending | authorized | declined
    human: pending
    verified-manifest-revision: pending
    binding-locator: "~/.jaiba/memory/bindings/<sha256(canonical-work-root)>.yaml"
    binding-format-version: "2"
    time: pending
  retirement-decision:
    state: pending              # pending | authorized | declined | not-applicable
    human: pending
    # external-traceless | other-source-store | not-applicable
    applies-to: pending
    ai-dir: pending             # retain | remove-after-active-verified | not-applicable
    agents-md: pending          # retain | strip-jaiba-preserve-user | remove-pure-marker | not-applicable
    time: pending
```

- Canonical effective installation:
- Last verified evidence / time:
- Migration request scope (not activation consent, not retirement consent):
- Scope/remap changes and any renewed approvals already named by the request:
- Cutover declined: source remains authoritative; retirement is not executed:

## Full sanitized bindings and scope

Repeat for source, staging and proposed active target. Distinguish routing
configuration from actual authority and from source provenance revisions.
Binding locator is the binding `v2` path above, or an explicit session-only
consent that is not that file. For a `JAIBA3` → `JAIBA4` transfer, staging
keeps `storage-profile` unset or still `jaiba-engram-storage/3` until the
activation decision writes `jaiba-engram-storage/4`.

| Role | Host/agent and exact absolute work roots | Adapter ID/version, representation/layout, wire protocol | Contract/version | Namespace/project ID and registry locator/ownership | Sanitized identity/approved aliases | Context IDs | Binding `v2` locator/revision or session-only consent |
|---|---|---|---|---|---|---|---|
| Source | | | `jaiba-memory-surface` `1.1.0` | | | | `~/.jaiba/memory/bindings/<sha256(canonical-work-root)>.yaml` |
| Staging | | | `jaiba-memory-surface` `1.1.0` | | | | not active |
| Proposed active target | | | `jaiba-memory-surface` `1.1.0` | | | | same v2 locator, written only if activation is authorized |

- Complete declared context registry inventory, including empty contexts:
- Included categories/contexts/roots:
- Excluded/inaccessible contexts/roots, reasons and explicit scoped limitation:
- Full-project or requested smaller scope / manifest completeness:
- Excluded-context routing and shared constitutive authority reconciliation:
- Logical ID/project/context/locator remap table (only remaps named in the request):
- Filesystem destination root per executive context (distinct roots required):
- Constitutive replica/root authority and writer policy (no implicit sync):
- Selection precedence/candidate set / override changes / target resolution proof:
- Capabilities, actual tool/permission probes, consistency and limits evidence:
- Source/target complete preflight inventories and collision blocks:
- Known affected writers, pause acknowledgements, handoff owner and guarantees:

## `snapshot.json` and `staging-manifest.json`

Both files record `contract.id: jaiba-memory-surface` and
`contract.version: "1.1.0"`, plus `transaction-id`. `snapshot.json` is the
canonical interchange envelope for the captured scope: all catalogue pages,
full bodies, metadata including unknown keys, relations, original
representations, registry/aliases, empty contexts, revisions and close IDs.
`staging-manifest.json` is not authority. It lists each staged address,
previous absence, stable request ID, mutation receipt, target revision and
full readback. When `protocol.conversion` is `JAIBA3-to-JAIBA4`, the manifest
also lists each `exec-base` at `seq: 0`, each initial `context-head` locator,
and the `JAIBA4.<sha256>.<base64>` wire digest. Neither file stores
credentials. Neither file is a binding.

## Complete inventory rows

One row per logical object, with complete manifests linked rather than summaries.
Journal rows point at `snapshot.json` / `staging-manifest.json`; they do not
replace those files.

| Source full logical address and locator | Source revision and full payload evidence | Approved target address/locator | Previous target absence/revision | Stable request ID | Mutation receipt and outcome | Target revision and full readback evidence | Pending/failed/unknown residual and exact retry checks |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

## Verification barrier

For each item record pending/failed/verified/not-applicable, exact evidence
and verifier/time. The `JAIBA3` → `JAIBA4` rows are `not-applicable` when
`protocol.conversion` is `none`, and required when it is `JAIBA3-to-JAIBA4`.

| Check | State | Evidence |
|---|---|---|
| Complete target inventory equality; no missing/extra/duplicate objects or contexts | pending | |
| Every object's full content/type/metadata including unknown fields | pending | |
| Original representations and lossless legacy reconstruction | pending | |
| Stable logical IDs, relations/unknown relation fields and internal resolution | pending | |
| External/source-unresolved link preservation and explicit findings | pending | |
| Historical logs and stable close IDs; no duplicate appends | pending | |
| Receipts, target revisions, complete chunk reconstruction/readback | pending | |
| Source full inventory/revisions unchanged after snapshot and before activation | pending | |
| Staging full inventory/revisions unchanged before activation | pending | |
| Writer serialization still established and scope request current | pending | |
| `JAIBA3.` decoded read-only; no in-place relabel; source `jaiba/v3/` unwritten | pending | |
| Monoliths are `exec-base` at `seq: 0`; no invented deltas | pending | |
| Re-encoded `JAIBA4.<sha256>.<base64>` under `jaiba/v4/<ns16>/` only | pending | |
| Initial `context-head` slots match those seq-0 bases | pending | |
| Lossless roundtrip of every converted object | pending | |

## Cutover decisions

Collected together in one questionnaire after `staging-verified`. Neither
decision is implied by the other or by the migration request. Declining
activation leaves the source authoritative and skips retirement execution.

- Activation decision: human / authorized or declined / verified manifest revision / time:
- Activation binding `v2` locator (written only when authorized):
- Proposed routing change, including `storage-profile: jaiba-engram-storage/4` when conversion is `JAIBA3-to-JAIBA4`:
- Retirement decision: human / authorized, declined, or not-applicable / time:
- Retirement scope: `.ai/` disposition and `AGENTS.md` disposition (strip JAIBA frontmatter/blocks and preserve other content, or remove a pure marker):
- Retirement not executed until `active-verified`, and not executed if activation was declined:

## Activation intent and confirmed authority

- Stable activation request ID / intent recorded before routing mutation:
- Exact previous routing fields/registry revisions and authority per root/scope:
- Exact proposed routing/registry/override changes and approved manifest revision:
- Activation mutation receipts / partial effects / unknown outcomes:
- Actual host re-resolution and persisted/session binding `v2` readback:
- Active ownership, full catalogue/entry reads and revision verification:
- Confirmed authority per category/context/root (only after verified activation):
- Source retained at / source no longer writable as authority after confirmation:
- Writer resume/handoff acknowledgement / effective time:
- If failed/unknown: paused dependents, exact routing reconciliation and retry checks:
- If outage: verified snapshot scope/revision, current-stability limitations,
  possible later writes and separate human recovery decision (no empty fallback):

## Attempt history and exact cleanup limits

Append, never reset a failed/unknown attempt or replace the transaction ID.
Reopen this directory; do not allocate a new `<tx-id>` for a retry.

| Attempt/time | Prior verified state | Operation/request ID and exact scope | Intent | Outcome: pending/partial/unknown/verified/blocked | Readback/revision evidence | Residual effects and required retry checks |
|---|---|---|---|---|---|---|
| | | | | | | |

- Default cleanup authorization: **none**; retain source, snapshot and journal.
- Retirement decision is the authorization recorded at the cutover gate, not a
  later confirmation. It still does not run before `active-verified`.
- Pre-cleanup complete re-enumeration/revision checks and ownership proof:
- `.ai/` deletions authorized/completed/unknown/remaining and final readback:
- `AGENTS.md`: JAIBA frontmatter/blocks removed; user content preserved; pure
  marker removed only when that disposition was the recorded retirement decision:
- Protected exclusions: unrelated objects, other contexts, `.atl/`, historical
  target logs, this transaction directory, `~/.jaiba/memory/`, and the only
  verified snapshot. No blanket purge or hidden mirror.
- Final report: last verified state, authority, limitations, retained artifacts,
  unresolved effects, paused writers and next explicit decision:
