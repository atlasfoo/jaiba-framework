---
name: jaiba-configure
description: Machine-level setup of JAIBA for the host agent. Installs or refreshes the global behavioral contract in the host's user-level config, installs the workflow/meta skillset (global, or project-local if the developer pins versions), and installs the subagent battery into the global agents folder. Not repo-scoped — instrumenting a specific project is jaiba-init's job. Safe to re-run to refresh a machine.
version: 2.1.0
author: atlasfoo<iscomejia15@outlook.com>
requires:
  - git
  - bash
tags:
  - jaiba
  - meta
  - jaiba-meta
  - configure
---

# jaiba-configure

The **machine setup** skill. `jaiba-configure` installs JAIBA into the
*host agent itself* — the behavioral contract it reads, the skills it
can call, the subagents it can fan out to. It is a *global* meta-skill:
installed once into your agent (e.g.
`npx skills add -y atlasfoo/jaiba-framework --skill jaiba-configure`) and
run once per machine, from anywhere. It does not need — and does not
assume — a target repository.

Its scope is exactly three installs:

1. the **global JAIBA Behavioral Contract**, in the host's user-level
   config folder;
2. the **workflow/meta skillset** from `assets/skillset.txt`;
3. the **subagent battery** from `assets/agents/`, in the host's global
   agents folder.

Everything scoped to *one repository* — the `AGENTS.md` marker, the
`.ai/` brain skeleton, the `.atl/` machine-local state, the constitutive
memory, the first doctor probe — belongs to **`jaiba-init`**, a separate
skill run from inside the repo being adopted. `jaiba-configure` never
invokes it; it names it as the next step and stops.

The boundary in one line: **`jaiba-configure` sets up the agent;
`jaiba-init` sets up a project.** They share no file paths and no
templates — `jaiba-configure` owns **no brain templates** whatsoever
(`AGENTS.md` §1, the framework hierarchy).

## Re-running is fine

Unlike the repo-scoped bootstrap, global configuration is **idempotent by
design and safe to re-run** — that is how a machine gets refreshed after
a framework upgrade. There is no "already configured, refuse to
continue" state.

What changes on a re-run is only the *posture toward existing files*:

| Situation | What to do |
|---|---|
| Contract / subagent definition absent | Install it |
| Present and identical to the packaged version | Skip it, note "already current" |
| Present but **different** (older version, or hand-edited) | **Ask** before overwriting — back up theirs, or keep theirs and note the drift |
| Skill already in `npx skills list -g` | Leave it; point at `npx skills update -g` |

Never silently clobber a file the developer may have edited. Every
divergence is a question, not an assumption.

## The bootstrap sequence

Before anything else, run the greeting banner so the developer sees the
run has kicked off:

```bash
bash <this-skill>/scripts/greeting.sh
```

Then run the three steps below in order. Surface what you did at the end
(see **Closing**).

### 1. Identify the host agent

The contract, the skills and the subagent battery must land where *the
agent running this skill* looks for them. You are that agent — so
determine the vendor by **introspecting yourself**, not by scanning any
directory:

- You know your own identity (e.g. Claude Code → `.claude`, Cursor →
  `.cursor`, Gemini CLI → `.gemini`, Windsurf → `.windsurf`, opencode →
  `.opencode`, GitHub Copilot → `.github/copilot`). Use it.
- Corroborate — don't replace — that identity with the config folder you
  actually read from at the user level (e.g. an existing `~/.claude/`).
- **Can't determine it, or you resolve to more than one plausible
  vendor** → use the neutral `~/.agents/`. Don't guess a vendor.

This yields the **global config root** for the rest of the run, rooted at
the user's home directory: `~/.claude/`, `~/.agents/`, and so on. Create
it if absent. Its subdirectories are the install targets:

- `<global config root>/jaiba-contract.md` — the contract (step 2)
- `<global config root>/skills/` — globally installed skills (step 3)
- `<global config root>/agents/` — the subagent battery (step 3)

> `~/.agents/` is the *neutral default*, not a vendor — resolving to it
> means "vendor unknown", not "no agent".

### 2. Install or refresh the behavioral contract (global)

The behavioral contract is **split**: behavior lives once per machine in
the agent's global config; a repo carries only a minimal marker pointing
at it (installed by `jaiba-init`, not here).

Copy `assets/jaiba-contract.md` into the global config root from step 1
as `jaiba-contract.md`. Then make sure the agent actually loads it: if
the vendor has a global instructions file (e.g. `~/.claude/CLAUDE.md`),
append a one-line reference to `jaiba-contract.md` unless one is already
present.

- **Already there and identical** → leave it, note "already current".
- **Already there but different** (an older or hand-edited copy) — this
  is the one-per-machine file, so ask: **update** (back up theirs,
  install the packaged version) or **keep theirs** (note the drift;
  `jaiba-doctor` will keep flagging it).

Never inline the behavioral rules anywhere else; this file is their only
home.

### 3. Install the skillset and the subagent battery

The JAIBA workflow skills (`assets/skillset.txt`) can live **globally**
(`~/.claude/skills/`, `~/.agents/skills/`, …) shared across every repo on
this machine, or **project-locally** in one project's agent folder, when
a developer wants that project's skill versions pinned independently.
Before fetching anything, find out what's already there — reinstalling
something a developer already has globally duplicates it and fragments
versions across repos.

1. **List global skills for this agent:**
   ```bash
   npx skills list -g
   ```
   This prints the skills installed at the user level, e.g.:
   ```
   Global Skills

   jaiba-configure   ~/.agents/skills/jaiba-configure   Agents: ...
   conduct           ~/.agents/skills/conduct           Agents: ...
   ```

2. **Resolve the name to look for, per `assets/skillset.txt` entry:**

   | Entry format | Name to check against the global list |
   |---|---|
   | `conduct` (bare name) | `conduct` |
   | `owner/repo#skill` | the part after `#`, e.g. `caveman` |
   | `owner/repo` (no `#`, installs everything from that repo) | can't be resolved to one name from the listing — treat as **missing** below; `npx skills add` is idempotent, so a redundant run for this format is harmless |

3. **Split** the skillset into *already global* and *missing*.

**Case A — everything is already global.** Install **nothing**. Tell the
developer their global skillset is complete, and point them at
`npx skills update -g` (or `npx skills update <skill> -g` for one at a
time) to keep it current. Then go straight to the subagent battery below.

**Case B — one or more entries are missing globally.** Before installing
anything, ask the developer **once** how the missing skills should be set
up:

- **Global** (recommended) — `npx skills add -y <source> --skill <skill> -g`.
  Available in every project on this machine from now on, and the scope
  that matches what `jaiba-configure` is for.
- **Project-local** — the same command without `-g`. Choose this only if
  the developer wants one project's skill versions pinned independently.
  It needs a target directory: use the **current working directory** as
  that project, resolving its agent folder the same way step 1 resolves
  the global one (an existing vendor dir at that root, else `.agents/`),
  and installing into its `skills/` subdirectory. If the current
  directory clearly isn't the project the developer means, **ask** for
  the path rather than guessing.

A single structured question with these two options is enough — offer
"decide per skill" only if the developer asks for it. Apply the choice to
the **missing** entries only. Skills already global stay exactly where
they are: don't reinstall them, and don't also copy them anywhere.

`skillset.txt` uses two entry formats:

| Line format | Meaning | Install command |
|---|---|---|
| `conduct` (bare name) | JAIBA skill from `atlasfoo/jaiba-framework` | `npx skills add -y atlasfoo/jaiba-framework --skill conduct [-g]` |
| `owner/repo` | all skills from an external GitHub repo | `npx skills add -y owner/repo [-g]` |
| `owner/repo#skill` | one skill from an external GitHub repo | `npx skills add -y owner/repo --skill skill [-g]` |

`[-g]` means: append `-g` if the developer chose global, omit it for
project-local. Process `skillset.txt` top to bottom: skip blank lines,
lines starting with `#`, and entries already confirmed global in substep
2. For each remaining (missing) entry, run the appropriate command with
the chosen scope flag. Install skills **one by one** to ensure each is
correctly registered:

```bash
# Example individual calls (global; drop -g for project-local)
npx skills add -y atlasfoo/jaiba-framework --skill conduct -g
npx skills add -y atlasfoo/jaiba-framework --skill jaiba-init -g
npx skills add -y juliusbrussee/caveman --skill caveman -g
```

If no skills package manager is available, say so and fall back to
cloning each source and copying the skill folders into the target — but
prefer the package manager so versions/locks stay honest.

> `jaiba-configure` never installs *itself* (it's already global) or
> unbuilt skills, and only installs entries from `assets/skillset.txt` —
> keep that list current, not hardcoded in prose.

**Then install the subagent battery.** Copy every definition in
`assets/agents/` (the three executors `executor-high/medium/low` plus the
specialists `code-analyst`, `business-analyst`, `verify` — the battery
`conduct/references/subagents.md` invokes) into the `agents/`
subdirectory of the **global** config root from step 1 (e.g.
`~/.claude/agents/`), creating it if absent. They install globally for
the same reason the contract does: one battery serves every repo, and
`execute`'s fan-out expects to find them at the agent level, not
per-project.

- A definition already present and identical → skip it.
- Already present but different → ask before overwriting (back up
  theirs), same policy as step 2.
- The host agent has no native subagent support → skip the copy, say so,
  and note that `conduct` will run its documented sequential fallback.

**Then select a model per tier.** The packaged definitions ship with no
`model:` field — absent means "inherit the orchestrator's model", the
router-friendly default and the right choice on hosts where model
selection isn't meaningful. Offer to pin one instead:

1. **Discover what's available.** Enumerate the models the *current host
   agent* can run, from its own configuration or your own knowledge of it
   at runtime. Never hardcode a provider's model list in this skill —
   the roster is a property of the host you're running on right now, not
   of this file.
2. **Ask once, per tier, not per agent.** Three tiers group the battery:
   **high** (`executor-high` alone — top reasoning), **medium**
   (`executor-medium`, `code-analyst`, `business-analyst`, `verify` —
   balanced), **low** (`executor-low` alone — fast/cheap). A single
   structured question per tier, options built from step 1's discovery,
   plus **"leave blank — inherit the orchestrator's model"** always
   offered as a choice, never just an implied default. For example, on
   Claude Code the tiers might resolve to an Opus-class, a Sonnet-class,
   and a Haiku-class model respectively — but that mapping is illustrative
   of the *shape* of the choice, not a list to hardcode; a different host
   surfaces whatever roster it actually has. Offer "select the specialists
   separately from `executor-medium`" only if the developer asks — by
   default the medium tier's choice applies to all four of its agents.
3. **Write the result into the installed copies**, not the packaged
   source: a chosen model becomes a `model: <value>` line in that
   definition's frontmatter at the install destination; leaving a tier
   blank means the copy keeps no `model:` field at all. Re-running this
   step on an already-configured machine (§ Re-running is fine) shows the
   current per-tier state and asks again rather than silently preserving
   or silently overwriting it.

## Closing

End with a short, honest report:

1. **Which host, and where things landed** — the vendor you identified
   and *how* (self-identification, corroborated or not; or "unknown →
   `~/.agents/`"), and the global config root that follows from it.
2. **Contract** — installed / already current / kept theirs with drift
   noted, plus whether a reference line was added to the vendor's global
   instructions file.
3. **Skills** — for each `skillset.txt` entry, whether it was already
   global (untouched), newly installed globally, or newly installed
   project-locally (and into which directory), with the source. If Case A
   applied, say so plainly and repeat the `npx skills update -g`
   reminder.
4. **Subagent battery** — which definitions were installed, skipped as
   current, or kept on the developer's request; or that the host lacks
   subagent support and `conduct` will fall back to sequential execution.
   Include the per-tier model result — pinned model or "inherits the
   orchestrator's model" for each of high/medium/low.
5. **Next step** — if the developer's intent is to set up JAIBA for a
   *specific project*, tell them to run **`jaiba-init`** from inside that
   repo: it lays the `.ai/` brain skeleton and the `AGENTS.md` marker,
   initializes constitutive memory, and hands off to `jaiba-doctor` for
   the first checkup. Mention it; **do not invoke it** — this machine is
   now configured, and that is where `jaiba-configure` ends.

## Boundaries

- **Global only.** `jaiba-configure` configures the machine and the host
  agent. It creates nothing inside a target repository — no `.ai/`, no
  `.atl/`, no `AGENTS.md`. That is `jaiba-init`'s job. The single
  exception is a project-local *skills* install the developer explicitly
  asked for.
- **Owns no brain templates.** The constitution / adr-log /
  reference-index templates belong to the repo-scoped skills.
  `jaiba-configure` never carries or writes them.
- **Never clobber.** An existing contract or subagent definition that
  differs is the developer's; ask, back up, prefer a non-destructive
  path.
- **Hand off, don't chain.** Naming `jaiba-init` as the next step *is*
  the hand-off. Invoking it, or doing its work inline, would violate the
  split this skill exists to enforce.
- **Install from source, not siblings.** Fetch the skill set from the
  canonical repo via the package manager. No runtime path into another
  skill's folder.
- **Don't duplicate global skills.** If `npx skills list -g` already
  covers a `skillset.txt` entry, leave it there — don't reinstall it
  globally and don't also copy it into a project.

## Common failure modes

- **Scanning a repo to identify the vendor.** The host knows what it is:
  ask *yourself*, not the filesystem, and fall back to `~/.agents/` when
  the answer is ambiguous.
- **Guessing a vendor when the identity is unclear.** Two plausible
  answers is not a license to pick one — `~/.agents/` is the neutral
  home.
- **Doing `jaiba-init`'s work.** Creating `.ai/`, writing an `AGENTS.md`
  marker, or probing a project's toolchain "while we're here". Stop at
  the hand-off sentence.
- **Refusing to re-run.** Global config is refreshable by design; a
  second run is an upgrade path, not an error. Compare, ask on
  divergence, continue.
- **Copying sibling skills from this skill's own folder.**
  `jaiba-configure` has no copies. Install from the canonical source so
  versions stay honest.
- **Skipping the global-skills check.** Installing the full
  `skillset.txt` without first running `npx skills list -g` duplicates
  skills the developer already has and fragments versions across repos.
- **Reinstalling an already-global skill "just in case."** If it's in
  `npx skills list -g`, leave it — point the developer at
  `npx skills update -g`.
- **Finishing silently.** The developer needs the closing report —
  especially any drift they chose to keep, and the `jaiba-init` next
  step.
