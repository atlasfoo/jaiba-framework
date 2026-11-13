# Ticket link

When conduct creates or amends a plan. Not a tracker client. The
approval gate does not move (`references/spec-mode.md` § The approval
gate). Do not replan the how.

## Evidence

Look only at the repo. No network. Any one of these is enough:

- a ticket id in a commit scope, body, or footer (local git history)
- a quality hook or script of the husky, lefthook, or `commit-msg` kind
  present in the repo
- an explicit ticket-linking rule in README, CONTRIBUTING, or project
  rules

Evidence is a reason to ask. Do not copy ids from it. If none of these
is present, do not ask and do not write `tickets:`.

## Record

If evidence exists and the plan has no `tickets:` line, ask which
tickets to link. If the line is already there, do not ask again.

Store the answer as one frontmatter line. No body section. Do not edit
the plan template:

`tickets: <ids the developer named>`

Ids as named, in that order, separated by a comma and a space
(`tickets: ABC-12, XYZ-3`). No quotes. No list brackets. If they name
none, omit the key. Do not write an empty value.

Do not call tracker APIs. Do not validate ids. Do not fetch or paste
the ticket body. Fetching the body stays with input knowledge plugins
(`source: ticket` on the PRD). This procedure only records the ids the
developer names.

## One id is wrong

Replace only that id in the `tickets:` line. Do not re-ask the list.
Do not validate the replacement. Leave the other ids unchanged.
