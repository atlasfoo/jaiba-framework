---
type: quality-gate
title: "Quality Gate"
description: "Phase gate runs `dotnet test`; plan gate adds the `snyk test` security scan — both sourced from `.github/workflows/ci.yml`."
tags: [identity, quality-gate, verification]
updated: "2026-06-02"
---

# Quality Gate

This project has no scriptfile — `.github/workflows/ci.yml` is the
only place commands live, so both tiers read their commands from
there.

## Phase Gate (runs after each phase — must be fast)

A phase is **not done** until all of these pass. If any fails, fix it
atomically before moving on.

- **Tests (affected):** `dotnet test` (per `.github/workflows/ci.yml`;
  the pipeline does not scope by affected module, so this runs the
  full suite).

> Linting, type checking and formatting have no dedicated step in CI
> and no scriptfile documents them — omitted rather than invented.

## Plan Gate (runs once at `conduct:validate` — may be slow)

A plan is **not done** until all of these pass. Failures block the
summary and require corrective action before closing.

- **Full test suite:** `dotnet test`
- **Security scan:** `snyk test` (per `.github/workflows/ci.yml`)

> Coverage and a dedicated build step are not configured in CI beyond
> the Dockerfile — omitted rather than invented.
