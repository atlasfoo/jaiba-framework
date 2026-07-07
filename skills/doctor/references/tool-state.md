# Diagnostic 2 — Tool state

**Question:** are the CLI tools the installed skills, subagents, and
hooks declare actually present on *this* machine?

This is the one diagnostic that **writes**: it refreshes
`.atl/tool-layout.md`. That file is machine state (gitignored, `AGENTS.md`
§6), not project memory, so rewriting it is squarely doctor's job — it
does not violate the "propose, don't patch" rule that governs the brain.
It is the same probe `scaffold` runs once at install time, re-run as a
maintenance check and widened to cover subagents and hooks.

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

   What it scans, across **each** skills directory given and its parent
   agent folder:
   - **Skills** — every `<skills-dir>/**/SKILL.md` `requires:` block.
   - **Subagents** — every `<agent-folder>/agents/*.md` that carries a
     `requires:` block. This includes the JAIBA battery `scaffold`
     installs into the **global** agents folder (`executor-high/
     medium/low`, `code-analyst`, `business-analyst`, `verify`) — the
     global skills dir passed to the probe makes its parent's `agents/`
     get scanned, so the battery's declared tools gain provenance rows
     (`subagent:executor-high`, …) automatically. If the battery is
     absent from a machine that has conduct installed, note it:
     `execute` will fall back to sequential mode until `jaiba-scaffold`
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
   - All present and all sources satisfied → ✅ healthy for this diagnostic.

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

The probe handles **CLI tools** — programs on `PATH`. It deliberately
does **not** try to verify **MCP servers**: whether an MCP is configured
and running is an agent-runtime fact the agent introspects directly, not
something a shell command can see. MCP availability is checked in
diagnostic 3 (reference health), where it's tied to the specific
reference that needs it. Don't duplicate that here.
