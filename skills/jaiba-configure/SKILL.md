---
name: jaiba-configure
description: Machine-level setup of JAIBA for the host agent. Installs or refreshes the global behavioral contract in the host's user-level config, installs the workflow/meta skillset (global, or project-local if the developer pins versions), and installs the subagent battery into the global agents folder. Not repo-scoped — instrumenting a specific project is jaiba-init's job. Safe to re-run to refresh a machine.
version: 3.0.0
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

## What this skill touches

`jaiba-configure` operates only within the host's global config root
(`~/.claude/`, `~/.agents/`, etc.) and its own packaged assets. Its full
read/write footprint:

**Writes:**
- `<global config root>/jaiba-contract.md` — installs/refreshes the contract
- the vendor's global instructions file (e.g. `~/.claude/CLAUDE.md`) —
  appends a one-line reference to the contract, if not already present
- `<global config root>/skills/` — installs missing skillset entries
  (global or project-local, per developer choice)
- `<global config root>/agents/` — installs/refreshes the subagent battery
- an installed subagent definition's own frontmatter — writes a `model:`
  line per tier, if the developer opts in

**Reads:**
- its own packaged assets: `assets/jaiba-contract.md`,
  `assets/skillset.txt`, `assets/agents/*.md`
- `npx skills list -g` output
- an installed skill's own
  `<global config root>/skills/<name>/SKILL.md` `version:` field
- the CLI's `.skill-lock.json` beside the global skills dir, if present
- the existing `<global config root>/jaiba-contract.md` and
  `<global config root>/agents/*.md`, to compare against the packaged
  versions
- the vendor's global instructions file, to check whether a contract
  reference line is already present

**Never reads:** chat/conversation history, credentials of any kind,
`settings*.json` (or any other hook/permission config), or anything else
in the global config folder beyond the paths listed above. Even though
it has filesystem access to the whole global config root, its read/write
surface is exactly what's enumerated here — nothing broader.

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
| Present but **different** (older version, or hand-edited) | **Ask** before overwriting — back up theirs to `<name>.bak-<YYYY-MM-DD>` (see step 2), or keep theirs and note the drift |
| Skill already in `npx skills list -g` | Leave it; point at `npx skills update -g` |

Never silently clobber a file the developer may have edited. Every
divergence is a question, not an assumption.

## The bootstrap sequence

Before anything else, tell the developer the jaiba-configure run has started.

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
a reference to `jaiba-contract.md` needs to land there. That file is the
developer's, not JAIBA's, and this skill did not create it — never
append to it silently. **Show the developer the diff** — the exact
one-line reference being added, and where it lands (appended at the
end, unless there's a clearer spot) — **and ask for explicit consent**
before writing. Only append after they say yes. If they decline, skip
the append, note the decline in the closing report, and say the agent
may not auto-load the contract without it. A line already present needs
no append and no ask.

- **Already there and identical** → leave it, note "already current".
- **Already there but different** (an older or hand-edited copy) — this
  is the one-per-machine file, so ask: **update** (back up theirs,
  install the packaged version) or **keep theirs** (note the drift;
  `jaiba-doctor` will keep flagging it). **Backing up theirs** means
  copying the developer's existing file to
  `<same-path>.bak-<YYYY-MM-DD>` (e.g. `jaiba-contract.md.bak-2026-09-15`)
  using **today's date** at the moment of the backup, **before** the
  packaged version overwrites the original. This is the one place this
  convention is spelled out in full; every other "back up theirs" in
  this file means exactly this.

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

1. **Read the packaged `ref:` pin — before anything else.**
   `assets/skillset.txt` carries a single `ref:` line (e.g. `ref: v2.1.0`)
   above the skill list, kept in lockstep with the framework's release
   tag by commitizen. That tag is the version every install in this step
   is pinned to. Read it **once**, here, and reuse that one value
   everywhere below — this skill only *reads* `ref:`, it never writes it.

   **If `skillset.txt` has no `ref:` line, stop this whole step.** Tell
   the developer plainly that the packaged `skillset.txt` carries no
   `ref:` pin, that this is a packaging error in `jaiba-configure`
   itself, and that installing without a pin would fetch whatever happens
   to be on the default branch at this moment. Do **not** fall back to an
   unpinned `npx skills add`, and do not guess or infer a ref from
   anywhere else. Skip the skillset entirely, continue to the subagent
   battery below, and say so in the closing report.

2. **List global skills for this agent:**
   ```bash
   npx skills list -g
   ```
   This prints the skills installed at the user level, e.g.:
   ```
   Global Skills

   jaiba-configure   ~/.agents/skills/jaiba-configure   Agents: ...
   conduct           ~/.agents/skills/conduct           Agents: ...
   ```
   Note what this output does **not** carry: no ref, tag or version
   column. It answers *"is it installed?"*, never *"at which ref?"* —
   that second question is answered in Case A below.

3. **Resolve the name to look for, per `assets/skillset.txt` entry:** every
   entry is a bare name (e.g. `conduct`); check that name directly against
   the global list. The `ref:` line is not an entry — it is the pin read
   in substep 1, never a skill to install.

   A line that is neither a comment, the `ref:` pin, nor a bare name —
   anything carrying a `/`, a `:`, a `#` fragment or other source syntax
   (e.g. `someoneelse/cool-skills-repo:turbo-lint`) — **is not an entry**.
   Skip it, never normalize it into a name, and never install from it:
   this skill installs only first-party skills from
   `atlasfoo/jaiba-framework`. Report that a malformed line was skipped
   and how many, so a planted entry isn't silently swallowed — but
   **never reproduce the line's content**, and never list it among the
   installed, already-current or pending skills. Echoing an untrusted
   source back into the report is what the skip exists to prevent.

4. **Split** the skillset into *already global* and *missing*.

**Case A — everything is already global.** Install **nothing** — then
check whether what *is* installed still matches the packaged `ref:`.
Presence alone is not currency:

- **Preferred signal — the installed skill's own `version:`.** Every
  JAIBA skill carries `version:` in its `SKILL.md` frontmatter, and it
  moves in lockstep with the release tag, so an installed
  `<global config root>/skills/<name>/SKILL.md` reading `version: 2.1.0`
  matches `ref: v2.1.0`. Read the artifact on disk; it is the one signal
  that doesn't depend on the CLI's output format.
- **Corroborating signal — the CLI's lockfile, if present.** The skills
  CLI may keep a `.skill-lock.json` beside the global skills directory
  recording each skill's `source`. If that source carries a `#<ref>`
  suffix, it names the pin the install was made from; a bare source with
  no `#<ref>` means that skill was installed **unpinned**, which is worth
  reporting on its own. Treat the file as best-effort: read it if it's
  there, don't manufacture it, don't fail the step over its absence.
- **Don't invent capabilities.** `npx skills list -g` shows no ref, so
  don't try to parse one out of it and don't pass it flags you haven't
  confirmed exist.

Then report accordingly:

- **Every installed skill matches the packaged `ref:`** → tell the
  developer their global skillset is complete and current at
  `atlasfoo/jaiba-framework#<ref>`, and point at `npx skills update -g`
  (or `npx skills update <skill> -g` for one at a time) as the upgrade
  path for the future.
- **One or more differ** → **name those skills specifically**, with what
  you found against the packaged `ref:` (e.g. "`conduct` is at
  `version: 2.0.1`, packaged ref is `v2.1.0`"), and point at
  `npx skills update -g` to bring them current.
- **The check was inconclusive** (no readable `version:`, no lockfile) →
  say so and say why. "Installed, ref not verified" is an honest answer;
  "everything is up to date" on the strength of presence alone is not.

Then go straight to the subagent battery below.

**Case B — one or more entries are missing globally.** Install nothing
yet. First build the **pre-install manifest** — one row per missing
entry, naming exactly what is about to land on this machine and from
where:

| skill | source#ref | scope |
|---|---|---|
| conduct | `atlasfoo/jaiba-framework#v2.1.0` | *(the choice below)* |
| jaiba-init | `atlasfoo/jaiba-framework#v2.1.0` | *(the choice below)* |

That table is illustrative: the rows are *this run's* missing entries,
and `#v2.1.0` stands for the `ref:` read in substep 1 — instantiate it
literally. Never show the developer a `<ref>` placeholder.

Then ask **one** structured question that puts that manifest and the
scope choice in the same breath. This is the confirmation gate: **no
`npx skills add` runs — and `-y` is never passed — until the developer
has answered it.**

- **Install all of the above globally** (recommended) —
  `npx skills add -y atlasfoo/jaiba-framework#<ref> --skill <skill> -g`.
  Available in every project on this machine from now on, and the scope
  that matches what `jaiba-configure` is for.
- **Install all of the above project-locally** — the same command without
  `-g`. Choose this only if the developer wants one project's skill
  versions pinned independently. It needs a target directory: use the
  **current working directory** as that project, resolving its agent
  folder the same way step 1 (*Identify the host agent*) resolves the
  global one (an existing vendor dir at that root, else `.agents/`), and
  installing into its `skills/` subdirectory. If the current directory
  clearly isn't the project the developer means, **ask** for the path
  rather than guessing.
- **Cancel** — install nothing and move on to the subagent battery,
  noting the skipped skills in the closing report.

One structured question with the manifest and these options is enough —
offer "decide per skill" only if the developer asks for it. The answer
applies to the **missing** entries only. Skills already global stay
exactly where they are: don't reinstall them, and don't also copy them
anywhere. If the developer changes the set (drops a skill, asks for a
different scope), show the amended manifest and confirm again — the rule
is that what runs is what they last saw.

`skillset.txt` entries are bare names of JAIBA skills from
`atlasfoo/jaiba-framework`, always pinned to the `ref:` from substep 1:
`npx skills add -y atlasfoo/jaiba-framework#<ref> --skill <name> [-g]`.

`#<ref>` is **not optional** — an unpinned source resolves to the default
branch, which is exactly the transparency hole this pin closes. `[-g]`
means: append `-g` if the developer chose global, omit it for
project-local. Process `skillset.txt` top to bottom: skip blank lines,
the `ref:` line, lines starting with `#`, any line that isn't a bare
name (substep 3), and entries already confirmed global in substep 3.
For each remaining (missing) entry, run the
appropriate command with the chosen scope flag. Install skills **one by
one** to ensure each is correctly registered:

```bash
# Example individual calls, with ref: v2.1.0 read in substep 1
# (global; drop -g for project-local)
npx skills add -y atlasfoo/jaiba-framework#v2.1.0 --skill conduct -g
npx skills add -y atlasfoo/jaiba-framework#v2.1.0 --skill jaiba-init -g
```

If no skills package manager is available, say so and fall back to
cloning each source **at the same `ref:` tag** (`git clone --depth 1
--branch <ref> …`) and copying the skill folders into the target — the
pin survives the fallback. Still prefer the package manager so
versions/locks stay honest.

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
- Already present but different → ask before overwriting — back up
  theirs to `<name>.bak-<YYYY-MM-DD>` (e.g.
  `executor-high.md.bak-2026-09-15`), same policy and naming as step 2.
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
   noted; if a backup was made when the developer chose to update over a
   differing file, name it (e.g. `jaiba-contract.md.bak-2026-09-15`).
   For the vendor's global instructions file: whether the developer
   consented and the reference line was added, or they declined and the
   append was skipped.
3. **Skills** — for each `skillset.txt` entry, whether it was already
   global (untouched), newly installed globally, or newly installed
   project-locally (and into which directory), each line naming the
   `source#ref` it came from (e.g. `atlasfoo/jaiba-framework#v2.1.0`),
   never a bare source. If Case A applied, say so plainly, report the ref
   check per skill — matching, drifted (with what you found), or not
   verifiable — and repeat the `npx skills update -g` reminder. If
   `skillset.txt` had no `ref:` line, report that the skillset step was
   **skipped as a packaging error** and that nothing was installed.
4. **Subagent battery** — which definitions were installed, skipped as
   current, or kept on the developer's request; name any backup file
   created for a definition that was overwritten (e.g.
   `executor-high.md.bak-2026-09-15`), so the developer can find their
   prior copy; or that the host lacks subagent support and `conduct`
   will fall back to sequential execution. Include the per-tier model
   result — pinned model or "inherits the orchestrator's model" for each
   of high/medium/low.
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
