---
type: log-entry
date: 2026-11-13
slug: executive-native-plan-client
kind: work-closure
depth: spec
adr: ADR-015, ADR-016, ADR-017, ADR-018 (proposed)
---

# Conduct consumes a native plan and routes executive lanes

## What happened

Conduct can take the host's native plan as the how, convert it outside a write-freezing mode, and keep the approval gate. Execute alerts before a sequential fallback. Fast and ask enter by context. Effort is written only when the host documents it. Tickets are recorded only from local evidence.

## Criteria delivered

- `EXEC-001` — native plan as spec input — delivered
- `EXEC-002` — offer to preserve a finished native plan — delivered
- `EXEC-003` — machine setting for the native-plan client — delivered
- `EXEC-004` — dispatch callable roles and alert before fallback — delivered
- `EXEC-005` — effort only when documented — delivered
- `EXEC-006` — fast delegates code and stays inline if needed — delivered
- `EXEC-007` — unnamed amendment enters fast — delivered
- `EXEC-008` — ask dispatches researcher without a model pin — delivered
- `EXEC-009` — received `/btw` enters ask — delivered
- `EXEC-010` — link tickets from local evidence, no API — delivered

## Phases executed

| # | Theme | Notable result |
|---|---|---|
| 1 | Routing | Side questions and unnamed amendments named in the contract. |
| 2 | Conduct client | Native-plan procedure and fallback alert. |
| 3 | Configure | `native-plan-client` setting, effort rule, `researcher` scaffold. |
| 4 | Fast and ask | Code delegation and research dispatch. |
| 5 | Evals | Cases for the client, setting, delegation, and `/btw`. |
| 6 | Tickets | Local-evidence question and one-line `tickets:` field. |

## Decisions and deviations

A missing `tickets:` line is asked again on a later amend; an empty key is not stored. An API-check request is not consent to write `tickets:`. Evals were syntax-checked, not model-replayed. The historical rehearsal hash lock fails because `SKILL.md` changed; that lock is not the dual-layout gate, which passed. No plan-gate check was waived. The installed global contract was not updated.

## ADR proposals & brain updates

**Proposed — ADR-015: Native plan is an input, not a second chain.** Extends [ADR-003](../decisions/003-unified-orchestrator-sdd-chain.md). Does not replace it.

- **Context:** Host plan mode freezes writes. Using it as the plan would skip JAIBA drafts and the approval gate.
- **Decision:** When `native-plan-client` is `auto` or `on` and the host exposes plan mode or a plan subagent, conduct asks for the text and converts it in a writable session. It does not replan the how. Empty text stops and asks. A finished native plan is preserved only if the developer accepts. `off`, or no plan mode, follows the current spec.
- **Alternatives:** Run spec inside native plan mode (cannot write). Always replan after the host text (throws away the how).
- **Consequences:** The approval gate does not move. The setting lives with machine setup, not in `.ai/memory/`.

**Proposed — ADR-016: Route by the message, not by its name.** Extends [ADR-004](../decisions/004-three-lane-routing-policy.md). Does not replace it.

- **Context:** An amendment that did not say `fast`, and a received `/btw`, could follow execute and mutate the active plan.
- **Decision:** With an active plan, a change outside current tasks enters `fast` even if it does not say `fast`. `continue` / `next` / `go` stay on execute. A received `/btw` or documented equivalent enters `ask` and does not mutate executive work. A command the agent never receives is a limit, not a hook.
- **Alternatives:** Add `/fast` and `/ask` (rejected). Treat every side command as intercepted (false).
- **Consequences:** A change that triages to `design` or deeper is still refused and offered for fold-in or replan.

**Proposed — ADR-017: Write effort only when the host documents it.** Extends [ADR-007](../decisions/007-global-repo-local-setup-split.md). Does not replace it.

- **Context:** A universal `effort:` field would invent a control some hosts do not have.
- **Decision:** Configure writes an effort control only when that host's docs and version verify it. Otherwise it leaves effort unset and says so. `researcher` installs with the battery and no `model:` pin. A file present is not callability.
- **Alternatives:** Hardcode `effort:` for every host. Invent a Cursor scaffold.
- **Consequences:** OpenCode stays unset until its docs verify a control.

**Proposed — ADR-018: Link tickets from local evidence only.**

- **Context:** Asking for tickets in every plan, or calling a tracker, would invent a workflow the repo may not have.
- **Decision:** If commits, a quality hook, or a project rule show ticket linking, conduct asks which ids to store as one `tickets:` line. No evidence means no question. No API call and no id check. A correction replaces only that id. Fetching the ticket body stays with input knowledge plugins.
- **Alternatives:** Always ask. Validate ids against a tracker.
- **Consequences:** A later amend with no `tickets:` line asks again.

Enact these with `jaiba-init:update-brain`. No other memory changes are proposed.

## Pointers

- Squash commit `2b7719a` on `feature/execute-improvements`.
- [Quality gate](../identity/quality-gate.md)
- [Prior delegation closure](2026-10-05-enforce-conduct-delegation.md)

## Suggested final commit

```
feat(conduct): consume native plans and route executive lanes

Use the host plan as the how, without replanning it or skipping approval.
Alert before a sequential fallback. Let fast and ask enter by context.
Write effort only when the host documents it. Link tickets only from local evidence.
```

Landed as `2b7719a` before this closure.

## Gate at close

Pass. Plan gate green: phase commands, toolchain probe (0 missing), injection fixture (4 rejected, no malicious render), legacy citations reviewed as deliberate, dual-layout archive fixtures passed, no `.ai/work/` in git status. Security scan omitted, not missing. No waiver.

<!-- jaiba-close-v1
contract jaiba-memory-surface 1.0.0
binding filesystem
project prj-c4e91b7a2d06
context ctx-8f2a71e04c3b
scope d2b21f774988598d197607a79a0a4cbabdd30ca1
close 2026-11-10-executive-native-plan-client
body 04f80d60afc4e5cff3fc68b4ccfd7e222e083225
plan.md fd8135d0be5cf5ff40c036d3411986c320d5101e
tasks.md 8a34daf35bf6df9554a44be0eb38828dc097a447
walkthrough.md c8dc507919984f1e6e32dd73ee5882a3acc6d982
PRD.md 3919249f112cb91c3f2b59edbccf651183643c7f
.gitignore absent
-->
