"""Unit tests for skills/jaiba-configure/scripts/jaiba_ssot.py.

Pure Python 3 stdlib unittest suite executed in isolated temporary directories.
"""

from __future__ import annotations

import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.dont_write_bytecode = True

SKILL_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = SKILL_DIR / "scripts"
CAVEATS_DIR = SKILL_DIR / "references" / "caveats"
BASE_AGENTS_DIR = SKILL_DIR / "assets" / "agents"

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import jaiba_ssot  # noqa: E402


def run_cli(argv: list[str]) -> tuple[int, dict]:
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = jaiba_ssot.main(argv)
    return code, json.loads(buf.getvalue())


class DetectHostsTests(unittest.TestCase):
    def test_distinguishes_antigravity_from_gemini_cli(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "home"
            ssot = home / ".jaiba"
            # Only ~/.gemini/config exists -> antigravity present, gemini-cli absent
            (home / ".gemini" / "config" / "agents").mkdir(parents=True)

            code, out = run_cli([
                "--home", str(home),
                "--ssot-root", str(ssot),
                "--caveats-dir", str(CAVEATS_DIR),
                "detect-hosts",
            ])
            self.assertEqual(code, 0)
            self.assertTrue(out["ok"])
            by_id = {h["host_id"]: h for h in out["hosts"]}
            self.assertTrue(by_id["antigravity"]["exists"])
            self.assertFalse(by_id["gemini-cli"]["exists"])

            # Adding ~/.gemini/GEMINI.md makes gemini-cli exist too
            (home / ".gemini" / "GEMINI.md").write_text("# Gemini\n", encoding="utf-8")
            code2, out2 = run_cli([
                "--home", str(home),
                "--ssot-root", str(ssot),
                "--caveats-dir", str(CAVEATS_DIR),
                "detect-hosts",
            ])
            self.assertEqual(code2, 0)
            by_id2 = {h["host_id"]: h for h in out2["hosts"]}
            self.assertTrue(by_id2["antigravity"]["exists"])
            self.assertTrue(by_id2["gemini-cli"]["exists"])

    def test_reports_legacy_and_third_party_markers(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "home"
            ssot = home / ".jaiba"
            claude_agents = home / ".claude" / "agents"
            claude_agents.mkdir(parents=True)
            (home / ".claude" / "jaiba-contract.md").write_text("# contract\n", encoding="utf-8")
            (home / ".claude" / "jaiba-configure.yaml").write_text('native-plan-client: "on"\n', encoding="utf-8")
            (claude_agents / "executor-medium.md").write_text("---\nname: executor-medium\n---\n", encoding="utf-8")
            (claude_agents / "custom-user-agent.md").write_text("---\nname: custom-user-agent\n---\n", encoding="utf-8")

            code, out = run_cli([
                "--home", str(home),
                "--ssot-root", str(ssot),
                "--caveats-dir", str(CAVEATS_DIR),
                "detect-hosts",
            ])
            self.assertEqual(code, 0)
            claude = next(h for h in out["hosts"] if h["host_id"] == "claude-code")
            self.assertTrue(claude["exists"])
            markers = claude["legacy_markers"]
            self.assertTrue(markers["jaiba_contract"])
            self.assertTrue(markers["jaiba_configure_yaml"])
            self.assertEqual(markers["jaiba_agents"], ["executor-medium"])
            self.assertEqual(markers["third_party_agents"], ["custom-user-agent.md"])


class HarvestLegacyTests(unittest.TestCase):
    def test_harvests_models_efforts_cursor_inline_plan_client_and_preserves_third_party(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "home"
            ssot = home / ".jaiba"

            # Claude Code: top-level model + effort, plus third-party agent
            claude_agents = home / ".claude" / "agents"
            claude_agents.mkdir(parents=True)
            (home / ".claude" / "jaiba-configure.yaml").write_text('native-plan-client: "on"\n', encoding="utf-8")
            (claude_agents / "executor-high.md").write_text(
                "---\nname: executor-high\nmodel: claude-opus-4-1\neffort: high\n---\nBody\n",
                encoding="utf-8",
            )
            third_party_claude = claude_agents / "my-helper.md"
            third_party_content = "---\nname: my-helper\ndescription: user custom\n---\nKeep untouched.\n"
            third_party_claude.write_text(third_party_content, encoding="utf-8")

            # Cursor: inline model[effort=...]
            cursor_agents = home / ".cursor" / "agents"
            cursor_agents.mkdir(parents=True)
            (cursor_agents / "executor-medium.md").write_text(
                "---\nname: executor-medium\nmodel: gpt-5[effort=medium]\n---\nBody\n",
                encoding="utf-8",
            )

            # Antigravity: pro + inherit
            ag_agents = home / ".gemini" / "config" / "agents"
            ag_agents.mkdir(parents=True)
            (ag_agents / "executor-low.md").write_text(
                "---\nname: executor-low\nmodel: flash\n---\nBody\n",
                encoding="utf-8",
            )

            code, out = run_cli([
                "--home", str(home),
                "--ssot-root", str(ssot),
                "--caveats-dir", str(CAVEATS_DIR),
                "harvest-legacy", "--write",
            ])
            self.assertEqual(code, 0)
            self.assertTrue(out["ok"])
            self.assertEqual(out["findings"], [])
            self.assertEqual(out["preserved_third_party"], {"claude-code": ["my-helper.md"]})
            self.assertEqual(third_party_claude.read_text(encoding="utf-8"), third_party_content)

            cfg = out["proposed_config"]
            self.assertEqual(cfg["native-plan-client"], "on")
            self.assertTrue(cfg["hosts"]["claude-code"]["enabled"])
            self.assertTrue(cfg["hosts"]["cursor"]["enabled"])
            self.assertTrue(cfg["hosts"]["antigravity"]["enabled"])

            m_hosts = out["proposed_mappings"]["hosts"]
            self.assertEqual(m_hosts["claude-code"]["roles"]["executor-high"]["model"], "claude-opus-4-1")
            self.assertEqual(m_hosts["claude-code"]["roles"]["executor-high"]["effort"], "high")
            self.assertEqual(m_hosts["cursor"]["roles"]["executor-medium"]["model"], "gpt-5")
            self.assertEqual(m_hosts["cursor"]["roles"]["executor-medium"]["effort"], "medium")
            self.assertEqual(m_hosts["antigravity"]["roles"]["executor-low"]["model"], "flash")

            # Verify written files exist and parse cleanly
            cfg_text = (ssot / "config.yaml").read_text(encoding="utf-8")
            self.assertIn('native-plan-client: "on"', cfg_text)
            parsed_map = jaiba_ssot.parse_yaml_subset((ssot / "mappings.yaml").read_text(encoding="utf-8"))
            self.assertEqual(parsed_map["hosts"]["cursor"]["roles"]["executor-medium"]["effort"], "medium")

    def test_flags_malformed_frontmatter_and_adr010_yaml_hazards_without_crashing(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "home"
            ssot = home / ".jaiba"
            claude_agents = home / ".claude" / "agents"
            claude_agents.mkdir(parents=True)

            # Unclosed frontmatter
            (claude_agents / "executor-high.md").write_text("---\nname: executor-high\nmodel: claude-opus\n", encoding="utf-8")
            # YAML tag / injection hazard in frontmatter
            (claude_agents / "executor-medium.md").write_text(
                "---\nname: executor-medium\nmodel: !!python/object/apply:os.system [\"echo pwn\"]\n---\n",
                encoding="utf-8",
            )
            # Tabs in indentation hazard
            (claude_agents / "executor-low.md").write_text(
                "---\nname: executor-low\n\tmodel: haiku\n---\n",
                encoding="utf-8",
            )
            # Researcher pin forbidden by ADR-017
            (claude_agents / "researcher.md").write_text(
                "---\nname: researcher\nmodel: claude-sonnet-4\n---\n",
                encoding="utf-8",
            )
            # Control character / whitespace hazard in scalar
            (claude_agents / "verify.md").write_text(
                '---\nname: verify\nmodel: "bad model with space"\n---\n',
                encoding="utf-8",
            )
            # Malformed legacy jaiba-configure.yaml
            (home / ".claude" / "jaiba-configure.yaml").write_text("native-plan-client: &anchor auto\n", encoding="utf-8")

            code, out = run_cli([
                "--home", str(home),
                "--ssot-root", str(ssot),
                "--caveats-dir", str(CAVEATS_DIR),
                "harvest-legacy",
            ])
            self.assertEqual(code, 0)
            self.assertTrue(out["ok"])
            kinds = {f["kind"] for f in out["findings"]}
            self.assertIn("malformed-frontmatter", kinds)
            self.assertIn("invalid-researcher-pin", kinds)
            self.assertIn("invalid-model", kinds)
            self.assertIn("malformed-jaiba-configure-yaml", kinds)
            self.assertNotIn("researcher", out["harvested_hosts"]["claude-code"]["roles"])

    def test_harvests_memory_surface_adapter_into_config_yaml(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "home"
            ssot = home / ".jaiba"
            adapter_dir = home / ".claude" / "skills" / "jaiba-engram-memory"
            adapter_dir.mkdir(parents=True)
            (adapter_dir / "SKILL.md").write_text(
                "---\n"
                "name: jaiba-engram-memory\n"
                "description: Engram MCP memory-surface adapter.\n"
                "version: 1.1.0\n"
                "category: memory-surface\n"
                "adapter-id: jaiba-engram-memory\n"
                "contract-id: jaiba-memory-surface\n"
                "contract-version: 1.1.0\n"
                "---\n"
                "# jaiba-engram-memory\n",
                encoding="utf-8",
            )

            code, out = run_cli([
                "--home", str(home),
                "--ssot-root", str(ssot),
                "--caveats-dir", str(CAVEATS_DIR),
                "harvest-legacy", "--write",
            ])
            self.assertEqual(code, 0)
            self.assertTrue(out["ok"])
            self.assertEqual(out["findings"], [])

            expected_adapter = {
                "adapter-id": "jaiba-engram-memory",
                "name": "jaiba-engram-memory",
                "category": "memory-surface",
                "version": "1.1.0",
                "contract-id": "jaiba-memory-surface",
                "contract-version": "1.1.0",
                "source-host": "claude-code",
                "source-path": "~/.claude/skills/jaiba-engram-memory",
            }
            self.assertEqual(out["memory_adapters"], [expected_adapter])
            self.assertEqual(out["proposed_config"]["memory-adapters"], [expected_adapter])

            parsed_cfg = jaiba_ssot.parse_yaml_subset((ssot / "config.yaml").read_text(encoding="utf-8"))
            self.assertEqual(parsed_cfg["memory-adapters"], [expected_adapter])

            # Re-running harvest-legacy --write deduplicates existing adapter entries
            code2, out2 = run_cli([
                "--home", str(home),
                "--ssot-root", str(ssot),
                "--caveats-dir", str(CAVEATS_DIR),
                "harvest-legacy", "--write",
            ])
            self.assertEqual(code2, 0)
            parsed_cfg2 = jaiba_ssot.parse_yaml_subset((ssot / "config.yaml").read_text(encoding="utf-8"))
            self.assertEqual(parsed_cfg2["memory-adapters"], [expected_adapter])


class ValidateMappingTests(unittest.TestCase):
    def test_valid_and_invalid_host_effort_and_researcher_rules(self):
        with tempfile.TemporaryDirectory() as tmp:
            ssot = Path(tmp) / ".jaiba"
            ssot.mkdir(parents=True)

            # Antigravity valid: pro / flash / inherit
            for model in ("pro", "flash", "inherit"):
                code, out = run_cli([
                    "--ssot-root", str(ssot),
                    "--caveats-dir", str(CAVEATS_DIR),
                    "validate-mapping",
                    "--host", "antigravity", "--role", "executor-medium", "--model", model,
                ])
                self.assertEqual(code, 0, f"expected {model} valid on antigravity: {out}")

            # Antigravity invalid model
            code, out = run_cli([
                "--ssot-root", str(ssot),
                "--caveats-dir", str(CAVEATS_DIR),
                "validate-mapping",
                "--host", "antigravity", "--role", "executor-medium", "--model", "claude-sonnet-4",
            ])
            self.assertEqual(code, 2)
            self.assertEqual(out["errors"][0]["error"], "invalid-host-model")

            # Claude Code valid effort
            code, out = run_cli([
                "--ssot-root", str(ssot),
                "--caveats-dir", str(CAVEATS_DIR),
                "validate-mapping",
                "--host", "claude-code", "--role", "executor-high", "--model", "claude-opus-4-1", "--effort", "xhigh",
            ])
            self.assertEqual(code, 0)

            # Claude Code forbidden effort ("ultracode")
            code, out = run_cli([
                "--ssot-root", str(ssot),
                "--caveats-dir", str(CAVEATS_DIR),
                "validate-mapping",
                "--host", "claude-code", "--role", "executor-high", "--model", "claude-opus-4-1", "--effort", "ultracode",
            ])
            self.assertEqual(code, 2)
            self.assertIn("forbidden-effort-value", {e["error"] for e in out["errors"]})

            # Unsupported effort on opencode / gemini-cli / windsurf / github-copilot per ADR-017
            for host in ("opencode", "gemini-cli", "windsurf", "github-copilot"):
                code, out = run_cli([
                    "--ssot-root", str(ssot),
                    "--caveats-dir", str(CAVEATS_DIR),
                    "validate-mapping",
                    "--host", host, "--role", "executor-medium", "--model", "some/model", "--effort", "high",
                ])
                self.assertEqual(code, 2, f"expected effort rejected on {host}")
                self.assertEqual(out["errors"][0]["error"], "effort-unsupported")

            # Cursor rejects inline [effort=] inside mappings.yaml model field
            code, out = run_cli([
                "--ssot-root", str(ssot),
                "--caveats-dir", str(CAVEATS_DIR),
                "validate-mapping",
                "--host", "cursor", "--role", "executor-medium", "--model", "gpt-5[effort=high]", "--effort", "high",
            ])
            self.assertEqual(code, 2)
            self.assertEqual(out["errors"][0]["error"], "ambiguous-cursor-model")

            # Researcher never allows model or effort on any host (ADR-017)
            code, out = run_cli([
                "--ssot-root", str(ssot),
                "--caveats-dir", str(CAVEATS_DIR),
                "validate-mapping",
                "--host", "claude-code", "--role", "researcher", "--model", "claude-sonnet-4", "--effort", "low",
            ])
            self.assertEqual(code, 2)
            errs = {e["error"] for e in out["errors"]}
            self.assertEqual(errs, {"researcher-model-pin-forbidden", "researcher-effort-forbidden"})

    def test_validate_mappings_file_rejects_researcher_tier(self):
        with tempfile.TemporaryDirectory() as tmp:
            m_path = Path(tmp) / "mappings.yaml"
            m_path.write_text(
                "schema_version: 1\nhosts:\n  opencode:\n    tiers:\n      researcher:\n        model: anthropic/claude-sonnet-4\n",
                encoding="utf-8",
            )
            code, out = run_cli([
                "--caveats-dir", str(CAVEATS_DIR),
                "validate-mapping", "--mappings", str(m_path),
            ])
            self.assertEqual(code, 2)
            self.assertEqual(out["errors"][0]["error"], "researcher-tier-forbidden")


class ProjectTests(unittest.TestCase):
    def test_project_opencode_claude_cursor_antigravity_disabled_and_third_party(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "home"
            ssot = home / ".jaiba"
            ssot.mkdir(parents=True)

            # Pre-seed third-party agent on claude-code and a file in disabled windsurf host
            (home / ".claude" / "agents").mkdir(parents=True)
            third_party = home / ".claude" / "agents" / "team-reviewer.md"
            third_party_text = "---\nname: team-reviewer\n---\nDo not touch.\n"
            third_party.write_text(third_party_text, encoding="utf-8")

            disabled_root = home / ".windsurf"
            disabled_root.mkdir(parents=True)
            disabled_marker = disabled_root / "existing.txt"
            disabled_marker.write_text("untouched\n", encoding="utf-8")

            config_yaml = """schema_version: 1
native-plan-client: "auto"
hosts:
  opencode:
    enabled: true
    config-root: ~/.config/opencode/
  claude-code:
    enabled: true
    config-root: ~/.claude/
  cursor:
    enabled: true
    config-root: ~/.cursor/
  antigravity:
    enabled: true
    config-root: ~/.gemini/config/
  windsurf:
    enabled: false
    config-root: ~/.windsurf/
"""
            mappings_yaml = """schema_version: 1
hosts:
  opencode:
    roles:
      executor-high:
        model: anthropic/claude-opus-4-1
  claude-code:
    roles:
      executor-high:
        model: claude-opus-4-1
        effort: high
  cursor:
    tiers:
      medium:
        model: gpt-5
        effort: medium
  antigravity:
    roles:
      executor-high:
        model: pro
      executor-low:
        model: inherit
"""
            (ssot / "config.yaml").write_text(config_yaml, encoding="utf-8")
            (ssot / "mappings.yaml").write_text(mappings_yaml, encoding="utf-8")

            # Dry run creates nothing in hosts
            code_dry, out_dry = run_cli([
                "--home", str(home),
                "--ssot-root", str(ssot),
                "--caveats-dir", str(CAVEATS_DIR),
                "--base-agents-dir", str(BASE_AGENTS_DIR),
                "project", "--dry-run",
            ])
            self.assertEqual(code_dry, 0)
            self.assertTrue(out_dry["dry_run"])
            self.assertFalse((home / ".config" / "opencode" / "agents").exists())

            # Real projection
            code, out = run_cli([
                "--home", str(home),
                "--ssot-root", str(ssot),
                "--caveats-dir", str(CAVEATS_DIR),
                "--base-agents-dir", str(BASE_AGENTS_DIR),
                "project",
            ])
            self.assertEqual(code, 0, out)
            self.assertTrue(out["ok"])
            self.assertTrue(out["seeded_ssot_contract"])
            self.assertEqual(out["disabled_hosts_untouched"], ["windsurf"])

            # Disabled host untouched
            self.assertFalse((disabled_root / "agents").exists())
            self.assertFalse((disabled_root / "jaiba-contract.md").exists())
            self.assertEqual(disabled_marker.read_text(encoding="utf-8"), "untouched\n")

            # Third-party agent preserved
            self.assertEqual(third_party.read_text(encoding="utf-8"), third_party_text)

            # OpenCode projection: mode: subagent + permission map, NO name:/requires:
            oc_exec_high, _ = jaiba_ssot.split_frontmatter(
                (home / ".config" / "opencode" / "agents" / "executor-high.md").read_text(encoding="utf-8")
            )
            self.assertEqual(oc_exec_high["mode"], "subagent")
            self.assertEqual(oc_exec_high["model"], "anthropic/claude-opus-4-1")
            self.assertEqual(oc_exec_high["permission"]["edit"], "allow")
            self.assertNotIn("name", oc_exec_high)
            self.assertNotIn("requires", oc_exec_high)

            oc_verify, _ = jaiba_ssot.split_frontmatter(
                (home / ".config" / "opencode" / "agents" / "verify.md").read_text(encoding="utf-8")
            )
            self.assertEqual(oc_verify["permission"]["edit"], "deny")
            oc_researcher, _ = jaiba_ssot.split_frontmatter(
                (home / ".config" / "opencode" / "agents" / "researcher.md").read_text(encoding="utf-8")
            )
            self.assertNotIn("model", oc_researcher)
            self.assertEqual(oc_researcher["permission"]["edit"], "deny")

            # Claude Code projection: effort: top-level key, researcher omits model/effort
            cc_high, _ = jaiba_ssot.split_frontmatter(
                (home / ".claude" / "agents" / "executor-high.md").read_text(encoding="utf-8")
            )
            self.assertEqual(cc_high["name"], "executor-high")
            self.assertEqual(cc_high["model"], "claude-opus-4-1")
            self.assertEqual(cc_high["effort"], "high")
            self.assertIn("requires", cc_high)
            cc_res, _ = jaiba_ssot.split_frontmatter(
                (home / ".claude" / "agents" / "researcher.md").read_text(encoding="utf-8")
            )
            self.assertNotIn("model", cc_res)
            self.assertNotIn("effort", cc_res)

            # Cursor projection: inline model[effort=]
            cur_med, _ = jaiba_ssot.split_frontmatter(
                (home / ".cursor" / "agents" / "executor-medium.md").read_text(encoding="utf-8")
            )
            self.assertEqual(cur_med["model"], "gpt-5[effort=medium]")
            self.assertNotIn("effort", cur_med)

            # Antigravity projection: pro kept, inherit omitted
            ag_high, _ = jaiba_ssot.split_frontmatter(
                (home / ".gemini" / "config" / "agents" / "executor-high.md").read_text(encoding="utf-8")
            )
            self.assertEqual(ag_high["model"], "pro")
            ag_low, _ = jaiba_ssot.split_frontmatter(
                (home / ".gemini" / "config" / "agents" / "executor-low.md").read_text(encoding="utf-8")
            )
            self.assertNotIn("model", ag_low)

            # Contract symlinks point to ~/.jaiba/contract/jaiba-contract.md
            ssot_contract = ssot / "contract" / "jaiba-contract.md"
            self.assertTrue(ssot_contract.is_file())
            for host_root in (
                home / ".config" / "opencode",
                home / ".claude",
                home / ".cursor",
                home / ".gemini" / "config",
            ):
                link = host_root / "jaiba-contract.md"
                self.assertTrue(link.is_symlink())
                self.assertEqual(link.resolve(), ssot_contract.resolve())

            # No leftover atomic temp files anywhere under home
            leftover_tmps = [p for p in home.rglob("*.tmp.*")]
            self.assertEqual(leftover_tmps, [])

    def test_project_fails_closed_before_writing_on_invalid_enabled_mapping(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "home"
            ssot = home / ".jaiba"
            ssot.mkdir(parents=True)
            (ssot / "config.yaml").write_text(
                "schema_version: 1\nhosts:\n  opencode:\n    enabled: true\n",
                encoding="utf-8",
            )
            (ssot / "mappings.yaml").write_text(
                "schema_version: 1\nhosts:\n  opencode:\n    roles:\n      executor-medium:\n        model: openai/gpt-5\n        effort: high\n",
                encoding="utf-8",
            )
            code, out = run_cli([
                "--home", str(home),
                "--ssot-root", str(ssot),
                "--caveats-dir", str(CAVEATS_DIR),
                "--base-agents-dir", str(BASE_AGENTS_DIR),
                "project",
            ])
            self.assertEqual(code, 2)
            self.assertFalse(out["ok"])
            self.assertEqual(out["errors"][0]["error"], "effort-unsupported")
            self.assertFalse((home / ".config" / "opencode" / "agents").exists())
            self.assertFalse((ssot / "contract" / "jaiba-contract.md").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
