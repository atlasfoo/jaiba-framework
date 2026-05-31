# `update-brain:initialize`

Build the long-term brain for the first time. End state: the three
artifacts exist and are populated from real repository evidence —
`.ai/memory/constitution.md`, `.ai/memory/adr-log.md`,
`.ai/memory/reference-index.md` — every determinable fact filled, every
undeterminable one either resolved by asking or marked and surfaced.

This is the onboarding mode. It runs on a brand-new project, on a legacy
codebase being adopted into JAIBA, or right after `scaffold` lays the
`.ai/` skeleton and hands off.

## Preconditions

1. The brain does not meaningfully exist yet: either `.ai/memory/*.md`
   are absent, or they are untouched templates (full of `[brackets]`).
   If they already carry real content, this is `update`, not
   `initialize` — stop and switch.
2. `.ai/memory/` exists (or you can create it). If the wider `.ai/`
   skeleton is missing and the developer expected `scaffold` to have run,
   say so — but creating the three files in `.ai/memory/` is within this
   mode's remit.

## Detect, then create

The templates live in this skill's `assets/`. For each of the three
artifacts:

- **If the target file is absent** → create it from the matching
  template (`assets/constitution-template.md`, etc.).
- **If it exists as a bare template** → fill it in place.
- **If it exists with real content** → you're in the wrong mode; stop.

Do not assume the files are missing — check first. (`scaffold` may or
may not have created empty ones; this mode is the same either way.)

## The evidence sweep

The brain must mirror the repository, so read before you write. Sources,
in **precedence order** — higher sources outrank lower ones on conflict:

1. **The code itself** — directory structure, architectural style,
   layering, the modules that carry the domain logic, the key packages
   the code actually imports (not just what's declared).
2. **Language / environment manifests** — `.csproj` / `.sln`,
   `pyproject.toml`, `Pipfile`, `package.json`, `pom.xml`, `go.mod`,
   `Cargo.toml`, etc. These give the stack, the framework, the
   dependency list, and the entry points.
3. **Written documentation** — `*.md`, API docs, OpenAPI specs — with
   **emphasis on `README.md`** (see "The README" below). The README is
   both a *source* for understanding the project and a *target* this
   mode may have to fill.
4. **Secondary helpers** — CI/CD pipelines, scripts, `justfile` /
   `Makefile`, and open-source meta files (`CONTRIBUTING`,
   `CODE_OF_CONDUCT`). These are where the verification commands and the
   workflow tooling (scanners, scans) usually surface.

Read for discovery, not bulk dump (`AGENTS.md` §3). You are building a
mental model of *what this project is*, then writing the distilled
version into the brain.

> **Security (`AGENTS.md` §4):** never open `.env`, `.pem`, or
> credential files during the sweep. Read `.env.example` and template
> files only. The reference-index points at *where* a secret lives
> (`connection string in .env.example`), never at the secret.

## Filling each artifact

### `constitution.md`

From the sweep, fill: project name and description (§1), architecture
style / language / framework / persistence / key packages (§2), business
objective and position (§3), upstream/downstream/infra (§4), scope (§5),
Quality Gate (§6), planning conventions (§7).

- **Quality Gate (§6) is evidence-bound.** The verification commands
  (test, lint, typecheck, build, coverage, scan) must come from the
  scriptfile (`justfile`/`Makefile`/`package.json` scripts/`pyproject`)
  or the README. If neither documents them, do **not** invent commands —
  mark `[MISSING]` and tell the human to add them (the template says
  exactly this).
- **Business objective, consumers, scope** are often *not* in the code.
  Ask the developer; mark `[MISSING]` / `[NEEDS CLARIFICATION]` for
  anything deferred.

### `adr-log.md`

- Keep the seed `ADR-001` (adoption of the JAIBA brain) — set its date
  to today.
- **Do not back-fill.** Do not mine git history for pre-adoption
  architecture decisions and write them up as ADRs. The log starts at
  adoption and grows forward. Leave it at `ADR-001` plus whatever the
  developer explicitly asks to record now.

### `reference-index.md`

Populate the two tiers (code-scope §1–§3, workflow tooling §4) from the
sweep:

- **Code-scope:** infra the code talks to at runtime, external APIs and
  their *external* spec/docs surface, packages needing non-obvious
  context.
- **Workflow tooling:** scanners / security / review agents found in CI
  or scriptfiles.
- **Consumption points must be real.** Point an API at its OpenAPI /
  vendored spec or docs, never at the internal contract assembly. If you
  can't find where something is consumed anywhere in the project, mark
  `[MISSING]` and surface it — never guess. Vendored copies live under
  `.ai/vendored/`; the entry points at that path.
- **Prune empty categories.** If the project has no external APIs, no
  business docs, or no verification tooling, **delete that whole
  section** rather than leaving its bracket rows. Renumber what remains.
  (This is not `[MISSING]` — that's for a fact that should exist; this
  is a category that doesn't apply at all.)

### The README

Apply the role test (requirements + how-to for a human developer):

- **Completely empty** → write `assets/readme-skeleton.md`, then fill its
  brackets from the same evidence (commands from the scriptfile, stack
  from the manifest). The README may be in the project's language.
- **Non-empty but missing a role** → leave it as is; tell the developer
  which role (requirements and/or how-to) is missing and suggest what to
  add. Do not overwrite their README.
- **Non-empty and complete** → nothing to do; note it's healthy.

## Closing

End every `initialize` run with a short report:

1. **What was created/filled**, file by file.
2. **What's outstanding** — every `[MISSING]` / `[NEEDS CLARIFICATION]` /
   unfilled `[bracket]` that remains, grouped by file. This is mandatory
   (`AGENTS.md` §5.4); the developer must never find an incomplete brain
   by surprise.
3. **Next step** — if gaps remain, the developer resolves them (re-run
   the relevant questions or fill by hand). If the brain is clean, the
   project is ready for `planning` / `specification`.

## Common failure modes

- **Writing before reading.** A constitution built from the prompt
  instead of the manifest invents a stack. Sweep first.
- **Confabulating the unknowable.** Business objective, consumers, gate
  thresholds — ask or mark, never guess.
- **Back-filling ADRs** from git history. The log starts at adoption.
- **Inventing Quality Gate commands** not found in the scriptfile/README.
  Mark `[MISSING]`.
- **Inventing index consumption points.** Ground every entry or mark it.
- **Overwriting a populated README**, or writing the brain in a
  non-English language.
- **Finishing silently** without listing the gaps.
