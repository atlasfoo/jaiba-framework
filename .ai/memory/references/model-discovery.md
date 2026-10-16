---
type: reference
title: "Agent model discovery (CLI and ACP)"
description: Versioned host CLI docs and ACP schemas guide safe model catalog discovery for `jaiba-configure`; catalogs do not prove inference success.
tier: workflow
kind: tooling
role: —
resource: "URL: `https://agentclientprotocol.com/protocol/v1/` / host CLI documentation for the detected host and version (e.g. `https://opencode.ai/docs/cli/`)"
tags: [models, cli, acp, jaiba-configure]
updated: "2026-10-15"
---

# Agent model discovery (CLI and ACP)

## What it is

Host command-line interfaces expose model catalogs with host-specific
semantics. The Agent Client Protocol (ACP) defines a versioned JSON-RPC
interface whose optional session configuration may expose model choices.
Neither source guarantees credentials, entitlement, inference success,
or task suitability.

## How the project uses it

`skills/jaiba-configure/references/model-discovery.md` applies these
surfaces to initial subagent model selection and exact-ID migrations.
The detected host's supported CLI catalog is primary; ACP is a bounded
fallback only when the CLI cannot provide a verifiable host catalog.

## How to consult it

Check the detected executable's version and help, then consult that
host/version's public CLI documentation before invoking its catalog
command. For ACP, use the published [v1 protocol documentation](https://agentclientprotocol.com/protocol/v1/)
and [stable v1 JSON Schema](https://github.com/agentclientprotocol/agent-client-protocol/blob/5ab891a2c38043b91259b21fc7b6c4f32d854a11/schema/v1/schema.json).
The implemented procedure and source-specific examples are recorded in
the `jaiba-configure` reference linked above.

## Gotchas

There is no universal host CLI command or ACP `models/list` method.
Treat CLI output as authoritative only when its documented semantics
establish availability in that host; do not use ACP to evade rejection
by a valid catalog. ACP option IDs may be session-local and are not
automatically valid native subagent `model:` values. Do not inspect
private settings or credentials, authenticate, install transports, or
send prompts to discover or validate model IDs. Follow the timeout,
consent, and no-pin-without-verification rules in the implementation
reference.
