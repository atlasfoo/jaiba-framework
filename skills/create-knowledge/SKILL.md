---
name: create-knowledge
description: Meta-skill that turns an existing skill into a JAIBA *knowledge plugin* — a skill that hooks into the `specification` and `planning` workflows without modifying them, enriching their input or augmenting their output. Use this whenever the developer has a skill full of domain knowledge (org architecture guides, testing/TDD rules, REST/OpenAPI conventions, a Linear/Jira tracker integration, ASP.NET best practices, documentation standards…) and wants it to take an *active* role during spec or plan creation instead of sitting inert until named. Trigger on phrases like "adapt this skill for JAIBA", "make this skill a knowledge plugin", "connect our Linear skill to specification", "make our ASP.NET rules feed into planning", "turn this into a plugin for the workflows", "hook this skill into spec/plan", "make this skill add tasks to plans". This skill ONLY rewrites the target skill's `SKILL.md` (its `description`, an injected `## JAIBA Integration` contract, and tags); it never touches the target's actual knowledge, references, assets, or folder structure, and it never edits a framework workflow. Do NOT use it to author a brand-new skill from scratch (that's `skill-creator`) or to edit a JAIBA workflow/meta skill itself.
version: 1.0.0
author: atlasfoo<iscomejia15@outlook.com>
requires:
  - git
tags:
  - jaiba
  - meta
  - jaiba-meta
  - knowledge-plugins
---

# create-knowledge

A JAIBA meta-skill. It takes a skill that already *holds knowledge* —
best practices, domain rules, an external-tracker integration — and
makes that knowledge **participate** in the `specification` and
`planning` workflows, automatically, at the right moment, without the
developer having to paste the rules into every prompt.

The output is the **same skill**, minimally rewritten so it behaves as
a *plugin*: it co-triggers with a workflow and folds itself in. You
change three things and nothing else: the `description` (so it triggers
at the right workflow moment), an injected `## JAIBA Integration`
section (the contract that says *how* it folds in), and the `tags`. The
knowledge itself — the body's rules, the `references/`, the `assets/`,
the folder layout — is left exactly as you found it.

## Why this works without touching the workflows

There is no runtime step where a workflow "calls its plugins". JAIBA
relies on something simpler: the agent running `planning:define` is the
*same* agent that has the knowledge skill sitting in its available
skills. Skill selection is driven by the `description`. So if a
knowledge skill's description is engineered to fire **on that workflow,
in that domain context**, it co-triggers and the agent weaves it in.

The vanilla workflows were built expecting this. The sockets already
exist — you are conforming a skill to them, not inventing them:

- **Input socket** — `specification/SKILL.md` §Inputs already states a
  tracker ticket is *"not handled by this skill on its own… JAIBA
  models tracker access as a knowledge skill… that declares it should
  fire when `specification:define` runs with a ticket reference."*
- **Output socket** — `planning/references/define-mode.md` lists
  *"knowledge skills"* among Sources consulted and inputs to the
  Technical approach, and `plan-template.md` carries a literal slot:
  `- <Knowledge skill name> (if applicable)`.

Because the connection is description + the existing sockets,
**installing an adapted skill modifies no framework artifact** — no
`AGENTS.md`, no constitution, no reference index. Dropping the skill in
is enough.

**The known tradeoff (be honest about it):** an output-modifier only
fires if its description is *pushy enough* to co-trigger during
`planning:define`. There is no poll that guarantees it. The mitigation
is description quality and an explicit hook line — not a workflow edit.
Say this to the developer when you adapt an output-modifier.

## The two modifier types

Every knowledge plugin is one or both of these. Decide which before
writing — it determines the hook and the behavior.

| Type | What it does | Hooks | Canonical example |
|---|---|---|---|
| **input** | Enriches the workflow's *input* before it drafts — fetches/derives context and hands it over as the requirement. | usually `specification:define` | A Linear skill: sees `LIN-1234` in the prompt, fetches the issue, passes its description as the spec's requirement. |
| **output** | Augments the workflow's *output* — contributes mandatory tasks, artifacts, and rules to the spec or plan. | usually `planning:define`, sometimes `specification:define` | A REST skill: when a plan adds endpoints, requires an `openapi.yaml` artifact and a doc task per endpoint. |
| **both** | Some skills do both. | both modes | A tracker skill that also imposes a "link the plan to the ticket" task. |

Read the matching reference before you write the contract:

- `references/input-modifier.md` — the input-enrichment pattern, its
  boundaries, and the Linear walkthrough.
- `references/output-modifier.md` — the output-augmentation pattern,
  its boundaries, and the ASP.NET / OpenAPI walkthrough.

## The transform

Work on the skill the developer points you at. Touch **only** its
`SKILL.md`.

1. **Locate and validate the target.** It must have a `SKILL.md` with
   YAML frontmatter. Refuse three things, with a one-line reason:
   - a JAIBA **workflow** skill (`planning`, `specification`, `ask`,
     `fast`, `update-brain`) — those are the sockets, not plugins;
   - a JAIBA **meta** skill (including this one);
   - anything without a `SKILL.md`.

2. **Read the target's `SKILL.md`** in full, and skim its `references/`
   only enough to understand the domain. Do not modify references or
   assets — you are reading them to classify, not to edit.

3. **Classify and locate the hook.** Decide: input, output, or both?
   Which workflow mode(s) does it plug into? What is the concrete
   **trigger signal** — the cue in a prompt or plan that means "this
   plugin applies now"? If any of these is ambiguous, ask the developer
   (one closed question each — see `AGENTS.md` §3 and the workflows'
   "Asking the Human"). Do not guess a tracker's ID format or a
   domain's boundary.

4. **Engineer the `description`.** Keep what the skill *knows* (so it
   still reads as itself), and add the JAIBA triggering clause that ties
   it to the workflow mode + trigger signal, pushy enough to co-trigger.
   The description is the whole triggering mechanism — if it doesn't
   name the workflow and the signal, the plugin is inert. See
   "Description shape" below.

5. **Inject or update the `## JAIBA Integration` section.** Use
   `assets/jaiba-integration-template.md` verbatim, filled in. This is
   the contract the agent reads at workflow time. **Idempotent:** if the
   section already exists (the skill was adapted before), update it in
   place — never append a second copy.

6. **Set the tags.** Add `jaiba` and `jaiba-knowledge`, plus
   `jaiba-input` and/or `jaiba-output` to match the type. Preserve the
   skill's existing tags.

7. **Leave everything else alone.** Knowledge body, `references/`,
   `assets/`, `scripts/`, structure — untouched. If the skill carried
   no `description` or frontmatter at all, add the minimum frontmatter
   needed and say so.

8. **Report.** Show the `description` before/after and the injected
   `## JAIBA Integration` block. State plainly: which workflow it now
   hooks, which signal fires it, and that **no framework artifact was
   modified** — installing it is just dropping the folder in.

## Description shape

A good adapted description has two halves: what the skill knows, and
when JAIBA should consult it. Keep the first; add the second.

**Example — input modifier (a Linear skill):**

Input (before): `Knows how to read Linear issues via the Linear MCP and summarize their requirements.`

Output (after): `Knows how to read Linear issues via the Linear MCP and summarize their requirements. JAIBA knowledge plugin (input): whenever the 'specification' workflow runs (especially 'specification:define') and the prompt contains a Linear issue reference (e.g. LIN-1234, or a linear.app/issue URL), trigger and fetch that issue, then hand its description to the spec as the requirement input — so the developer never has to paste the ticket. See this skill's 'JAIBA Integration' section.`

**Example — output modifier (an ASP.NET skill):**

Input (before): `Organization's ASP.NET Core best practices: clean architecture layering, xUnit testing conventions, and per-endpoint Markdown docs.`

Output (after): `Organization's ASP.NET Core best practices: clean architecture layering, xUnit testing conventions, and per-endpoint Markdown docs. JAIBA knowledge plugin (output): whenever 'planning:define' (or 'specification:define') is producing a plan or spec for ASP.NET Core work — new controllers, endpoints, or services — trigger and contribute its mandated tasks and artifacts (e.g. a Markdown doc task per endpoint, the layering and xUnit rules) into the workflow's output, and cite this skill under the plan's 'Sources consulted'. See this skill's 'JAIBA Integration' section.`

Notice both name the **workflow mode** and the **trigger signal**
explicitly, and stay pushy ("whenever… trigger and…"). That is what
makes co-triggering reliable.

## Boundaries

- **Adapt, don't rewrite.** The developer's skill is theirs. You are
  adding a triggering clause and a contract, not re-authoring their
  knowledge or "improving" their rules.
- **One skill, one job.** Don't merge two knowledge skills, and don't
  split one. Adapt the skill as it is.
- **Never edit a workflow.** If you feel the only way to make a plugin
  work is to change `planning` or `specification`, stop and say so —
  that is a framework change, out of scope here, and it would break the
  "installs with zero framework edits" guarantee.
- **No invented integrations.** If the skill claims an MCP or API that
  isn't there, surface the gap (`AGENTS.md` §5.3); don't paper over it
  in the contract.

## Common failure modes

- **A description that names the domain but not the workflow.** Then it
  triggers on chit-chat about the domain, not at spec/plan time. Always
  bind it to `specification:define` / `planning:define`.
- **Editing the knowledge.** Out of scope. If the rules are wrong,
  that's a conversation, not a silent rewrite.
- **Double-injecting the contract** on a re-run. Update in place.
- **Over-promising an output-modifier.** It co-triggers; it isn't
  guaranteed by a runtime poll. Say so, and make the description carry
  its weight.
- **Adapting a workflow skill.** Workflows are the sockets. Refuse.
