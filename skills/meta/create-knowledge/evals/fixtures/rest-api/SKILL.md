---
name: rest-api
description: Team conventions for designing and shipping REST APIs — resource modeling, the OpenAPI-first workflow, and contract testing. Use when designing or building HTTP endpoints.
version: 2.0.0
author: acme-platform
tags:
  - rest
  - openapi
  - api-design
---

# rest-api

How this team designs and ships REST endpoints.

## Design first

Before any endpoint is built, its shape is agreed: resource,
HTTP verb, path, request/response schema, status codes, and error
cases. A feature that adds endpoints must list them explicitly up
front.

## OpenAPI-first

- The source of truth is `openapi.yaml` at the service root.
- New or changed endpoints are written into `openapi.yaml` **before**
  implementation.
- Handlers are expected to match the spec; drift is a bug.

## Contract testing

- Every endpoint has a contract test asserting the response matches the
  OpenAPI schema (status code, body shape, error envelope).
- Contract tests run in CI and block merge on drift.

## Conventions

- Plural nouns for collections (`/bookings`), no verbs in paths.
- Cursor pagination for list endpoints.
- Errors use a consistent envelope: `{ "error": { "code", "message" } }`.
