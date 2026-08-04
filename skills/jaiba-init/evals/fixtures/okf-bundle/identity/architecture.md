---
type: architecture
title: "Architecture"
description: "Layered ASP.NET Core 8 Web API (Api/Application/Domain/Infrastructure) persisting to PostgreSQL via EF Core."
tags: [identity, architecture, stack]
updated: "2026-06-02"
---

# Architecture

- **Architecture style:** Layered (Api / Application / Domain / Infrastructure)
- **Primary language:** C# / .NET 8
- **Primary framework:** ASP.NET Core 8 Web API
- **Persistence:** PostgreSQL via Entity Framework Core (EFCore.Npgsql)
- **Key packages:** EFCore.Npgsql, MediatR, Serilog

> The **complete** dependency map lives in `Orders.csproj`, and each
> integration lives in its own `reference` concept. Not duplicated
> here — this concept holds the shape of the system, not its
> inventory.
