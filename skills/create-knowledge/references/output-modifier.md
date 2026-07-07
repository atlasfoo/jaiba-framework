# Output modifier — augment the workflow's output

An **output** plugin contributes to what a workflow *produces*: extra
tasks in `tasks.md`, extra artifacts (an `openapi.yaml`, a doc file),
and rules that shape the Technical approach. It encodes "here is what
our team always does for this kind of work" so the agent doesn't have
to be reminded each time.

This is the pattern `conduct` already anticipates: knowledge
skills are listed among the Technical-approach sources in
`spec-mode.md`, and `plan-template.md` carries a literal slot —
`- <Knowledge skill name> (if applicable)`.

## Where it hooks

Usually **`conduct:spec`** at its design step (where the
Technical approach and artifacts are decided) and
**`conduct:tasks`** (where the task graph is laid out). Sometimes
the *define* step too, when the rule shapes the PRD itself (e.g. "a
REST feature's spec must declare its endpoints"). A skill can hook
several — say so in the contract.

## The flow when it triggers

1. **Detect the domain match.** The contract's *Trigger signal* is a
   property of the work being planned — "the plan adds REST endpoints",
   "an ASP.NET controller is involved". When `conduct:spec` is
   shaping such a design, the plugin co-triggers.
2. **Contribute concrete tasks and artifacts.** Translate the skill's
   rules into imperative tasks the workflow can drop straight into
   `tasks.md`, and name any artifacts to create. "Write
   `docs/endpoints/<name>.md` for each new endpoint" — not "remember to
   document things".
3. **Shape the Technical approach.** Where the rules constrain *how*
   (layering, test framework, error-contract conventions), feed them
   into the plan's Technical approach section.
4. **Cite yourself.** Add this skill to the plan's "Sources consulted"
   (that's what the `<Knowledge skill name>` slot is for). This is how a
   reviewer sees the plugin shaped the plan.
5. **Slot into the right phase.** A doc task follows the endpoint it
   documents; a test rule rides with the implementation pair. Respect
   the workflow's TDD posture and phase structure rather than dumping a
   flat list at the end.

## Boundaries

- **Contribute, don't hijack.** The workflow still owns the plan and
  the approval gate. You add tasks; you don't approve, reorder
  everything, or override the developer's scope.
- **Don't duplicate.** If the plan already has the task, don't add it
  again. Co-triggering means you're working alongside the workflow, not
  blindly stamping a checklist.
- **Honor the templates.** Tasks go in `tasks.md` in its format;
  artifacts are real files the plan creates; rules inform the Technical
  approach. Don't invent a parallel structure.
- **Be honest about reach.** This plugin fires by co-triggering on its
  description. There is no runtime poll guaranteeing it. A weak
  description means a plugin that silently doesn't fire — which is why
  the adapted description must explicitly bind to `conduct:spec`
  (and/or `:tasks`) and name the trigger signal.

## Walkthrough — an ASP.NET best-practices plugin

The org's `aspnet-practices` skill holds clean-architecture layering,
xUnit conventions, and a rule that every endpoint gets a Markdown doc.
Adapt it as an output modifier:

- **Hook:** `conduct:spec` design step + `conduct:tasks`
  (and the define step for the endpoint-declaration rule).
- **Modifier type:** output.
- **Trigger signal:** a plan or spec for ASP.NET Core work — new
  controllers, endpoints, or application services.
- **Behavior:** when such a plan is being defined, contribute: (a) a
  task to write `docs/endpoints/<name>.md` for each new endpoint; (b)
  the layering rule (Domain / Application / Infrastructure / API) into
  the Technical approach; (c) the xUnit test conventions, paired with
  each implementation task under TDD; and cite `aspnet-practices` in
  "Sources consulted".

## Walkthrough — a REST / OpenAPI plugin (both types)

A `rest-api` skill can be **both**: at PRD time it requires the spec
to declare its endpoints (input-shaping on `conduct:spec`'s
define step), and at design/tasks time it requires an `openapi.yaml`
artifact and a contract test per endpoint (output on the design step
and `conduct:tasks`). Its contract names both hooks and lists the
obligations under each.

Result: the developer plans "add the bookings endpoints" and the plan
comes out already carrying the `openapi.yaml` task and the per-endpoint
docs — because the team's standard rode in with the plugin, and
`conduct` was never edited to know about REST.
