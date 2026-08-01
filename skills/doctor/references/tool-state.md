# Diagnostic 2 — Tool state

**Question:** are the CLI tools the installed skills, subagents, and
hooks declare actually present on *this* machine?

This is the one diagnostic that **writes**: it refreshes
`.atl/tool-layout.md`. That file is machine state (gitignored, `AGENTS.md`
§6), not project memory, so rewriting it is squarely doctor's job — it
does not violate the "propose, don't patch" rule that governs the brain.
doctor owns this probe outright: `jaiba-init` defers the first run here
(bootstrap step 5) rather than probing itself, and every later checkup
re-runs it, widened to cover subagents and hooks.

## Procedure

1. **Run the bundled probe** against every skills directory you located in
   the preconditions — project-local, global, or both, joined with `:`:

   ```bash
   bash <this-skill>/scripts/check-tools.sh "<local-skills-dir>:<global-skills-dir>" <project-root>
   ```

   Pass just one path (no `:`) if only one of the two exists. The script
   derives required tools from three sources, unions a small framework
   baseline (`git bash rg curl`), checks each against the machine,
   records **which skill/subagent/hook needs each tool** (provenance),
   and rewrites `.atl/tool-layout.md`. It always exits 0 — the missing
   count comes back on stdout and in the file.

   Two things beyond the flat tool list:
   - Every `requires:` entry prefixed `mcp:` is classified separately from
     CLI tools — `command -v` can't resolve an MCP server, so these are
     never marked present or missing. They render as their own `❔
     [UNVERIFIED]` rows in **Probed Tools** and feed an **Unverified
     (MCP)** counter in the file header, distinct from `missing`/`total`.
   - The file also gets a full **`## Agent Layers`** section: every skill
     the probe scanned (name, origin — `framework` if its SKILL.md
     `tags:` carries `jaiba`, `external` otherwise — and its `requires:`
     list or "none declared"), every subagent likewise, and a one-line
     summary of what the hooks scan found. This is a straight inventory:
     a skill or subagent shows up here even if it declares no tools at
     all, so nothing scanned is invisible.

   What it scans, across **each** skills directory given and its parent
   agent folder:
   - **Skills** — every `<skills-dir>/**/SKILL.md` `requires:` block.
   - **Subagents** — every `<agent-folder>/agents/*.md` that carries a
     `requires:` block. This includes the JAIBA battery
     `jaiba-configure` installs into the **global** agents folder
     (`executor-high/
     medium/low`, `code-analyst`, `business-analyst`, `verify`) — the
     global skills dir passed to the probe makes its parent's `agents/`
     get scanned, so the battery's declared tools gain provenance rows
     (`subagent:executor-high`, …) automatically. If the battery is
     absent from a machine that has conduct installed, note it:
     `execute` will fall back to sequential mode until `jaiba-configure`
     reinstalls the definitions.
   - **Hooks** — the leading executable of each hook `command` in
     `<agent-folder>/settings.json` / `settings.local.json` (best-effort,
     `jq`-gated; hooks can run arbitrary shell, so only the invoked
     program is claimed). A global agent folder rarely has hooks/subagents
     of its own, but the probe checks anyway — cheap and avoids assuming.

   **Windows Shell Host Detection:**
   Under Windows, the probe introspects the shell environment to detect and label the flavor (e.g. `git-bash` via `$MSYSTEM` or `wsl` via `/proc/version` / `$WSL_DISTRO_NAME`). It annotates the `bash` baseline row accordingly so Git Bash and WSL are never conflated (they use different execution and path styles). On Linux/macOS, it reports `native`.

2. **Read the result back.** Open the refreshed `.atl/tool-layout.md` and
   turn its rows into findings:
   - A tool marked **❌ missing** → a **Broken** finding. Name the tool
     *and* its "Needed by" provenance — a missing tool whose only
     consumer is a hook you never trigger is less urgent than one a core
     workflow skill needs, and the developer can only judge that if you
     tell them who needs it.
   - A skill or source marked **❌ broken** in the **Skill-Specific Health Rollup**
     → a **Broken** finding naming the specific skill and its missing tool(s).
     This rollup ensures that skill-specific dependencies (such as `python`
     or `just`) surface prominently as an unhealthy *skill* instead of
     getting lost in a flat tool list.
   - A row marked **❔ [UNVERIFIED]** (in Probed Tools) or a source
     verdict of **❔ unverified** (in the rollup) → an **Unverified**
     finding, not a Broken one. It means "not checked here, route to the
     right verifier":
     - MCP entries (`mcp:*`, "verify via doctor diagnostic 3") → point the
       developer at diagnostic 3, which ties the MCP to the specific
       reference that needs it.
     - The `hook` rollup row reading "unverified — jq missing, hooks not
       scanned" → the fix is installing `jq` and re-running this probe,
       not diagnostic 3; hooks are a CLI-tool concern this diagnostic
       owns, it just couldn't parse `settings*.json` without `jq`.
     Don't fold either into the missing/broken count — a broken finding
     says "this will fail," an unverified one says "this wasn't checked."
   - All present and all sources satisfied (no unverified rows either)
     → ✅ healthy for this diagnostic.

3. **Compare against the previous probe if it matters.** If a tool that a
   running workflow assumed present is now missing, that's the §6.3
   "probe went stale" case — flag it prominently, because something that
   worked before will now fail mid-run.

## Reporting

- The "Needed by" column is the whole point — carry it into the report.
  "`sonar-scanner` missing" is weaker than "`sonar-scanner` missing,
  needed by skill:conduct's quality gate."
- The **fix** for a missing tool is an install, not another skill: say so
  plainly (e.g. "install `jq` — `brew install jq` / `apt install jq`").
  doctor doesn't install it for them.
- Mention that `.atl/tool-layout.md` was refreshed, so the developer knows
  the §6 session warning now reflects reality.

## Boundary

The probe handles **CLI tools** — programs on `PATH` — and that stays its
domain: it deliberately does **not** try to *verify* **MCP servers**.
Whether an MCP is configured and running is an agent-runtime fact the
agent introspects directly, not something a shell command can see.

What changed is that the probe now **indexes** what it can't verify,
instead of dropping it silently. `mcp:` entries in a skill's or
subagent's `requires:` get their own rows and provenance in
`.atl/tool-layout.md` — so they have a paper trail and are counted in
**Unverified (MCP)** — but they are never marked present (nothing probed
them) and never counted toward missing (absence of proof isn't proof of
absence). *Indexing* is this diagnostic's job; *verifying* MCP
reachability is diagnostic 3's, tied to the specific reference that
needs it. Don't duplicate that verification here — just make sure the
index points there.

The same index-vs-verify split applies to hooks when `jq` is missing:
the probe can't parse `settings*.json` without it, so it can't derive
hook tool needs — but instead of silently reporting zero hook
dependencies (indistinguishable from "hooks need nothing"), it emits an
explicit unverified marker in both the Agent Layers hooks summary
(`⚠️ Not scanned — jq is missing, so hook commands in settings*.json
could not be parsed. Hook-derived tool needs are unknown.`) and the
health rollup (`❔ unverified — jq missing, hooks not scanned`). The fix there is
narrower than MCP's: install `jq` and re-run this same probe, since
hooks are a CLI-tool fact this diagnostic is equipped to check once it
can parse the config.
