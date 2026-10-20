# create-memory conformance fixtures

These are authored, synthetic test inputs for the prompts in `../evals.json`.
They are data, not executable tool definitions. No MCP server, adapter,
backend, installer, or conformance runner is supplied here. Do not import these
schemas into a real tool registry or treat their expected outcomes as observed
backend evidence.

For a future authorized behavioral run, copy fixtures into a fresh isolated
workspace under `/tmp/opencode/jaiba-memory-surfaces/<run>/`, use synthetic
in-memory state only, and discard that run directory afterward. This location
is guidance, not authorization to create it during structural validation.
Never point a test at a real namespace or credential-bearing endpoint.

The JSON files declare exact scenario IDs, inputs, expected results and full
payloads where preservation matters. `layout-bundle.json` and
`layout-legacy.json` are compact document inventories rather than actual
directory trees; their `path` fields model the source paths. The separate
`layout-boundaries.json` tests dual/no entry markers. No migration, cleanup,
global configuration edit, or real installation scenario is included.

`transfer-recovery-cases.json` models an approved, inert synthetic scope
inventory for future migration exercises. It is not a fully instrumented brain,
an active source/target, or evidence that a target adapter conforms. Its
validator checks structure and computes fingerprints only; operational faults
and retries belong to separately authorized isolated mock-storage exercises.

These evals have not been executed. JSON/schema and fixture consistency checks
are structural checks only; they do not simulate tool calls, adapter behavior,
or certify conformance. Comparative with/without-skill viewing is reserved for
the separately approved Phase 6 T-027 and is not launched here.
