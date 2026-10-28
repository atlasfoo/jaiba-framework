# Memory-surface conformance evidence

This is an **unexecuted template**, not certification. Fill it with observed,
redacted evidence under the effective `create-memory` contract. Never mark a
row passed merely because its instructions, a nature profile, or eval JSON
exist. A contrasted profile is a precondition for depending on a physical
claim. It is not a passed conformance row and not product certification.
A generated draft is not activated.

## Claim envelope

- Adapter ID/version, backend/tool/schema versions: `<fill>`
- Effective `create-memory` installation and contract: `jaiba-memory-surface`
  `1.0.0`; `<verified host-visible locator>`
- Procedure provenance locator: `<generation-time installation>/references/storage-nature.md`.
  Historical. Not a sibling path, not this package's profile, and not
  authority after the package moves. Date and resolution method are
  separate fields, not part of the path.
- Active procedure reference: `<this host's re-resolved installation>/references/storage-nature.md`,
  or `not-yet-resolved`. Same string in the profile, mapping, and this
  record. An unidentified relevant procedure or contract change blocks
  re-derivation of affected claims. Do not ship a repository absolute
  path as universal active configuration.
- Filled profile: package `references/storage-nature.md`; role
  `backend-specific-profile`; status `<unfilled / hypothesis-only /
  incomplete / discrepant / contrasted>`
- Sufficient guarantees the mapping depends on: `<assertion ids, or none>`
- Blocked guarantees: `<unknown / inferred / documented-only / discrepant>`
- Profile evidence locator, versions, date, environment: `<durable locator
  outside the repository and the backend, or absent>`
- Host, date, tester and documentation sources: `<fill>`
- Nature-experiment scope: `<namespace / location / identities; physical
  project or account only if explicitly authorized and ownership is
  checkable; or not-run>`
- Conformance scope: `<new namespace, location, and identities>`. A shared
  physical backend project or account is allowed only under that same
  explicit, checkable isolation. Do not require a newly registered
  physical project. Do not reuse experiment records, bindings, locators,
  or caps.
- Residue-gate outcome, if the nature experiment depended on a historically
  contaminated store: `<not-applicable / blocked / retirement-verified /
  abstention-accepted>` — exact ids and actions, or the named residual
  conditions the human accepted. A generic continuation is not this field.
- Fixture mutation/cleanup authorization and writer handoff: `<fill>`
- Fixture inventory, expected payloads and redacted evidence location: `<fill>`
- Costs the mapping declares: `<records, calls, data bytes, control bytes;
  shared index vs per-object; unknown is not zero>`
- Recovery boundaries: `<non-atomic points, retry identity, last guaranteed
  version; or not derived>`
- Required capabilities: `<supported / unsupported / unverified, each>`
- Optional capabilities, including native CAS: `<supported / unsupported /
  unverified, each, with actual guarantees>` — single-writer evidence is
  not a CAS pass.
- Limits/encoding/normalization and unknown restrictions: `<fill with units;
  documented limit, observed sample, and operating cap stay separate>`
- Overall: **UNVERIFIED** until every required check passes for this envelope
  and the mapping depends only on sufficient guarantees from a contrasted
  profile. Unsupported required capabilities, a necessary guarantee without
  sufficient evidence, or a docs/observation discrepancy mean
  **NONCONFORMING**. Blocked/not-run checks remain unverified. No
  whole-backend or all-version certification. Do not upgrade the verdict
  because the profile exists.

## Profile precondition

Record this before any operation row is treated as evidence for a physical
claim. `contrasted` here means the comparison was made. It does not pass
the operation matrix.

| Check | Evidence required | Status / evidence |
|---|---|---|
| Procedure locator | Provenance locator preserved. Active reference re-resolved on this host and identical in the profile, the mapping, and this record. Not a relative link to the package profile, not a sibling assumption, and not a stored absolute path treated as authority. | not run |
| Profile is filled evidence | Instantiated from the profile template. Not a paste of the factory procedure. Assertion states are only documented, observed, inferred, unknown, or discrepant. | not run |
| Contrast | Documented and observed claims compared; both sides of a discrepancy kept; evidence locator recovers original, stored, and transported bytes plus the full comparison. | not run |
| Sufficiency | Every physical claim the mapping depends on cites a sufficient assertion. Empty list means no physical dependence. | not run |
| Scope separation | New namespace, location, and identities for conformance. Shared physical project or account only if explicitly authorized and ownership is checkable. Experiment records, bindings, locators, and caps were not reused. Historical residues were not product fixtures. | not run |
| Residue gate | If the experiment depended on residual conditions, acceptance is verified retirement of exact ids and actions, or explicit human acceptance of named residual conditions. Generic cue is not consent. Protected records untouched. No candidate-body reads. | not run |

## Operation and readback receipts

For every row record **passed / failed / blocked / not run**, expected state,
observed state, exact redacted evidence locator and remaining uncertainty.
Receipts identify contract/version, adapter/binding, operation, complete
scope/address, request/idempotency ID, verified prior revision/absence,
resulting revision and complete payload/readback comparison. Archive receipts
also bind close ID, verified log address/revision and exact executive inventory.
Keep payload evidence outside machine routing configuration. A successful
readback is only a readback claim; it does not prove crash atomicity or a
maximum.

| Family | Evidence required | Status / evidence |
|---|---|---|
| probe / resolve | Actual callable tools, permissions, exact ownership, contract/version, identities and limits; no default-project assumption. | not run |
| catalog | All unfiltered and type-filtered pages, completion/continuation, consistency and authoritative inventory including logs/unrecognized objects. Search/FTS is not this row. | not run |
| read | Exact address, complete content/metadata/relations/revision; deterministic chunk reconstruction and explicit end only when chunking was derived. | not run |
| create | Authoritative absence, collision refusal, receipt and full exact readback including unknown fields. Returned id checked against logical address and ownership before adopt. | not run |
| update | Pre-read full revision, preservation of unrelated/unknown fields, changed revision, receipt and intended full-object readback. | not run |
| append-log | Immutable entry, close ID, exact readback; same key/payload returns existing verified receipt; changed payload conflicts. | not run |
| archive | Verified log receipt and frozen complete context inventory with addresses/revisions/payload evidence. | not run |
| clear-work | Re-enumeration/revision check, selective unchanged-object deletion, authoritative absence, unchanged other contexts/logs; exact residuals after partial deletion. | not run |
| export | Complete scoped manifest/full payloads/unknown fields/relations/original forms/IDs/source revisions; stable source inventory. | not run |
| import | Separate staging, collision refusal, every-object full readback, no missing/extra objects, resolvable relations and stable source; no automatic activation. Multi-object migration journal retained. | not run |

## Derivation, cost, and recovery

These rows grade the mapping, not the prose around it. A reconstructed
specimen does not pass an unjustified extra control.

| Check | Observable safe result | Status / evidence |
|---|---|---|
| One native unit | Passed only when the profile shows the object fits and intact verification and publication are supported, so one unit holds complete payload and ownership. An extra control fails only when unjustified. A concrete observed verification or publication gap may authorize the necessary control even if the byte length fits. Absence of CAS and an artificial cap do not. | not run |
| Owned index | Present only when native enumeration is unavailable. Full-text search is not the index and does not prove absence. Shared-index and per-object costs are separate. | not run |
| Extra controls | Each names a demonstrated capability gap, assertion ids, cost, and bounded enumeration/reconstruction. Absence of CAS and an artificial cap are not the gap. Controls themselves fit; no unbounded further layer. | not run |
| Chunking / excess | Only a real identified insufficiency, including a concrete observed verification or publication gap. Forbidden when the object fits and can be verified and published intact. Unsupported when reassembly or enumeration cannot be stated. Unknown limit stays unknown; no maxima campaign. | not run |
| Non-atomic boundary | Interruption points, retry identity, and finite reconciliation to the last guaranteed version are explicit. No second logical object. Not called a transaction unless atomicity was observed. | not run |
| Costs | Create, read, update, retry, and archive state records, calls, data bytes, and control bytes. Unmeasured is unknown, not zero. | not run |
| History vs snapshots | Native history replaces snapshots only when fidelity and retention are both verified. | not run |
| Suggestions | Own and foreign suggestions recorded as effects. They do not block publication alone, authorize candidate reads or mutations, or emit automatic judgments. Host judgment protocol untouched. | not run |
| Logical collision | Mismatch of logical address, owner, revision, or bytes blocks. Returned id after dedupe is validated before adopt. Upsert key is not exclusive create. | not run |
| Historical encodings | Current `JAIBA1` / `JAIBA2` records were not reinterpreted or migrated by generation. An incompatible new representation has a distinct discriminator and version. Unexercised migration is not completed. | not run |

## Fixture preservation and roundtrip

Run create → complete catalogue/read → update → append/archive/selective
clear for one context, with another context and ordinary backend objects as
negative controls. Export/import a populated independent fixture scope into
staging, then re-export/compare logical payloads and original representations.
Source revision tokens remain provenance, not valid target mutation tokens.
This scope is isolated from the nature experiment as the claim envelope
requires. Do not reuse that experiment's records or bindings. A shared
physical project is not, by itself, a failure.

- Inventory includes all sixteen existing types when testing full type
  coverage, optional empty types, unknown/missing types and unlinked logs.
- Preserve nested unknown metadata and relation fields, full multi-chunk
  content when chunking was derived, stable logical IDs, log close IDs and
  original link/document forms.
- If filesystem compatibility is claimed, exercise concept bundle and legacy
  flat fixtures with raw untyped documents/sections and absent frontmatter;
  neither is implicitly migrated. Both entry markers block as ambiguous.
  Do not impose another backend's record graph on filesystem.
- Test multiple catalogue pages and, only when derived, deterministic chunk
  boundaries, explicit size units, encoding and normalization, boundary/oversize
  errors before mutation or verified lossless chunking. No summary/truncated
  substitution. A passing sample is not a maximum.
- Record complete object comparisons and internal relation resolution;
  unresolved links are reported/preserved, never invented or discarded.
- Confirm source and negative controls unchanged, staged inventory exact,
  no active binding switch and no source retirement.
- Exercise each declared non-atomic boundary: an interruption keeps the last
  guaranteed version and does not mint a second logical object.

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
| Concurrent edit or stale revision | Conflict, no silent overwrite; demonstrated serialization or proven native CAS. Single-writer is not recorded as CAS. | not run |
| Unknown write outcome / eventual consistency | No fresh duplicate create/append; reconcile exact state and verify final full read. | not run |
| Close retry same/different payload | Same receipt without duplicate / conflict without editing prior log. | not run |
| New or changed object after archive | Cleanup blocked despite existing verified log. | not run |
| Partial deletion | Exact completed/failed/unknown/residual inventory; retry only unchanged residuals with archive evidence. | not run |
| Oversize or lossy fields/encoding | Limit error before mutation or verified lossless reconstruction, never truncation. Unknown limit does not become an invented oversized pass. | not run |
| Import collision, partial stage or source change | No overwrite/activation/cleanup; source authoritative, reconcile/reverify. | not run |
| Mapping before contrasted profile, or conforming claim on discrepancy / missing guarantee | Diagnosis and incomplete or discrepant profile retained; no selectable conforming surface. | not run |
| Procedure copied into the profile, or procedure linked at the profile / a sibling path | Package rejected until the resolved procedure locator and a filled profile are distinct. | not run |
| Suggestion treated as a lock, or candidate read/judgment | Similarity does not block; no candidate body read; no automatic judgment; host protocol independent. | not run |
| Generic continuation used as retirement consent | Dependent experiment stays blocked. Exact id/action consent or explicit accepted abstention required. | not run |

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
  work without sibling directories. Re-resolve the active procedure on this
  host; preserve provenance; a stored absolute path is not authority and is
  not the installed profile. Global visibility does not widen backend
  scope. Failed persistence offers explicit session-only use, no `.ai/` cache.
- Optional coordination is separate, consumer-identified and not required.
  Absence is not inferred from memory availability, and no mission model is
  defined.
- Installation and activation are separate. A copied package, including a
  contrasted profile, is not an active binding and not a migration of
  historical encodings.

## Verdict and delivery

List passed/failed/blocked/not-run checks, optional exclusions, retained
fixture state and authorized cleanup results, exact evidence locators,
revalidation triggers and remaining risks. Distinguish the nature profile,
generated evals, executed backend checks, and separately approved
comparative skill evaluations. State draft/conformance, installed/host-visible,
and activated status independently. No migration, consumer activation, or
native CAS claim without its own observed evidence and explicit authority.
Do not report engine emptiness, and do not report a profile as certification.
