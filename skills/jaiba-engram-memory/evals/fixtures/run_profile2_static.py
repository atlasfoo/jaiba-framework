#!/usr/bin/env python3
"""Static fixture byte checks; not skill execution or operational conformance."""
import base64
import hashlib
import json
import pathlib
import sys

fixture = pathlib.Path(__file__).with_name("profile-2-static-cases.json")
evidence = pathlib.Path(sys.argv[1])
evidence.mkdir(parents=True, exist_ok=True)
data = json.loads(fixture.read_text(encoding="utf-8"))
assert data["static"] is True

for response in data["mcp_responses"]:
    lines = response["lines"]
    labels = {"wire": [x for x in lines if x.startswith("JAIBA2.")], "project": [x for x in lines if x.startswith("Project:")], "scope": [x for x in lines if x.startswith("Scope:")]}
    ok = all(len(values) == 1 for values in labels.values())
    assert ok == (response["expected"] == "pass"), response["name"]
assert [len(x["lines"]) for x in data["mcp_responses"][:2]] == [9, 10]
receipt = data["receipt"]
assert type(receipt["elapsed_from_intent_seconds"]) is float
assert all(type(value) is int for value in receipt["protocol"].values())

snapshot = json.dumps(data["snapshot"], ensure_ascii=False, separators=(",", ":")).encode("utf-8")
wire = "JAIBA2." + base64.b64encode(snapshot).decode("ascii")
decoded = base64.b64decode(wire[len("JAIBA2."):], validate=True)
assert base64.b64encode(decoded).decode("ascii") == wire[len("JAIBA2."):]
assert decoded == snapshot
obj = json.loads(decoded)
assert "\r\n" in obj["content"] and all(x in obj["content"] for x in ("café", "🧭"))
assert obj["metadata"]["unknown_extension"]["decimal_token"] == "1.00"
assert [r["target"] for r in obj["relations"]] == ["first", "second"]
assert len(wire.encode("ascii")) != receipt["truncation"]["original_bytes"]

for candidate in (wire[:-2], wire[:-1] + ("A" if wire[-1] != "A" else "B")):
    try:
        raw = base64.b64decode(candidate[len("JAIBA2."):], validate=True)
        valid = raw == snapshot
    except (ValueError, base64.binascii.Error):
        valid = False
    assert not valid
legacy = data["legacy_wire"]
assert legacy.startswith("JAIBA1.")
try:
    if not legacy.startswith("JAIBA2."):
        raise ValueError("unsupported profile")
    base64.b64decode(legacy[len("JAIBA2."):], validate=True)
except ValueError:
    pass
else:
    raise AssertionError("JAIBA1 accepted")

for name, payload in (("snapshot.json", snapshot), ("readback.json", decoded)):
    (evidence / name).write_bytes(payload)
result = {"case_kind": "static fixture computation; not skill execution or operational conformance", "snapshot_bytes": len(snapshot), "snapshot_sha256": hashlib.sha256(snapshot).hexdigest(), "readback_bytes": len(decoded), "readback_sha256": hashlib.sha256(decoded).hexdigest(), "wire_bytes": len(wire.encode("ascii")), "mcp_line_counts": [9, 10], "truncation_original_bytes": receipt["truncation"]["original_bytes"], "protocol_checks": "pass", "preservation": "pass", "truncation_corruption": "fail closed", "JAIBA1": "rejected before decode"}
(evidence / "receipt.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, sort_keys=True))
