---
name: linear-tickets
description: Read and summarize Linear issues using the Linear MCP. Use when the developer references a Linear ticket and wants its details pulled into the conversation.
version: 0.2.0
author: acme-eng
tags:
  - linear
  - tracker
---

# linear-tickets

How this team works with Linear from inside the agent.

## Fetching an issue

Linear issues are referenced as `<TEAM>-<NUMBER>` (e.g. `ENG-204`,
`LIN-1234`) or as `linear.app/acme/issue/ENG-204/...` URLs.

To read one, use the Linear MCP:

1. Call `linear.get_issue` with the issue identifier.
2. From the response, take `title`, `description`, `state`, and any
   acceptance-criteria checklist in the description body.
3. If the issue has a parent or sub-issues, note them but don't recurse
   unless asked.

## Summarizing

Produce a short brief: the goal in one sentence, the acceptance
criteria as bullets, and any explicit out-of-scope notes. Keep it
faithful to the ticket — don't add requirements the ticket doesn't
state.

## Notes

- The Linear MCP must be configured; if `linear.get_issue` is
  unavailable, say so.
- Never paste API tokens; the MCP handles auth.
