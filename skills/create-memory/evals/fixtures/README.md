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
the separately approved Phase 15 work and is not launched here.

`contrasting-profiles.json` is an additional synthetic, declarative input for
the factory-decision evals. Its profile claims, schemas, permissions, outcomes,
identities, byte counts, costs, and interruption states are invented fixture
conditions—not observed or documented claims about Engram, a filesystem, or
any product. The fixture is unexecuted and makes no backend calls. Grading is
intended to inspect the generated representation, cost/recovery plan, profile
claim states, and reject/adopt decisions against those inputs; matching
instruction keywords in Markdown is not evidence of a conforming decision.

The separately approved comparative evaluation should use the same
requirements, tools, and profiles with and without the skill, save complete
outputs and grading, and include viewer-based human review. No such generation,
run, grading, or viewer review occurred here. Valid JSON is not conformity.

## Contract 1.1.0 extensions

Additional fixtures support 1.1.0 capabilities and conformance gates:
- `cross-host-portability.json`: Claim envelope portability (backend, tools, protocol, contract); host provenance vs scope; agent-agnostic tool exposure mapping (`MSV-001`).
- `binding-v2-cases.json`: Binding v2 path formula (`~/.jaiba/memory/bindings/<sha256>.yaml`), Step 0 O(1) discovery, agreeing legacy consolidation, and conflict blocking (`MSV-002`).
- `multihost-installation-cases.json`: Discovery of JAIBA-configured hosts, multi-selection, timestamped backups (`.bak-<timestamp>`) on collision, and readback verification (`MSV-003`).
- `archetype-cases.json`: Classification of `document-tree` (in-place edits, no context-head) vs `record-store` (journaled base + deltas + context-head), and `unknown` blocking (`MSV-004`).
- `script-ast-validation.json` & `validate_scripts_ast.py`: Static AST validation of package scripts asserting Python 3 standard library imports only, zero pip dependencies, declared transport modes, and canonical subcommands (`MSV-006`).
- `efficiency-gate-cases.json`: Efficiency Gate evaluating 5 SDD lifecycle scenarios with $O(\delta)$ deltas in `spec` draft adjustments, execute waves, plan approval, and marking monolithic full-object overwrites on `record-store` as NONCONFORMING (`MSV-007`).
- `upgrade-repair-cases.json`: Upgrade/repair workflow covering 1.0.x audit, contrasted profile preservation, dropping host locks, canonical tool normalization, incremental conformance, and multi-host reinstallation (`MSV-009`).

