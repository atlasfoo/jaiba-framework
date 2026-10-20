"""Strict structural checks for synthetic interchange fixtures only.

No adapter, transfer, filesystem migration, or backend conformance is exercised.
"""
import hashlib
import json
import re
from pathlib import Path

import yaml

DATA = json.loads(Path(__file__).with_name("transfer-recovery-cases.json").read_text())
CONSTITUTIVE = {"index", "project", "architecture", "purpose", "scope", "sub-unit", "quality-gate", "convention", "decision", "reference", "snippet", "log-entry"}
EXECUTIVE = {"prd", "plan", "tasks", "walkthrough"}
OBJECTS = DATA["objects"]
BY_ADDRESS = {tuple(o["address"]): o for o in OBJECTS}

assert DATA["contract"] == {"id": "jaiba-memory-surface", "version": "1.0.0"}
assert DATA["fingerprint"]["covers"] == ["address", "type", "content", "metadata", "relations"]
assert len(BY_ADDRESS) == len(OBJECTS), "duplicate logical address"
assert len(DATA["registry"]["contexts"]) == 3
assert {c["id"] for c in DATA["registry"]["contexts"]} >= {"ctx-alpha", "ctx-beta", "ctx-empty"}

def frontmatter(content):
    match = re.match(r"\A---\n(.*?)\n---\n", content, re.S)
    assert match, "expected frontmatter on concept/executive object"
    return yaml.safe_load(match.group(1))

for obj in OBJECTS:
    address = obj["address"]
    assert len(address) == 5 and all(isinstance(v, str) and v for v in (address[0], address[1], address[2], address[4]))
    ns, project, category, context, logical_id = address
    assert isinstance(obj["content"], str) and obj["content"]
    assert isinstance(obj["metadata"], dict) and isinstance(obj["relations"], list)
    assert obj["revision_evidence"] == "computed-by-validator"
    assert category in {"constitutive", "executive"}
    if ns == "jaiba":
        assert project == DATA["registry"]["project_id"]
        if category == "constitutive":
            assert context is None, "constitutive address context must be absent/null"
            assert obj["type"] in CONSTITUTIVE
        else:
            assert context in {c["id"] for c in DATA["registry"]["contexts"]}
            assert obj["type"] in EXECUTIVE
        fm = frontmatter(obj["content"])
        assert fm["type"] == obj["type"], f"frontmatter/type mismatch for {logical_id}"
    else:
        assert logical_id == "witness" and ns == "ordinary", "unexpected non-owned fixture object"
    for rel in obj["relations"]:
        assert rel["source"] == address
        target = rel["target"]
        assert isinstance(target, list) and len(target) == 5
        assert tuple(target) in BY_ADDRESS, f"unresolved internal relation target: {target}"

# Required executive payload shape, including real PRD criteria YAML and explicit null/absent distinction.
prd = next(o for o in OBJECTS if o["type"] == "prd")
criteria_match = re.search(r"```yaml\n(.*?)\n```", prd["content"], re.S)
assert criteria_match
criteria = yaml.safe_load(criteria_match.group(1))["criteria"]
assert len(criteria) == 1 and criteria[0]["id"] == "XFER-001"
assert criteria[0]["happy"] and criteria[0]["sad"]
plan = next(o for o in OBJECTS if o["type"] == "plan" and o["address"][3] == "ctx-alpha")
assert plan["metadata"]["related_prd"] == prd["address"]
assert frontmatter(plan["content"])["status"] == "approved"
tasks = next(o for o in OBJECTS if o["type"] == "tasks")
assert "## Gate Commands" in tasks["content"] and "T-001" in tasks["content"]
walkthrough = next(o for o in OBJECTS if o["type"] == "walkthrough")
assert "Checkpoint — Phase 1" in walkthrough["content"]
beta_plan = next(o for o in OBJECTS if o["type"] == "plan" and o["address"][3] == "ctx-beta")
assert beta_plan["metadata"]["related_prd"] is None
assert "related_prd" not in next(o for o in OBJECTS if o["type"] == "tasks")["metadata"]
assert next(o for o in OBJECTS if o["address"][4] == "close-immutable-7")["metadata"]["close_id"] == "close-immutable-7"
assert DATA["envelope_extensions"]["vendor.optional"] == {"opaque": [1, None, "retained"]}
assert DATA["required_extension_negative"]["expected"] == "block"
assert DATA["relation_findings"][0]["expected"] == "preserve-and-report"
assert DATA["relation_findings"][0]["source"] in [o["address"] for o in OBJECTS]
assert {"bundle-to-external", "legacy-to-external", "external-a-to-external-b", "external-b-to-external-a"} <= set(DATA["transfer_pairs"])
assert "external-to-filesystem-distinct-context-roots" in DATA["transfer_pairs"]
assert {"changed-source-same-count", "foreign-identical-payload-collision", "activation-partial", "unknown-routing-no-rollback", "archive-interrupted-selective-clear-log-verified"} <= set(DATA["faults"])

legacy = DATA["legacy_representation"]
assert legacy["frontmatter"] == "absent" and len(legacy["mapping"]) == 3
for name, body in legacy["documents"].items():
    assert body.startswith("# ") and not body.startswith("---\n")
    assert any(row["document"] == name and row["type"] is None for row in legacy["mapping"])

# Calculate the declared complete-object fingerprint; fixture revisions are never fabricated tokens.
fingerprints = {}
for obj in OBJECTS:
    covered = {k: obj[k] for k in ("address", "type", "content", "metadata", "relations")}
    encoded = json.dumps(covered, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    fingerprints[tuple(obj["address"])] = hashlib.sha256(encoded).hexdigest()
assert all(len(value) == 64 for value in fingerprints.values())
assert len(set(fingerprints.values())) == len(fingerprints)
print(f"fixture structure valid; computed {len(fingerprints)} complete-object fingerprints; no adapter or transfer exercised")
