## JAIBA Integration

> Added by the `create-knowledge` meta-skill. This section makes the
> skill above a JAIBA **knowledge plugin**: it co-triggers with a
> workflow and folds the knowledge above into that workflow's run. It
> changes nothing the workflow writes on disk beyond the contributions
> declared here, and it requires no edit to any framework artifact.

- **Hook:** <the workflow mode(s) this plugs into — `specification:define`,
  `planning:define`, or both. Name the exact mode, not just the skill.>
- **Modifier type:** <`input` | `output` | `both`>
- **Trigger signal:** <the concrete cue that means "this plugin applies
  now". Be specific and matchable: a Linear issue reference like
  `LIN-1234` or a `linear.app/issue/...` URL in the prompt; a plan or
  spec whose subject touches REST/HTTP endpoints; an ASP.NET controller
  or service being added. If there is no signal, the plugin can't know
  when to fire — go back and find one.>
- **Behavior:**
  <Spell out exactly what to do when triggered.

  For an INPUT modifier: how to fetch or derive the external context
  using this skill's own knowledge/tools, what to hand to the workflow
  and in what form (it becomes the requirement input the workflow
  drafts from), and what to do if the fetch fails (fall back to asking
  the developer — never block the workflow). Surface what was fetched
  so the human can see it shaped the spec.

  For an OUTPUT modifier: the exact tasks, artifacts, and rules to
  contribute to the workflow's output — phrased as concrete,
  imperative tasks/artifacts the workflow can drop into `tasks.md` or
  the plan (e.g. "add a task: write `docs/endpoints/<name>.md` for each
  new endpoint"; "require an `openapi.yaml` artifact"). Say which phase
  they belong to when it matters. Always cite this skill under the
  plan's "Sources consulted". Contribute; do not duplicate tasks the
  plan already has, and do not seize the workflow's approval gate.>
