# `jaiba-init:update-brain:initialize`

Build the long-term brain for the first time. End state: `.ai/memory/`
holds a populated **concept bundle** — `index.md` plus one file per
concept under `identity/`, `decisions/` and `references/` — every
concept populated from real repository evidence, every determinable
fact filled, every undeterminable one either resolved by asking or
marked and surfaced.

This is the onboarding mode. It runs on a brand-new project, on a legacy
codebase being adopted into JAIBA, or as step 4 of this skill's own
**bootstrap** mode, right after it lays the `.ai/` skeleton.

The bundle layout, the closed `type:` vocabulary, the per-type
frontmatter and the link convention are **not restated here** — they are
`references/okf-pattern.md`'s job, and each `assets/concepts/<name>.md`
template is the authority on its own fields. This file is the
*procedure*: what to read, in what order, and what to write from it.

## Preconditions

1. The brain does not meaningfully exist yet: either `.ai/memory/`
   holds no concepts at all, or the concepts present are untouched
   templates (full of `[brackets]`). If they already carry real
   content, this is `update`, not `initialize` — stop and switch.
2. `.ai/memory/` exists (or you can create it). If the wider `.ai/`
   skeleton is missing, the repo was never bootstrapped — say so and
   offer `jaiba-init`'s bootstrap mode, which lays the skeleton and then
   returns here. Creating the bundle inside `.ai/memory/` is still
   within this mode's remit if the developer prefers to press on.

## Detect, then create

**Resolve the layout first**, per the dual-resolution rule in
`jaiba-contract.md` §1 (do not restate it, apply it). What you find
decides whether this mode runs at all:

| `.ai/memory/` holds | This means | Do |
|---|---|---|
| nothing — no `index.md`, no `constitution.md` | no brain at all | **This mode.** Create the bundle skeleton and populate it. |
| `index.md` + concepts that are bare templates | a partial run stopped | **This mode.** Fill the templates in place; create whatever concept is missing. |
| `index.md` + concepts with real content | already instrumented | Wrong mode — stop, route to `update`. |
| flat `constitution.md`, no `index.md`, real content | a populated legacy brain | Not this mode. It is a supported layout: `update` maintains it in place, and converting it to the bundle is `references/migrate-mode.md`. |
| both `index.md` and `constitution.md` | ambiguous | **Stop and surface it** (contract §1). Never silently pick a half. |

When this mode does run, create the bundle skeleton —

```
.ai/memory/
├── index.md
├── identity/
├── decisions/
└── references/
```

— and populate each concept from its template in this skill's
`assets/concepts/`. `log/` already exists from bootstrap (create it if
absent) and **starts empty**: `initialize` writes nothing into it.
`snippets/` is optional and is not created here either; a canonical
in-project example is something the project earns later, not something
onboarding invents.

Two rules on creation:

- **Do not create a concept for something the repository doesn't
  have.** No `identity/units/` in a single-unit repo, no placeholder
  `reference` for a category that doesn't apply. See the `reference`
  section below.
- **Do not assume the files are missing — check first.** Bootstrap lays
  only directories, but a prior partial run may have left bare
  templates; per-concept, absent and bare-template are the same job.

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
> files only. A `reference` concept points at *where* a secret lives
> (`connection string in .env.example`), never at the secret.

### What the sweep yields

The sweep does not produce three documents to be filled in order. It
produces **a set of concepts**, and the set is not known until you have
read. Use this as the mapping from what you found to what you write:

| What the sweep turned up | Becomes |
|---|---|
| Repo layout, layering, domain modules | `architecture` — plus one `sub-unit` per deliverable unit *only if* the repo holds more than one |
| Manifest stack, framework, persistence, the packages the code leans on | `architecture` |
| A package needing context beyond standard usage (fork, pinned patch, non-default config) | its own `reference`, `kind: package` |
| Datastores, brokers, cloud services the running code talks to | one `reference` each, `kind: infrastructure`, `role: infrastructure` |
| A third-party API the code calls, or a consumer that calls this project | one `reference` each, `kind: external-api`, `role: upstream` / `downstream` |
| A contract between two units of the same solution | one `reference` each, `kind: internal-contract` |
| Name, description, lifecycle status | `project` |
| Why the project exists, who it serves | `purpose` (ask if the code can't say) |
| What the project does and deliberately doesn't | `scope` |
| Scriptfile / CI verification recipes | `quality-gate` |
| CI scanners, security audits, review agents | one `reference` each, `tier: workflow`, `kind: tooling` |
| Product specs, glossaries, data dictionaries | one `reference` each, `tier: workflow`, `kind: business-doc` |
| Team planning norms; where style is configured | `convention` |
| The adoption of JAIBA itself | the seed `decision`, `ADR-001` — and nothing else |

Every concept in that right-hand column is one file. Nothing on the
list is inventoried inside another concept.

## Filling each concept

Copy each template from `assets/concepts/` and fill its `[brackets]`
from the sweep. The eight single-instance identity templates are
copy-and-fill documents; `decision` and `reference` are N-instance
templates whose fenced example is what you copy per instance (SKILL.md's
"Artifacts at a Glance" explains the split — don't restructure either).

The **`[MISSING]` / `[NEEDS CLARIFICATION]` discipline is unchanged**
and now applies at concept granularity: prefer to ask; if the developer
defers, mark rather than confabulate; and list every remaining marker
**per concept** in the closing report. A gap in one concept is a gap in
that concept's file — never paper it over from a sibling.

### Identity concepts — `identity/*.md`

From the sweep, fill:

| Concept | Holds |
|---|---|
| `identity/project.md` | project name, description, lifecycle status |
| `identity/architecture.md` | architecture style, language, framework, persistence, key packages |
| `identity/purpose.md` | business objective, position in the bigger picture |
| `identity/scope.md` | in scope, out of scope, cross-cutting packages |
| `identity/units/<slug>.md` | one per deliverable unit — **multi-unit repos only** |
| `identity/quality-gate.md` | phase gate and plan gate |
| `identity/conventions.md` | planning conventions, and where style is defined |

- **The Quality Gate is evidence-bound.** The verification commands
  (test, lint, typecheck, build, coverage, scan) must come from the
  scriptfile (`justfile`/`Makefile`/`package.json` scripts/`pyproject`)
  or the README. If neither documents them, do **not** invent commands —
  mark `[MISSING]` and tell the human to add them (the template says
  exactly this).
- **Business objective, consumers, scope** are often *not* in the code.
  Ask the developer; mark `[MISSING]` / `[NEEDS CLARIFICATION]` for
  anything deferred.
- **Single-unit repository:** `scope.md` reads "Single unit." and
  `identity/units/` **does not exist at all**. Do not create the
  directory to hold a placeholder.

**Upstream, downstream and infrastructure facts are not written into
identity concepts.** There is no inventory section anymore: each
external surface is its own `reference` concept carrying its `role:`,
and `purpose.md` / `scope.md` **link** to the ones that matter to them
from their `## Relations` section — `purpose.md` links the surfaces that
give the project its reason to exist, `scope.md` the ones that draw a
boundary. One line, one link; the `reference` concept owns the facts.
Re-creating that inventory inline is the single duplication the bundle
exists to remove (`okf-pattern.md`, "One deliberate improvement").

### `decision` concepts — `decisions/<NNN>-<slug>.md`

- Write the seed `ADR-001` (adoption of the JAIBA brain) at
  `decisions/001-jaiba-brain-adoption.md`, copying the worked example in
  `assets/concepts/decision.md` — set its `date` to today.
- **Do not back-fill.** Do not mine git history for pre-adoption
  architecture decisions and write them up as decision concepts. The
  series starts at adoption and grows forward. Leave it at `ADR-001`
  plus whatever the developer explicitly asks to record now.

### `reference` concepts — `references/<slug>.md`

One file per external surface, `tier:` carrying the precedence the flat
index expressed as sections:

- **`tier: code-scope`** (primary): infra the code talks to at runtime,
  external APIs and their *external* spec/docs surface, internal
  cross-component contracts (event schemas, internal APIs between
  sub-units of the same solution), packages needing non-obvious context.
- **`tier: workflow`** (secondary): scanners / security / review agents
  found in CI or scriptfiles, and non-code sources of truth.

Then `kind:` says what the surface *is* and `role:` says how this
project relates to it (`role` only at `tier: code-scope`) — the
vocabulary and worked examples are in `assets/concepts/reference.md`.

- **Consumption points must be real.** Point an API at its OpenAPI /
  vendored spec or docs, never at the internal contract assembly. If you
  can't find where something is consumed anywhere in the project, mark
  `[MISSING]` and surface it — never guess. Vendored copies live under
  `.ai/vendored/`; the `resource:` points at that path.
- **Don't create a concept for a category that doesn't apply.** There is
  no monolithic index to prune anymore: if the project has no external
  APIs, no business docs, or no verification tooling, those files simply
  **do not exist** — no empty `references/` placeholder, no bracket-only
  concept. (This is not `[MISSING]` — that's for a fact that should
  exist but couldn't be found; this is a category that doesn't apply at
  all.)

### `index.md` — written last

Regenerate `index.md` **after** every other concept exists, from
`assets/concepts/index.md`: one link and one line — each concept's
`description:` frontmatter, verbatim — grouped by `type:`, linking
directly to the concept. Delete the groups for types this repository has
none of. `log/` is indexed as a group, never per entry. The index is a
map, not a summary: resolving one fact must cost reading `index.md` plus
*one* concept file.

## The README

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

1. **What was created/filled**, concept by concept — but **grouped by
   `type:`**, not as a wall of paths. Name the single-instance identity
   concepts individually (they are seven files at most); for `decision`
   and `reference`, give the count and the titles (`3 references: Auth0,
   Postgres, Snyk`), not a path list. A reader must be able to see the
   shape of the brain in one glance.
2. **What's outstanding** — every `[MISSING]` / `[NEEDS CLARIFICATION]` /
   unfilled `[bracket]` that remains, **named against the concept that
   carries it**. Here the file is named explicitly: this is the list the
   developer acts on. This is mandatory (`AGENTS.md` §5.4); the developer
   must never find an incomplete brain by surprise.
3. **Next step** — if gaps remain, the developer resolves them (re-run
   the relevant questions or fill by hand). If the brain is clean, the
   project is ready for the `conduct` chain.

## Common failure modes

- **Writing before reading.** An `architecture` concept built from the
  prompt instead of the manifest invents a stack. Sweep first.
- **Confabulating the unknowable.** Business objective, consumers, gate
  thresholds — ask or mark, never guess.
- **Back-filling decisions** from git history. The series starts at
  adoption.
- **Inventing Quality Gate commands** not found in the scriptfile/README.
  Mark `[MISSING]`.
- **Inventing a `reference`'s consumption point.** Ground every
  `resource:` or mark it.
- **Re-inventorying partners inside `purpose.md` / `scope.md`** instead
  of linking the `reference` concepts that carry the `role:`. That
  duplication is exactly what the bundle removed.
- **Writing placeholder concepts** for categories the project doesn't
  have — an empty `references/` stub, an `identity/units/` holding one
  "single unit" file.
- **Leaving `index.md` stale** — written before the last concept, or
  fattened with summaries until it costs as much as the bundle it maps.
- **Overwriting a populated README**, or writing the brain in a
  non-English language.
- **Finishing silently** without listing the gaps.
