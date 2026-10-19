# Fast surface rehearsal

Actual source-guided executor-as-consumer synthetic outputs and exact tool
traces are indexed in [conduct's regression evidence](../../conduct/evals/README.md)
and `../../conduct/evals/fixtures/surface-rehearsal/index.json`.

The `fast` span on all three surfaces edits a private tax helper and its actual
test, records red then green command output, and makes no executive update
before confirmation. Refusal leaves all work objects unchanged. The confirmed
handoff goes to conduct; its stale revision attempt conflicts without mutation.
Renewed synthetic approval preserves the human annotation and unknown metadata,
appends T-002 without renumbering, and verifies complete readbacks. No commits.

Run the shared check from repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 skills/conduct/evals/test_workflow_rehearsal.py CapturedRehearsal.test_fast_actual_code_test_confirmation_handoff_conflict
```

Existing eval IDs 1–6 are explicitly filesystem-scoped and retain their stated
layouts; case 7 is external. The external handoff is simulated transport
behavior, not live Engram/adapter conformance or a real plan amendment.
