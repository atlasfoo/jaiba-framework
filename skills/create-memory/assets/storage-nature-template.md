# Storage nature profile

Unexecuted template for a **backend-specific filled profile**. Filling
it in does not certify a backend, an adapter, or `jaiba-memory-surface`
**1.1.0**. A profile that is still `unfilled`, `hypothesis-only`,
`incomplete`, or `discrepant` is a diagnosis at most. Even `contrasted`
only means documentation and observation were compared. Depend on a
physical claim only when the derivation section names that claim and
cites sufficient assertions.

This document is not the factory procedure. The procedure stays in the
effective `create-memory` installation. Record that installation's
resolved procedure locator in the identity table. Do not assume a
sibling directory, and do not point this file at itself: once
instantiated, this profile is often `references/storage-nature.md` in
the generated package, which is a different file from the procedure of
the same name. Do not paste the procedure here as if the blanks were
already evidence. Raw evidence stays outside the repository and outside
the backend; this profile holds locators and claims, not the captured
bodies.

```yaml
document-role: backend-specific-profile
# Not the factory procedure. Do not replace this with a path to this file.
profile-status: unfilled
# unfilled | hypothesis-only | incomplete | discrepant | contrasted
# contrasted is not certification. Empty sufficiency list => depend on nothing.
contract-id: jaiba-memory-surface
contract-version: "1.1.0"
logical-guarantees-changed: no
archetype: unknown # document-tree | record-store | unknown (unknown strictly blocks derivation)
factory-procedure-locator: "<generation-time resolved procedure locator; provenance only>"
factory-procedure-revision: "<identified revision or exact source digest>"
factory-procedure-resolved-at: "<date>"
factory-procedure-resolution-method: "<host resolution or explicit disambiguation>"
```

## 1. Identity and evidence

Replace every placeholder. Leave unknown facts as `unknown`; do not
invent a version, a unit, or a locator.

| Field | Value |
|---|---|
| Document role | Backend-specific filled profile, not the factory procedure. |
| Factory procedure provenance | `<generation-time resolved locator, revision/digest, date and method; not a sibling or self path>` |
| Backend / tools | `<names and versions actually used>` |
| Schema and docs | `<identifiers, versions, date read>` |
| Host / environment | `<sanitized; no secrets>` |
| Experiment date | `<date, or not-run>` |
| Disposable namespace / physical project / location | `<authorized new scope, or not-authorized>` |
| Separation | `<how this scope differs from historical trials, residue probes, and product conformance>` |
| Durable evidence locator | `<outside repository and backend; or absent>` |
| What that locator holds | `<original, stored, transported bytes; hashes; full comparison>` |
| Auxiliary scratch | `<optional; not the record>` |
| Host deadline enforcement | `<can-abort / cannot-abort; intended bounds are not a guarantee>` |

Host bookkeeping outside the durable locator is not evidence for this
profile.

Preserve generation-time provenance when a host or installation changes.
Re-resolve the effective installation before characterization or derivation,
compare its relevant procedure revision and contract version with this
profile, and update active references consistently only after that check.
An unidentified or uncovered relevant change blocks affected claims, not
unrelated observations that remain current.

## 2. Assertion ledger

One claim per row. Default state is `unknown`. Allowed states:
`documented`, `observed`, `inferred`, `unknown`, `discrepant`.

A discrepant row must cite both sides and must not pick a winner.
Do not merge a documented limit and a passing sample into one claim.
A successful readback is only a readback claim.
`Depends-on blocked?` defaults to yes where a mapping would need the
claim. `no` on a suggestion row means that effect is not an integrity
lock, not that the effect was observed. Change a `yes` to `no` only
when the procedure marks that claim sufficient.

| Id | Dimension | Claim | State | Documentary source | Observation locator | Depends-on blocked? |
|---|---|---|---|---|---|---|
| A-archetype | Archetype | `<document-tree (editable Markdown documents, direct in-document patch) vs record-store (database/records, mandatory executive journal); unknown strictly blocks derivation>` | unknown | `<or none>` | `<or none>` | yes |
| A-unit | Native unit | `<which record a write accepts>` | unknown | `<or none>` | `<or none>` | yes |
| A-atom-payload | Atomic scope | `<payload commits with what>` | unknown | | | yes |
| A-atom-meta | Atomic scope | `<metadata>` | unknown | | | yes |
| A-atom-history | Atomic scope | `<history>` | unknown | | | yes |
| A-atom-index | Atomic scope | `<index / side effects>` | unknown | | | yes |
| A-crash | Atomic scope | `<crash or interrupted-call atomicity; readback does not answer this>` | unknown | | | yes |
| A-logical-id | Identity | `<logical address is preserved as itself>` | unknown | | | yes |
| A-upsert | Identity | `<native upsert key; not exclusive-create proof>` | unknown | | | yes |
| A-content-dedupe | Identity | `<content dedupe across logical addresses>` | unknown | | | yes |
| A-locator | Identity | `<native locator; not a portable id>` | unknown | | | yes |
| A-sync | Identity | `<sync id, or none observed>` | unknown | | | yes |
| A-enum | Enumeration | `<complete list with continuation and completion, or not>` | unknown | | | yes |
| A-search | Enumeration | `<search/FTS is discovery only>` | unknown | | | yes |
| A-trunc | Effects | `<truncation>` | unknown | | | yes |
| A-norm | Effects | `<normalization / text removal>` | unknown | | | yes |
| A-capture | Effects | `<extra capture>` | unknown | | | yes |
| A-sug-own | Effects | `<own-record suggestions are effects, not locks>` | unknown | | | no |
| A-sug-foreign | Effects | `<foreign suggestions are effects, not locks>` | unknown | | | no |
| A-limit-doc | Size | `<documented limit and exact unit, or unknown>` | unknown | | | yes |
| A-limit-sample | Size | `<observed sample; not a maximum>` | unknown | | | yes |
| A-limit-cap | Size | `<chosen operating cap, if any; a choice, not a measured max>` | unknown | | | yes |
| A-bytes | Size | `<original vs stored vs retrieved vs transport, with units>` | unknown | | | yes |
| A-rev | Revision | `<revision covers the full object, or not>` | unknown | | | yes |
| A-hist-fid | Revision | `<history fidelity>` | unknown | | | yes |
| A-hist-ret | Revision | `<history retention>` | unknown | | | yes |
| A-cas | Revision | `<native CAS, or absent / not-assumed; read/compare/write is not CAS>` | unknown | | | no |
| A-cost-create | Cost | `<records, calls, data bytes, control bytes>` | unknown | | | yes |
| A-cost-read | Cost | `<records, calls, data bytes, control bytes>` | unknown | | | yes |
| A-cost-update | Cost | `<records, calls, data bytes, control bytes>` | unknown | | | yes |
| A-cost-retry | Cost | `<records, calls, data bytes, control bytes>` | unknown | | | yes |
| A-cost-archive | Cost | `<records, calls, data bytes, control bytes>` | unknown | | | yes |
| A-coord | Optional | `<coordination boundary observed or absent; not inferred>` | unknown | | | no |

Add further rows for separate claims. Do not overload a row to hide a
disagreement. Invalidate affected rows when version, schema, or a
relevant configuration changes; do not routine-repeat rows the same
evidence still covers. Note the invalidation:

- Invalidated claims: `<none yet>`
- Why: `<version/schema/config change, or none>`

## 3. Experiment plan (before any effect)

Leave this section as the plan until the authorized experiment runs.
`not-run` is an honest result. Do not back-fill a plan after the calls.

| Bound | Declared value |
|---|---|
| Authorized operations | `<exact list, or not-authorized>` |
| Variants | `<write/readback, update, repeated key, content dedupe across two logical addresses>` |
| Max backend calls | `<finite total for the declared plan, grouped in named batches>` |
| Max mutations | `<finite>` |
| Intended native / auxiliary time bounds | `<15s / 60s, operator-watched; LLM turn time is not a bound>` |
| Host can enforce those deadlines | `<yes/no; if no, say so>` |
| Max sizes and units | `<finite>` |
| Expected receipts | `<what success and expected rejection look like>` |
| Stop conditions | `<unexpected contradiction, unnamed effect, uncertain ACK, budget>` |
| Specimen hash / description | `<small, Unicode, CRLF, synthetic transformable text, no secrets>` |
| Operating threshold | `<chosen, at most 80% of the documented physical limit, in its unit; a choice, not a measurement>` |
| Oversized | `<not-run unless current pertinent limit and unit are known; at most one chunk-path confirmation>` |
| Oversized size, computed once, overhead included | `<or not-applicable>` |
| Protective encoding batch | `<later, separate; not assumed from plaintext>` |
| JAIBA root / journal / catalogue created to study the record | `no` |

Observed outcome, after the fact, cites evidence locators. Expected
truncation is evidence of loss, not intact persistence. One diagnosis
on stop; no automatic retry.

- Batches run: `<0>`
- Last verified state: `<none>`
- Residues of this experiment only: `<none / list>`
- Cleanup permission and what remains: `<not-authorized / result>`

## 4. Residue gate

Independent of factory approval and of the nature-experiment consent.
A continuation cue is not acceptance of a retirement list. The protected
set and any previously prohibited resources come from the authorized
scope; do not hard-code a repository's trial identifiers into this
profile. Do not read candidate, foreign, or protected judgment bodies.

| Step | Result |
|---|---|
| Gate status | `<blocked>` |
| Inventory | `<not-started / read-only classification, enumeration gaps stated>` |
| Classes excluded | `ordinary, useful, protected, unknown` |
| Eligible set | `<exact ids, or none>` |
| External verified copies | `<locator, coverage, history/export limits; not a restore guarantee>` |
| Native retirement mechanism | `<inspected / absent / unverified; deletion was not assumed>` |
| Effects and permissions | `<including indirect effects; harmlessness not claimed>` |
| Exact-id / exact-action consent | `<absent / granted for this list only>` |
| Retirement check | `<not-run / verified effect / abstained>` |
| Human acceptance of residual conditions | `<absent / explicit, naming the conditions>` |

Gate acceptance is only `retirement-verified` or `abstention-accepted`
with that explicit human acceptance. Anything else blocks a dependent
experiment. Do not claim engine emptiness or semantic isolation. A name
prefix does not provide either.

- Accepted outcome: `<none>`
- Residual conditions the experiment must live with: `<unnamed>`
- Protected records and incident endpoints: `untouched`
- Previously prohibited resources: `inaccessible`

## 5. Derivation authorization

List only controls the profile's sufficient assertions justify. No row
means the control is not authorized. Absence of CAS is not a justification.
An artificial cap is not a justification.

| Control | Gap it closes | Assertion ids | Cost (records / calls / bytes) | Enumerated and reconstructed how | Authorized? |
|---|---|---|---|---|---|
| Archetype mapping | `<document-tree: in-document patch, trivial materialization; record-store: mandatory executive journal (base+deltas+context-head); unknown strictly blocks>` | `<ids>` | `<cost>` | `<document edit vs journaled deltas>` | no |
| Single native unit for payload + ownership | `<fits and verifies, or not shown>` | `<ids>` | `<cost>` | `<readback method>` | no |
| Minimal own index | `<only if native enumeration is unavailable>` | | `<shared vs per-object>` | `<not FTS>` | no |
| Payload/index reconciliation | `<non-atomic pair; preserves last guaranteed version>` | | | `<finite recovery; no second logical object>` | no |
| Staging / chunks / manifest | `<real insufficiency only>` | | | `<bounded; no recursive controls>` | no |
| Native history instead of snapshots | `<fidelity and retention both verified>` | | | | no |
| Protective encoding | `<observed transform; tested in its own batch>` | | | `<standard hash/base64/comparison, labeled framing>` | no |

Sufficient guarantees (the only physical claims a mapping may depend on):

- `<none>`

Blocked guarantees (mapping and conformant generation must not depend
on these):

- `<every necessary guarantee still unknown, inferred, documented-only, or discrepant; archetype unknown strictly blocks derivation>`

Logical collisions that block, regardless of suggestions: namespace,
project, category, context when present, logical id, owner, revision,
bytes. Suggestions stay in A-sug-own / A-sug-foreign. No candidate reads.
No automatic judgments. Host personal judgment protocol: independent,
not resolved here.

Multi-object migration journal: retained. Logical contract version:
unchanged at **1.1.0**.

## 6. Non-claims

Leave these sentences in the filled profile. Delete nothing in this list
to make a package look certified.

- This profile is not conformance, not installation, and not activation.
- A probe, a schema, or a document is not a substitute for the missing
  observations above.
- A passing sample is not a maximum.
- A successful readback is not crash atomicity.
- Search is not a complete catalogue.
- Absence of CAS is not distributed exclusion and does not authorize
  extra per-object controls. A-cas `observed` records only that CAS
  observation; it does not certify the adapter.
- Historical physical encodings, including historical `JAIBA1` / `JAIBA2`
  where those labels exist, were not used as evidence and were not
  reinterpreted.
- No backend call, retirement, or product trial is authorized by the
  blank template. A filled profile records only the authorization that
  was actually given.
