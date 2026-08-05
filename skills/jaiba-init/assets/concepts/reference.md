# Reference Concept

> **Meta-instruction for the agent:**
>
> One file is **exactly one external surface** the project touches — a
> datastore, a third-party API, a contract with a sibling component, a
> package needing non-obvious context, a workflow tool, a business
> document. References live at `.ai/memory/references/<slug>.md` with a
> kebab-case slug naming the surface: `references/postgres.md`, not
> `references/PostgreSQL_DB.md`.
>
> **Before implementing an external integration, querying an external
> system, or using a non-trivial library, read the reference concept
> for it first.** It tells you *how* to consult that surface — MCP
> server, CLI tool, dashboard URL, OpenAPI spec, vendored docs. If no
> reference concept exists for a surface you need, **stop and ask**. Do
> not invent integration details from memory; propose a stub concept so
> the gap is visible to the team.
>
> **Never invent the consumption point.** The `resource:` of every
> reference must be grounded in something that actually exists — a
> config file, an env var, a vendored spec, a CI step. For an external
> API, point at its **external** surface (the OpenAPI/vendored spec or
> docs URL), **not** the internal assembly where the data contracts are
> written. If you cannot find the consumption point anywhere in the
> project, **stop and ask the human**; record `[MISSING]` rather than
> guessing. This holds for workflow tooling exactly as it holds for
> code-scope surfaces: if a CI step names a tool but you cannot locate
> how it is configured or invoked, that is `[MISSING]`, not a guess.
>
> **Do not duplicate the package manifest.** The full dependency list
> lives in `pyproject.toml` / `package.json` / `pom.xml`. Write a
> `kind: package` reference only for packages that need extra context:
> custom configuration, non-obvious usage, an internal fork.
>
> **A category that doesn't apply simply has no files.** In the flat
> index an unused section had to be pruned so it wouldn't read as
> unfinished work; in the graph the equivalent is: don't create the
> concept. Never write a placeholder reference for a surface the
> project doesn't have. Distinguish this from `[MISSING]`, which is a
> fact that *should* exist but couldn't be found — that one gets
> written down and surfaced to the human.
>
> **References are external; snippets are internal.** A canonical
> example of a recurring in-project pattern ("how we fetch data", "how
> we write a migration") is a `snippet` concept, not a reference.
>
> Locally stored ("vendored") copies of external material live under
> `.ai/vendored/`. A reference *points at* a vendored path; the copy
> itself is not a concept.

---

## Template

```markdown
---
type: reference
title: "[Surface name]"
description: [One line: what this surface is and what the project uses it for]
tier: [code-scope | workflow]
kind: [infrastructure | external-api | internal-contract | package | tooling | business-doc]
role: [upstream | downstream | infrastructure | —]
resource: [MCP `<server>` / CLI `<tool>` / URL: `<address>` / vendored at `<path>` / spec at `<path>`]
tags: [tag, tag]
updated: "[YYYY-MM-DD]"
---

# [Surface name]

## What it is

[One short paragraph: what this surface does, and where the boundary
with this project runs.]

## How the project uses it

[Which parts of the project talk to it, and for what. For a package,
this is the "why it needs an entry" — the non-obvious configuration or
the fork's divergence.]

## How to consult it

[Expand the `resource:` above into something actionable: the exact
command, the env var holding the connection string, the config file,
the CI step. Ground every claim; `[MISSING]` anything you cannot find.]

## Gotchas

[Constraints, rate limits, version pins, "do not upgrade without
coordinating", auth quirks. Omit the section if there are none.]
```

## Frontmatter keys

| Key | Status | Meaning |
|---|---|---|
| `type` | **mandatory** | always `reference` |
| `title` | recommended | human-readable name of the surface |
| `description` | recommended | one line; this is what `index.md` shows |
| `tier` | mandatory in practice | the precedence class — see below |
| `kind` | mandatory in practice | what the surface **is** — see below |
| `role` | at `tier: code-scope` | how **this project** relates to it — see below |
| `resource` | mandatory in practice | where it is consulted, in the vocabulary below |
| `tags` | recommended | list, for grouping and search |
| `updated` | recommended | `YYYY-MM-DD` of the last substantive change |

Only `type:` is a validity condition. A missing optional key is at most
a quality note, never a rejection.

### `tier:` — the precedence

Two tiers, and the first outranks the second. When two references
disagree, or when attention has to be rationed, `code-scope` wins.

| `tier:` | Means |
|---|---|
| `code-scope` | the **running code** depends on it. Infrastructure, external APIs, internal cross-component contracts, packages. Primary. |
| `workflow` | the **development workflow** depends on it. Quality scanners, security audits, remote review agents, product documentation. Useful, but the code runs without them. |

### `kind:` — what the surface is

| `kind:` | One file is | Typical `tier:` |
|---|---|---|
| `infrastructure` | a datastore, message broker, cloud service, or other infra the project talks to at runtime | `code-scope` |
| `external-api` | a third-party HTTP API and its contract | `code-scope` |
| `internal-contract` | a contract between components of the *same* solution — a sibling package in the monorepo, another project in the `.sln`, a sister service of the same product. Both sides are under the team's control, but a change on one side still breaks the other, so the contract needs an explicit consultable surface. From each sub-unit's point of view these are external | `code-scope` |
| `package` | a library or SDK that needs context beyond standard usage — non-default configuration, an internal fork, a pinned patch | `code-scope` |
| `tooling` | a tool the development workflow relies on: static analysis, security scans, coverage gates, remote review agents. `jaiba-doctor` tests these for reachability; the concept records *where they are configured and how to invoke them* | `workflow` |
| `business-doc` | a non-code source of truth: product spec, glossary, data dictionary | `workflow` |

The `tier` column is the usual pairing, not a rule the concept
enforces — if the running code genuinely depends on a surface, it is
`code-scope` whatever its `kind`.

### `role:` — how this project relates to the surface

`role` is what `purpose.md` and `scope.md` navigate by. They **link**
reference concepts by role instead of repeating an inventory of
partners inline; never re-create that duplicated list anywhere.

| `role:` | Means |
|---|---|
| `upstream` | this project **consumes** it — an identity provider, a payments API, a shared database it reads |
| `downstream` | it **consumes this project** — a web frontend, a mobile app, a reporting service calling this project's contract |
| `infrastructure` | this project **operates on** it at runtime — cache, object storage, message broker |
| `—` | role does not apply |

`role` and `kind` overlap on the word `infrastructure`, and that is
fine: `kind` is what the surface *is*, `role` is the relation. A Redis
instance is `kind: infrastructure`, `role: infrastructure`. An upstream
auth service is `kind: external-api`, `role: upstream`.

**`role` is only meaningful at `tier: code-scope`.** Workflow tooling
and business documents have no upstream/downstream relation to the
running system — write `role: —` to make the non-applicability
explicit, or omit the key entirely; both read the same under the
tolerance rule.

## `resource:` — the consultation vocabulary

`resource:` names *where* the surface is consulted, using these
conventions:

- **MCP `<server-name>`** — an MCP server is configured for this
  resource; query it directly via the agent's MCP tools.
- **CLI `<tool>`** — a command-line tool is available; use it for
  inspection and queries.
- **URL: `<address>`** — a web dashboard or doc site is available;
  fetch it if web tools are available.
- **Vendored at `<path>`** — the relevant docs or source have been
  packed locally under `.ai/vendored/` (e.g., a Repomix bundle, a
  physical copy of an API's OpenAPI/docs) and can be read from disk.
- **Spec at `<path>`** — there is a machine-readable contract
  (OpenAPI, GraphQL SDL, JSON Schema) at this path.

If a reference is reachable through several channels, list the most
direct one first (MCP > CLI > URL > vendored).

A `business-doc` whose source of truth is a file already in the
repository is reached by reading it: the repo-relative path *is* the
resource (`docs/business/data-dictionary.md`). The five forms above
describe how to reach an external system; a document in the tree needs
no ceremony beyond its path.

## Worked examples

An upstream API — the shape `purpose.md` and `scope.md` link to when
they need the project's upstream partners:

```markdown
---
type: reference
title: "Auth0"
description: Identity provider; issues the JWTs the API validates on every request.
tier: code-scope
kind: external-api
role: upstream
resource: URL: `auth0.com/docs` / vendored at `.ai/vendored/auth0.txt`
tags: [auth, identity, external]
updated: "[YYYY-MM-DD]"
---
```

Infrastructure the project operates:

```markdown
---
type: reference
title: "Redis"
description: Cache and session store behind the API's read paths.
tier: code-scope
kind: infrastructure
role: infrastructure
resource: CLI `redis-cli` / connection string in `REDIS_URL`
tags: [cache, sessions, infra]
updated: "[YYYY-MM-DD]"
---
```

Workflow tooling, where `role` does not apply:

```markdown
---
type: reference
title: "SonarQube"
description: Static analysis and quality gate; runs in CI on every pull request.
tier: workflow
kind: tooling
role: —
resource: CLI `sonar-scanner` / URL: `sonar.company.com`
tags: [quality, ci]
updated: "[YYYY-MM-DD]"
---
```
