# Diagnostic 2 — Tool state

**Question:** are the CLI tools the installed skills, subagents, and
hooks declare actually present on *this* machine?

This is the one diagnostic that **writes**: it refreshes
`.ai/tools-state.md`. That file is machine state (gitignored, `AGENTS.md`
§6), not project memory, so rewriting it is squarely doctor's job — it
does not violate the "propose, don't patch" rule that governs the brain.
It is the same probe `scaffold` runs once at install time, re-run as a
maintenance check and widened to cover subagents and hooks.

## Procedure

1. **Run the bundled probe** against the skills directory you located in
   the preconditions:

   ```bash
   bash <this-skill>/scripts/check-tools.sh <agent-folder>/skills <project-root>
   ```

   The script derives required tools from three sources, unions a small
   framework baseline (`git bash rg curl`), checks each against the
   machine, records **which skill/subagent/hook needs each tool**
   (provenance), and rewrites `.ai/tools-state.md`. It always exits 0 —
   the missing count comes back on stdout and in the file.

   What it scans:
   - **Skills** — every `<skills-dir>/**/SKILL.md` `requires:` block.
   - **Subagents** — every `<agent-folder>/agents/*.md` that carries a
     `requires:` block.
   - **Hooks** — the leading executable of each hook `command` in
     `<agent-folder>/settings.json` / `settings.local.json` (best-effort,
     `jq`-gated; hooks can run arbitrary shell, so only the invoked
     program is claimed).

2. **Read the result back.** Open the refreshed `.ai/tools-state.md` and
   turn its rows into findings:
   - A tool marked **❌ missing** → a **Broken** finding. Name the tool
     *and* its "Needed by" provenance — a missing tool whose only
     consumer is a hook you never trigger is less urgent than one a core
     workflow skill needs, and the developer can only judge that if you
     tell them who needs it.
   - All present → ✅ healthy for this diagnostic.

3. **Compare against the previous probe if it matters.** If a tool that a
   running workflow assumed present is now missing, that's the §6.3
   "probe went stale" case — flag it prominently, because something that
   worked before will now fail mid-run.

## Reporting

- The "Needed by" column is the whole point — carry it into the report.
  "`sonar-scanner` missing" is weaker than "`sonar-scanner` missing,
  needed by skill:planning's quality gate."
- The **fix** for a missing tool is an install, not another skill: say so
  plainly (e.g. "install `jq` — `brew install jq` / `apt install jq`").
  doctor doesn't install it for them.
- Mention that `.ai/tools-state.md` was refreshed, so the developer knows
  the §6 session warning now reflects reality.

## Boundary

The probe handles **CLI tools** — programs on `PATH`. It deliberately
does **not** try to verify **MCP servers**: whether an MCP is configured
and running is an agent-runtime fact the agent introspects directly, not
something a shell command can see. MCP availability is checked in
diagnostic 3 (reference health), where it's tied to the specific
reference that needs it. Don't duplicate that here.
