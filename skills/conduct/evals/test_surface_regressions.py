"""Surface regression fixtures. All filesystem archives use isolated temp roots.

ExternalStore is a deterministic fake: its tests exercise adapter-shaped
catalogue/read/revision/append/clear calls, not live Engram and not LLM behavior.
"""
from __future__ import annotations

import os
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
ARCHIVE = ROOT / "skills/conduct/scripts/archive.sh"
SCRATCH_PARENT = Path("/tmp/opencode/jaiba-memory-surfaces/phase4-t021")
SCRATCH_PARENT.mkdir(parents=True, exist_ok=True)
SCRATCH = Path(tempfile.mkdtemp(prefix="run-", dir=SCRATCH_PARENT))
TRACE = []


class ExternalStore:
    """Fake owned object store recording exact scoped operations and revisions."""
    def __init__(self):
        self.objects = {}
        self.calls = []
        self.revision = 0

    def put(self, context, key, value):
        self.revision += 1
        self.objects[(context, key)] = (value, str(self.revision))

    def catalogue(self, context):
        self.calls.append(("catalogue", context))
        return sorted(k for c, k in self.objects if c == context)

    def full_read(self, context, key):
        self.calls.append(("full_read", context, key))
        return self.objects[(context, key)]

    def update(self, context, key, value, expected_revision):
        self.calls.append(("update", context, key, expected_revision))
        old, revision = self.objects[(context, key)]
        if revision != expected_revision:
            raise RuntimeError("revision conflict")
        self.put(context, key, value)

    def append(self, context, key, payload, approved):
        self.calls.append(("append", context, key, approved))
        if not approved:
            return False
        if (context, key) in self.objects:
            old, rev = self.objects[(context, key)]
            if old != payload:
                raise RuntimeError("append conflict")
            return rev
        self.put(context, key, payload)
        return self.objects[(context, key)][1]

    def clear(self, context, key, expected_revision, approved):
        self.calls.append(("clear", context, key, expected_revision, approved))
        if not approved:
            return False
        if self.objects[(context, key)][1] != expected_revision:
            raise RuntimeError("revision conflict")
        del self.objects[(context, key)]
        return True


class SurfaceRegressionTests(unittest.TestCase):
    def tearDown(self):
        (SCRATCH / "scenario-trace.json").write_text(
            json.dumps({
                "evidence_kind": "fake backend orchestration + actual filesystem helper operations",
                "live_engram_tested": False,
                "llm_instruction_compliance_tested": False,
                "scenarios": TRACE,
            }, ensure_ascii=False, indent=2) + "\n"
        )

    def test_archive_bundle_and_legacy_in_temp_roots(self):
        for marker in ("index.md", "constitution.md"):
            with self.subTest(marker=marker), tempfile.TemporaryDirectory(prefix="jaiba-archive-", dir=SCRATCH) as td:
                root = Path(td)
                (root / ".ai/work").mkdir(parents=True)
                (root / ".ai/memory").mkdir()
                (root / ".ai/memory" / marker).write_text("fixture\n")
                work = root / ".ai/work"
                (work / "plan.md").write_text("created: 2026-10-01\n")
                (work / "tasks.md").write_text("- [x] T-001\n")
                (work / "walkthrough.md").write_text("evidence\n")
                (work / "demo-summary.md").write_text("English summary\n")
                env = dict(os.environ, JAIBA_ARCHIVE_FILESYSTEM="1", JAIBA_ARCHIVE_SERIALIZED="1")
                for mode in ("prepare", "archive"):
                    result = subprocess.run(
                        ["bash", str(ARCHIVE), mode, "demo", "project-fixture", "context-fixture"],
                        cwd=root, env=env, capture_output=True, text=True,
                    )
                    self.assertEqual(result.returncode, 0, result.stderr)
                    TRACE.append({"scenario": "filesystem-archive", "layout": marker, "operation": mode,
                                  "argv": [mode, "demo", "project-fixture", "context-fixture"],
                                  "result": result.stdout.strip()})
                log = root / ".ai/memory/log/2026-10-01-demo.md"
                self.assertTrue(log.is_file())
                self.assertIn("English summary", log.read_text())
                self.assertFalse((work / "tasks.md").exists())

    def test_external_context_reads_update_and_revision_conflict(self):
        store = ExternalStore()
        store.put("ctx-current", "plan", "plan A")
        store.put("ctx-current", "tasks", "tasks A")
        store.put("ctx-other", "plan", "plan B")
        self.assertEqual(store.catalogue("ctx-current"), ["plan", "tasks"])
        self.assertEqual(store.full_read("ctx-current", "plan")[0], "plan A")
        self.assertNotIn(("full_read", "ctx-other", "plan"), store.calls)
        rev = store.full_read("ctx-current", "tasks")[1]
        store.update("ctx-current", "tasks", "tasks A+", rev)
        self.assertEqual(store.full_read("ctx-current", "tasks")[0], "tasks A+")
        with self.assertRaisesRegex(RuntimeError, "revision conflict"):
            store.update("ctx-current", "tasks", "stale", rev)
        TRACE.append({"scenario": "read-only-context+revision-update", "calls": store.calls})

    def test_external_close_refusal_verified_readback_and_resume(self):
        store = ExternalStore()
        store.put("ctx-current", "plan", "approved plan")
        store.put("ctx-current", "tasks", "all checked")
        plan_rev = store.full_read("ctx-current", "plan")[1]
        tasks_rev = store.full_read("ctx-current", "tasks")[1]
        inventory = {"plan": plan_rev, "tasks": tasks_rev}
        self.assertFalse(store.append("ctx-current", "log/close-1", "summary", approved=False))
        self.assertEqual(store.catalogue("ctx-current"), ["plan", "tasks"])
        log_rev = store.append("ctx-current", "log/close-1", "summary", approved=True)
        self.assertEqual(store.full_read("ctx-current", "log/close-1"), ("summary", log_rev))
        # Interruption after append: no cleanup. Resume uses same receipt/close ID.
        self.assertEqual(store.append("ctx-current", "log/close-1", "summary", approved=True), log_rev)
        self.assertEqual(store.full_read("ctx-current", "plan")[1], inventory["plan"])
        for key, rev in inventory.items():
            self.assertTrue(store.clear("ctx-current", key, rev, approved=True))
        self.assertEqual(store.catalogue("ctx-current"), ["log/close-1"])
        self.assertFalse(any(call[1] == "ctx-other" for call in store.calls))
        TRACE.append({"scenario": "close-refusal+append-readback+resume-clear", "inventory": inventory,
                      "log_revision": log_rev, "calls": store.calls})


if __name__ == "__main__":
    unittest.main(verbosity=2)
