---
name: jaiba-scaffold
description: >-
  First-run bootstrap of the JAIBA framework into a project — the meta-skill that turns an un-instrumented repo into a JAIBA-instrumented one. Use this whenever JAIBA is not yet present and the developer wants to adopt it: "scaffold jaiba", "set up jaiba in this project", "initialize the jaiba framework here", "bootstrap jaiba", "install jaiba", "add jaiba to this repo", or the explicit /jaiba-scaffold call. It lays the `.ai/` brain skeleton and its internal `.gitignore`, installs the JAIBA behavioral `AGENTS.md`, installs the JAIBA workflow + meta skills into the project's agent folder (`.agents/`, or a detected vendor folder like `.claude/`), probes the local machine for the CLI tools those skills need and records them in `.ai/tools-state.md`, then hands off to `update-brain:initialize` to populate the long-term brain. Run it on greenfield and legacy repos alike, as the very first JAIBA action in a project. Do NOT use it when `.ai/` already exists or the project is already JAIBA-instrumented — building or reconciling the brain is `update-brain`, planning work is `planning`, asking what the brain says is `ask`; scaffold only does the one-time install, then steps aside.
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
skeleton, drops in the behavioral `AGENTS.md`, installs the
project-scoped JAIBA skills into the right agent folder, probes the
local toolchain, and then **hands the project to `update-brain:initialize`**,
which fills the long-term brain from the repository. After that,
scaffold has no further role — the everyday work is `planning`,
`specification`, `ask`, `fast`, and `update-brain`.

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
| `.ai/memory/*.md` with **real content** | Fully instrumented | `update-brain` (drift/update), `planning`, or `ask` |
| `.ai/` skeleton but **empty/bare** `memory/` | Half-scaffolded (a prior run stopped before the brain was built) | Resume: skip to **step 6** (hand off to `update-brain:initialize`) |
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
absent. Hold onto this path; the tool-check step (5) scans it.

> `.agents/` itself is the *neutral default*, not a vendor — its presence
> does not count as "an agent is configured."

### 2. Lay the `.ai/` brain skeleton

Create the directory tree the brain lives in (empty — you are **not**
filling it; `update-brain` does that in step 6):

```
.ai/
├── memory/        (update-brain fills this in step 6)
├── specs/         (mid-term; starts empty)
├── session/       (short-term; gitignored)
└── vendored/      (local copies of external refs; starts empty)
```

Then write `.ai/.gitignore` from `assets/ai.gitignore` — it ignores
`session/` (per-developer scratch) and `tools-state.md` (machine state).
Add a `.gitkeep` to `specs/` and `vendored/` so the empty tracked dirs
survive a commit (`session/` is gitignored, so it needs none).

### 3. Install the behavioral `AGENTS.md`

Copy `assets/AGENTS.md` (the JAIBA Behavioral Protocol) to the repo root
as `AGENTS.md`.

**Edge case — the repo already has an `AGENTS.md`.** Do not overwrite it;
that's likely the developer's own contract. Stop and ask, offering two
non-destructive choices:

- **Replace** — back up theirs (e.g. `AGENTS.bak.md`) and install JAIBA's.
- **Coexist** — install JAIBA's as `AGENTS.jaiba.md` and tell the
  developer to merge or reference it from their own.

Never silently clobber an existing `AGENTS.md`.

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
   planning         ~/.agents/skills/planning         Agents: ...
   ```

2. **Resolve the name to look for, per `assets/skillset.txt` entry:**

   | Entry format | Name to check against the global list |
   |---|---|
   | `planning` (bare name) | `planning` |
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
| `planning` (bare name) | JAIBA skill from `atlasfoo/jaiba-framework` | `npx skills add -y atlasfoo/jaiba-framework --skill planning [-g]` |
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
npx skills add -y atlasfoo/jaiba-framework --skill planning
npx skills add -y atlasfoo/jaiba-framework --skill specification
npx skills add -y juliusbrussee/caveman --skill caveman
```

If no skills package manager is available, say so and fall back to
cloning each source and copying the skill folders into the target —
but prefer the package manager so versions/locks stay honest.

> Scaffold never installs *itself* (it's global) or unbuilt skills, and
> only installs entries from `assets/skillset.txt` — keep that list
> current, not hardcoded in prose.

### 5. Probe the local toolchain

Run the bundled script against the directory (or directories) that
actually hold this project's JAIBA skills now, which depends on how step
4 went:

- **Case A (everything stayed global):** point the probe at the global
  skills directory — `~/<agent-folder>/skills`, e.g. `~/.claude/skills`
  or `~/.agents/skills` (same vendor folder name as step 1, rooted at the
  user's home directory).
- **Everything installed locally:** `<agent-folder>/skills` as before.
- **Mixed** (some stayed global, some were installed locally): pass both
  — `check-tools.sh` accepts a colon-separated list of directories.

```bash
bash <this-skill>/scripts/check-tools.sh "<skills-dir-1>[:<skills-dir-2>]" <project-root>
```

It derives the required tools from each installed skill's `requires:`
frontmatter, unions a small framework baseline (`git bash rg curl`),
checks each against the machine, and writes `.ai/tools-state.md`.

**Warn and continue — never block.** If anything is missing, name the
tool(s) and the skill(s) that need them in your closing report, but
proceed to step 6. The persistent warning lives in `AGENTS.md` §6, which
re-surfaces missing tools every session until they're resolved — so a
gap here is recorded, not lost.

### 6. Hand off to `update-brain:initialize`

The house is built; now fill the brain. Invoke `update-brain` in
**initialize** mode — it sweeps the repository and populates
`constitution.md`, `adr-log.md`, and `reference-index.md`, asking the
developer for what it can't derive. This is a real hand-off: scaffold
does not write `.ai/memory/` itself.

If `update-brain` isn't installed for some reason (step 4 was skipped or
failed), say so and point the developer at it — don't try to build the
brain yourself.

## Closing

End with a short, honest report:

1. **Where things landed** — the agent folder used and *why* (zero/one/
   many vendor dirs detected), the `.ai/` tree created, where `AGENTS.md`
   went (and how any existing one was handled).
2. **Skills installed** — for each `skillset.txt` entry, whether it was
   already global (untouched), newly installed globally, or newly
   installed project-locally, and the source. If Case A applied
   (everything was already global), say so plainly and repeat the
   `npx skills update -g` reminder here.
3. **Toolchain** — green if all present; otherwise list each **missing**
   tool and the skill(s) that need it (this is the §6 warning's first
   airing).
4. **Hand-off** — that control now passes to `update-brain:initialize`,
   and whatever it still needs from the developer (its own gaps report).

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
