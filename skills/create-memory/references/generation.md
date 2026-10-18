# Generating a memory-surface extension

Use with the effective `create-memory` installation's
[contract](memory-surface-contract.md) and [resolution](resolution.md).
This procedure produces an adapter skill, not an executable backend layer.

## Discovery evidence

1. Record current host, visible tools and schema discovery mechanism. Inspect
   exact callable names, versions, required/optional arguments, output shapes,
   pagination tokens, truncation flags, errors and permissions. Tool names
   are evidence, not conventions to extrapolate. Sanitize evidence at capture.
2. Consult current documentation for the actual backend/tool version. For
   library/API/CLI questions use Context7 ID resolution then focused docs
   queries; record source/version/date. If docs and schemas disagree, block
   the disputed mapping pending clarification. No secret-bearing requests.
3. Probe approved existing scopes non-destructively. Establish exact ownership
   predicates and complete catalogue visibility, not just connectivity. Do
   not use a tool's implicit/default project as the confirmed project.
4. Build an operation matrix for `probe`, `resolve`, `catalog`, `read`,
   `create`, `update`, `append-log`, `archive`, `clear-work`, `export`,
   `import`. Each row gives real tool/schema, argument mapping from the full
   logical address, all steps, output/completion evidence, revisions,
   readback, errors, permissions, limits and status. If composed from several
   tools, describe and test the entire workflow, including interruptions.
5. Document pagination termination and consistency; chunk ordering/end marker
   and deterministic reconstruction; metadata/relation encoding; exact
   absence vs denied/hidden data; and changed-object detection. A hidden
   backend field cannot be claimed preserved without lossless evidence.
6. State actual concurrency guarantees. No native CAS claim from a normal
   update call, revision timestamp, or read/compare/write sequence. Without
   verified native CAS use demonstrated single-writer/serialized handoff;
   if uncontrolled writers remain, block mutation. Catalogue snapshots and
   native transactions are optional, not assumptions.

Unknown limits stay visibly unverified. If limits are necessary for safety,
block the affected operation until measured/documented. Do not probe limits
by sending production data or silently truncating it.

## Output package

Choose a user-confirmed, collision-free skill name and stable adapter ID.
Use the [surface template](../assets/memory-surface-template.md) as a starting
point, replacing all placeholders with supported facts or explicit pending
findings. Keep adapter version independent from contract version; this
generator's own framework version follows `.cz.toml`, not backend releases.

```text
<adapter-name>/
  SKILL.md
  references/backend-mapping.md
  references/conformance.md
  assets/configuration-template.md
  evals/evals.json
  evals/fixtures/                 # synthetic, no real memory or secrets
```

Additional references are useful when size warrants them; scripts are not a
way to hide a new driver/runtime or silently add a dependency. Generate only
what the chosen tools and approved task require.

### Skill and mapping

The description names what the skill does and specific trigger contexts:
consult it when resolving or operating its **selected** memory surface, not
every time a user mentions memory. An adapter is neither a workflow nor a
knowledge plugin. It does not override constitutive write ownership or gain
conduct's executive authority. Record actual tool dependencies in host-
supported `requires:` syntax; list dynamic capabilities in the mapping,
not as fictional callable names.

The generated skill resolves the host's effective `create-memory` skill and
reads `references/memory-surface-contract.md`, `resolution.md`, and relevant
filesystem/interchange references there. If unavailable, ambiguous or
unsupported, stop. Do not embed a forked canonical contract or use paths such
as `../../create-memory/...`. Resolve `jaiba-init` separately for OKF-owned
definitions when needed. These are discoverable dependencies, not broken
relative Markdown links to an assumed sibling installation.

Map all sixteen existing types without inventing backend-specific OKF types.
Preserve unknown/missing types for diagnosis, raw legacy documents and absent
frontmatter, full content, unknown metadata and original relation forms.
Stable IDs survive locator changes. Preserve log close IDs and immutable
history. Optional coordination remains separate and consumer-identified.

### Safe configuration

Adapt the effective [binding template](../assets/binding-template.md) into
an inactive example, never an auto-activated binding. Include only sanitized
IDs/locators/versions for host, absolute work root, adapter, namespace,
project registry/identity and context. Explain that eventual routing records
belong under `~/.jaiba/memory/` keyed by exact host and root, not `.ai/`.
Authentication uses the host's existing mechanism; do not read credentials
or generate live tokens/endpoints with embedded userinfo.

Document session-only consent if persistence is unavailable; do not fabricate
saved state, create an `.ai/` mirror or mint new contexts on retries. Installation
visibility is independent of backend account/namespace scope. Installing
globally must not hardcode one project's live binding for all projects.

### Evals and fixtures

Generate `evals/evals.json` with `skill_name` and `evals` entries containing
`id`, realistic `prompt`, `expected_output`, `files`, and observable
`assertions`. Follow the host's skill-creator schema if available. Example
case, to specialize with actual fixture paths and schema-backed tools:

```json
{
  "skill_name": "example-memory-surface",
  "evals": [{
    "id": 1,
    "prompt": "Use the approved isolated fixture project to roundtrip its multi-page inventory, update one concept, close only context A, then stage an export/import. Do not activate the target.",
    "expected_output": "Full preservation and verified receipts, with context B and the source intact; no activation.",
    "files": ["evals/fixtures/roundtrip.json"],
    "assertions": [
      "Every fixture catalogue page is consumed with explicit completion evidence.",
      "Exact readback equals the full expected payload including unknown metadata and relations.",
      "A verified closing log precedes deletion of only unchanged context A objects.",
      "Source inventory and context B are unchanged and the staged target is not activated."
    ]
  }]
}
```

Add negative cases: search-only tools; permission denial/truncated reads;
wrong namespace/project/context; ambiguous adapters; unavailable selected
adapter with no filesystem fallback; changed revision/concurrent writer;
oversize payload; duplicate close ID with same/different payload; new work
after archive; partial deletion; import collision or changed source; local
installation shadowing global; global installation with isolated scopes.
Check backend state and receipts, not whether output repeats safety wording.

Fixtures include multiple pages/chunks, linked objects, unknown nested fields,
unlinked log entries, multiple contexts, unrelated ordinary memory, malformed
types, and both filesystem layouts when applicable. Synthetic fixtures must
not require live secrets. Comparative agent evaluations/viewer runs require
their own approved evaluation step; generating cases is not running them.

## Validation and conformance

Fill the [conformance template](../assets/conformance-template.md). Before
live mutation confirm isolated fixture ownership, authorized operations and
writer discipline. Inventory the fixture scope first; never clear unrelated
objects to make a test pass. Real permission to create test data is required.

Execute every required family and full roundtrip. Record exact expected vs
observed state with redacted tool receipts, complete readback comparisons and
catalogue completeness evidence. Include failures and verified partial
effects; no fabricated results. Unsupported optional features are acceptable
unless required for a safe mapping. Missing mandatory operations mean
nonconforming; blocked/unrun checks mean unverified. A static review may
produce a useful draft but cannot certify a mutable surface.

Before delivery check frontmatter/description length, package-relative links,
placeholder and secret scans, JSON syntax, actual `requires:` availability,
and canonical dependency resolution through the target host. Do not interpret
syntactic checks as backend conformance. Report evidence scope, backend/tool/
adapter/contract versions and date; changing them requires revalidation.

## Installation without activation

1. Discover the current host's documented skill installation locations and
   resolution rules. Do not assume `.agents/skills`, `~/.claude/skills`, or
   any other host's directory is visible to this host. Read current host docs
   as needed; do not invent an installer command. Ask when visibility is
   uncertain.
2. Present draft-only, project-local and global-host options. Confirm the
   selected exact destination and files, status, dependency gaps and expected
   precedence effects before writing. Even a conforming extension is not an
   automatic installation authorization. A draft installed for inspection
   must be marked nonconforming and not exposed as a selectable
   `category: memory-surface` until all mandatory evidence passes.
3. Inspect the destination for collisions. Do not overwrite, merge or delete
   an existing skill automatically. Show a diff and obtain explicit replacement
   approval if necessary; preserve the prior installation for recovery.
4. Copy only the reviewed package. Do not bundle credentials, fixture run
   payloads, machine bindings or third-party services. Verify installed file
   contents and all internal links by readback; test host discovery in that
   scope (or report refresh/restart as pending). If the host cannot see it,
   report installed-on-disk but **not verified host-visible**.
5. Resolve the installed canonical dependency without assuming a sibling.
   Confirm adapter ID/version and whether a local copy shadows a global one.
   If multiple winning IDs remain, report ambiguity instead of choosing.
6. Report exactly what was installed and what was not. Leave active bindings,
   consumers, project markers, source data and the pinned first-party
   distribution untouched. Selection effects still need existing-data
   authority checks; installation does not authorize activation/migration.

No backend service installation, automatic dependency acquisition, implicit
instrumentation, source retirement or consumer patch belongs to this flow.
