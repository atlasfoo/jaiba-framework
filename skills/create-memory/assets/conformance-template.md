# Memory-surface conformance evidence

This is an **unexecuted template**, not certification. Fill it with observed,
redacted evidence under the effective `create-memory` contract. Never mark a
row passed merely because its instructions or eval exist.

## Claim envelope

- Adapter ID/version, backend/tool/schema versions: `<fill>`
- Effective `create-memory` installation and contract: `jaiba-memory-surface`
  `1.0.0`; `<verified host-visible locator>`
- Host, date, tester and documentation sources: `<fill>`
- Exact isolated namespace, project, categories and contexts: `<fill>`
- Fixture mutation/cleanup authorization and writer handoff: `<fill>`
- Fixture inventory, expected payloads and redacted evidence location: `<fill>`
- Required capabilities: `<supported / unsupported / unverified, each>`
- Optional capabilities, including native CAS: `<supported / unsupported /
  unverified, each, with actual guarantees>`
- Limits/encoding/normalization and unknown restrictions: `<fill with units>`
- Overall: **UNVERIFIED** until every required check passes for this envelope.
  Unsupported required capabilities mean **NONCONFORMING**. Blocked/not-run
  checks remain unverified. No whole-backend or all-version certification.

## Operation and readback receipts

For every row record **passed / failed / blocked / not run**, expected state,
observed state, exact redacted evidence locator and remaining uncertainty.
Receipts identify contract/version, adapter/binding, operation, complete
scope/address, request/idempotency ID, verified prior revision/absence,
resulting revision and complete payload/readback comparison. Archive receipts
also bind close ID, verified log address/revision and exact executive inventory.
Keep payload evidence outside machine routing configuration.

| Family | Evidence required | Status / evidence |
|---|---|---|
| probe / resolve | Actual callable tools, permissions, exact ownership, contract/version, identities and limits; no default-project assumption. | not run |
| catalog | All unfiltered and type-filtered pages, completion/continuation, consistency and authoritative inventory including logs/unrecognized objects. | not run |
| read | Exact address, complete content/metadata/relations/revision; deterministic chunk reconstruction and explicit end. | not run |
| create | Authoritative absence, collision refusal, receipt and full exact readback including unknown fields. | not run |
| update | Pre-read full revision, preservation of unrelated/unknown fields, changed revision, receipt and intended full-object readback. | not run |
| append-log | Immutable entry, close ID, exact readback; same key/payload returns existing verified receipt; changed payload conflicts. | not run |
| archive | Verified log receipt and frozen complete context inventory with addresses/revisions/payload evidence. | not run |
| clear-work | Re-enumeration/revision check, selective unchanged-object deletion, authoritative absence, unchanged other contexts/logs; exact residuals after partial deletion. | not run |
| export | Complete scoped manifest/full payloads/unknown fields/relations/original forms/IDs/source revisions; stable source inventory. | not run |
| import | Separate staging, collision refusal, every-object full readback, no missing/extra objects, resolvable relations and stable source; no automatic activation. | not run |

## Fixture preservation and roundtrip

Run create → complete catalogue/read → update → append/archive/selective
clear for one context, with another context and ordinary backend objects as
negative controls. Export/import a populated independent fixture scope into
staging, then re-export/compare logical payloads and original representations.
Source revision tokens remain provenance, not valid target mutation tokens.

- Inventory includes all sixteen existing types when testing full type
  coverage, optional empty types, unknown/missing types and unlinked logs.
- Preserve nested unknown metadata and relation fields, full multi-chunk
  content, stable logical IDs, log close IDs and original link/document forms.
- If filesystem compatibility is claimed, exercise concept bundle and legacy
  flat fixtures with raw untyped documents/sections and absent frontmatter;
  neither is implicitly migrated. Both entry markers block as ambiguous.
- Test multiple catalogue pages and deterministic chunk boundaries, explicit
  size units, encoding and normalization, boundary/oversize errors before
  mutation or verified lossless chunking. No summary/truncated substitution.
- Record complete object comparisons and internal relation resolution;
  unresolved links are reported/preserved, never invented or discarded.
- Confirm source and negative controls unchanged, staged inventory exact,
  no active binding switch and no source retirement.

## Negative-path matrix

For each case capture the error, verified effects or unknown outcome, and
proof that dependent writes/cleanup stopped. Do not manufacture production
failures; use isolated fixtures or a clearly identified controlled simulation.
Simulation alone cannot establish unavailable live-tool guarantees.

| Case | Observable safe result | Status / evidence |
|---|---|---|
| Search-only or missing required tool | No full-surface claim, absent-object inference, guessed tool or fallback. | not run |
| Permission filtering, hidden pages, unavailable service/version | Explicit failure, not empty brain; no writes based on incomplete visibility. | not run |
| Partial/truncated read or missing readback | Unverified outcome; no dependent mutation/clear; exact reconciliation before retry. | not run |
| Wrong namespace/project/context | Refusal; ordinary memory and other work remain unchanged. | not run |
| Unknown required extension / invalid object | Block affected use; preserve data for diagnosis without type coercion. | not run |
| Concurrent edit or stale revision | Conflict, no silent overwrite; demonstrated serialization or proven native CAS. | not run |
| Unknown write outcome / eventual consistency | No fresh duplicate create/append; reconcile exact state and verify final full read. | not run |
| Close retry same/different payload | Same receipt without duplicate / conflict without editing prior log. | not run |
| New or changed object after archive | Cleanup blocked despite existing verified log. | not run |
| Partial deletion | Exact completed/failed/unknown/residual inventory; retry only unchanged residuals with archive evidence. | not run |
| Oversize or lossy fields/encoding | Limit error before mutation or verified lossless reconstruction, never truncation. | not run |
| Import collision, partial stage or source change | No overwrite/activation/cleanup; source authoritative, reconcile/reverify. | not run |

## Identity, precedence and installation checks

Record actual evidence or fixture outcomes separately from live claims:

- Explicit override, local-before-global, same-ID local shadowing, multiple
  winning IDs, failed/disappeared selected adapter and changed candidate set.
  No saved-binding precedence tier, silent lower-level choice or fallback.
- Normalized credential-free remote identity, nonportable fallback labels,
  basename collision, changed origin/root, confirmed registry aliases and
  unknown/multiple exact matches; no implicit identity creation.
- Stable per-root context across sessions/branches; independent worktrees;
  explicit existing-context resume with writer handoff, not “latest plan”.
- Both populated stores require an authority decision; a marker, routing
  record, probe or empty catalogue does not establish instrumentation.
- Local/global host-visible installation and canonical dependency resolution
  work without sibling directories. Global visibility does not widen backend
  scope. Failed persistence offers explicit session-only use, no `.ai/` cache.
- Optional coordination is separate, consumer-identified and not required.

## Verdict and delivery

List passed/failed/blocked/not-run checks, optional exclusions, retained
fixture state and authorized cleanup results, exact evidence locators,
revalidation triggers and remaining risks. Distinguish generated evals,
executed backend checks and separately approved comparative skill evals.
State draft/conformance and installed/host-visible status independently.
No migration, consumer activation or native CAS claim without its own
observed evidence and explicit authority.
