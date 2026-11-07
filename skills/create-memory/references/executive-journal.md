# Executive journal

Normative detail for `jaiba-memory-surface` **1.1.0**, capability
`executive-journal`. The canonical copy is this reference in the
**effective `create-memory` installation**. Consumers resolve that
installation and `memory-surface-contract.md` first. This file is not
a second contract, an SDK, a storage schema, a writer runtime, or the
archetype profile.

The contract owns the guarantees and points here from the sections that
own operations, capabilities, closure, and interchange. This reference
owns the closed vocabulary, materialization, heads, compaction, and
`context-head` rules. If it is missing or ambiguous, do not invent a
journal. A consumer that needs `patch` stops. A `1.0.x` adapter remains
usable only under the contract's compatibility rule.

Conduct's templates own executive artifact contents. This reference
does not redefine a PRD, plan, task list, or walkthrough. It defines
how an authorized single writer may splice one.

## 1. What this reference does not define

- The archetype dimension's states, experiments, and profile fields.
  The contract only names `document-tree` and `record-store` so this
  capability can attach. `storage-nature.md` remains the procedure.
- Interchange field layout. The contract states the logical interchange
  rule; `interchange.md` will realize it later.
- A physical encoding, filesystem path, record layout, or script.
  A binding may store journal state in another form if it can produce
  the canonical digest input below and the same materialized object.
- A lock service, a multi-writer protocol, or atomic compare-and-swap.
  `expected-head` is a pre-check under the contract's single executive
  writer. Comparing it is not CAS, even if a binding also has native
  CAS on its head record.
- The migration transaction journal required by the contract's export
  and import rules. Retiring or simplifying this executive journal
  does not remove that journal, and the reverse is not true either.
- Conduct's phase machine. Phase boundaries are only the suggested
  moment for optional compaction.

## 2. Applicability and compatibility

`patch` and `compact` are executive-category operations. They apply
only to logical types `prd`, `plan`, `tasks`, and `walkthrough`. A
constitutive address, an unknown type, or a `context-head` addressed
as if it were an artifact is `invalid-object`. `patch` never creates
an absent object: authoritative absence is `not-found`, as for
`update`. Ambiguous address resolution is `ambiguous` and blocks the
call.

Archetype attaches the capability as follows. Names are exact.
Insufficient evidence is `unknown`, not a guess from a backend's
product name.

| Declaration | Journal obligation |
|---|---|
| Adapter `1.0.x`, archetype absent | Pre-dimension. No `patch`, no `compact`, no `context-head`. A 1.1 consumer uses full `update` and records an efficiency warning (§3). Not `unknown`. |
| `1.1.x` + `document-tree` | `patch` is required and is realized as an edit of the executive document. A stored delta chain and a `context-head` are not required. `compact` on a document with no deltas is a no-op success. |
| `1.1.x` + `record-store` | Stored journal is required: base, ordered deltas, and one `context-head` per executive context. Omitting it is `missing-capability`. The §3 full-`update` path must not hide that gap. |
| `1.1.x` + `unknown`, or `1.1.x` with no archetype | Insufficient evidence. Block derivation of a conformant mapping. Do not issue `patch` and do not invent the realization. `update` may still be used only under the contract's existing 1.0 write rules if the surface otherwise supports them. |

A different major version remains `unsupported-version`. A 1.1.0
consumer does not treat minor `1.2` or above as compatible. A consumer
that implements only 1.0.0 is not required to accept a 1.1 adapter.

Declaring the capability means every rule in this reference is in
force for that realization, including refusals. A `document-tree`
edit that skips the pre-check, the closed vocabulary, or the
draft-only rule is not `patch`.

## 3. Compatibility path for adapters without `patch`

When §2 says the consumer uses full `update`:

1. Resolve and read the object under the contract. Do not send `patch`
   or `compact` to that adapter.
2. Apply the same ordered ops locally, enforcing every refusal in this
   reference, including ID permanence. If an op would be refused, do
   not write.
3. `update` the complete intended object. Unknown fields, relations,
   pre-read revision check, receipt, and full readback stay as the
   contract requires. The path must not weaken them.
4. Record an efficiency warning on the mutation receipt:
   `efficiency-warning: full-update-without-patch`. The warning is not
   an error, not `missing-capability`, and not permission to skip
   verification. It states that the write rewrote the whole object
   rather than appending a delta.

A `1.0.x` adapter has no `compact`. The consumer skips compaction and
may note that on the receipt. It does not fail the work solely because
compaction is unavailable. This path is only the `1.0.x` row of §2. A
`1.1.x` adapter, of either named archetype, that does not realize
`patch` is `missing-capability` and does not use this path.

The consumer must not approximate ops with an ad-hoc edit. If this
reference cannot be resolved, stop; do not `update`.

## 4. Journal model

A journaled executive object has a **base** and zero or more **deltas**.

- The base is a complete logical object: address, type, metadata,
  full content, and relations. A monolithic object, including every
  object written before this capability existed, is an implicit base
  with no deltas.
- A delta is the record of one accepted `patch`. It is not a logical
  object, has no OKF type, and never appears in `catalog`. It stores
  the target address, a contiguous sequence number, the request
  identifier, and the ops in order. It does not store a second copy of
  unrelated objects.
- Sequence numbers start at `1` for the first delta after the current
  base and increase by `1` with no gaps. `seq` `0` means the base
  alone. A gap, a duplicate sequence, or a delta whose address differs
  from the object fails materialization.
- `read` returns the canonical object: base, then each active delta in
  sequence order. Callers never receive a delta as the object.

On `record-store`, a successful `patch` persists exactly one new delta
and updates that object's slot in the context's `context-head`. It
does not rewrite the project catalogue, other contexts, other
executive objects, or those objects' bodies. Rewriting the patched
object's base on every `patch`, or rewriting the catalogue, is `update`,
not this capability.

On `document-tree`, a successful `patch` edits the executive document
so that a following `read` returns the materialized result. The
document remains an implicit base unless the binding declares that it
also stores a journal. No `context-head` record is required. Rewriting
the document is the realization, not a violation. The cost bound of
one delta plus one head is a `record-store` rule, not a `document-tree`
rule.

Delta and head writes are two records when both exist. Do not describe
them as one transaction unless a nature profile observed that
atomicity. If the head and the delta chain disagree so that
materialization is not determined, `read` fails `invalid-object` and
returns no object. Do not prefer the longer chain, the head alone, or
the base alone. Reconciliation is a writer action under the contract,
not an automatic repair.

## 5. Heads and revisions

Two distinct values identify a journaled object. They must not be
compared as if they were the same token.

| Value | What it identifies |
|---|---|
| Logical revision | The binding's declared deterministic fingerprint of the **materialized** logical object (metadata, content, and relations). This is the revision `read` and mutation receipts report. |
| `expected-head` | The journal pre-check: `seq` plus `chain-digest`. It identifies the active base and delta chain, not the rendered prose by itself. |

`seq` is the sequence of the last active delta, or `0` when there are
none. `chain-digest` is the binding's object-fingerprint function
applied to the canonical chain input in §6. The function must be the
one the binding already declares for logical revisions. A fingerprint
that is not a single line token without spaces cannot be used as a
head field; the capability is then unverified and `patch` stays
blocked (`missing-capability`), rather than a shortened digest being
invented.

The pre-check is equality of both fields with the current head.
Numeric `seq` is compared as an integer (`01` is not a different
sequence from `1` only when both parse as the integer 1; a non-integer
is `invalid-object`). `chain-digest` uses the binding's declared
fingerprint comparison. The default is exact, case-sensitive match.
A missing field on the request is `invalid-object`, not `conflict`.
A well-formed head that does not match the current head is `conflict`.
No delta is written.

An implicit base (monolith, freshly imported object, or `document-tree`
document with no stored journal) has `seq` `0` and the chain digest of
that base with an empty delta list. A missing `context-head` slot
means that implicit head. It does not mean the object is absent.

Compaction may change `expected-head` while leaving the logical
revision unchanged. A caller must refresh the head after `compact`
even when `read` content is identical. `expected-head` is not a
concurrency token for another binding. Imported source heads are
provenance, like imported source revisions.

Matching `expected-head` does not exclude another writer. Without the
contract's single-writer discipline, block mutation. Native CAS, if
the binding actually has it, may additionally guard the head record.
That does not make the logical pre-check CAS, and it does not
authorize a lock protocol this contract does not define.

## 6. Canonical digest input

This encoding is the digest input. It is not an on-disk schema. A
change to it changes head comparison and would be a breaking contract
change. Within **1.1.0** it is fixed. Bytes are UTF-8. The canonical
text uses `\n` (U+000A) regardless of the document's stored newlines.
A trailing newline ends every canonical document.

Escape a field value onto one line: `\` becomes `\\`, U+000A becomes
`\n`, and U+000D becomes `\r`. No other escaping is applied. Field
lines inside an op are sorted by field name, byte order.

A delta's canonical form:

```
jaiba-journal-delta/1
namespace <namespace>
project-id <project-id>
category executive
context-id <context-id>
logical-id <logical-id>
seq <integer>
request-id <request-id>
op-count <n>
op <name>
<field> <escaped value>
end
```

Repeat `op` … `end` once per op, in request order. Then the chain
input:

```
jaiba-journal-chain/1
base <base-revision>
```

followed, when `seq` > 0, by each active delta's canonical form in
sequence order. `base-revision` is the fingerprint of the base logical
object, not of the materialized object, except when there are no
deltas — in that case the base is the materialized object, and
`base-revision` equals the logical revision's fingerprint input only
through the binding's function; the chain digest is still the
fingerprint of this wrapper, not the revision token itself.

The same base bytes and the same deltas must produce the same chain
input on a binding. Pretty-printers, map reordering, and locale rules
must not touch this input.

## 7. Materialization

Materialization is a pure function of the current base and the active
deltas in sequence order. Same inputs yield the same canonical object.
`read` either returns that object, with completeness indicated, or
fails. It never returns a prefix of the chain.

Rules:

- Apply every op of delta `1`, then delta `2`, and so on, each delta's
  ops in listed order, to a working copy that starts as the base.
- Unrelated bytes are preserved. Ops splice; they do not reflow
  Markdown, reorder YAML, renumber headings, or rewrite relations.
- If any op in the stored chain cannot be applied, fail the entire
  `read` with `invalid-object`. Do not return the last good working
  copy. Error evidence may name the sequence at which application
  stopped; that evidence is not a successful object.
- A delta that was invalid at write time must not have been stored.
  A later failure means the stored chain no longer matches these
  rules (corruption, a gap, or a foreign address). Fail closed the
  same way.
- Relations and unknown metadata survive every op unless
  `set-frontmatter` changes that one metadata key. After
  materialization, frontmatter in the content and the logical
  metadata projection of those keys agree. If they cannot, the read
  is `invalid-object`.
- `read` does not compact, does not append, and does not repair.

Line endings of preserved bytes stay as they are. An inserted
separator uses the document's newline sequence only when that
sequence is uniform (`\n` or `\r\n`). Mixed newlines in one document
make a splicing op `invalid-object` rather than a normalization pass.
The digest input in §6 still uses `\n` after escaping; that is the
digest wrapper, not a rewrite of the document.

A successful `patch` applies the request's ops to a working copy of
the current materialized object under the same splice rules, then
commits one delta (or, on `document-tree` without a stored journal,
replaces the document base). If any op fails, no delta is written,
the document is unchanged, and the receipt is not success. An empty
`ops` array is `invalid-object`. It must not advance `seq`.

## 8. Operation `patch`

```
patch(address, expected-head, ops[])
```

`address` is the logical address tuple. Category must be `executive`,
and `context-id` must be present. `expected-head` is §5. `ops` is an
ordered, non-empty list from the closed vocabulary in §9.

Order of checks:

1. Surface, version, capability, and archetype obligations (§2). A
   missing required capability stops before any splice.
2. Address resolution. Absence, ambiguity, and non-executive targets
   fail as §2 states, before a write.
3. `expected-head` against the current head. Mismatch is `conflict`.
4. Apply ops in order on a working copy. The first refusal fails the
   whole request. Earlier ops in that request are not committed.
5. Persist under §4, then read back the materialized object and the
   resulting head. Readback must match the intended object and the
   head this request should have produced. An acknowledgement alone
   is not verification.

Receipts follow the contract's mutation receipt. A `patch` receipt
also identifies the previous head, the resulting head, the logical
revision before and after, and the op names. It does not replace
full readback. The same request identifier with the same canonical
payload returns the existing verified receipt and does not append a
second delta. The same identifier with a different payload is
`conflict`.

A retry after an unknown outcome re-reads the head and the object. If
the head advanced and the materialized object matches the intended
result, the write happened; do not append again. If the head is
unchanged, the write did not commit; a retry with the same
`expected-head` is allowed. If the head advanced and the object does
not match, `conflict`; reconcile by exact reads. Do not invent a
compensating delta.

`patch` does not add a writer and does not widen authority. Conduct
remains the executive writer. Delegated workers still report rather
than write.

## 9. Closed op vocabulary

Names and parameter sets below are closed. An unknown name, a missing
parameter, an extra parameter that changes meaning, or an op used on
a type that does not list it, is `invalid-object`. The whole request
fails. Parameters are logical fields, not a command-line spelling.

| Type | Legal ops |
|---|---|
| `tasks` | `check`, `uncheck`, `add-task`, `amend-task` |
| `plan` | `set-frontmatter`, `replace-section`, `append-section`, `append-to-section`, `remove-section` |
| `prd` | every `plan` op, plus `add-criterion`, `update-criterion`, `remove-criterion`, `set-criterion-status` |
| `walkthrough` | `append-entry` |

No other combination is legal. There is no `remove-task`, no
walkthrough rewrite, and no constitutive op.

### 9.1 Shared splice rules

Headings are ATX headings (`#` through `######`) at the start of a
line. A `heading` argument is the heading text without the marker and
without surrounding whitespace. Match is exact and case-sensitive
against that text, not a search over the body. Zero matches is
`invalid-object` (the object exists; the section does not). Two
matches at any level is `ambiguous`. The section body runs from after
the heading line until the next heading of the same or higher level,
or the end of the document, whichever comes first. Subsections are
inside the body.

`replace-section` replaces the body and keeps the heading line.
`remove-section` removes the heading line and the body, including
subsections. It does not remove YAML frontmatter. Removing the
document's single H1 title is `invalid-object`. `append-to-section`
inserts `content` at the end of the body, before the next heading.
`append-section` inserts a new heading of the anchor's level after
the anchor's entire section. `after` for `append-section` must name
an existing heading. The new heading text must not already exist;
a duplicate is `ambiguous`.

Inserted content starts on its own line. If the splice point lacks a
line break, insert one separator of the document's uniform newline
sequence. Do not trim or rewrap neighboring lines. Empty `content` is
legal for `replace-section` (the heading remains, the body becomes
empty) and illegal for `append-entry` and for `append-to-section`
(those ops would advance the journal without a change). Empty
`content` on `append-section` creates the heading and an empty body.

Frontmatter is the single YAML block delimited by opening and closing
`---` lines at the start of the document, as conduct templates use.
If that block is missing or unclosed, `set-frontmatter` is
`invalid-object`. The op does not invent a frontmatter wrapper.

### 9.2 Tasks

Task IDs are the current conduct tasks-template form: `T-` followed
by one or more digits, written on the checkbox line as `**T-NNN**`.
This reference does not allocate IDs. Existing IDs are never
renumbered. A gap is not a collision. Reuse of an ID that is present
is `conflict`.

A task checkbox line is a line of the form `- [ ] **T-NNN**` or
`- [x] **T-NNN**`. The capital `- [X]` form is treated as checked on
read, but `check` writes a lowercase `x`, so the result is
deterministic. Any other bullet or checkbox spelling is
`invalid-object`; do not repair it. A task block is that line through
the line before the next task checkbox line or heading.

| Op | Parameters | Effect |
|---|---|---|
| `check` | `ids` | Set each named task's checkbox to checked. |
| `uncheck` | `ids` | Set each named task's checkbox to unchecked. |
| `add-task` | `after`, `block` | Insert `block` after the anchor. |
| `amend-task` | `id`, `block` | Replace that task's block in place. |

`ids` is a non-empty ordered list. An empty list, a token that is not
a task ID, or an ID with no checkbox line is `invalid-object`. An ID
that appears on two checkbox lines is `ambiguous`. `check` of an
already checked task, and `uncheck` of an already unchecked task, is
a no-op for that ID, not `conflict`. Duplicate entries in `ids` are
the same no-op. Only the character inside the brackets changes.

`after` is either a present task ID or a heading text. A token that
matches a task ID selects that task, and the block is inserted
immediately after its task block. Otherwise `after` must match one
heading, and the block is inserted at the end of that section's body
(after phase metadata and existing tasks, before the next
same-or-higher heading). No match is `invalid-object`.

`block` must contain exactly one task checkbox line. For `add-task`
that ID must not already be present. For `amend-task` the ID must
equal `id`, and `id` must already be present. The op does not move
other tasks and does not rewrite their lines. A block that renumbers
or drops another ID is `invalid-object`.

### 9.3 Plan and PRD sections

| Op | Parameters | Effect |
|---|---|---|
| `set-frontmatter` | `key`, `value` | Set one top-level frontmatter key. |
| `replace-section` | `heading`, `content` | Replace that section body. |
| `append-section` | `after`, `heading`, `content` | Insert a sibling section after the anchor. |
| `append-to-section` | `heading`, `content` | Append to that section body. Plan amendments use this. |
| `remove-section` | `heading` | Remove that section. |

`key` is one top-level frontmatter name, not a dotted path. `type`
cannot be changed; the attempt is `invalid-object`. Other keys,
including unknown keys, may be set. Unnamed keys are preserved.
`value` must be representable as one YAML line. A key that already
occupies one line is replaced on that line. A missing key is appended
as one new line before the closing `---`. A multi-line value, or an
existing multi-line value for that key, is `invalid-object` rather
than a re-serialization. This is the draft and amendment path for
prose sections. It is not a way to drop permanent criterion IDs
(§9.4).

`append-to-section` does not create a missing section. The caller
names the heading. The current plan template's amendments heading is
an example of `heading`, not a special case the surface searches for
under another name.

### 9.4 PRD criteria

Criterion ops apply only to `prd`. The criteria block is the unique
fenced block opened by a line `` ```yaml `` and closed by a line
`` ``` ``, whose body is in the subset below. Zero such blocks is
`invalid-object`. More than one is `ambiguous`.

The subset is the shape the conduct PRD template already uses, so a
splice does not need a general YAML pretty-printer:

- a line `criteria:`
- each item begins with a line `- id: <token>` at one consistent
  indentation
- `id` is a single-line token
- `status`, when present, is a single-line scalar on its own line

Flow style, anchors, multi-line IDs, or any other shape is outside
the subset. Criterion ops then fail `invalid-object`. They do not
best-effort parse. While the document is still a legal draft (§9.5),
`replace-section` may replace the surrounding section with an
in-subset block. `read` does not require the subset; an out-of-subset
PRD remains readable.

| Op | Parameters | Effect |
|---|---|---|
| `add-criterion` | `yaml` | Append one criterion item. |
| `update-criterion` | `id`, `yaml` | Replace that item's bytes. Draft only. |
| `remove-criterion` | `id` | Delete that item. Draft only. |
| `set-criterion-status` | `id`, `status` | Set that item's `status` scalar. |

`yaml` is one criterion mapping supplied by the caller. The surface
inserts or replaces that item and preserves every other byte of the
block, including order. It does not re-emit YAML. Insertion is
deterministic: existing `- id:` lines must share one indentation, or
the op is `invalid-object`. The new or replacement item is the caller
bytes, shifted so its first line's `- id:` (or a supplied `id:` line,
which gains a `- ` prefix) sits at that indentation. Later lines keep
their indentation relative to the first line. No other whitespace in
the item is rewritten. The item is appended after the last existing
item, before the closing fence, with one separator newline if the
preceding byte is not already a newline. `set-criterion-status`
writes `status:` at the indentation of that item's existing `status`
line, or, if absent, at the indentation of its first key line other
than `- id:`. If the item has no such key line, use the `- id:`
indentation plus two spaces. The mapping's `id`
must be present. For `update-criterion` it must equal the parameter
`id`. Changing an ID through `update-criterion` is `invalid-object`
(that would renumber). An `id` that is already present makes
`add-criterion` a `conflict`. A missing `id` on update, remove, or
set-status is `invalid-object`, including when the document is
approved: absence of an ID is not a successful removal and is not
`not-found` of the PRD.

`set-criterion-status` replaces the item's single-line `status`
scalar, or inserts one at the end of the item if the key is absent,
using the item's indentation. The value must be a single-line plain
scalar with no line break. This op is legal in any document status,
including `approved` and `delivered`. It does not remove the item and
does not change its `id`. The current template's criterion statuses
are `open` and `delivered`. This reference does not add statuses and
does not re-read the template on each call. A consumer that must
enforce the template enum does so before the call. A value that
cannot be spliced as one scalar is `invalid-object`.

`add-criterion` is legal in any document status, so a corrective
criterion can be appended after approval. It still cannot reuse an ID
that is present.

Draft correction of a spec, while `status` is `draft`, is
`replace-section`, `update-criterion`, and `remove-criterion`, plus
the other section ops. The authority for "draft" is the materialized
frontmatter `status` scalar, not the name of a conduct phase.

### 9.5 ID permanence

Criterion IDs are permanent once the PRD is not a draft. The check is
exact, case-sensitive equality of the frontmatter `status` scalar with
`draft`.

- If the pre-patch materialized `status` is not `draft`, the patch is
  **frozen** for criterion identity.
- If `status` is missing or is not a single-line scalar, destructive
  criterion ops fail `invalid-object` (the surface cannot classify the
  document as a draft). Do not assume `draft`.
- If any op in the patch sets `status` to a value other than `draft`,
  the patch latches frozen for every later op. A later
  `remove-criterion` or `update-criterion` in that same patch fails,
  and the whole patch is rejected.
- `set-frontmatter` that would set `status` back to `draft` from a
  non-draft pre-patch status is `conflict`. This stops a patch from
  reopening permanence. It does not invent a tombstone store.

While frozen:

- `remove-criterion` of an ID that is present fails `conflict`.
- `remove-criterion` of an ID that is absent, or a criteria block that
  cannot be read as the §9.4 subset, fails `invalid-object`.
- `update-criterion` uses the same split: `conflict` when the ID is
  present, `invalid-object` when it is not or the block cannot be
  spliced.
- A section op that would change any byte inside the criteria fence,
  drop or reorder `- id:` tokens, or remove the section that contains
  the fence, fails `conflict` when the fence bytes and IDs can be
  compared, and `invalid-object` when they cannot. Preserving the
  fence bytes exactly is success for that check. `replace-section` is
  not a back door around `remove-criterion`.
- `set-criterion-status` and `add-criterion` of a new ID remain legal.

A conforming surface must not return success, `not-found`, or a
partially updated object for a frozen `remove-criterion`. The refusal
codes are only `conflict` and `invalid-object`, assigned as above, not
chosen freely.

While the pre-patch status is `draft` and the patch has not latched
frozen, `update-criterion` and `remove-criterion` are legal. Removal
does not record a tombstone. The surface therefore enforces uniqueness
of IDs that are **present** and permanence once the document is not a
draft. It does not enforce historical non-reuse of an ID removed
while the document was still a draft. Conduct's template still
forbids reuse; that duty stays with the writer. Compaction must not
be asked to remember retired IDs.

A human or external edit that changes `status` is not silently
overwritten. After reconciliation under the contract, the pre-patch
status of a later `patch` is whatever the reconciled object says. This
reference does not keep a hidden approved-bit to override that
reconciled read.

### 9.6 Walkthrough

| Op | Parameters | Effect |
|---|---|---|
| `append-entry` | `content` | Append `content` at the end of the document. |

`content` is non-empty. The surface does not interpret task IDs,
phase headings, or checkpoint blocks inside it. The caller supplies
the markdown the conduct walkthrough template requires. Earlier bytes
are preserved. Append is not idempotent except through the request
identifier in §8: a new request with a new head appends again.

## 10. `context-head`

On `record-store`, each executive context has at most one
`context-head` record. It is adapter bookkeeping, not a seventeenth
OKF type, not a constitutive object, and not an executive artifact.
`catalog` does not list it. `create`, `update`, and `patch` addressed
at it are `invalid-object`. `probe` may report that the record exists;
that report is not a logical read.

The record holds one slot per executive object in that context that
has a journal head beyond a purely implicit missing slot. Each slot
stores the logical address, the type, `seq`, `chain-digest`, and the
logical revision of the materialized object. It does not store full
content, deltas, or other contexts. A mutation updates the slot for
the patched object and writes one delta. It does not rewrite other
objects' bodies. Updating the head record may rewrite that small
record; that is the one head write the cost bound allows. It is not a
rewrite of the project catalogue.

A missing slot plus a readable base means the implicit head of §5.
The first `patch` creates the slot. `create` of an executive object
writes the logical object under the contract's create rules and need
not write a slot. The head is not a second catalogue: completeness
still comes from `catalog` and exact reads. A head that lists an
address `catalog` does not contain, or that cites a chain `read`
cannot materialize, is an inconsistent journal. `read` of that
address fails `invalid-object`. Do not adopt the head as catalogue
truth.

`document-tree` does not require this record. Its head is derived
from the document (§5). Inventing a sidecar `context-head` for a
document tree is a physical choice this reference does not make; §11
of the contract still requires a demonstrated gap before extra control
records.

Limits on delta size, delta count, and head-record size follow the
contract: the binding declares them with units, or declares them
unknown. No universal numeric maximum is set here. Exceeding a
declared limit is `limit-exceeded` before the write, never a silent
truncation. A sample that fit is not a maximum.

## 11. Compaction

```
compact(address, expected-head)
```

`compact` is part of the capability. Invoking it is optional. A
journal that has not been compacted is still valid. `read` and `patch`
must not compact implicitly, because an implicit compact would move
`expected-head` under the caller.

The pre-check is the same `expected-head` comparison, and it is still
not CAS. Mismatch is `conflict`, and nothing is retired.

When the head matches and at least one active delta exists:

- the new base is the materialized object, byte for byte at the
  logical level (same metadata, content, relations, and logical
  revision);
- active deltas are retired and are no longer inputs to
  materialization;
- the new head has `seq` `0` and the chain digest of that new base
  with an empty delta list;
- a `record-store` slot is updated to that head.

When there are no active deltas, `compact` succeeds, writes nothing,
retires nothing, and returns the existing head. That includes a
`document-tree` document realized as an implicit base.

Retired deltas are not logical objects and must not re-enter
`catalog`. They are not a history log unless the binding separately
declares the optional history capability. Logical history of record
is the constitutive log, not a retired delta. A binding that cannot
exclude retired deltas from materialization must not claim `compact`
succeeded.

The binding declares `executive-journal.compaction-threshold` as a
count of active deltas per object (unit: deltas), an integer greater
than or equal to `0`, or `unknown`. No default number is implied. When
the declared threshold is known and the active count exceeds it
(strictly greater), the executive writer should compact at the next
conduct phase boundary. The suggestion is advisory. Exceeding the
threshold does not fail `patch`, does not fail the phase gate, and
does not authorize the surface to compact on its own. An unknown
threshold means the suggestion does not fire; an explicit `compact`
is still allowed.

`compact` receipts follow the contract and identify the previous head,
the resulting head, the logical revision (unchanged), and how many
deltas were retired.

## 12. Archive, clear-work, and interchange

Archive and clear-work stay the contract's sequence. This capability
adds retirement of journal state bound to the frozen inventory. It
does not add objects to that inventory's logical catalogue.

Archive evidence for each frozen executive object that has a journal
binds the base, the active sequence range, the chain digest, and, on
`record-store`, the `context-head`. Deltas are identified by the
object address and sequence, not by new logical IDs. Unknown journal
state blocks cleanup the same way an unexpected logical object does.

`clear-work` removes the verified logical objects and, with them, their
bases, active deltas, residual retired deltas the binding can still
enumerate, and the context's `context-head` when no executive object
of that context remains. It removes a slot when the object remains
elsewhere only if that object was in the frozen inventory. It does not
touch another context, the project catalogue of surviving objects, or
the verified constitutive log. If residuals cannot be enumerated, the
outcome is partial or unknown; do not report a clean clear. A verified
log with retained journal state is recoverable. Cleared work without
a verified log is not.

`compact` is not archive. Archive does not require a preceding
`compact`.

Export and import, which `interchange.md` will realize later, operate
on the materialized object. Logical losslessness is equality of that
object: address, type, full content, metadata including unknown keys,
relations, and logical IDs. Journal lineage — base identity, deltas,
sequence, chain digest, head slots — is optional metadata. A complete
export does not require it. Omitting it is not, by itself, an
incomplete export. A target that drops lineage must say so; it must
not report lineage as preserved. Lineage is known optional journal
metadata, not an unknown extension whose survival is mandatory.

A monolithic object, a `1.0.x` object, and an export that has no
lineage are imported and read as an implicit base with `seq` `0` and
no deltas. Import does not replay deltas in order to be logically
lossless. If optional lineage is present and the target supports this
capability, the target may preserve it only when a following `read`
materializes the same object. It must not be required for activation.
Collisions remain conflicts, not upserts. Source heads are not target
concurrency tokens.

## 13. Errors

Journal results use the contract's codes. This reference adds none.

| Condition | Code |
|---|---|
| Address resolves to no object | `not-found` |
| Address, heading, task ID, or criteria block is not unique | `ambiguous` |
| Adapter version outside the accepted set | `unsupported-version` |
| Required journal capability or archetype evidence missing, including a 1.1 `record-store` without the stored journal | `missing-capability` |
| Unknown op, wrong type, empty `ops`, malformed head, missing section, missing task, out-of-subset criteria block, `type` change, splice that cannot be made without a rewrite, stored chain that cannot be applied | `invalid-object` |
| `expected-head` mismatch; frozen `remove-criterion` or `update-criterion` of a present ID; status rewind to `draft`; same request ID with a different payload; ID already present on `add-criterion` | `conflict` |
| Declared size or count exceeded before write | `limit-exceeded` |
| Write acknowledgement whose readback does not match the intended object or head | `verification-failed` |
| Some but not all journal residuals removed, with the survivors identified | `partial` |

A frozen `remove-criterion` does not return `not-found` merely because
the ID must be kept. Present ID and a readable non-draft object:
`conflict`. Unreadable block or absent ID: `invalid-object`.

An unknown write outcome stays unknown. It is not retried as a fresh
`create` or as a second `patch` until an exact read distinguishes the
cases in §8. Redact secret-bearing backend data in head records and
error evidence as the contract already requires.
