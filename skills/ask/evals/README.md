# Ask surface rehearsal

Actual source-guided executor-as-consumer synthetic outputs and exact tool
traces are indexed in [conduct's regression evidence](../../conduct/evals/README.md)
and `../../conduct/evals/fixtures/surface-rehearsal/index.json`.

For all three surfaces, the `ask` turn answers the full-read selected
checkout-A plan/tasks/PRD, citing exact addresses/revisions. The `ask-failure`
turn reports permission-denied without claiming absence or reading checkout-B.
The recorded span has only catalogue/read operations: no source changes,
executive/binding mutations, fallback mirror or Quality Gate command.

Run the shared check from repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 skills/conduct/evals/test_workflow_rehearsal.py CapturedRehearsal.test_ask_read_only_exact_context_and_failure_without_fallback
```

Existing eval IDs 1–8 are explicitly filesystem-scoped and retain their stated
layouts; case 9 is external. Recordings are synthetic rehearsal evidence, not
live Engram, new model evaluation, or child inheritance certification.
