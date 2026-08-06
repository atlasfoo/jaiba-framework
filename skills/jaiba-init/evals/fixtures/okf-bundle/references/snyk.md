---
type: reference
title: "Snyk"
description: Dependency vulnerability scan, run as a step in `.github/workflows/ci.yml`.
tier: workflow
kind: tooling
role: —
resource: "CLI `snyk test`"
tags: [security, ci, tooling]
updated: 2026-06-02
---

# Snyk

## What it is

A dependency vulnerability scanner run in CI on every build; not
consulted by the running code.

## How the project uses it

The development workflow relies on it to catch known vulnerabilities
in `Orders.csproj`'s dependencies before merge.

## How to consult it

Invoked as a `snyk test` step in `.github/workflows/ci.yml`.
