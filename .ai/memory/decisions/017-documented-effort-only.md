---
type: decision
id: ADR-017
title: "Write effort only when the host documents it"
description: "jaiba-configure writes an effort control only when that host's docs and version verify it; researcher installs with no model pin."
status: accepted
date: "2026-11-13"
tags: [setup, models, effort]
updated: "2026-11-13"
---

# ADR-017: Write effort only when the host documents it

## Context

[ADR-007](007-global-repo-local-setup-split.md) keeps model choice on the machine and forbids hardcoded model IDs in the shipped battery. A universal `effort:` field would invent a control some hosts do not have. This decision extends ADR-007. It does not replace it.

## Decision

`jaiba-configure` writes an effort control beside the chosen model only when that host's documentation and version verify the exact field and syntax. Otherwise it leaves effort unset and says so. It does not invent a Cursor scaffold. `researcher` installs with the battery and no `model:` pin. A file present is not proof the role is callable.

## Alternatives Considered

- Hardcode `effort:` for every host — writes a field the host may ignore or reject.
- Invent a Cursor agent scaffold to hold a guessed syntax — no verified control, so no scaffold.

## Consequences

- *Positive:* Installed agents do not carry an unverified effort field.
- *Negative / Risks:* OpenCode stays unset until its docs verify a control.
- *Follow-ups:* None.
