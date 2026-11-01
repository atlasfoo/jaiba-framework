#!/usr/bin/env python3
"""Local stdlib checks for the `JAIBA3` (jaiba-engram-storage/3) wire profile.

Pure byte/structure computation on synthetic data. It never calls Engram,
never certifies the adapter, and is not operational conformance. Usage:
    python3 run_jaiba3_static.py [evidence_dir]
"""
import base64
import hashlib
import json
import pathlib
import re
import sys

PREFIX = "JAIBA3."
DIRECT_MAX = 30000          # raw UTF-8 bytes of the logical snapshot
LIMIT_BYTES = 50000         # Engram MaxObservationLength (documented)
TOPIC_MAX = 60
SHA = re.compile(r"^[0-9a-f]{64}$")


class Fail(Exception):
    pass


def sha(b):
    return hashlib.sha256(b).hexdigest()


def snapshot_bytes(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def encode(raw):
    return PREFIX + sha(raw) + "." + base64.b64encode(raw).decode("ascii")


def decode(line):
    """Strict decode of one wire line; fails closed on anything unexpected."""
    if line != line.strip() or "\n" in line or "\r" in line:
        raise Fail("whitespace at edges or inside the wire line")
    if "<" in line or ">" in line or "[REDACTED]" in line:
        raise Fail("redaction markers or angle brackets in wire")
    if not line.startswith(PREFIX):
        raise Fail("unsupported profile prefix")
    digest, _, b64 = line[len(PREFIX):].partition(".")
    if not SHA.match(digest) or not b64:
        raise Fail("malformed digest or payload")
    try:
        raw = base64.b64decode(b64, validate=True)
    except Exception as exc:
        raise Fail("invalid base64") from exc
    if base64.b64encode(raw).decode("ascii") != b64:
        raise Fail("non-canonical base64")
    if sha(raw) != digest:
        raise Fail("sha256 mismatch")
    return raw


def extract(response_lines, project, scope):
    """Pick the single JAIBA3 line from an observation read; verify labels."""
    wires = [x for x in response_lines if x.startswith(PREFIX)]
    projects = [x for x in response_lines if x.startswith("Project:")]
    scopes = [x for x in response_lines if x.startswith("Scope:")]
    if len(wires) != 1 or len(projects) != 1 or len(scopes) != 1:
        raise Fail("expected exactly one wire, Project and Scope line")
    if projects[0].split(":", 1)[1].strip() != project:
        raise Fail("foreign Project")
    if scopes[0].split(":", 1)[1].strip() != scope:
        raise Fail("foreign Scope")
    for x in response_lines:
        if x.rstrip().endswith("... [truncated]"):
            raise Fail("truncated read")
    return decode(wires[0])


def topic_key(kind, ns16, ident):
    if kind == "cat":
        key = f"jaiba/v3/{ns16}/cat/{ident[:24]}"
    elif kind == "obj":
        key = f"jaiba/v3/{ns16}/obj/{ident[:24]}"
    else:
        ver, idx = ident
        key = f"jaiba/v3/{ns16}/chk/{ver[:20]}/{idx:04d}"
    if len(key) > TOPIC_MAX:
        raise Fail("topic_key longer than 60")
    return key


def split_chunks(raw):
    return [raw[i:i + DIRECT_MAX] for i in range(0, len(raw), DIRECT_MAX)]


def chunked_object(raw, ns16, ids):
    chunks = split_chunks(raw)
    ver = sha(raw)
    entries = []
    for i, part in enumerate(chunks):
        entries.append({"index": i, "obs_id": ids[i], "topic_key": topic_key("chk", ns16, (ver, i)),
                        "bytes": len(part), "sha256": sha(part)})
    return chunks, {"kind": "chunked-object", "logical_sha256": ver, "logical_bytes": len(raw), "chunks": entries}


def reassemble(manifest, reads):
    """reads: {obs_id: wire line}. Fail closed on any gap, order or digest issue."""
    parts = []
    for i, e in enumerate(manifest["chunks"]):
        if e["index"] != i:
            raise Fail("chunk order")
        part = decode(reads[e["obs_id"]])
        if len(part) != e["bytes"] or sha(part) != e["sha256"]:
            raise Fail("chunk mismatch")
        parts.append(part)
    raw = b"".join(parts)
    if len(raw) != manifest["logical_bytes"] or sha(raw) != manifest["logical_sha256"]:
        raise Fail("logical digest mismatch")
    return raw


def expect_fail(fn, label):
    try:
        fn()
    except Fail:
        return
    raise AssertionError(f"{label} was accepted")


def reconcile(catalog, observed):
    """Finite reconcile: object/chunks first, then catalog. Never mint a second object."""
    out = {}
    for addr, obj_id in observed.items():
        entry = catalog["entries"].get(addr)
        out[addr] = "adopt-existing" if entry is None else ("ok" if entry["obs_id"] == obj_id else "mismatch-stop")
    return out


def main(evidence):
    evidence.mkdir(parents=True, exist_ok=True)
    ns16 = "0123456789abcdef"
    project, scope = "jaiba-framework", "project"

    # 1. Direct object: CRLF, Unicode, literal <private> text survive as bytes.
    obj = {"kind": "object", "address": "decisions/001", "revision": 3,
           "content": "línea\r\ncafé 🧭 <private>secret-like</private>\r\n",
           "metadata": {"unknown_extension": {"decimal": "1.00"}},
           "relations": [{"target": "a"}, {"target": "b"}]}
    raw = snapshot_bytes(obj)
    assert len(raw) <= DIRECT_MAX
    wire = encode(raw)
    assert "<" not in wire and ">" not in wire and wire == wire.strip()
    assert len(wire.encode("ascii")) <= LIMIT_BYTES * 0.8 + 100
    assert decode(wire) == raw and json.loads(raw)["content"] == obj["content"]

    # 2. Framing: 9 vs 10 line responses both extract by prefix.
    base = ["Observation #1", "Title: x", "Type: manual", "Topic: t", wire, "Created: now"]
    r9 = base + ["Project: jaiba-framework", "Scope: project", "Revisions: 1"]
    r10 = base + ["Updated: now", "Project: jaiba-framework", "Scope: project", "Revisions: 1"]
    assert extract(r9, project, scope) == extract(r10, project, scope) == raw

    # 3. Fail-closed cases.
    expect_fail(lambda: extract(r9, "other-project", scope), "foreign project")
    expect_fail(lambda: extract(r9, project, "personal"), "foreign scope")
    expect_fail(lambda: extract([x for x in r9 if not x.startswith("Project:")], project, scope), "missing Project")
    expect_fail(lambda: extract(r9[:-3] + [wire[:-3] + "... [truncated]"] + r9[-3:], project, scope), "truncated")
    expect_fail(lambda: decode(wire[:-2]), "truncated wire")
    flipped = wire[:-1] + ("A" if wire[-1] != "A" else "B")
    expect_fail(lambda: decode(flipped), "bit flip")
    expect_fail(lambda: decode(" " + wire), "leading space")
    expect_fail(lambda: decode(wire + "\n"), "trailing newline")
    expect_fail(lambda: decode(wire.replace(PREFIX, "[REDACTED]", 1)), "redacted")
    expect_fail(lambda: decode("JAIBA2." + wire[len(PREFIX):]), "JAIBA2 prefix")
    expect_fail(lambda: decode("JAIBA1." + wire[len(PREFIX):]), "JAIBA1 prefix")

    # 4. Topic keys.
    for k in (topic_key("cat", ns16, "a" * 40), topic_key("obj", ns16, "b" * 40), topic_key("chk", ns16, ("c" * 64, 1))):
        assert len(k) <= TOPIC_MAX, k

    # 5. Large object > 30,000 raw bytes: chunked, lossless, enumerable.
    big = {"kind": "object", "address": "work/plan", "revision": 1, "content": ("plan línea 🧭\r\n" * 2800)}
    big_raw = snapshot_bytes(big)
    assert len(big_raw) > DIRECT_MAX
    ids = list(range(100, 100 + (len(big_raw) + DIRECT_MAX - 1) // DIRECT_MAX))
    chunks, manifest = chunked_object(big_raw, ns16, ids)
    assert len(chunks) >= 2 and all(len(c) <= DIRECT_MAX for c in chunks)
    reads = {i: encode(c) for i, c in zip(ids, chunks)}
    assert all(len(w) < LIMIT_BYTES for w in reads.values())
    assert reassemble(manifest, reads) == big_raw
    damaged = dict(reads)
    damaged[ids[1]] = encode(chunks[1][:-1] + b"X")
    expect_fail(lambda: reassemble(manifest, damaged), "corrupt chunk")
    missing = {k: v for k, v in reads.items() if k != ids[0]}
    try:
        reassemble(manifest, missing)
    except KeyError:
        pass
    else:
        raise AssertionError("missing chunk accepted")
    swapped = dict(manifest, chunks=list(reversed(manifest["chunks"])))
    expect_fail(lambda: reassemble(swapped, reads), "chunk order")

    # 6. Catalogue reconciliation.
    catalog = {"kind": "catalog", "entries": {"decisions/001": {"obs_id": 7, "state": "live"}}}
    rec = reconcile(catalog, {"decisions/001": 7, "decisions/002": 9})
    assert rec == {"decisions/001": "ok", "decisions/002": "adopt-existing"}
    assert reconcile(catalog, {"decisions/001": 8}) == {"decisions/001": "mismatch-stop"}

    # 7. judgment_required is advisory: never a verification input.
    advisory = r9 + ["Suggestion: judgment_required candidate #999"]
    assert extract(advisory, project, scope) == raw

    receipt = {"case_kind": "static local computation; not skill execution or operational conformance",
               "direct_snapshot_bytes": len(raw), "direct_wire_bytes": len(wire),
               "large_snapshot_bytes": len(big_raw), "large_chunks": len(chunks),
               "checks": "pass"}
    (evidence / "snapshot.json").write_bytes(raw)
    (evidence / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, sort_keys=True))


if __name__ == "__main__":
    main(pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/opencode/jaiba3-static"))
