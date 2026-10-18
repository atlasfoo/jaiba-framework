# `jaiba-init` — bootstrap mode

Adopt **this project** into JAIBA on its resolved surface. In filesystem
mode the end state is unchanged: the repo carries the
`AGENTS.md` marker, the `.ai/` brain skeleton and the `.atl/`
machine-state directory exist, the constitutive memory is populated, and
`jaiba-doctor` has run the first checkup.

This is the mode `jaiba-init` runs when invoked bare, with no sub-mode.
It is a *first-run* action, scoped entirely to one repository — it
installs **nothing** at the machine level. That half of the setup
(behavioral contract, skillset, subagent battery) belongs to
`jaiba-configure` and is only ever *checked for* here, never performed.

## Resolve first — external registration/linking

Apply SKILL.md's Universal Preconditions, binding/identity procedure,
mutation discipline and Phase3 gates **before** the filesystem sequence.
Resolve canonical definitions from the host-effective `create-memory`
installation, not a checkout or assumed sibling directory. These are
declarative operations using already available tools, not service setup.

For an **external** selection, run this branch instead of filesystem
steps 1–3 below:

1. Validate real callable tools, contract/version, all required guarantees
   and exact owned namespace/registry. A draft or unverified mutable adapter
   cannot be used to bootstrap. Failure is not an empty brain.
2. Resolve the sanitized origin/full namespace identity (absolute-root +
   host fallback only without origin). Inspect existing local memory/work
   without changing it. A populated-store transition is **blocked pending
   Phase5**, not a fresh initialization; offer the explicit filesystem
   exception. Do not transfer, ignore, merge or dual-write existing stores.
3. Look up the exact identity in the owned registry. If it already resolves
   a real external brain, verify the complete catalogue, full index and
   entry concepts, then **link**, do not seed/overwrite. Obtain explicit
   approval for a new alias or root association and check collisions first.
   Ordinary backend notes/search hits are never a brain to adopt.
4. If the registry identity is unknown, ask whether to associate an exact
   existing project or create a new project. New creation needs an
   authoritatively empty scope and explicit namespace/project approval;
   an empty catalogue alone is not instrumentation. Multiple matches,
   partial/template state or unknown ownership require reconciliation.
5. Confirm a fresh per-root context identity, or exact existing context
   with single-writer handoff. Only authorized registry identities may be
   created here; initial executive content stays empty. Persist and read
   back the routing-only host/root binding under `~/.jaiba/memory/`, or
   obtain explicit session-only consent. Verify registry writes individually
   with pre-read revision, full readback and receipt before proceeding.
6. Do **not** write the filesystem marker template, `.ai/` skeleton,
   `.ai/.gitignore`, `.gitkeep` files or any cache. External `AGENTS.md`
   override is optional selection data, written only if requested/approved,
   preserving existing content. Verify instrumentation from registry and
   real constitutive objects, never from that override.
7. For a new empty brain transition internally to `initialize`'s external
   branch. A verified existing brain needs no initialization; use `update`
   only for an approved content change. Hand off to `jaiba-doctor` for the
   checkup and local ATL probe, then report **consumer capability pending
   Phase4** and stop, not `conduct`/`ask`/`fast` or the battery.

ATL always lives at `<work-root>/.atl/tool-layout.md`, even with no local
brain. If ignore is needed without tracked repo changes, add the narrow
ATL exclusion to the Git-resolved local exclusion file, preserving existing
entries; do not create `.ai/` to hold machine state. The existing filesystem
bootstrap's self-ignoring `.atl/.gitignore` remains supported.

Report selected adapter/version, namespace/project/context IDs, sanitized
identity, verified catalogue/entry reads, binding persistence or session-only
status, mutation receipts/partial effects, gaps and pending capability.
Never report a mere binding/probe as completed instrumentation.

## When NOT to bootstrap — filesystem

If the repo is already instrumented, bootstrapping would clobber real
work. Read the state first, then pick the row.

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

1. **Where things landed** — selected surface and verified identity/binding;
   for filesystem, the agent folder detected for this repo and
   *why* (zero/one/many vendor dirs), the `.ai/` tree created, the
   `.atl/` directory, and where the repo `AGENTS.md` marker went (and how
   an existing one was handled).
2. **Global prerequisites** — whether the machine-level
   `jaiba-contract.md`, the workflow/meta skillset, and the subagent
   battery were found for *this agent*, and if not, an explicit "run
   `jaiba-configure`" recommendation naming what's missing.
3. **Brain state** — what `initialize` created or filled, and every
   `[MISSING]` / `[NEEDS CLARIFICATION]` that remains, per concept
   (`AGENTS.md` §5.4).
4. **Hand-off** — that control now passes to `jaiba-doctor` for the first
   checkup and the local `.atl/tool-layout.md` probe.

## Common failure modes

- **Bootstrapping an instrumented repo.** Overwriting a real
  `.ai/memory/` or `AGENTS.md`. Check the "When NOT to bootstrap" table
  first; route to `update-brain` mode when JAIBA is already there.
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
