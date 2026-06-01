# Diagnostic 1 — Memory coherence

**Question:** are the three long-term brain artifacts —
`constitution.md`, `adr-log.md`, `reference-index.md` — complete, and
consistent both with **each other** and with the **repository**?

This diagnostic is **read-only**. doctor never edits `.ai/memory/` — that
is `update-brain`'s sole right (`AGENTS.md` §2.9). Every finding here
resolves to the same prescription: *run `update-brain`* (update mode to
reconcile drift, or initialize mode if a file is still a bare template).
Your job is to make the finding **specific enough to act on**, not to
fix it.

## What to check

Three layers, cheapest first. Stop escalating a given file once you've
found a Broken finding for it — the fix (`update-brain`) is the same
regardless of how many more issues it has, and a deep audit is
`update-brain`'s job, not doctor's.

### Layer 1 — Completeness (per file)

A brain artifact that still carries template residue is not yet a brain.
Scan each of the three files for:

- Unfilled template placeholders — `[bracket]` text left from the
  template.
- The canonical gap markers `[MISSING]` and `[NEEDS CLARIFICATION]`.

Any of these → **Broken** if the file is essentially still a template
(pervasive brackets), **Degraded** if it's mostly filled with a few gaps
remaining. This is the §5.4 discipline: an incomplete brain the
developer doesn't know about gets trusted as if it were complete.

> A file that is *all* brackets means initialize never finished (or never
> ran). That's still a finding here, not a stop condition — report it and
> route to `update-brain` (initialize mode).

### Layer 2 — Internal coherence (file vs file)

The three artifacts describe one project from three angles; they must
agree. Look for contradictions such as:

- **Constitution stack ↔ reference-index.** The constitution names the
  project's stack, infrastructure, and quality gate. Anything external it
  mentions (a database, a third-party API, a scanner enforcing the gate)
  should have a corresponding `reference-index.md` entry. A datastore in
  the constitution with no index row is a gap; an index row for a service
  the constitution never mentions is the inverse.
- **ADR log ↔ constitution.** An accepted ADR that changed identity,
  scope, an upstream/downstream dependency, or the quality gate should be
  reflected in the constitution. An ADR superseding a decision the
  constitution still states the old way is drift.
- **ADR log integrity.** IDs contiguous from `ADR-001`, no rewritten or
  deleted past entries, supersessions reference the old ID (per the adr
  template's rules). A broken chain is a finding.

### Layer 3 — Coherence with the repository (drift)

The brain is supposed to mirror the repo. Do a **light** drift sweep —
enough to catch obvious staleness, not a full re-analysis (that *is*
`update-brain:update`). Cheap, high-signal probes:

- **Manifest vs constitution.** Does the language/stack the constitution
  claims match the actual manifest(s) (`package.json`, `pyproject.toml`,
  `pom.xml`, `go.mod`, …)? A constitution that says "Python service" over
  a repo that's now mostly Go is loud drift.
- **New external surfaces vs reference-index.** Scan config / compose /
  CI for services the index doesn't list — a `docker-compose.yml` with a
  `postgres` service, an env var pointing at a new API, a CI step
  invoking a scanner not in §4. Use `rg` for speed; don't read whole
  files.
- **Recency signal.** If `git log` shows substantial structural change
  (new top-level dirs, a dependency added, CI reworked) landing *after*
  the brain files were last touched, that's a drift smell worth flagging
  even if you can't pin the exact contradiction.

Keep this proportionate: doctor *detects and routes*; it does not
reconcile. Two or three concrete, evidenced contradictions are more
useful than an exhaustive audit.

## Reporting

- **Make every finding evidenced and routed.** Not "brain is stale" but
  "`constitution.md` claims a Python stack; `pyproject.toml` is gone and
  `go.mod` is present — run `update-brain` (update mode)."
- **Collapse to the right fix.** Pervasive brackets / a never-populated
  file → `update-brain` **initialize**. Drift or a few gaps in an
  otherwise real brain → `update-brain` **update**.
- **Don't confabulate the fix content.** doctor says *what's wrong* and
  *which skill fixes it*; it never drafts the corrected constitution text
  — that would be patching the brain by the back door.
