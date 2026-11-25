"""Unit tests for skills/doctor/scripts/check-tools.sh.

Pure Python 3 stdlib unittest suite executed in isolated temporary directories.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True

REPO_ROOT = Path(__file__).resolve().parents[3]
CHECK_TOOLS_SH = REPO_ROOT / "skills" / "doctor" / "scripts" / "check-tools.sh"
PACKAGED_CONTRACT = REPO_ROOT / "skills" / "doctor" / "assets" / "jaiba-contract.md"
INJECTED_SKILLS_REL = "skills/doctor/evals/fixtures/injected-skills/skills"
INJECTED_SKILLS_DIR = REPO_ROOT / INJECTED_SKILLS_REL
CANONICAL_BATTERY = (
    "executor-high",
    "executor-medium",
    "executor-low",
    "code-analyst",
    "business-analyst",
    "verify",
    "researcher",
)


def _run_check_tools(
    args: list[str],
    *,
    cwd: Path,
    home: Path,
    ssot_root: Path,
) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["HOME"] = str(home)
    env["JAIBA_SSOT_ROOT"] = str(ssot_root)
    return subprocess.run(
        ["bash", str(CHECK_TOOLS_SH), *args],
        cwd=str(cwd),
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


def _write_agent(path: Path, name: str, tool: str = "git") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"---\nname: {name}\ndescription: test agent\nrequires:\n  - {tool}\n---\nBody\n",
        encoding="utf-8",
    )


def _write_skill(path: Path, name: str, tool: str, *, jaiba_tag: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tags_block = "tags:\n  - jaiba\n" if jaiba_tag else ""
    path.write_text(
        f"---\nname: {name}\ndescription: test skill\nrequires:\n  - {tool}\n{tags_block}---\nBody\n",
        encoding="utf-8",
    )


def _seed_multihost_env(tmp_path: Path, *, extra_hosts_yaml: str = "") -> dict[str, Path]:
    home = tmp_path / "home"
    ssot = tmp_path / "custom-ssot"
    project = tmp_path / "project"
    home.mkdir(parents=True)
    ssot.mkdir(parents=True)
    (project / ".ai" / "memory").mkdir(parents=True)
    (project / ".ai" / "memory" / "index.md").write_text("# Index\n", encoding="utf-8")

    # Canonical SSOT contract, base battery, and shared skill
    ssot_contract = ssot / "contract" / "jaiba-contract.md"
    ssot_contract.parent.mkdir(parents=True)
    ssot_contract.write_text(PACKAGED_CONTRACT.read_text(encoding="utf-8"), encoding="utf-8")

    for role in CANONICAL_BATTERY:
        _write_agent(ssot / "agents" / "base" / f"{role}.md", role)

    _write_skill(ssot / "skills" / "shared-ssot-skill" / "SKILL.md", "shared-ssot-skill", "bash", jaiba_tag=True)

    # Host 1: claude-code (enabled: true, symlinked contract in sync, 7/7 canonical, skills present)
    claude_root = home / ".claude"
    claude_root.mkdir(parents=True)
    (claude_root / "jaiba-contract.md").symlink_to(ssot_contract)
    for role in CANONICAL_BATTERY:
        _write_agent(claude_root / "agents" / f"{role}.md", role)
    _write_skill(claude_root / "skills" / "claude-local-skill" / "SKILL.md", "claude-local-skill", "git", jaiba_tag=True)

    # Host 2: opencode (enabled: true, drifted copy contract, 5/7 canonical (+1 third-party), skills absent)
    opencode_root = home / ".config" / "opencode"
    opencode_root.mkdir(parents=True)
    (opencode_root / "jaiba-contract.md").write_text("# Drifted contract copy\n", encoding="utf-8")
    for role in CANONICAL_BATTERY[:5]:
        _write_agent(opencode_root / "agents" / f"{role}.md", role)
    _write_agent(opencode_root / "agents" / "custom-opencode-agent.md", "custom-opencode-agent", "git")

    # Host 3: cursor (enabled: false, has skills/agents that must NOT be scanned)
    cursor_root = home / ".cursor"
    _write_skill(
        cursor_root / "skills" / "cursor-disabled-skill" / "SKILL.md",
        "cursor-disabled-skill",
        "cursor-disabled-tool",
    )
    _write_agent(
        cursor_root / "agents" / "cursor-disabled-agent.md",
        "cursor-disabled-agent",
        "cursor-disabled-agent-tool",
    )

    config_yaml = (
        "schema_version: 1\n"
        'contract-path: "~/.jaiba/contract/jaiba-contract.md"\n'
        'skills-dir: "~/.jaiba/skills"\n'
        "hosts:\n"
        "  claude-code:\n"
        "    enabled: true\n"
        "    config-root: ~/.claude\n"
        "  opencode:\n"
        "    enabled: true\n"
        "    config-root: ~/.config/opencode\n"
        "  cursor:\n"
        "    enabled: false\n"
        "    config-root: ~/.cursor\n"
        f"{extra_hosts_yaml}"
    )
    (ssot / "config.yaml").write_text(config_yaml, encoding="utf-8")

    return {"home": home, "ssot": ssot, "project": project}


class CheckToolsMultiHostTests(unittest.TestCase):
    def test_auto_multihost_host_projections_contract_sync_drift_and_disabled_isolation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            paths = _seed_multihost_env(Path(tmp))
            res = _run_check_tools(
                ["--auto", str(paths["project"])],
                cwd=paths["project"],
                home=paths["home"],
                ssot_root=paths["ssot"],
            )
            self.assertEqual(res.returncode, 0, res.stderr)

            layout_path = paths["project"] / ".atl" / "tool-layout.md"
            self.assertTrue(layout_path.is_file())
            report = layout_path.read_text(encoding="utf-8")

            self.assertIn("## Host Projections", report)
            self.assertIn("✅ in sync with packaged contract", report)
            self.assertIn("7/7 canonical", report)
            self.assertIn("- **Disabled hosts (untouched, not scanned):** `cursor`", report)

            self.assertIn(
                "| `claude-code` | `~/.claude` | ✅ symlinked (in sync) | 7/7 canonical | present |",
                report,
            )
            self.assertIn(
                "| `opencode` | `~/.config/opencode` | ⚠️ drifted (copy differs from SSOT) | 5/7 canonical (+1 third-party) | absent |",
                report,
            )

            # Disabled host skills/agents/tools must never be scanned
            for forbidden in (
                "cursor-disabled-skill",
                "cursor-disabled-tool",
                "cursor-disabled-agent",
                "cursor-disabled-agent-tool",
            ):
                self.assertNotIn(forbidden, report)

    def test_combined_explicit_and_ssot_scans_both_and_emits_host_projections(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            paths = _seed_multihost_env(Path(tmp))
            explicit_skills = paths["project"] / ".agents" / "skills"
            _write_skill(
                explicit_skills / "explicit-local-skill" / "SKILL.md",
                "explicit-local-skill",
                "explicit-probe-cli",
            )

            res = _run_check_tools(
                [str(explicit_skills), str(paths["project"])],
                cwd=paths["project"],
                home=paths["home"],
                ssot_root=paths["ssot"],
            )
            self.assertEqual(res.returncode, 0, res.stderr)

            report = (paths["project"] / ".atl" / "tool-layout.md").read_text(encoding="utf-8")
            self.assertIn("`explicit-local-skill`", report)
            self.assertIn("`explicit-probe-cli`", report)
            self.assertIn("`claude-local-skill`", report)
            self.assertIn("`shared-ssot-skill`", report)
            self.assertIn("## Host Projections", report)
            self.assertIn(
                "| `claude-code` | `~/.claude` | ✅ symlinked (in sync) | 7/7 canonical | present |",
                report,
            )
            self.assertIn(
                "| `opencode` | `~/.config/opencode` | ⚠️ drifted (copy differs from SSOT) | 5/7 canonical (+1 third-party) | absent |",
                report,
            )
            self.assertIn("- **Disabled hosts (untouched, not scanned):** `cursor`", report)
            self.assertNotIn("cursor-disabled-tool", report)

    def test_malformed_config_yaml_entries_rejected_without_echoing_raw_values(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bad_entries = (
                '  "evil;host$(whoami)":\n'
                "    enabled: true\n"
                "    config-root: ~/.evil\n"
                "  travhost:\n"
                "    enabled: true\n"
                "    config-root: ~/.claude/../../etc/passwd\n"
            )
            paths = _seed_multihost_env(Path(tmp), extra_hosts_yaml=bad_entries)

            res = _run_check_tools(
                ["--auto", str(paths["project"])],
                cwd=paths["project"],
                home=paths["home"],
                ssot_root=paths["ssot"],
            )
            self.assertEqual(res.returncode, 0, res.stderr)
            self.assertIn("rejected by validation", res.stdout)

            report = (paths["project"] / ".atl" / "tool-layout.md").read_text(encoding="utf-8")
            self.assertIn("## Rejected entries", report)
            self.assertIn("| `config:host:<redacted>` | invalid host id | 1 |", report)
            self.assertIn("| `config:host:travhost` | invalid config-root | 1 |", report)

            for raw in ("evil;host", "$(whoami)", "whoami", "../../etc/passwd"):
                self.assertNotIn(raw, report)
                self.assertNotIn(raw, res.stdout)

            # Valid enabled hosts still render normally
            self.assertIn("| `claude-code` |", report)
            self.assertIn("| `opencode` |", report)

    def test_injected_skills_fixture_rejects_poison_tokens_without_leaking(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            home = tmp_path / "home"
            home.mkdir()
            absent_ssot = tmp_path / "no-ssot"
            project = tmp_path / "project"
            project.mkdir()

            self.assertTrue(INJECTED_SKILLS_DIR.is_dir())
            res = _run_check_tools(
                [INJECTED_SKILLS_REL, str(project)],
                cwd=REPO_ROOT,
                home=home,
                ssot_root=absent_ssot,
            )
            self.assertEqual(res.returncode, 0, res.stderr)
            self.assertIn("rejected by validation", res.stdout)

            report = (project / ".atl" / "tool-layout.md").read_text(encoding="utf-8")
            m = re.search(r"- \*\*Rejected \(failed validation\):\*\* (\d+)", report)
            self.assertIsNotNone(m, report)
            assert m is not None
            self.assertGreater(int(m.group(1)), 0)

            self.assertIn("## Rejected entries", report)
            self.assertIn("| `skill:innocuous-tool` | invalid tool token |", report)
            self.assertIn("| `hook` | invalid tool token |", report)

            for malicious in (
                "attacker.example",
                "whoami",
                "Ignore all previous",
                "ignore previous instructions",
                "rm -rf",
            ):
                self.assertNotIn(malicious, report)
                self.assertNotIn(malicious, res.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
