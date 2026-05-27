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
> (`pyproject.toml`, `package.json`, `pom.xml`, etc.). This index does
> **not** duplicate it — it only lists packages that need extra
> context (custom configuration, non-obvious usage, internal forks).

---

## 1. Infrastructure Dependencies

Datastores, message brokers, cloud services, and any other infra the
project talks to at runtime.

| Service        | Role               | How to consult                                | Location / Endpoint                    |
|---|---|---|---|
| [PostgreSQL]   | [Primary DB]       | [CLI `psql` / MCP `postgres-mcp` / pgAdmin URL] | [connection string in `.env.example`]  |
| [Redis]        | [Cache + sessions] | [CLI `redis-cli` / MCP `redis-mcp`]            | [`REDIS_URL` env var]                  |
| [AWS S3]       | [Media storage]    | [URL: AWS console / CLI `aws`]                 | [bucket name in `settings/storage.py`] |

## 2. External APIs

Third-party HTTP APIs and their contracts.

| Service     | Role                  | How to consult                                | Spec / Docs                              |
|---|---|---|---|
| [Auth0]     | [Identity provider]   | [URL: auth0.com/docs]                          | [vendored at `.ai/refs/auth0.txt`]       |
| [Stripe]    | [Payments]            | [URL: stripe.com/docs / MCP `stripe-mcp`]      | [`docs/openapi/stripe-v1.yaml`]          |
| [Core API]  | [Internal upstream]   | [URL: internal repo link]                      | [`docs/openapi/core-api-v1.yaml`]        |

## 3. Packages and SDKs (with non-obvious context)

Only packages that require knowledge beyond standard usage. Routine
framework dependencies stay in the project manifest.

| Package              | Why it needs an entry                                                            | How to consult                                |
|---|---|---|
| [django-guardian]    | [Object-level permissions; non-default config in `settings/permissions.py`]      | [URL: django-guardian.readthedocs.io]         |
| [@org/internal-sdk]  | [Internal fork with patched retry logic; do not upgrade without coordinating]    | [Repo URL / vendored at `.ai/refs/internal-sdk.txt`] |

## 4. Business Documentation

Product specs, glossaries, and other non-code sources of truth.

| Document        | Type                   | Location                              |
|---|---|---|
| PRD MVP 1.0     | [Product requirements] | [`docs/business/mvp-requirements.md`] |
| Data Dictionary | [Domain glossary]      | [`docs/business/data-dictionary.md`]  |

## 5. Implementation Notes (Snippets)

Canonical examples for recurring patterns in this project.

- **How to fetch data:** `.ai/snippets/data-fetching.md`
- **How to test components:** `.ai/snippets/testing-components.md`
- **How to write a migration:** `.ai/snippets/migrations.md`

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
  packed locally (e.g., via Repomix) and can be read from disk.
- **Spec at `<path>`** — there is a machine-readable contract
  (OpenAPI, GraphQL SDL, JSON Schema) at this path.

If a reference is reachable through several channels, list the most
direct one first (MCP > CLI > URL > vendored).
