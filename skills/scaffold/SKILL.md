---
name: jaiba-scaffold
description: First-run bootstrap of JAIBA into a project. Lays brain skeleton, installs the global behavioral contract plus the minimal AGENTS.md repo marker, installs workflow/meta skills and the subagent battery, then hands to update-brain (which hands to doctor for toolchain probe). One-time install only — don't use if .ai/ exists already.
version: 1.0.0
author: atlasfoo<iscomejia15@outlook.com>
requires:
  - git
  - bash
tags:
  - jaiba
  - meta
  - jaiba-meta
  - scaffold
---

# jaiba-scaffold

The **kickoff** skill. `jaiba-scaffold` is a *global* meta-skill —
installed once into your agent (e.g.
`npx skills add -y atlasfoo/jaiba-framework --skill jaiba-scaffold`), not
per-project — and run from inside a target repo to adopt JAIBA there.

It does the one-time install and nothing else. It lays the brain
skeleton, installs the **global JAIBA Behavioral Contract** into the
agent's user-level config (once per machine), drops the minimal
per-repo `AGENTS.md` marker at the project root, installs the
project-scoped JAIBA skills into the right agent folder plus the
subagent battery into the global agents folder, and then
**hands the project to `update-brain:initialize`**, which fills the
long-term brain from the repository. After that, scaffold has no further
role — the everyday work is `conduct`, `ask`, `fast`, and
`update-brain`.

Think of the boundary this way: **scaffold builds the empty house and
hands over the keys; `update-brain` moves the furniture in.** Scaffold
owns *structure and installation*; it owns **no brain templates** — those
belong to `update-brain` (`AGENTS.md` §1, the framework hierarchy). The
two never share a file path; the connection is a hand-off (skills
package independently).

## When NOT to scaffold

Scaffold is a *first-run* action. If the repo is already JAIBA-instrumented,
you'd be clobbering real work — stop and route instead.

| The repo already has… | Meaning | Route to |
|---|---|---|
| `.ai/memory/*.md` with **real content** | Fully instrumented | `update-brain` (drift/update), `conduct`, or `ask` |
| `.ai/` skeleton but **empty/bare** `memory/` | Half-scaffolded (a prior run stopped before the brain was built) | Resume: skip to **step 5** (hand off to `update-brain:initialize`) |
| Nothing JAIBA under `.ai/` | Greenfield or legacy, not yet adopted | Continue here |

If you're unsure which case you're in, read `.ai/memory/constitution.md`
(if it exists): bare `[brackets]` = skeleton, real prose = instrumented.
When still ambiguous, **ask the developer** rather than risk overwriting.

## The bootstrap sequence

Before anything else, run the greeting banner so the developer sees
scaffold has kicked off:

```bash
bash <this-skill>/scripts/greeting.sh
```

Then run the steps below in order. Steps 2–6 each have a precondition or
an edge case; don't barrel through them. Surface what you did at the end
(see **Closing**).

### 0. Confirm you're at the project root

You should be at the top of the repo the developer wants to adopt —
where `.git/` lives. If you can't tell, ask. Everything below is written
relative to this root.

### 1. Detect the agent folder

The JAIBA skills must land where *this* agent looks for skills. Detect by
counting vendor-specific agent config directories at the root:

- Look for: `.claude/`, `.cursor/`, `.gemini/`, `.windsurf/`,
  `.opencode/`, `.github/copilot/` (and similar vendor markers).
- **Zero found** → use the generic `.agents/` folder.
- **Exactly one found** → use that one (e.g. `.claude/`).
- **Two or more found** → use the generic `.agents/` folder (don't guess
  which vendor the developer means; `.agents/` is the neutral home).

The install **target** is the `skills/` subdirectory of the chosen
folder — e.g. `.claude/skills/` or `.agents/skills/`. Create it if
absent. Hold onto this path; `jaiba-doctor` will scan it when
probing the toolchain.

> `.agents/` itself is the *neutral default*, not a vendor — its presence
> does not count as "an agent is configured."

### 2. Lay the `.ai/` brain skeleton

Create the directory tree the brain lives in (empty — you are **not**
filling it; `update-brain` does that in step 5):

```
.ai/
├── memory/        (constitutive memory; update-brain fills this in step 5)
│   └── log/       (append-only record: closed work + brain changelog)
├── work/          (executive memory: PRD, plan, tasks, walkthrough; gitignored)
└── vendored/      (local copies of external refs; starts empty)
```

There is no `specs/` directory: when a change is deep enough to
produce a PRD, that PRD is an executive artifact and lives in `work/`
until the work closes and its essence is archived into `memory/log/`.

Then write `.ai/.gitignore` from `assets/ai.gitignore` — it ignores
`work/` (per-developer executive memory).
Add a `.gitkeep` to `memory/log/` and `vendored/` so the empty tracked
dirs survive a commit (`work/` is gitignored, so it needs none).

Also, create the `.atl/` directory at the project root and write its
`.gitignore` (from `assets/atl.gitignore`) containing `*` so that the
entire directory is ignored from source control, keeping machine-local
state out of the repository.

### 3. Install the behavioral contract (global) + the repo marker

The behavioral contract is **split**: behavior lives once per machine
in the agent's global config; the repo carries only a minimal marker
that points to it. Two installs:

**3a. Global contract — `assets/jaiba-contract.md`.** Determine the
*global* agent config folder matching the vendor detected in step 1,
rooted at the user's home directory (e.g. `~/.claude/` for `.claude/`,
`~/.agents/` otherwise — create it if absent). Copy
`assets/jaiba-contract.md` there as `jaiba-contract.md`, then make
sure the agent actually loads it: if the vendor has a global
instructions file (e.g. `~/.claude/CLAUDE.md`), append a one-line
reference to `jaiba-contract.md` unless one is already present.

- **Already there and identical** → leave it, note "already
  installed".
- **Already there but different** (an older or hand-edited copy) —
  this is the one-per-machine file, so ask: **update** (back up
  theirs, install the packaged version) or **keep theirs** (note the
  drift; `jaiba-doctor` will keep flagging it).

**3b. Repo marker — `assets/AGENTS.md`.** Copy the minimal per-repo
`AGENTS.md` to the repo root. It only confirms instrumentation, points
behavior at the global contract, and defers project facts to the
constitution.

**Edge case — the repo already has an `AGENTS.md`.** Do not overwrite it;
that's likely the developer's own contract. Stop and ask, offering two
non-destructive choices:

- **Replace** — back up theirs (e.g. `AGENTS.bak.md`) and install JAIBA's.
- **Coexist** — install JAIBA's as `AGENTS.jaiba.md` and tell the
  developer to merge or reference it from their own.

Never silently clobber an existing `AGENTS.md` — and never inline the
full behavioral rules into the repo copy; behavior belongs to the
global contract file.

### 4. Check what's already installed globally, then install what's missing

The project-scoped skills (`assets/skillset.txt`) can live **globally**
(`~/.claude/skills/`, `~/.agents/skills/`, …) shared across every repo on
this machine, or **locally** in this project's agent folder. Before
fetching anything, find out which is already true — reinstalling
per-project something a developer already has globally would duplicate
it and fragment versions across repos.

1. **List global skills for this agent:**
   ```bash
   npx skills list -g
   ```
   This prints the skills installed at the user level, e.g.:
   ```
   Global Skills

   jaiba-scaffold   ~/.agents/skills/jaiba-scaffold   Agents: ...
   conduct     ~/.agents/skills/conduct     Agents: ...
   ```

2. **Resolve the name to look for, per `assets/skillset.txt` entry:**

   | Entry format | Name to check against the global list |
   |---|---|
   | `conduct` (bare name) | `conduct` |
   | `owner/repo#skill` | the part after `#`, e.g. `caveman` |
   | `owner/repo` (no `#`, installs everything from that repo) | can't be resolved to one name from the listing — treat as **missing** below; `npx skills add` is idempotent, so a redundant run for this format is harmless |

3. **Split** the skillset into *already global* and *missing*.

**Case A — everything is already global.** Install **nothing** — not
globally, not into this project. Tell the developer their global
skillset already covers this project, and point them at
`npx skills update -g` (or `npx skills update <skill> -g` for one at a
time) to keep it current. Then go to step 5, pointing the toolchain probe
at the **global** skills directory instead of the project's (nothing was
installed there).

**Case B — one or more entries are missing globally.** Before installing
anything, ask the developer **once** how the missing skills should be
set up:

- **Global** — `npx skills add -y <source> --skill <skill> -g`. Available
  in every project on this machine from now on. Recommended for the JAIBA
  workflow skills, since most developers work across several repos.
- **Project-local** — the same command without `-g`, landing in the
  `skills/` subdir of the agent folder chosen in step 1. Use this if the
  developer wants this project's skill versions pinned independently.

A single structured question with these two options is enough — offer
"decide per skill" only if the developer asks for it. Apply the choice to
the **missing** entries only. Skills already global stay exactly where
they are: don't reinstall them, and don't also copy them into the
project.

`skillset.txt` uses two entry formats:

| Line format | Meaning | Install command |
|---|---|---|
| `conduct` (bare name) | JAIBA skill from `atlasfoo/jaiba-framework` | `npx skills add -y atlasfoo/jaiba-framework --skill conduct [-g]` |
| `owner/repo` | all skills from an external GitHub repo | `npx skills add -y owner/repo [-g]` |
| `owner/repo#skill` | one skill from an external GitHub repo | `npx skills add -y owner/repo --skill skill [-g]` |

`[-g]` means: append `-g` if the developer chose global, omit it for
project-local. Process `skillset.txt` top to bottom: skip blank lines,
lines starting with `#`, and entries already confirmed global in step 2.
For each remaining (missing) entry, run the appropriate command with the
chosen scope flag. Install skills **one by one** to ensure each is
correctly registered:

```bash
# Example individual calls (project-local; add -g for global)
npx skills add -y atlasfoo/jaiba-framework --skill conduct
npx skills add -y atlasfoo/jaiba-framework --skill update-brain
npx skills add -y juliusbrussee/caveman --skill caveman
```

If no skills package manager is available, say so and fall back to
cloning each source and copying the skill folders into the target —
but prefer the package manager so versions/locks stay honest.

> Scaffold never installs *itself* (it's global) or unbuilt skills, and
> only installs entries from `assets/skillset.txt` — keep that list
> current, not hardcoded in prose.

**Then install the subagent battery.** Copy every definition in
`assets/agents/` (the three executors `executor-high/medium/low` plus
the specialists `code-analyst`, `business-analyst`, `verify` — the
battery `conduct/references/subagents.md` invokes) into the
`agents/` subdirectory of the **global** agent folder from step 3a
(e.g. `~/.claude/agents/`), creating it if absent. They install
globally for the same reason the contract does: one battery serves
every repo, and `execute`'s fan-out expects to find them at the agent
level, not per-project.

- A definition already present and identical → skip it.
- Already present but different → ask before overwriting (back up
  theirs), same policy as 3a.
- The host agent has no native subagent support → skip the copy, say
  so, and note that `conduct` will run its documented sequential
  fallback.

### 5. Hand off to `update-brain:initialize`

The house is built; now fill the brain. Invoke `update-brain` in
**initialize** mode — it sweeps the repository and populates
`constitution.md`, `adr-log.md`, and `reference-index.md`, asking the
developer for what it can't derive. This is a real hand-off: scaffold
does not write `.ai/memory/` itself.

If `update-brain` isn't installed for some reason (step 4 was skipped or
failed), say so and point the developer at it — don't try to build the
brain yourself.

### 6. Hand off to `jaiba-doctor`

Once the brain has been initialized, hand control off to `jaiba-doctor`
to perform the first complete project checkup. This includes probing the
local machine toolchain for the installed skills (writing the local
`.atl/tool-layout.md`), checking memory coherence, and verifying external
references. By deferring the tool probe to `doctor`, we prevent duplication
and ensure the environment is fully verified with the newly populated memory.

## Closing

End with a short, honest report:

1. **Where things landed** — the agent folder used and *why* (zero/one/
   many vendor dirs detected), the `.ai/` tree created, where the global
   `jaiba-contract.md` went (installed / already current / kept theirs
   with drift noted), where the repo `AGENTS.md` marker went (and how
   any existing one was handled), and which subagent definitions were
   installed into the global `agents/` folder (or that the host lacks
   subagent support).
2. **Skills installed** — for each `skillset.txt` entry, whether it was
   already global (untouched), newly installed globally, or newly
   installed project-locally, and the source. If Case A applied
   (everything was already global), say so plainly and repeat the
   `npx skills update -g` reminder here.
3. **Hand-off** — that control now passes to `update-brain:initialize`, which will initialize the long-term memory, followed by `jaiba-doctor` to run the first checkup, probe the local machine toolchain, and write the local `.atl/tool-layout.md` file.

## Boundaries

- **One-time install only.** Scaffold sets up structure; it does not do
  project work and does not re-run as a maintenance tool. Re-adoption of
  an already-instrumented repo is `update-brain`, not scaffold.
- **Owns no brain templates.** The constitution / adr-log /
  reference-index templates belong to `update-brain`. Scaffold never
  carries or writes them — it lays empty dirs and hands off.
- **Never clobber.** An existing `AGENTS.md` or a populated `.ai/` is the
  developer's; ask before touching, prefer a non-destructive coexist
  path.
- **Don't fill the brain.** Step 6 is a hand-off, not a thing scaffold
  does. Writing `.ai/memory/` here would violate `AGENTS.md` §2.9.
- **Install from source, not siblings.** Fetch the skill set from the
  canonical repo via the package manager. No runtime path into another
  skill's folder.
- **Don't duplicate global skills.** If `npx skills list -g` already
  covers a `skillset.txt` entry, leave it there — don't reinstall it
  globally and don't also copy it into the project.

## Common failure modes

- **Scaffolding an instrumented repo.** Overwriting a real `.ai/memory/`
  or `AGENTS.md`. Check the "When NOT to scaffold" table first; route to
  `update-brain` when JAIBA is already there.
- **Guessing the agent folder when several exist.** Two vendor dirs is
  not a license to pick one — fall back to `.agents/`.
- **Copying sibling skills from scaffold's own folder.** Scaffold has no
  copies. Install from the canonical source so versions stay honest.
- **Blocking on a missing tool.** The tool check is advisory; record it
  and continue. AGENTS.md §6 keeps the warning alive.
- **Building the brain inline** instead of handing off to
  `update-brain:initialize`. Scaffold lays structure; it does not write
  memory.
- **Finishing silently.** The developer needs the closing report —
  especially missing tools and whatever `update-brain` still needs.
- **Skipping the global-skills check.** Installing the full
  `skillset.txt` locally without first running `npx skills list -g`
  duplicates skills the developer already has globally and fragments
  versions across repos.
- **Reinstalling an already-global skill "just in case."** If it's in
  `npx skills list -g`, leave it — point the developer at
  `npx skills update -g` instead of adding a project-local copy.
