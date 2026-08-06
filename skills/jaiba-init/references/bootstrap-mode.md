# `jaiba-init` — bootstrap mode

Adopt **this repository** into JAIBA. End state: the repo carries the
`AGENTS.md` marker, the `.ai/` brain skeleton and the `.atl/`
machine-state directory exist, the constitutive memory is populated, and
`jaiba-doctor` has run the first checkup.

This is the mode `jaiba-init` runs when invoked bare, with no sub-mode.
It is a *first-run* action, scoped entirely to one repository — it
installs **nothing** at the machine level. That half of the setup
(behavioral contract, skillset, subagent battery) belongs to
`jaiba-configure` and is only ever *checked for* here, never performed.

## When NOT to bootstrap

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

## The bootstrap sequence

Run the steps below in order. Each has a precondition or an edge case;
don't barrel through them. Surface what you did at the end (see
**Closing**).

### 0. Confirm you're at the project root

You should be at the top of the repo the developer wants to adopt —
where `.git/` lives. If you can't tell, ask. Everything below is written
relative to this root.

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

1. **Where things landed** — the agent folder detected for this repo and
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
