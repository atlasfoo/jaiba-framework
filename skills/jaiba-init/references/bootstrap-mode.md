# `jaiba-init` — bootstrap mode

Adopt **this project** into JAIBA on its resolved surface. This skill is a
**1.1.0** consumer of `jaiba-memory-surface`. In filesystem mode the end
state is unchanged: the repo carries the `AGENTS.md` marker, the `.ai/`
brain skeleton and the `.atl/` machine-state directory exist, the
constitutive memory is populated, and `jaiba-doctor` has run the first
checkup.

External selection is **traceless**. JAIBA instruments the external brain
without writing any file into the repository. `AGENTS.md` and `.ai/` are
omitted. The only JAIBA record saved is machine binding `v2`. Zero
repository files are committed or dirtied.

This is the mode `jaiba-init` runs when invoked bare, with no sub-mode.
It is a *first-run* action, scoped entirely to one repository — it
installs **nothing** at the machine level except that routing binding.
The behavioral contract, skillset, and subagent battery belong to
`jaiba-configure` and are only ever *checked for* here, never performed.

## Resolve first — traceless external registration/linking

Apply SKILL.md's Universal Preconditions, binding/identity procedure,
mutation discipline and effective capability checks **before** the filesystem
sequence.
Resolve canonical definitions from the host-effective `create-memory`
installation, not a checkout or assumed sibling directory. Binding path,
digest, and consolidation rules are `references/resolution.md` §2 and §4.
Do not re-derive them. These are declarative operations using already
available tools, not service setup.

For an **external** selection, run this branch instead of filesystem
steps 1–3 below. Do not use the filesystem "When NOT to bootstrap" table
to decide that a missing `.ai/` means a greenfield brain.

### Traceless file rule

Traceless mode writes **no work-tree file**.

- Do not create `AGENTS.md`, `.ai/`, `.ai/.gitignore`, `.gitkeep`,
  `.atl/.gitignore`, a cache, or a mirror. `AGENTS.md` is not created by
  default.
- Do not `git add` and do not commit. After this branch, `git status`
  must show no new or modified tracked or untracked repository file from
  this run. Pre-existing files are left untouched and are not deleted.
- An explicit human request to write one `AGENTS.md` selection override
  leaves traceless for that file only. Preserve existing content, confirm
  the repository edit, and report that the zero-file guarantee no longer
  holds for that file. Do not offer this. Verify instrumentation from the
  registry and real constitutive objects, never from that override.
- `.atl/tool-layout.md` still belongs at `<work-root>/.atl/tool-layout.md`.
  This mode does not write it; `jaiba-doctor` does. Exclude the directory
  first so that later probe does not dirty the repo.

#### Git exclusion

When the work root is a Git checkout or worktree:

1. From that exact root, resolve the local exclude file with
   `git rev-parse --git-path info/exclude`. Use that path. Do not hardcode
   `.git/info/exclude` — a worktree's git dir is not the common git dir.
   The path is Git metadata, not a tracked repository file.
2. Read it if it exists. If a non-comment line is already `.atl`, `.atl/`,
   or `.atl/**`, leave the file unchanged.
3. Otherwise append exactly one line, `.atl/`, preserving every existing
   entry. Create the exclude file at the resolved git-path only when it
   is absent. Do not rewrite other lines.
4. Never create `.atl/.gitignore` or any other repository ignore file as
   a substitute.

Outside Git, report that exclusion is unavailable. Do not create
`.atl/.gitignore` to compensate, and do not claim `.atl/` is ignored.
The filesystem bootstrap's self-ignoring `.atl/.gitignore` remains the
filesystem-mode mechanism only. It is not used here.

### Link a verified brain, or create a project

1. Validate real callable tools, contract/version, all required guarantees
   and exact owned namespace/registry. A draft or unverified mutable adapter
   cannot be used to bootstrap. Failure is not an empty brain. This skill
   consumes contract **1.1.0**; a selected package whose contract major is
   not 1, or whose required capabilities are missing, blocks. Do not fall
   back to filesystem.
2. Resolve the sanitized origin/full path identity (absolute-root + host
   fallback only without origin). Inspect existing local memory/work
   without changing it. A populated-store transition is not fresh
   initialization: route an explicit migration request to `migrate-surface`
   (`references/surface-migration.md`), or offer the explicit filesystem
   exception. Require verified endpoint capabilities and separate
   staging/activation approvals; do not transfer, ignore, merge or
   dual-write existing stores under bootstrap. Do not delete local `.ai/`
   or `AGENTS.md` to make the checkout look traceless.
3. Apply the traceless file rule and Git exclusion above before any later
   step that could cause `jaiba-doctor` to write `.atl/`.
4. Look up the exact identity in the owned registry. A valid binding `v2`
   for this canonical root is reused without asking, including when
   `last-verified-by` names another agent; still recompute precedence and
   verify registry ownership. A malformed v2 record for this root stops.
   Do not repair it from legacy or from a sibling binding. If v2 is absent,
   consolidate agreeing legacy records for **this** root per
   `resolution.md` §4 before treating the project as unknown. Disagreeing
   legacy blocking fields need an explicit human choice, not a new project.
5. **Link.** If the identity already resolves a real external brain, verify
   the complete catalogue, full index and entry concepts, then link. Do not
   seed or overwrite. Do not run the questionnaire below. Obtain explicit
   approval for a new alias or root association and check collisions first.
   Ordinary backend notes, titles, and search hits are never a brain to
   adopt. A verified existing brain is not initialized again. Inventory
   depth does not apply: full must not overwrite it. Reuse the binding's
   `context-id` when v2 is valid. If this root has no context yet, confirm
   a fresh per-root context or an explicitly selected existing one — that
   single question is not the four-question form.
6. **Not in the registry.** Skip this step, step 7, and step 9 when step 5
   linked a verified brain; persist at step 8 if needed, then hand off.
   If this identity is unknown, no reusable v2 or
   agreeing legacy record names a project, and the lookup is an
   authoritative miss — not a permission error, partial page, or search
   miss — run the single questionnaire in the next section. Multiple
   matches, partial/template state, or unknown ownership stop for
   reconciliation. Do not create a second brain to get past a collision.
7. After the questionnaire, use the project-id and context choice already
   given in its third question. Do not ask either again. Only authorized
   registry identities may be created here. Initial executive content
   stays empty: no PRD, plan, tasks, or walkthrough. Verify each registry
   write with a pre-read revision, full readback, and receipt before the
   next write.
8. Persist binding `v2` at
   `~/.jaiba/memory/bindings/<sha256(canonical-work-root)>.yaml`
   (`binding-format-version: "2"`) per `resolution.md` §4, and read the
   routing fields back before claiming it saved. Do not create the file
   merely to test the path. Do not hash a URI, a trailing slash, or a
   relative path. Do not write `~/.jaiba/memory/<host-agent-id>/`.
   `host-agent-id` is provenance (`last-verified-by`), not a key. If
   persistence is unavailable, obtain explicit session-only consent or
   stop. A session-only selection is not the v2 file. Never mint a new
   context silently on every session.
9. **Create, then depth.** A new project needs an authoritatively empty
   scope. Empty catalogue alone is not instrumentation.
   - **minimal** — registry project, empty context identity, and binding
     `v2` only. Do not create constitutive concepts. Say plainly that the
     project is not yet instrumented.
   - **full** — after that empty scope is verified, transition internally
     to `initialize`'s external branch and populate the concept bundle.
     Still write no repository file.
   Linking an existing empty project uses the same depth choice. Linking
   a verified brain does not.
10. Hand off to `jaiba-doctor` for the checkup and the local ATL probe.
    Report verified versus unverified consumer capabilities. Later
    `conduct` / `ask` / `fast` or battery use needs its own effective
    surface procedure, callable tools, exact ownership, and approval.
    A green checkup alone grants no consumer mutation or activation
    authority. A binding or probe is not completed instrumentation.

Report selected adapter/version, namespace/project/context IDs, sanitized
identity, whether this run linked or created, inventory depth when it
applied, verified catalogue/entry reads, binding path or session-only
status, the exclude path or why exclusion was unavailable, mutation
receipts/partial effects, gaps, and pending capability. State that no
repository file was written, or name the one explicit override if the
human left traceless for `AGENTS.md`.

### Issue #17 C3 — one questionnaire, at most four questions

Run this only when the project is **not** in the registry and no reusable
binding already names it. Ask once. Use `ask_user_input_v0` if available,
otherwise one chat message. All four questions go in that single
questionnaire. Do not drip them across turns. Do not add a fifth question.
One topic per question. Unanswered questions block the action that needs
them. Closed options where the answer space is closed.

1. **Adapter / backend.** Confirm the already-selected external surface:
   adapter id, version, and contract **1.1.0** consumer. Options: confirm
   this surface, or stop. This is not a menu of every installed adapter
   and not a silent switch. A different backend is a selection change:
   stop and re-resolve. Ambiguous winning-level IDs are resolved by
   SKILL.md's selection rule before this questionnaire, not inside it.
   Declining does not fall back to filesystem.
2. **Namespace.** Confirm or customize the JAIBA-owned namespace. The
   default, when C4 below yields exactly one, is that sibling namespace.
   No sibling suggestion means there is no default: the human supplies
   the exact namespace or stops. Do not adopt the backend's default
   project, a title, or a search hit. Do not mint `jaiba/v4/<ns16>/` or
   any other namespace string.
3. **Stable project-id.** This one question is the link-versus-create
   decision, and it carries the per-root context choice so the
   questionnaire stays at four.
   - **Link** — the human confirms an exact existing `project-id`. Exact
     registry lookup and a collision check come first. A search hit is
     not a match. If that id is a verified brain, link and do not seed;
     question 4 does not authorize an overwrite.
   - **Create** — the human approves a new stable `project-id`. Do not
     derive it from the directory basename, branch, or session.
   - **Context**, in the same answer: default is a fresh context-id for
     this canonical work root. An existing context is used only when the
     human names it and an authoritative lookup plus single-writer
     handoff succeeds. Do not pick the latest plan, a branch name, or
     another checkout's context.
4. **Inventory depth.** Minimal versus full bootstrap, as defined in
   step 9 above. Ask it even when question 3 might link a verified brain;
   if the lookup then shows a verified brain, report that depth was not
   applied rather than asking again.

If a lookup inside question 3 reveals multiple matches, a partial or
template brain, or unknown ownership, stop. Do not finish create or full
initialize on that evidence.

### Issue #17 C4 — suggest `namespace` from sibling bindings

Before question 2, inspect existing routing bindings. Read routing fields
only: namespace, adapter id, sanitized identity (`kind`, host or host-id,
path, non-default port), and canonical work root. Do not print payloads,
credentials, raw remote URLs, or file bodies. A file that is not valid
routing YAML is skipped for suggestion. Do not repair or delete it.

Locations, and no others:

- `~/.jaiba/memory/bindings/*.yaml` — binding `v2`.
- Legacy: immediate child directories of `~/.jaiba/memory/` other than
  `bindings`, and the `*.yaml` records inside them. Do not follow a
  symlink out of `~/.jaiba/memory/`. Do not search the rest of the
  filesystem. Do not treat `bindings` as a host id.

This root's own binding is not a sibling. Sibling means either:

- **Remote.** Same sanitized host **and** same first path segment
  (the group) as this repo's origin candidate. `code.example` + `acme/payments`
  is a sibling of `acme/billing` on that host, not of `acme/billing` on
  another host, and not of `other/billing` on the same host.
- **Parent directory.** The other binding's canonical work-root parent
  equals this work root's parent. Do not walk higher. If the only shared
  parent is `/` or the user home directory, that match is too broad —
  do not suggest from it.

If one or more siblings have a configured namespace and those namespaces
agree, suggest that existing string as question 2's default. Show the
sibling's sanitized identity and adapter id beside it so confirmation is
not blind. The example shape of an existing Engram namespace is
`jaiba/v4/<sibling-ns16>/`; suggest the sibling's actual string, whatever
it is. Do not synthesize a new `ns16`, and do not copy the sibling's
`project-id` or `context-id`.

If sibling namespaces disagree, list the distinct strings as options
inside question 2. Do not pick by recency, host order, or basename.
A binding with no namespace is not a suggestion. Suggestion is a default,
not approval. The human confirms it in question 2.

## When NOT to bootstrap — filesystem

This table is filesystem only. An external selection does not use it:
absence of `.ai/` is expected in traceless mode and is not a greenfield
brain. If the repo is already instrumented on filesystem, bootstrapping
would clobber real work. Read the state first, then pick the row.

| The repo already has… | Meaning | Do this |
|---|---|---|
| `.ai/memory/index.md` (bundle) or flat `constitution.md` (legacy), either with **real content** | Fully instrumented | Don't bootstrap. Route to `jaiba-init:update-brain` (drift/update), `conduct`, or `ask` |
| `.ai/` skeleton but `memory/` holds neither `index.md` nor `constitution.md` — or only bare, untouched templates | Half-bootstrapped (a prior run stopped before the brain was built) | Resume: skip steps 1–3 and go straight to **step 4** (`update-brain:initialize`) |
| Nothing JAIBA under `.ai/` | Greenfield or legacy, not yet adopted | Continue with the full sequence below |

If you're unsure which case you're in, check `.ai/memory/` for
`index.md` (bundle layout) or `constitution.md` with no `index.md`
(legacy flat layout) — resolve per the dual-resolution rule in
`jaiba-contract.md` §1. Within whichever layout you find: bare
`[brackets]` = skeleton, real prose = instrumented. If **both**
`index.md` and `constitution.md` are present, that's the ambiguous case
the contract calls out — **ask the developer** rather than risk
overwriting.

## The bootstrap sequence — filesystem only

This sequence writes repository files. It is not traceless. Run it only
for a filesystem selection, or for an explicit filesystem exception that
retains existing local memory. An external selection uses the traceless
branch above, even when `.ai/` and `AGENTS.md` are absent.

Run the steps below in order. Each has a precondition or an edge case;
don't barrel through them. Surface what you did at the end (see
**Closing**).

### 0. Confirm you're at the project root

Use the exact checkout/worktree root established in Universal Preconditions,
not the common Git directory or the skill installation; without Git use
the absolute host workspace root. If ambiguous, ask. Everything below is
written relative to this root.

### 1. Detect this repo's agent folder

Detect which agent folder *this project* uses, by counting
vendor-specific agent config directories at the root:

- Look for: `.claude/`, `.cursor/`, `.gemini/`, `.windsurf/`,
  `.opencode/`, `.github/copilot/` (and similar vendor markers).
- **Zero found** → use the generic `.agents/` folder.
- **Exactly one found** → use that one (e.g. `.claude/`).
- **Two or more found** → use the generic `.agents/` folder (don't guess
  which vendor the developer means; `.agents/` is the neutral home).

Hold onto this path — it is where any *project-local* skills live, and
`jaiba-doctor` will scan it when probing the toolchain in step 5. This
detection is about **this repository's** vendor markers; it is not the
host-level introspection `jaiba-configure` does for machine-wide
installs.

> `.agents/` itself is the *neutral default*, not a vendor — its presence
> does not count as "an agent is configured."

### 2. Lay the `.ai/` brain skeleton

Create the directory tree the brain lives in (empty — you are **not**
filling it; step 4 does that):

```
.ai/
├── memory/          (constitutive memory; step 4 fills this)
│   ├── identity/    (empty; step 4 fills this)
│   ├── decisions/   (empty; step 4 fills this)
│   ├── references/  (empty; step 4 fills this)
│   └── log/         (append-only record: closed work + brain changelog)
├── work/            (executive memory: PRD, plan, tasks, walkthrough; gitignored)
└── vendored/        (local copies of external refs; starts empty)
```

There is no `specs/` directory: when a change is deep enough to
produce a PRD, that PRD is an executive artifact and lives in `work/`
until the work closes and its essence is archived into `memory/log/`.

Then write `.ai/.gitignore` from `assets/ai.gitignore` — it ignores
`work/` (per-developer executive memory).
Add a `.gitkeep` to `memory/identity/`, `memory/decisions/`,
`memory/references/`, `memory/log/` and `vendored/` so the empty
tracked dirs survive a commit (`work/` is gitignored, so it needs none).

Also, create the `.atl/` directory at the project root and write its
`.gitignore` (from `assets/atl.gitignore`) containing `*` so that the
entire directory is ignored from source control, keeping machine-local
state out of the repository.

### 3. Drop the repo marker `AGENTS.md`

Copy `assets/AGENTS.md` to the repo root. It is the minimal per-repo
marker: it only confirms instrumentation, points behavior at the global
contract, and defers project facts to the constitution.

**Edge case — the repo already has an `AGENTS.md`.** Do not overwrite it;
that's likely the developer's own contract. Stop and ask, offering two
non-destructive choices:

- **Replace** — back up theirs (e.g. `AGENTS.bak.md`) and install JAIBA's.
- **Coexist** — install JAIBA's as `AGENTS.jaiba.md` and tell the
  developer to merge or reference it from their own.

Never silently clobber an existing `AGENTS.md` — and never inline the
full behavioral rules into the repo copy; behavior belongs to the
**global** contract file.

**While you're here, check the global side — and only check.** The repo
marker points at a machine-level `jaiba-contract.md` (e.g.
`~/.claude/jaiba-contract.md`, `~/.agents/jaiba-contract.md`), the
subagent battery in the matching global `agents/` folder, and the
JAIBA workflow/meta skillset (`conduct`, `ask`, `fast`, `jaiba-doctor`,
…) — check your own skill list, not the machine's, since a machine can
have `jaiba-configure` run for one agent and not another. If any of the
three is absent, this agent was never configured:

- Say so plainly, name what's missing (contract, skillset, battery, or
  any combination).
- Point the developer at **`jaiba-configure`** as the prerequisite.
- **Do not install it yourself.** Global setup is `jaiba-configure`'s
  entire job; doing it here would rebuild the coupling this split
  removed.

The repo bootstrap can still finish without it — the marker, the
skeleton and the brain are all repo-local — but the developer must know
their agent will be running without the behavioral contract until they
run `jaiba-configure`.

### 4. Populate the brain — `update-brain:initialize`

The house is built; now fill it. Switch into this skill's
`update-brain` mode, `initialize` sub-mode, and follow
`references/initialize-mode.md`: it sweeps the repository and populates
the concept bundle — `index.md` plus one file per concept under
`identity/`, `decisions/` and `references/` — asking the developer for
what it can't derive.

This is an **in-skill mode transition**, not a hand-off — `jaiba-init`
owns the brain templates and the initialize logic itself. Don't stop and
tell the developer to invoke another skill; just continue into the mode.

### 5. Hand off to `jaiba-doctor`

Once the brain is initialized, hand control to `jaiba-doctor` for the
first complete project checkup: probing the local machine toolchain for
the installed skills (writing the local `.atl/tool-layout.md`), checking
memory coherence, and verifying external references. Deferring the tool
probe to `doctor` avoids duplicating the probe and verifies the
environment against the freshly populated memory.

This one **is** a real hand-off — it is where `jaiba-init`'s
responsibility ends.

## Closing

End with a short, honest report:

1. **Where things landed** — selected surface and verified identity/binding.
   For traceless: linked versus created, inventory depth if it applied,
   the binding `v2` path or session-only status, the `info/exclude` path
   or why exclusion was unavailable, and an explicit statement that no
   repository file was written (or the one approved `AGENTS.md` override).
   For filesystem: the agent folder detected for this repo and
   *why* (zero/one/many vendor dirs), the `.ai/` tree created, the
   `.atl/` directory, and where the repo `AGENTS.md` marker went (and how
   an existing one was handled).
2. **Global prerequisites** — whether the machine-level
   `jaiba-contract.md`, the workflow/meta skillset, and the subagent
   battery were found for *this agent*, and if not, an explicit "run
   `jaiba-configure`" recommendation naming what's missing.
3. **Brain state** — linked verified brain, minimal association (not yet
   instrumented), or what `initialize` created or filled. Every
   `[MISSING]` / `[NEEDS CLARIFICATION]` that remains, per concept
   (`AGENTS.md` §5.4). A binding alone is not instrumentation.
4. **Hand-off** — that control now passes to `jaiba-doctor` for the first
   checkup and the local `.atl/tool-layout.md` probe.

## Common failure modes

- **Bootstrapping an instrumented repo.** Overwriting a real
  `.ai/memory/` or `AGENTS.md`. Check the "When NOT to bootstrap" table
  first on filesystem; route to `update-brain` mode when JAIBA is already
  there. On an external surface, missing local files are not absence —
  link a verified brain instead of seeding it.
- **Dirtying the repo in traceless mode.** Creating `AGENTS.md`, `.ai/`,
  `.atl/.gitignore`, or any other work-tree file, or committing the
  exclude change. Exclusion belongs in `git rev-parse --git-path
  info/exclude`. Binding `v2` lives under `~/.jaiba/memory/bindings/`,
  not in the repository.
- **Dripping bootstrap decisions.** Asking adapter, namespace, project-id,
  and inventory depth as separate turns, or adding a fifth question, when
  the project is not in the registry. One questionnaire, at most four.
- **Inventing a namespace.** Minting `jaiba/v4/<ns16>/`, copying a
  sibling `project-id`, or treating a sibling suggestion as already
  approved. Suggest the existing sibling namespace as the default; the
  human confirms it.
- **Using full depth to overwrite a linked brain.** Inventory depth
  applies to a new or still-empty project. A verified brain is linked,
  not re-initialized.
- **Re-laying the skeleton on a half-bootstrapped repo** instead of
  resuming at step 4. An existing `.ai/` with a bare `memory/` is a
  *resume*, not a fresh start.
- **Guessing the agent folder when several exist.** Two vendor dirs is
  not a license to pick one — fall back to `.agents/`.
- **Installing global things.** Copying a contract, a skillset or the
  subagent battery into `~/.claude/` from here. Detect, report, route to
  `jaiba-configure` — never install.
- **Blocking on a missing global contract.** It's a warning, not a stop
  condition; the repo-local work still stands.
- **Treating step 4 as a hand-off.** `initialize` is this skill's own
  mode; continue into it rather than telling the developer to invoke
  something else.
- **Finishing silently.** The developer needs the closing report —
  especially the global prerequisites and whatever the brain still needs.
