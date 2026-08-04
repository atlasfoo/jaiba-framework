---
type: reference
title: PostgreSQL
description: Primary datastore for orders, accessed via Entity Framework Core.
tier: code-scope
kind: infrastructure
role: infrastructure
resource: "CLI `psql` / connection string in `ConnectionStrings__Orders` (env var)"
tags: [database, infra, persistence]
updated: 2026-06-02
---

# PostgreSQL

## What it is

The primary relational datastore backing the Orders domain — orders,
their line items, and status history.

## How the project uses it

The Infrastructure layer persists and queries orders through Entity
Framework Core (`EFCore.Npgsql`); no other layer talks to the database
directly.

## How to consult it

Connect with `psql` using the connection string held in the
`ConnectionStrings__Orders` environment variable.
