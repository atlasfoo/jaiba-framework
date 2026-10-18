# Synthetic eval fixtures

These files are protocol-analysis inputs, not a backend dump, executable adapter,
or evidence of conformance. Use the `evals.json` prompts with the skill eval
runner; keep any scratch output under `/tmp/opencode/jaiba-memory-surfaces/<run>`.
Do not point an eval at a live Engram backend or use these fixtures to authorize
mutations. T009 owns authorized live conformance checks.

Large-object and digest cases intentionally specify computed properties rather
than fabricated expected hashes. A behavioral harness must compute canonical
bytes, lengths and SHA-256 with a verified implementation and compare observed
bytes; static JSON validation only checks fixture structure and cannot exercise
the storage protocol.
