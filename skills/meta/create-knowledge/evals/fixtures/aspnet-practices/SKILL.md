---
name: aspnet-practices
description: Acme's ASP.NET Core engineering standards — clean architecture layering, xUnit testing conventions, and API documentation rules. Use when writing or reviewing ASP.NET Core code at Acme.
version: 1.4.0
author: acme-platform
tags:
  - aspnet
  - dotnet
  - standards
---

# aspnet-practices

Acme's house rules for ASP.NET Core services. These are mandatory for
any new controller, endpoint, or application service.

## Architecture

Four layers, dependencies point inward only:

- **Domain** — entities, value objects, domain events. No framework
  references.
- **Application** — use-cases (one handler per use-case), DTOs,
  interfaces for infrastructure.
- **Infrastructure** — EF Core, external clients, implementations of
  Application interfaces.
- **API** — controllers, filters, DI wiring. Thin; delegates to
  Application handlers.

## Testing

- xUnit, one test class per handler.
- Arrange/Act/Assert, no logic in tests.
- Every use-case handler ships with happy-path and failure tests.
- Integration tests use `WebApplicationFactory` against an in-memory
  or testcontainer DB.

## Documentation

- **Every endpoint gets a Markdown doc** under `docs/endpoints/`, named
  after the route (e.g. `docs/endpoints/post-bookings.md`), covering
  request/response shape, status codes, and auth.
- Public DTOs carry XML doc comments.

## Error contract

All endpoints return RFC 7807 `ProblemDetails` on error. No bare 500s
with stack traces.
