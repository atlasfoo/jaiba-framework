# Input modifier — enrich the workflow's input

An **input** plugin runs *before* a workflow drafts and feeds it
context it would otherwise have to be told by hand. The workflow's job
is unchanged; it simply receives a richer requirement than the prompt
alone carried.

This is the pattern the `specification` skill already anticipates in
its §Inputs: a tracker ticket is "not handled by `specification` on its
own" — a knowledge skill fetches it and supplies the content.

## Where it hooks

Almost always **`specification:define`** (and, by extension,
`specification:brainstorm` when the requirement starts there). Occasionally
`planning:define`, if the enrichment is tactical rather than a product
requirement. Name the exact mode in the contract.

## The flow when it triggers

1. **Detect the signal in the prompt.** A ticket ID, a URL, a document
   reference — whatever the contract's *Trigger signal* names. If it
   isn't present, the plugin stays quiet; the workflow proceeds on chat
   input as normal.
2. **Fetch / derive the context** using *this skill's own* knowledge
   and tools (e.g. the Linear MCP). The meta-skill does not invent the
   fetch — that capability already lives in the skill being adapted.
3. **Hand it to the workflow as the requirement input**, in the form
   the workflow expects: prose describing the *what* and *why*, not a
   raw API dump. The workflow then runs its normal `define` flow —
   surveying the code, clarifying gaps, writing the PRD — using this as
   the starting requirement instead of (or alongside) the chat text.
4. **Record the provenance.** The workflow's PRD frontmatter has
   `source` / `source-ref` fields; the fetched ticket is `source:
   ticket`, `source-ref: LIN-1234`. The plugin's job is to make that
   true.

## Boundaries

- **Enrich, don't replace the workflow.** You supply the requirement;
  `specification:define` still surveys the code, still clarifies gaps,
  still stops for approval. Don't let the fetched ticket short-circuit
  the workflow's own discipline.
- **Surface what you fetched.** The developer must be able to see that
  the spec was shaped by ticket content, and what that content was — a
  short summary, not a silent injection.
- **Fail soft.** If the fetch fails (no access, bad ID, MCP down), do
  not block. Fall back to the workflow's own instruction: ask the
  developer to paste the ticket text. A plugin that can't fetch must
  not stop the human from working.
- **Respect security.** Tracker content can carry secrets; follow
  `AGENTS.md` §4 — redact tokens, don't echo credentials.

## Walkthrough — a Linear plugin

The team's `linear-tickets` skill already knows how to read a Linear
issue via the Linear MCP. Adapt it as an input modifier:

- **Hook:** `specification:define` (and `:brainstorm`).
- **Modifier type:** input.
- **Trigger signal:** a Linear reference in the prompt — `LIN-1234`,
  `ENG-88`, or a `linear.app/.../issue/...` URL.
- **Behavior:** on that signal, call the Linear MCP to fetch the
  issue's title, description, and acceptance notes; summarize them into
  a requirement statement; hand that to `specification:define` as the
  input it drafts the PRD from; set the PRD's `source: ticket` /
  `source-ref: <id>`. If the MCP call fails, tell the developer and ask
  them to paste the issue body instead.

Result: the developer types *"let's spec LIN-1234"* and the spec
workflow starts already knowing the requirement — no copy-paste, no
extra prompt, and `specification` itself was never modified.
