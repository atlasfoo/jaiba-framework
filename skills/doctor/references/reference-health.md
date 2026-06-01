# Diagnostic 3 — External-reference health

**Question:** for every entry in `reference-index.md`, is the surface it
points at actually reachable *right now*? That breaks into three sub-
checks per entry: is its **access channel** available (the MCP/CLI it
names), is its **checkpoint reachable** (a remote spec/URL responds, a
vendored file exists), and — for vendored copies — is it **fresh** (not
drifted stale)?

This diagnostic is **read-only**: it tests, it doesn't repair. Fixes
route out — install the missing MCP/CLI, restore the dead endpoint, or
re-vendor via `update-brain`.

> Depends on diagnostic 1: if memory coherence found the index is still a
> bare template or riddled with `[MISSING]`, say so and note that
> reference health can't be meaningfully tested until the index is real.
> Don't test bracketed placeholder rows.

## How the index encodes a reference

Each row's "How to consult" / "Location" column uses the index's
vocabulary (see the reference-index template's "How to Consult"
section). The channel keyword tells you what to test:

| Channel in the index | What to verify |
|---|---|
| **MCP `<server>`** | the agent has that MCP server installed *and* enabled/running |
| **CLI `<tool>`** | the command is on `PATH` (overlaps diagnostic 2 — reuse that result) |
| **URL: `<addr>`** | the address responds (if web/fetch tools are available) |
| **Spec at `<path>`** | the file exists in-repo |
| **Vendored at `<path>`** | the file exists under `.ai/vendored/` **and** is fresh |

Walk all entries, but honor the index's **precedence**: §1–§3 (code-scope
— infra, external APIs, packages the running code needs) outrank §4
(workflow & verification tooling). A broken code-scope reference is a
heavier finding than a broken scanner, and the report ordering should
reflect that.

## Sub-check A — Access channel (MCP / CLI availability)

For each entry, test the channel it actually names:

- **MCP `<server>`** — introspect the agent's own available MCP tools and
  confirm a server matching `<server>` is present and responding. This is
  an agent-runtime fact you can see directly; the shell probe in
  diagnostic 2 **cannot** see it, which is why MCPs are checked here.
  Missing/disabled MCP that a code-scope reference depends on → **Broken**
  (a skill that tries to query it will fail). If you have no way to
  enumerate MCP servers in this runtime, mark the entry `[UNVERIFIED]`
  with that reason — never assume it's fine.

  *Example:* an entry says `How to consult: MCP postgres-mcp`. Check the
  agent's tools for a `postgres-mcp` server. Absent → "postgres-mcp not
  installed/enabled — the PostgreSQL reference is unreachable via its
  stated channel."

- **CLI `<tool>`** — you already inventoried CLI tools in diagnostic 2.
  Reuse that result rather than re-probing. If the named CLI is in the
  missing set, the reference is degraded/broken by the same token.

## Sub-check B — Checkpoint reachability

- **URL / remote spec** — if web or fetch tools are available, do a
  lightweight reachability check (a HEAD/GET that you don't need to fully
  read — you're testing the endpoint lives, not ingesting it). A remote
  OpenAPI URL that 404s or times out → **Broken** for that reference.
  **No web tools in this session?** Mark `[UNVERIFIED]` — *do not* report
  it as reachable. Stay within `AGENTS.md` §4: never fetch a
  secret-bearing URL or paste credentials; test only public/spec
  endpoints, and skip anything that looks like it carries a token.

- **Local spec / vendored path** — confirm the file exists at the path
  the index gives. A `Spec at docs/openapi/foo.yaml` or `Vendored at
  .ai/vendored/foo.txt` that isn't on disk → **Broken** (the index points
  at nothing — this is also the README's promise that doctor checks every
  vendored path resolves).

## Sub-check C — Vendored freshness (staleness)

Vendored copies are versioned-in-repo snapshots of an external surface
(`.ai/vendored/`). Their virtue is that they don't drift when upstream
changes — but that's also their risk: a months-old snapshot may no longer
match reality. So for each existing vendored file, get its **last
modification date from git** and compare to now:

```bash
git log -1 --format=%cs -- <vendored-path>   # YYYY-MM-DD of last commit touching it
```

- Older than **1 month** → **Degraded (stale)**: warn that the vendored
  reference may be outdated and suggest re-vendoring (re-pack the
  Repomix/OpenAPI copy) — the *fix* of recording the refreshed copy in
  the index is `update-brain`'s.
- Within a month → ✅ fresh.
- No git history for the path (untracked, just added) → not stale;
  note it's not yet committed if relevant, but don't flag as old.

Use the **commit** date, not the filesystem mtime — a fresh `git clone`
rewrites every file's mtime to checkout time, which would make every
vendored file look brand-new and defeat the check.

## Reporting

- **One finding per reference**, carrying: the reference name, the
  channel tested, and the result. Group by the index's precedence
  (code-scope findings before workflow-tooling findings).
- **Route each fix to its owner:** missing MCP/CLI → install it; dead
  URL → fix the endpoint or re-point the index (`update-brain`); missing
  vendored file or stale snapshot → re-vendor, then record via
  `update-brain`.
- **List `[UNVERIFIED]` entries explicitly** with the reason (no web
  tools, no MCP introspection). The framework's whole gap discipline
  (§5.4) is that an unchecked dependency must never masquerade as a
  healthy one.
