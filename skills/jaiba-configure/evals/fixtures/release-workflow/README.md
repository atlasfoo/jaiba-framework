# Release workflow harness

Run from the repository root with `python3 skills/jaiba-configure/evals/fixtures/release-workflow/harness.py`.
The harness extracts the `Bump version` and `Publish GitHub Release` shell
blocks from `.github/workflows/bump.yml` and runs them with temporary mocked
`git`, `gh`, and `cz` commands. It makes no network calls and uses no secrets.
