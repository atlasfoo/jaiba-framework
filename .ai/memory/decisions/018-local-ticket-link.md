---
type: decision
id: ADR-018
title: "Link tickets from local evidence only"
description: "Conduct asks which tickets to link only when the repo already shows local ticket evidence, and never calls a tracker API."
status: accepted
date: "2026-11-13"
tags: [workflow, conduct, tickets]
updated: "2026-11-13"
---

# ADR-018: Link tickets from local evidence only

## Context

Some repos already link commits or plans to tickets. Asking in every plan, or calling a tracker to validate an id, would invent a workflow the repo may not have and would pull ticket bodies that belong to input knowledge plugins.

## Decision

If a commit scope, body, or footer, a quality hook such as husky, lefthook, or `commit-msg`, or an explicit rule in README, CONTRIBUTING, or project rules shows ticket linking, conduct asks which ids to store as one `tickets:` line on the plan. No evidence means no question and no key. Conduct does not call a tracker API and does not validate ids. A correction replaces only that id. Fetching the ticket body stays with input knowledge plugins.

## Alternatives Considered

- Always ask — nags repos that do not use tickets.
- Validate ids against a tracker — requires an API and invents validity.

## Consequences

- *Positive:* Ticket links are developer-named records, not fetched issues.
- *Negative / Risks:* A later amend of a plan with no `tickets:` line asks again, because an empty key is not stored.
- *Follow-ups:* None.
