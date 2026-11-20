# Native plan client

An entry into `spec`, not a replacement for the chain. The approval
gate does not move (`references/spec-mode.md` § The approval gate).

## Setting

`native-plan-client` is `auto` (default), `on`, or `off`.
`jaiba-configure` owns where the machine setting is stored. Do not
invent a path, filename, or schema. Do not store it in `.ai/memory/`.
If the setting is absent or unreadable, treat it as `auto`.

`auto` and `on` run this client only when the host exposes plan mode
or a plan subagent. If the host exposes neither, or the setting is
`off`, follow the current spec. Do not block.

## When the client runs

**Before planning — uninstrumented check.** Run Step 0 first. If the
repository is authoritatively uninstrumented (no `v2` binding, no
`AGENTS.md` pin, no `.ai/memory/`, and no external registry match), **stop
before starting native planning and suggest orchestrating the project
first with `jaiba-init`**. Offer the developer two choices:
1. Run `jaiba-init` now to orchestrate the project before planning.
2. Continue explicitly with native planning alone without JAIBA — in which
   case JAIBA stays dormant, writes no memory or executive artifacts
   (`.ai/work/`), and does not re-block the session.

Ask the native plan mode or plan subagent for the plan text and wait.
Do not write executive artifacts inside a mode that freezes writes.
Convert after the text returns, in a session that can write.

Do not replan the how. Memory contrast and knowledge skills mark
conflicts; they do not replan. Write the PRD (only at `spec` depth, as
today) and the plan as drafts. Ask for approval before `tasks`.

Empty text: stop and ask. Do not invent a plan.

## A native plan already finished

If the developer already finished a native plan and invokes conduct,
offer to preserve it as JAIBA artifacts. If they reject the offer, do
not write.
