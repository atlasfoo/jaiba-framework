# `conduct:summarize`

Close the selected work context: distill its essence, present it, propose
what the brain should learn, then obtain **one explicit confirmation** to
append the closing log and selectively clear verified executive memory.
Presenting first is mandatory; drafting and archiving unseen is not a
shortcut. Amendments require re-presentation and renewed confirmation.

## Preconditions and scope

- `validate` passed (gate green; criteria delivered or waivers recorded).
  Otherwise return to validate; summarize never substitutes for it.
- Use conduct's resolved surface, namespace, stable project ID and exact
  executive context. Resolve the effective `create-memory` installation
  through host skill resolution and read its canonical
  `references/memory-surface-contract.md` (§7 governs closure) and the
  selected binding instructions. Never assume sibling installations.
- Require complete catalogue, full reads, revisions, immutable idempotent
  append-log, archive evidence and selective clear-work. Establish actual
  serialized executive and shared constitutive writers. Missing capability,
  ambiguous ownership/context, inaccessible or partial data blocks closure;
  it is not an empty context or permission to fall back to filesystem.
- A plan and completed task evidence must be available, except on recovery
  from an already verified log with partially cleared work. Recover the
  original frozen inventory and close ID, not a new summary or close ID.

Filesystem keeps both supported layouts: resolve the concept bundle
through `index.md`, or the legacy flat brain when only `constitution.md`
exists. Both markers or neither block mutation. Do not migrate to close.
Filesystem locators below are examples, not logical addresses for external
surfaces. No constitutive editing is authorized beyond append-log.

## Flow

1. **Catalogue and fully read the exact executive context.** Read the
   entire plan, tasks, walkthrough and PRD when present, with completion
   evidence; `cat`/complete reads on filesystem, not search snippets or a
   truncated preview. Include malformed/unexpected objects in enumeration;
   surface them and stop cleanup. Freeze known addresses, full source
   payload/revision evidence, and the scope. Filesystem `.gitignore` is a
   preserved control file, not an executive concept.
2. **Draft the closing summary** using conduct's
   `assets/plan-summary-template.md`. A filesystem draft is
   `.ai/work/<slug>-summary.md`; an external draft may remain in the
   conversation until append, not a fabricated executive type or local
   durable mirror. Hard rules:
   - **English, always**, even when executive artifacts use another language.
   - **Concise**: one screen of outcomes, not the walkthrough's narrative.
   - Record delivered criteria (flag corrective ones), deviations and why,
     and waived checks.
   - **Preserve citations as verifiable links** under conduct's *Citing the
     brain* rules, retaining logical identity and the selected surface's
     direct locator. Filesystem links resolve from the eventual log home:
     `../identity/quality-gate.md` or `../decisions/004-event-bus.md` in a
     bundle; `../constitution.md` or `../reference-index.md` in legacy.
     Never replace links with prose, section numbers, fuzzy search or a
     local path for an external concept. Resolve dead links before archive;
     surface unresolved targets while the work evidence still exists.
3. **Evaluate brain changes.** For each non-trivial walkthrough decision,
   ask whether future work needs its structural *why*. If yes, include a
   proposed `decision` (status: Proposed). Otherwise state "No ADR proposed;
   all decisions were tactical." Likewise propose missing `reference`
   concepts and changes to `scope`, `quality-gate` or `sub-unit` when
   warranted. Name the concept by `type:` and preserve citations; only
   `jaiba-init:update-brain` enacts these proposals, under either layout.
4. **Suggest a final conventional-commit message**, inferred from the work
   (`feat` / `fix` / `refactor` / `perf` / `chore` / `docs`). Do not run git
   unasked. Assign a stable close ID before the first append attempt and
   bind the prepared payload to the exact project/context and inventory.
5. **Present and confirm.** Show the summary and its recoverable proposed
   log address, close ID, scope and exact cleanup inventory. Ask:
   *"Append this closing entry to <resolved log address>, verify its full
   readback, then clear only this unchanged work inventory in <context>?
   Proceed?"* One yes authorizes that payload and inventory only. After
   changes, freeze again and re-present; never reuse a previously appended
   close ID for a changed payload.
6. **Append, verify, then clear-work**, in that order:
   - Append-log uses the stable close ID as idempotency key. Same ID and
     identical complete payload reuses the verified receipt. Different
     payload is a conflict, never overwrite or automatic `-2` suffix.
   - Read the log **in full by exact address**, verifying the entire
     payload, close ID, scope and revision against the intended object.
     A write acknowledgement, search hit or preview is insufficient.
     Missing/mismatched readback leaves all executive work intact.
   - Retain the recoverable receipt: binding/version, project/context,
     close ID, log address/revision and exact frozen inventory/revisions.
     Evidence may be in the log and tool/conversation results; do not add
     a hidden durable cache or second memory copy.
   - Re-enumerate the complete context and reread known revisions before
     clear-work. Unexpected files/objects, directories, symlinks, changed
     revisions or ownership block cleanup **even if the log exists**.
   - Delete only those known, unchanged objects under serialized access,
     checking revisions at deletion. Verify absence with exact reads and
     complete enumeration, not search. No project/category-wide purge.
7. **Report and hand off.** Give the verified log's recoverable address,
   close ID/revision and exact cleanup outcome. Work is ready for the next
   task only after verified clearing; preserved control files are fine.
   If brain changes were proposed, hand off to `jaiba-init:update-brain`.

## Filesystem helper (only the resolved default filesystem context)

Resolve conduct's effective installation and read `scripts/archive.sh`
before use. It is a bounded local implementation, **not** a resolver or a
general memory backend. Never run it for external memory, another context,
mounted/symlinked scopes or another selected root. Do not create local
`.ai/work/` just to run it. Unsupported identifiers or a request to keep
executive objects require an explicitly reviewed surface operation (or a
stop), not an improvised recursive removal.

From the selected repository root, after resolving the stable IDs and
establishing serialized writers, prepare **before presenting**:

```bash
JAIBA_ARCHIVE_FILESYSTEM=1 JAIBA_ARCHIVE_SERIALIZED=1 \
  bash "<effective-conduct>/scripts/archive.sh" prepare "<slug>" "<project-id>" "<context-id>"
```

These flags attest caller-verified filesystem binding and single-writer
discipline; they are not locks, CAS or permission to guess identity. The
script checks Bash 4+ and each additional CLI dependency before mutation
(`git`, `grep`, `sed`, `tail`, `cat`, `cmp`, `date`, `mkdir`, `rm`). It
requires a safe nonempty **slug** containing letters/digits/dot/underscore/
hyphen and beginning with a letter or digit, because the slug enters paths.
Project/context IDs are opaque, exact, quoted single-line values: colon,
slash, spaces (including trailing spaces) and Unicode are preserved without
sanitizing, trimming or using them in paths. For example, a resolved project
ID may be `git:github.com/team/repo` or `path:/selected/project root`.
Empty IDs and any CR/LF are rejected before mutation. Shell arguments cannot
carry NUL. Pass the same exact IDs on retries; do not normalize identity in
this helper. The old single-slug invocation fails safely.

Prepare appends a visible, versioned receipt to the draft, naming the
contract/version, filesystem binding and project/context IDs, and freezing
the root/project/context fingerprint, close ID, full summary body fingerprint,
and byte fingerprints/absence for the four executive files and preserved
`.gitignore`. Git blob fingerprints use all bytes without filters, including
serialized metadata/relations; OS attributes are not logical revisions.
The close ID is `<YYYY-MM-DD>-<slug>` using plan `created:` (else UTC today).
The draft filename stays `<slug>-summary.md`; the eventual log is
`.ai/memory/log/<close-id>.md`. This receipt is closure evidence in the
visible draft/log, not a hidden store or a duplicate of executive contents.

Read the complete prepared summary back, present it, and obtain explicit
confirmation. Only then:

```bash
JAIBA_ARCHIVE_FILESYSTEM=1 JAIBA_ARCHIVE_SERIALIZED=1 \
  bash "<effective-conduct>/scripts/archive.sh" archive "<slug>" "<project-id>" "<context-id>"
```

Archive copies without overwrite, verifies the complete log against the
prepared payload, rechecks the frozen inventory, and removes only unchanged
`plan.md`, `tasks.md`, `walkthrough.md`, `PRD.md`, then the draft. It preserves
`.gitignore`. Any other entry (including a directory or symlink under a
known name) blocks the operation. It supports bundle and legacy markers
without editing either. It does not establish portable logical identity,
resolve backend declarations, validate acceptance criteria, or replace
conduct's full catalogue/read/confirmation obligations.

## Recovery and limits

- **Verified log, work retained:** recoverable, not failed archiving to
  redo with a new ID. Keep the log and original receipt. Reconcile exact
  reads, then retry `archive` with the same slug/project/context under
  serialization; do not `prepare` again. The log payload must match in
  full. Only unchanged residual executive files may be cleared.
- **Partial cleanup:** report removed and remaining objects exactly. The
  helper prints each verified deletion and retained inventory on failure.
  If the draft is gone, it requires the unique existing date/slug log and
  verifies its embedded scope, close ID and frozen evidence. It never
  recomputes a date from a missing plan or the retry day's clock.
- **Changed/new data:** stop and reconcile with the human. A prior log
  does not authorize deleting a new plan, modified work or new context.
  Do not edit old evidence or discard unexpected data to force a retry.
- **Append interrupted or readback unavailable:** work stays intact;
  report the candidate log address and unknown/partial outcome. An existing
  different/truncated entry is a conflict requiring reconciliation, not
  overwrite or a fresh append. Corrections are new entries referencing the
  old one, explicitly authorized, never historical edits.
- **No atomic transaction/CAS:** the helper uses compare/read/write/read
  under the caller's real serialization. It cannot police uncontrolled
  human/external writers. Without that discipline, block mutation. No
  archive/cleanup transaction is assumed; cleared work without a verified
  log is never an acceptable state.
