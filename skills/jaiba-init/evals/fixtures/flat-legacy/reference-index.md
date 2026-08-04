# Reference Index

> **Meta-instruction for the agent:**
>
> Before implementing an external integration, querying an external
> system, or using a non-trivial library, **search this index first**.
> It maps every external surface the project touches and tells you
> *how* to consult each one (MCP server, CLI tool, dashboard URL,
> OpenAPI spec, vendored docs).
>
> If a needed reference is missing, **stop and ask**. Do not invent
> integration details from memory. Propose adding a stub entry so the
> gap is visible to the team.
>
> The full package dependency list lives in the project's manifest
> (`Orders.csproj`). This index does **not** duplicate it — it only
> lists packages that need extra context (custom configuration,
> non-obvious usage, internal forks).
>
> **Two tiers, in precedence order.** Entries fall into two classes and
> the first outranks the second:
> 1. **Code-scope references** (§1–§2) — infrastructure, external APIs,
>    internal cross-component contracts, and packages the *running
>    code* depends on. These come first.
> 2. **Workflow & verification tooling** (§3) — auxiliaries the
>    *development workflow* depends on (quality scanners, security
>    audits, remote review agents). Secondary: useful, but the code
>    runs without them.
>
> **Never invent a consumption point.** The "How to consult" /
> "Location" of every entry must be grounded in something that actually
> exists in the repo (a config file, an env var, a vendored spec, a CI
> step). For an external API, point at its **external** surface — the
> OpenAPI/vendored spec or docs URL — **not** the internal assembly
> where the data contracts are written. If you cannot find the
> consumption point anywhere in the project, **stop and ask the human**;
> record it as `[MISSING]` rather than guessing.
>
> **Prune what doesn't apply.** A *whole section* the project simply
> doesn't have (no external APIs, no business docs, no verification
> tooling) should be **removed**, not left as a heading full of bracket
> rows. An empty section is noise that looks like unfinished work.
> Distinguish this from `[MISSING]`: `[MISSING]` is a fact that *should*
> exist but couldn't be found (ask the human); a pruned section is a
> category that genuinely *doesn't apply* to this project. Keep the
> numbering contiguous after removing a section.
>
> Locally stored ("vendored") copies of external references live under
> `.ai/vendored/` — see the framework README.
>
> This project has no internal cross-component contracts (single
> `.csproj`, not a monorepo), no packages needing context beyond
> standard usage, no business documentation in the repository, and no
> implementation-pattern snippets recorded yet — those sections are
> pruned entirely rather than left as empty headings.

---

## 1. Infrastructure Dependencies

Datastores, message brokers, cloud services, and any other infra the
project talks to at runtime.

| Service    | Role        | How to consult    | Location / Endpoint                     |
|---|---|---|---|
| PostgreSQL | Primary DB  | CLI `psql`        | connection string in `ConnectionStrings__Orders` (env var) |

## 2. External APIs

Third-party HTTP APIs and their contracts.

| Service      | Role                | How to consult                            | Spec / Docs                             |
|---|---|---|---|
| Payments API | Upstream payment processor, called via a typed HttpClient | vendored OpenAPI | vendored at `docs/openapi/payments-v2.yaml` |

## 3. Workflow & Verification Tooling

Secondary references: tools the *development workflow* relies on, not
the running code — static analysis, security scans, coverage gates,
remote review agents. The `doctor` skill tests these for reachability;
this index records *where they are configured and how to invoke them*.

| Tool | Role                             | How to consult / invoke | Where it's configured           |
|---|---|---|---|
| Snyk | Dependency vulnerability scan    | CLI `snyk test`         | `.github/workflows/ci.yml` step |

---

## How to Consult — Vocabulary

The "How to consult" column uses these conventions:

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
