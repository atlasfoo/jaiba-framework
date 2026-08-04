# Diagnostic 1 — Memory coherence

**Question:** are the behavioral contract (repo marker + global copy)
and the constitutive brain in `.ai/memory/` — in whichever of the two
supported layouts the repository holds it, plus the append-only
`.ai/memory/log/` — complete, and consistent both with **each other**
and with the **repository**?

This diagnostic is **read-only**. doctor never edits `.ai/memory/` — that
is `jaiba-init:update-brain`'s sole right (`AGENTS.md` §2.9). Every brain
finding here resolves to the same prescription: *run
`jaiba-init:update-brain`* (update mode to reconcile drift, or initialize
mode if a file is still a bare template). The one exception is the
*global* contract in layer 0, which is machine-level and belongs to
`jaiba-configure`. Your job is to make the finding **specific enough to
act on**, not to fix it.

## What to check

Five layers, cheapest first. Stop escalating a given file once you've
found a Broken finding for it — the fix (`jaiba-init:update-brain`) is
the same regardless of how many more issues it has, and a deep audit is
that skill's job, not doctor's.

### Layer 0 — Behavioral contract (repo marker + global)

The behavioral contract is split across the two setup skills: a minimal
`AGENTS.md` marker in the repo (dropped by `jaiba-init`, bootstrap step
3), and the actual rules in `jaiba-contract.md` inside the agent's
**global** config folder (installed by `jaiba-configure`, step 2 — e.g.
`~/.claude/`, `~/.agents/`). Each half routes to its own skill. Check
both:

- **Repo marker.** `AGENTS.md` exists at the project root and points
  to the global contract (or is a legacy full JAIBA protocol — see
  below). Missing or unrelated → **Broken**; route to `jaiba-init`
  (bootstrap step 3 owns the coexist/replace decision).
- **Global contract present.** `jaiba-contract.md` exists in the
  global agent folder you located in the preconditions. A repo marker
  pointing at a contract that isn't there means every session runs
  ruleless → **Broken**; route to `jaiba-configure` (step 2 installs or
  refreshes it).
- **Drift vs the packaged version.** Diff the installed copy against
  this skill's own reference copy, `assets/jaiba-contract.md`
  (kept in lockstep with the canonical copy `jaiba-configure` ships):

  ```bash
  diff -q --strip-trailing-cr <global-agent-folder>/jaiba-contract.md <this-skill>/assets/jaiba-contract.md
  ```

  Different → **Degraded**: the machine runs older (or hand-edited)
  rules than the framework ships. Report *that* it drifted (quote the
  version marker in the file's first line if present); the fix is
  re-running `jaiba-configure` step 2, which asks before overwriting and
  backs up the developer's copy. Don't overwrite it yourself — doctor
  routes.
- **Legacy monolith.** A repo `AGENTS.md` that still contains the full
  behavioral protocol (numbered rules, brain map) instead of the
  minimal marker predates the global split → **Degraded**; works, but
  drifts silently as the framework evolves. Route to `jaiba-init`
  (bootstrap step 3, which offers replace/coexist for an existing
  `AGENTS.md`), and to `jaiba-configure` step 2 if the global contract is
  absent too.

### Layer 1 — Layout and graph integrity

`.ai/memory/` comes in two supported shapes, and which one the repo
holds decides how every later layer reads it. Resolve it exactly as
`jaiba-contract.md` §1 (Brain Map, *Dual resolution*) prescribes — this
file neither restates that rule nor adds cases to it. Same for the
bundle's vocabulary: the closed `type:` set, the directory layout and
the file-relative link convention live in
`jaiba-init/references/okf-pattern.md`, which is the authority here.
Every check below is a plain-markdown read — does this path exist, does
this frontmatter carry `type:`. Never invoke an OKF-specific tool,
parser or validator, and never report an *unknown* frontmatter key: the
tolerance rule makes `type:` the only key whose absence is a finding.

Resolved **legacy flat** (`constitution.md`, no `index.md`)? Nothing in
this layer applies — go to Layer 2 and read the flat files as before.
Resolved **neither**? There is no brain to diagnose: stop and route to
`jaiba-init` (see "When NOT to run doctor"). Resolved the **bundle**, or
found **both**, and these apply:

- **Ambiguous layout.** Both `.ai/memory/index.md` and
  `.ai/memory/constitution.md` present → **Broken**, and it halts *this*
  diagnostic (diagnostics 2 and 3 still run). A half-migrated brain read
  from the wrong half is worse than no brain, so do not pick a side and
  do not diagnose either half's contents — the contract's own instruction
  is to surface it to the human, not to choose. Report both paths and one
  discriminating fact about each (how many concepts `index.md` indexes,
  how long `constitution.md` is, which was touched last per `git log`), so
  the developer can tell an interrupted migration from an abandoned one.
  Route to `jaiba-init:update-brain:migrate`, which owns the conversion
  and its backup — and say plainly that doctor did not choose.
- **Broken link.** A markdown link inside a concept file whose target
  file does not exist. Resolve each link **relative to the file it is
  written in** — a link that only resolves from the repo root is itself
  the bug — and report the pair: **origin file → destination as written**,
  never a guess at what the destination was meant to be. Naming the
  dangling target and routing *is* the whole job. Severity splits on
  reachability: dangling **from `index.md`** → **Broken**, because the
  concept the index promises is unreachable from the entry point and
  every skill resolving by `type:` misses it; dangling **between
  concepts** (a decision's `superseded-by`, a scope's link to a
  reference, an executive artifact's `../memory/…` citation) →
  **Degraded**, the concept still resolves but the relation does not.
  Link targets that are URLs or vendored copies belong to diagnostic 3,
  not here. Route: `jaiba-init:update-brain` (update mode).
- **Concept without `type:`.** A markdown file in the bundle whose
  frontmatter has no `type:` key — or whose `type:` falls outside the
  closed vocabulary, which `okf-pattern.md` treats as the same reportable
  case → **Broken**. This is not cosmetic: every skill resolves the brain
  by asking for a `type:`, so a concept declaring none is invisible no
  matter how good its content is, and `index.md` cannot group it. Name
  the file, and quote the offending value when there is one; do **not**
  propose which type it should be — inventing a `type:` is precisely the
  failure mode `okf-pattern.md` names, and the call belongs to
  `jaiba-init:update-brain` (update mode) with the human. Missing
  *optional* keys (`title`, `description`, `tags`, `updated`) are at most
  a quality note, never a finding on their own.

> **The flat layout is not a finding.** A repository holding
> `constitution.md` / `adr-log.md` / `reference-index.md` and no
> `index.md` is **✅ Healthy** — the dual read is first-class support, not
> a fallback, and this layout is a deliberately supported state rather
> than drift toward broken. Report it, at most, as a one-line
> *informative* note saying which layout was diagnosed; never as
> ⚠️ Degraded, and never with a migration offer attached. The bundle is
> opt-in and human-triggered (`jaiba-init:update-brain:migrate`) —
> doctor diagnoses it, doctor does not nudge toward it.

### Layer 2 — Completeness (per file)

A brain artifact that still carries template residue is not yet a brain.
Scan each brain file — the three flat artifacts, or every concept in the
bundle — for:

- Unfilled template placeholders — `[bracket]` text left from the
  template.
- The canonical gap markers `[MISSING]` and `[NEEDS CLARIFICATION]`.

Any of these → **Broken** if the file is essentially still a template
(pervasive brackets), **Degraded** if it's mostly filled with a few gaps
remaining. This is the §5.4 discipline: an incomplete brain the
developer doesn't know about gets trusted as if it were complete.

> A file that is *all* brackets means initialize never finished (or never
> ran). That's still a finding here, not a stop condition — report it and
> route to `jaiba-init:update-brain` (initialize mode).

### Layer 3 — Internal coherence (file vs file)

The brain describes one project from several angles, and the angles must
agree. In the flat layout those angles are the three files; in the bundle
they are concepts you reach by `type:` through `index.md`. The
contradictions are the same either way — read each flat filename below as
shorthand for whichever concept carries that content (the constitution's
stack → the `architecture` concept, an `adr-log.md` entry → a `decision`,
a `reference-index.md` row → a `reference`). Look for contradictions such
as:

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
- **Curated vs chronological separation.** `adr-log.md` is *curated*
  memory (decisions currently in force); `.ai/memory/log/` is the
  *chronological* append-only record (work closures + brain
  changelog), one file per entry named `<YYYY-MM-DD>-<slug>.md`.
  Findings: work-history narrative accumulating inside `adr-log.md`
  (belongs in `log/`); a structural decision that exists only as a
  log entry with no ADR (should be proposed into `adr-log.md`); log
  filenames that don't follow the dated naming; an accepted ADR whose
  enactment has no `brain-change` log entry (the trail is broken).
- **Obsolete `.ai/` directories.** A `.ai/memory/archive/`, `.ai/specs/`,
  or `.ai/session/` directory still present means the project predates
  the `work/` + `memory/log/` layout — **Degraded**; route to
  `jaiba-init:update-brain` (update mode) and the framework README's manual
  migration notes. Note this is *not* the flat-vs-bundle question, which
  Layer 1 settles and which is never a Degraded finding: these
  directories are superseded in **both** supported layouts, and the dual
  read does nothing for them. Executive memory lives in `.ai/work/` and is
  gitignored; a tracked `work/` (or a tracked plan/tasks/walkthrough
  anywhere under `.ai/`) is a finding too.

### Layer 4 — Coherence with the repository (drift)

The brain is supposed to mirror the repo. Do a **light** drift sweep —
enough to catch obvious staleness, not a full re-analysis (that *is*
`jaiba-init:update-brain:update`). Cheap, high-signal probes:

- **Manifest vs constitution.** Does the language/stack the constitution
  claims match the actual manifest(s) (`package.json`, `pyproject.toml`,
  `pom.xml`, `go.mod`, …)? A constitution that says "Python service" over
  a repo that's now mostly Go is loud drift.
- **New external surfaces vs reference-index.** Scan config / compose /
  CI for services the index doesn't list — a `docker-compose.yml` with a
  `postgres` service, an env var pointing at a new API, a cross-component
  contract (event schema, internal API between sub-units) not in §3, a
  CI step invoking a scanner not in §5. Use `rg` for speed; don't read
  whole files.
- **Recency signal.** If `git log` shows substantial structural change
  (new top-level dirs, a dependency added, CI reworked) landing *after*
  the brain files were last touched, that's a drift smell worth flagging
  even if you can't pin the exact contradiction.

Keep this proportionate: doctor *detects and routes*; it does not
reconcile. Two or three concrete, evidenced contradictions are more
useful than an exhaustive audit.

## Reporting

- **Say which layout you diagnosed.** One informative line, before the
  findings — "concept bundle, 14 concepts indexed" or "legacy flat
  layout" — so the developer reads the rest in the right frame. It is
  context, not a finding: it carries no severity of its own, and the flat
  case in particular is neither a warning nor a migration prompt.
- **Make every finding evidenced and routed.** Not "brain is stale" but
  "`constitution.md` claims a Python stack; `pyproject.toml` is gone and
  `go.mod` is present — run `jaiba-init:update-brain` (update mode)."
- **Collapse to the right fix.** Pervasive brackets / a never-populated
  file → `jaiba-init:update-brain` **initialize**. Drift or a few gaps
  in an otherwise real brain, a dangling link, a concept missing `type:`
  → `jaiba-init:update-brain` **update**. Two layouts coexisting →
  `jaiba-init:update-brain` **migrate**, the only mode that owns the
  conversion.
- **Don't confabulate the fix content.** doctor says *what's wrong* and
  *which skill fixes it*; it never drafts the corrected constitution text
  — that would be patching the brain by the back door.
