#!/usr/bin/env python3
"""JAIBA4 codec for the jaiba-engram-memory adapter.

Physical protocol ``jaiba-engram-storage/4`` (``JAIBA4``). Logical rules
stay in the effective ``create-memory`` contract and ``executive-journal``
reference; this file is the deterministic codec and agent-relay argument
builder, not a backend client, a second contract, or a transaction engine.

Transport is ``agent-relay`` only. No subcommand opens a socket, spawns a
backend CLI, or writes a binding file. ``encode``, ``decode``, ``delta``,
``materialize``, ``render``, ``binding-path``, and ``cost`` never call the
backend. ``batch-prepare`` emits canonical tool arguments. ``batch-verify``
compares reads the agent supplies.

Wire line (ASCII, one line, no whitespace)::

    JAIBA4.<sha256_hex>.<base64_rfc4648>

``sha256_hex`` is 64 lowercase hex digits over the raw payload bytes.
``base64`` is RFC 4648 standard padded encoding of those same bytes.
Decode also accepts a legacy ``JAIBA3.`` line and never relabels it.
``JAIBA1.`` and ``JAIBA2.`` are rejected.

New JSON payloads are canonicalised with ``sort_keys``, ``ensure_ascii=False``,
compact separators, and ``allow_nan=False``. Decode returns the exact payload
bytes (``payload_b64``); it does not re-serialise them for comparison.
``--raw`` wraps retained bytes without parsing.

Direct records are raw payloads of at most 30,000 bytes. Larger payloads are
split into 30,000-byte slices plus one ``chunked-object`` record. Topic keys
are at most 60 characters under ``jaiba/v4/<ns16>/``.

Logical revision and chain digest are SHA-256 hex of the canonical projection
and of the executive-journal chain wrapper, respectively. They are not the
same token.
"""

from __future__ import annotations

import argparse
import base64
import copy
import hashlib
import json
import os
import re
import sys
from pathlib import Path

PROTOCOL = "jaiba-engram-storage/4"
PREFIX = "JAIBA4."
LEGACY_PREFIX = "JAIBA3."
ACCEPTED_PREFIXES = (PREFIX, LEGACY_PREFIX)
DIRECT_MAX = 30000
TOPIC_MAX = 60
NS16_RE = re.compile(r"^[0-9a-f]{16}$")
SHA_RE = re.compile(r"^[0-9a-f]{64}$")
TASK_ID_RE = re.compile(r"^T-\d+$")
TASK_LINE_RE = re.compile(r"^- \[([ xX])\] \*\*(T-\d+)\*\*(.*)$")
LOOSE_BOX_RE = re.compile(r"^- \[[^\]]*\]")
HEADING_RE = re.compile(r"^(#{1,6})[ \t]+(.*)$")
FENCE_OPEN_RE = re.compile(r"^```yaml[ \t]*$")
FENCE_CLOSE_RE = re.compile(r"^```[ \t]*$")
CRITERIA_RE = re.compile(r"^([ \t]*)criteria:[ \t]*$")
ITEM_RE = re.compile(r"^([ \t]*)- id: (\S+)[ \t]*$")
STATUS_RE = re.compile(r"^([ \t]*)status:[ \t]*(.*)$")
KEY_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_-]*$")
FM_KEY_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*):(.*)$")

EXECUTIVE_TYPES = ("prd", "plan", "tasks", "walkthrough")
PLAN_OPS = {
    "set-frontmatter",
    "replace-section",
    "append-section",
    "append-to-section",
    "remove-section",
}
LEGAL = {
    "tasks": {"check", "uncheck", "add-task", "amend-task"},
    "plan": set(PLAN_OPS),
    "prd": set(PLAN_OPS) | {
        "add-criterion",
        "update-criterion",
        "remove-criterion",
        "set-criterion-status",
    },
    "walkthrough": {"append-entry"},
}
PARAMS = {
    "check": {"ids"},
    "uncheck": {"ids"},
    "add-task": {"after", "block"},
    "amend-task": {"id", "block"},
    "set-frontmatter": {"key", "value"},
    "replace-section": {"heading", "content"},
    "append-section": {"after", "heading", "content"},
    "append-to-section": {"heading", "content"},
    "remove-section": {"heading"},
    "add-criterion": {"yaml"},
    "update-criterion": {"id", "yaml"},
    "remove-criterion": {"id"},
    "set-criterion-status": {"id", "status"},
    "append-entry": {"content"},
}

DRAFT = "draft"
FROZEN = "frozen"
UNCLASSIFIED = "unclassified"

ADDRESS_ALIASES = {
    "namespace": "namespace",
    "project-id": "project-id",
    "project_id": "project-id",
    "category": "category",
    "context-id": "context-id",
    "context_id": "context-id",
    "logical-id": "logical-id",
    "logical_id": "logical-id",
}


class JaibaError(Exception):
    def __init__(self, code: str, detail: str, evidence: dict | None = None):
        super().__init__(detail)
        self.code = code
        self.detail = detail
        self.evidence = evidence or {}


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json_bytes(value) -> bytes:
    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise JaibaError("invalid-object", "value is not canonical JSON") from exc


def reject_dupes(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise JaibaError("invalid-object", f"duplicate key {key}")
        obj[key] = value
    return obj


def _reject_nonfinite(_value):
    raise JaibaError("invalid-object", "non-finite number")


def parse_json_bytes(data: bytes):
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise JaibaError("invalid-object", "input is not UTF-8") from exc
    try:
        return json.loads(text, object_pairs_hook=reject_dupes, parse_constant=_reject_nonfinite)
    except JaibaError:
        raise
    except json.JSONDecodeError as exc:
        raise JaibaError("invalid-object", "input is not JSON") from exc


def emit(obj) -> None:
    sys.stdout.write(json.dumps(obj, ensure_ascii=False, separators=(",", ":"), sort_keys=True, allow_nan=False))
    sys.stdout.write("\n")


def emit_err(exc: JaibaError) -> None:
    body = {"ok": False, "error": exc.code, "detail": exc.detail}
    if exc.evidence:
        body["evidence"] = exc.evidence
    sys.stderr.write(json.dumps(body, ensure_ascii=False, separators=(",", ":"), sort_keys=True) + "\n")


def escape_field(value: str) -> str:
    return value.replace("\\", "\\\\").replace("\n", "\\n").replace("\r", "\\r")


def b64_len(n: int) -> int:
    return 4 * ((n + 2) // 3)


def wire_len(n: int) -> int:
    return len(PREFIX) + 64 + 1 + b64_len(n)


def encode_wire(raw: bytes, prefix: str = PREFIX) -> str:
    if not isinstance(raw, (bytes, bytearray)):
        raise JaibaError("invalid-object", "payload must be bytes")
    digest = sha256_hex(raw)
    payload = base64.b64encode(raw).decode("ascii")
    return prefix + digest + "." + payload


def decode_wire(line: str) -> tuple[str, bytes]:
    if not isinstance(line, str):
        raise JaibaError("invalid-object", "wire must be a string")
    if line != line.strip() or "\n" in line or "\r" in line or " " in line or "\t" in line:
        raise JaibaError("invalid-object", "whitespace in wire line")
    if "<" in line or ">" in line or "[REDACTED]" in line:
        raise JaibaError("invalid-object", "redaction marker or angle bracket in wire")
    if line.endswith("... [truncated]") or "... [truncated]" in line:
        raise JaibaError("verification-failed", "truncated wire")
    prefix = None
    for candidate in ACCEPTED_PREFIXES:
        if line.startswith(candidate):
            prefix = candidate
            break
    if prefix is None:
        raise JaibaError("unsupported-version", "wire prefix is not JAIBA4 or legacy JAIBA3")
    digest, dot, b64 = line[len(prefix):].partition(".")
    if dot != "." or not SHA_RE.fullmatch(digest) or not b64:
        raise JaibaError("invalid-object", "malformed digest or payload")
    try:
        raw = base64.b64decode(b64, validate=True)
    except Exception as exc:
        raise JaibaError("invalid-object", "invalid base64") from exc
    if base64.b64encode(raw).decode("ascii") != b64:
        raise JaibaError("invalid-object", "non-canonical base64")
    if sha256_hex(raw) != digest:
        raise JaibaError("verification-failed", "sha256 mismatch")
    return prefix, raw


def extract_wire(text: str) -> str:
    if "... [truncated]" in text:
        raise JaibaError("verification-failed", "truncated read")
    lines = text.splitlines()
    foreign = [ln for ln in lines if ln.startswith("JAIBA") and not ln.startswith(ACCEPTED_PREFIXES)]
    if foreign:
        raise JaibaError("unsupported-version", "wire prefix is not JAIBA4 or legacy JAIBA3")
    wires = [ln for ln in lines if ln.startswith(ACCEPTED_PREFIXES)]
    if len(wires) != 1:
        raise JaibaError("invalid-object", "expected exactly one JAIBA4 or JAIBA3 wire line")
    return wires[0]


def label_value(text: str, label: str) -> str | None:
    hits = [ln for ln in text.splitlines() if ln.startswith(label + ":")]
    if not hits:
        return None
    if len(hits) != 1:
        raise JaibaError("invalid-object", f"expected exactly one {label} line")
    return hits[0].split(":", 1)[1].strip()


def normalize_address(raw) -> dict:
    if not isinstance(raw, dict):
        raise JaibaError("invalid-object", "address must be an object")
    found = {}
    for key, value in raw.items():
        if key not in ADDRESS_ALIASES:
            raise JaibaError("invalid-object", f"unknown address field {key}")
        canon = ADDRESS_ALIASES[key]
        if canon in found:
            raise JaibaError("invalid-object", f"duplicate address field {canon}")
        if not isinstance(value, str) or value == "":
            raise JaibaError("invalid-object", f"address field {canon} must be a non-empty string")
        found[canon] = value
    for req in ("namespace", "project-id", "category", "logical-id"):
        if req not in found:
            raise JaibaError("invalid-object", f"address missing {req}")
    if found["category"] not in ("constitutive", "executive"):
        raise JaibaError("invalid-object", "category must be constitutive or executive")
    if found["category"] == "executive" and "context-id" not in found:
        raise JaibaError("invalid-object", "executive address requires context-id")
    if found["category"] == "constitutive" and "context-id" in found:
        raise JaibaError("invalid-object", "constitutive address must not include context-id")
    ordered = {
        "namespace": found["namespace"],
        "project-id": found["project-id"],
        "category": found["category"],
    }
    if "context-id" in found:
        ordered["context-id"] = found["context-id"]
    ordered["logical-id"] = found["logical-id"]
    return ordered


def address_canonical_text(address) -> str:
    norm = normalize_address(address)
    lines = [
        f"namespace {escape_field(norm['namespace'])}",
        f"project-id {escape_field(norm['project-id'])}",
        f"category {escape_field(norm['category'])}",
        f"context-id {escape_field(norm.get('context-id', ''))}",
        f"logical-id {escape_field(norm['logical-id'])}",
    ]
    return "\n".join(lines) + "\n"


def address_slot_key(address) -> str:
    norm = normalize_address(address)
    return " ".join([
        "namespace=" + escape_field(norm["namespace"]),
        "project-id=" + escape_field(norm["project-id"]),
        "category=" + escape_field(norm["category"]),
        "context-id=" + escape_field(norm.get("context-id", "")),
        "logical-id=" + escape_field(norm["logical-id"]),
    ])


def context_canonical_text(namespace: str, project_id: str, context_id: str) -> str:
    return (
        f"namespace {escape_field(namespace)}\n"
        f"project-id {escape_field(project_id)}\n"
        f"context-id {escape_field(context_id)}\n"
    )


def check_ns16(ns16: str) -> str:
    if not isinstance(ns16, str) or not NS16_RE.fullmatch(ns16):
        raise JaibaError("invalid-object", "ns16 must be 16 lowercase hex digits")
    return ns16


def _fit_key(key: str) -> str:
    if len(key) > TOPIC_MAX:
        raise JaibaError("limit-exceeded", "topic_key longer than 60")
    return key


def topic_key(kind: str, ns16: str, ident) -> str:
    ns16 = check_ns16(ns16)
    if kind == "cat":
        if not isinstance(ident, str) or ident == "":
            raise JaibaError("invalid-object", "catalog topic requires project-id")
        digest = sha256_hex(ident.encode("utf-8"))
        return _fit_key(f"jaiba/v4/{ns16}/cat/{digest[:24]}")
    if kind == "obj":
        digest = sha256_hex(address_canonical_text(ident).encode("utf-8"))
        return _fit_key(f"jaiba/v4/{ns16}/obj/{digest[:24]}")
    if kind == "chk":
        ver, idx = ident
        if not isinstance(ver, str) or not SHA_RE.fullmatch(ver):
            raise JaibaError("invalid-object", "chunk topic requires a snapshot digest")
        if isinstance(idx, bool) or not isinstance(idx, int) or idx < 0 or idx > 9999:
            raise JaibaError("limit-exceeded", "chunk index does not fit in 4 digits")
        return _fit_key(f"jaiba/v4/{ns16}/chk/{ver[:20]}/{idx:04d}")
    if kind == "ctx":
        namespace, project_id, context_id = ident
        digest = sha256_hex(context_canonical_text(namespace, project_id, context_id).encode("utf-8"))
        return _fit_key(f"jaiba/v4/{ns16}/ctx/{digest[:24]}")
    if kind == "base":
        digest = sha256_hex(address_canonical_text(ident).encode("utf-8"))
        return _fit_key(f"jaiba/v4/{ns16}/base/{digest[:22]}")
    if kind == "del":
        address, seq = ident
        if isinstance(seq, bool) or not isinstance(seq, int) or seq < 1 or seq > 9999:
            raise JaibaError("limit-exceeded", "delta seq does not fit in 4 digits")
        digest = sha256_hex(address_canonical_text(address).encode("utf-8"))
        return _fit_key(f"jaiba/v4/{ns16}/del/{digest[:18]}/{seq:04d}")
    raise JaibaError("invalid-object", f"unknown topic kind {kind}")


def logical_projection(obj: dict) -> dict:
    if not isinstance(obj, dict):
        raise JaibaError("invalid-object", "logical object must be an object")
    if "type" not in obj or not isinstance(obj["type"], str) or obj["type"] == "":
        raise JaibaError("invalid-object", "type must be a non-empty string")
    if "content" not in obj or not isinstance(obj["content"], str):
        raise JaibaError("invalid-object", "content must be a string")
    metadata = obj.get("metadata", {})
    relations = obj.get("relations", [])
    if not isinstance(metadata, dict):
        raise JaibaError("invalid-object", "metadata must be an object")
    if not isinstance(relations, list):
        raise JaibaError("invalid-object", "relations must be a list")
    return {
        "address": normalize_address(obj["address"]),
        "content": obj["content"],
        "metadata": metadata,
        "relations": relations,
        "type": obj["type"],
    }


def fingerprint(obj: dict) -> str:
    return sha256_hex(canonical_json_bytes(logical_projection(obj)))


def parse_seq(value, *, allow_zero: bool) -> int:
    if isinstance(value, bool):
        raise JaibaError("invalid-object", "seq is not an integer")
    if isinstance(value, int):
        number = value
    elif isinstance(value, str) and re.fullmatch(r"[+-]?\d+", value):
        number = int(value, 10)
    else:
        raise JaibaError("invalid-object", "seq is not an integer")
    if number < 0 or (number == 0 and not allow_zero):
        raise JaibaError("invalid-object", "seq out of range")
    return number


def parse_head(raw) -> tuple[int, str]:
    if not isinstance(raw, dict):
        raise JaibaError("invalid-object", "expected-head must be an object")
    allowed = {"seq", "chain_digest", "chain-digest"}
    if set(raw) - allowed:
        raise JaibaError("invalid-object", "unexpected expected-head field")
    if "seq" not in raw:
        raise JaibaError("invalid-object", "expected-head missing seq")
    if "chain_digest" in raw and "chain-digest" in raw:
        raise JaibaError("invalid-object", "duplicate chain-digest field")
    digest = raw.get("chain_digest", raw.get("chain-digest"))
    if not isinstance(digest, str) or not SHA_RE.fullmatch(digest):
        raise JaibaError("invalid-object", "chain-digest must be 64 lowercase hex")
    return parse_seq(raw["seq"], allow_zero=True), digest


def delta_canonical(address, seq: int, request_id: str, ops: list) -> str:
    norm = normalize_address(address)
    if norm["category"] != "executive":
        raise JaibaError("invalid-object", "delta address must be executive")
    lines = [
        "jaiba-journal-delta/1",
        f"namespace {escape_field(norm['namespace'])}",
        f"project-id {escape_field(norm['project-id'])}",
        "category executive",
        f"context-id {escape_field(norm['context-id'])}",
        f"logical-id {escape_field(norm['logical-id'])}",
        f"seq {seq}",
        f"request-id {escape_field(request_id)}",
        f"op-count {len(ops)}",
    ]
    for op in ops:
        lines.append(f"op {op['op']}")
        fields = [(k, op[k]) for k in op if k != "op"]
        for key, value in sorted(fields, key=lambda item: item[0].encode("utf-8")):
            rendered = render_field(value)
            lines.append(f"{key} {escape_field(rendered)}")
        lines.append("end")
    return "\n".join(lines) + "\n"


def render_field(value) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, bool) or value is None or isinstance(value, int):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"), allow_nan=False)
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True, allow_nan=False)


def chain_input(base_revision: str, deltas: list) -> str:
    if not SHA_RE.fullmatch(base_revision):
        raise JaibaError("invalid-object", "base-revision must be 64 lowercase hex")
    text = f"jaiba-journal-chain/1\nbase {base_revision}\n"
    for delta in deltas:
        text += delta_canonical(delta["address"], delta["seq"], delta["request_id"], delta["ops"])
    return text


def chain_digest(base_revision: str, deltas: list) -> str:
    return sha256_hex(chain_input(base_revision, deltas).encode("utf-8"))


def detect_nl(text: str) -> str | None:
    bare_r = False
    bare_n = False
    crlf = False
    i = 0
    while i < len(text):
        ch = text[i]
        if ch == "\r":
            if i + 1 < len(text) and text[i + 1] == "\n":
                crlf = True
                i += 2
                continue
            bare_r = True
            i += 1
            continue
        if ch == "\n":
            bare_n = True
        i += 1
    if bare_r or (crlf and bare_n):
        return None
    if crlf:
        return "\r\n"
    return "\n"


def require_nl(text: str, *inserts: str) -> str:
    style = detect_nl(text)
    if style is None:
        raise JaibaError("invalid-object", "mixed newlines")
    for ins in inserts:
        if not ins:
            continue
        if "\r" in ins or "\n" in ins:
            ins_style = detect_nl(ins)
            if ins_style is None or ins_style != style:
                raise JaibaError("invalid-object", "splice newline does not match the document")
    return style


def iter_lines(text: str):
    i = 0
    n = len(text)
    while i < n:
        j = text.find("\n", i)
        if j < 0:
            yield i, n, text[i:], ""
            return
        end = j + 1
        content = text[i:j]
        nl = "\n"
        if content.endswith("\r"):
            content = content[:-1]
            nl = "\r\n"
        yield i, end, content, nl
        i = end


def parse_heading(content: str):
    match = HEADING_RE.match(content)
    if not match:
        return None
    title = re.sub(r"[ \t]+#+\s*$", "", match.group(2).strip()).strip()
    if title == "":
        return None
    return len(match.group(1)), title


def heading_spans(text: str) -> list:
    spans = []
    for start, end, content, _nl in iter_lines(text):
        parsed = parse_heading(content)
        if parsed:
            level, title = parsed
            spans.append({"start": start, "line_end": end, "level": level, "title": title})
    return spans


def section_bounds(text: str, title: str):
    spans = heading_spans(text)
    matches = [span for span in spans if span["title"] == title]
    if not matches:
        raise JaibaError("invalid-object", "section not found")
    if len(matches) > 1:
        raise JaibaError("ambiguous", "heading is not unique")
    head = matches[0]
    body_end = len(text)
    for span in spans:
        if span["start"] > head["start"] and span["level"] <= head["level"]:
            body_end = span["start"]
            break
    return head, head["line_end"], body_end


def ensure_following_break(piece: str, follows: bool, nl: str) -> str:
    if follows and piece and not piece.endswith("\n"):
        return piece + nl
    return piece


def prepend_break_if_needed(text: str, at: int, piece: str, nl: str) -> str:
    if at > 0 and text[at - 1] != "\n":
        return nl + piece
    return piece


def replace_section(text: str, title: str, content: str) -> str:
    nl = require_nl(text, content)
    _head, body_start, body_end = section_bounds(text, title)
    piece = content
    if body_start > 0 and text[body_start - 1] != "\n":
        piece = nl + piece
    piece = ensure_following_break(piece, body_end < len(text), nl)
    return text[:body_start] + piece + text[body_end:]


def remove_section(text: str, title: str) -> str:
    head, _body_start, body_end = section_bounds(text, title)
    if head["level"] == 1 and sum(1 for span in heading_spans(text) if span["level"] == 1) == 1:
        raise JaibaError("invalid-object", "cannot remove the document's single H1 title")
    return text[:head["start"]] + text[body_end:]


def append_to_section(text: str, title: str, content: str) -> str:
    if content == "":
        raise JaibaError("invalid-object", "empty content")
    nl = require_nl(text, content)
    _head, _body_start, body_end = section_bounds(text, title)
    piece = prepend_break_if_needed(text, body_end, content, nl)
    piece = ensure_following_break(piece, body_end < len(text), nl)
    return text[:body_end] + piece + text[body_end:]


def append_section(text: str, after: str, heading: str, content: str) -> str:
    if heading == "":
        raise JaibaError("invalid-object", "empty heading")
    nl = require_nl(text, content)
    head, _body_start, body_end = section_bounds(text, after)
    if any(span["title"] == heading for span in heading_spans(text)):
        raise JaibaError("ambiguous", "heading already exists")
    block = f"{'#' * head['level']} {heading}{nl}"
    if content:
        block += content
    block = prepend_break_if_needed(text, body_end, block, nl)
    block = ensure_following_break(block, body_end < len(text), nl)
    return text[:body_end] + block + text[body_end:]


def append_entry(text: str, content: str) -> str:
    if content == "":
        raise JaibaError("invalid-object", "empty content")
    nl = require_nl(text, content)
    piece = content
    if text and not text.endswith("\n"):
        piece = nl + piece
    return text + piece


def frontmatter_region(text: str):
    if not text.startswith("---"):
        return None
    rows = list(iter_lines(text))
    if not rows:
        return None
    if rows[0][2].rstrip(" \t") != "---":
        return None
    for start, end, content, _nl in rows[1:]:
        if content.rstrip(" \t") == "---":
            return {"start": 0, "end": end, "close_start": start, "body_start": rows[0][1]}
    return None


def frontmatter_entries(text: str):
    region = frontmatter_region(text)
    if region is None:
        return None
    rows = []
    for start, end, content, nl in iter_lines(text[region["body_start"]:region["close_start"]]):
        abs_start = region["body_start"] + start
        abs_end = region["body_start"] + end
        match = FM_KEY_RE.match(content)
        rows.append({
            "start": abs_start,
            "end": abs_end,
            "content": content,
            "nl": nl if nl else "\n",
            "key": match.group(1) if match else None,
            "raw_value": match.group(2) if match else None,
        })
    return region, rows


def key_is_multiline(rows, index: int) -> bool:
    if index + 1 >= len(rows):
        return False
    nxt = rows[index + 1]["content"]
    return nxt.startswith(" ") or nxt.startswith("\t")


def parse_scalar(raw: str) -> str:
    s = raw.strip()
    if s == "":
        return ""
    if s[0] == '"':
        out = []
        i = 1
        while i < len(s):
            ch = s[i]
            if ch == "\\":
                if i + 1 >= len(s):
                    raise JaibaError("invalid-object", "unclosed quoted scalar")
                nxt = s[i + 1]
                mapping = {"n": "\n", "r": "\r", "t": "\t", "\\": "\\", '"': '"'}
                out.append(mapping.get(nxt, nxt))
                i += 2
                continue
            if ch == '"':
                return "".join(out)
            out.append(ch)
            i += 1
        raise JaibaError("invalid-object", "unclosed quoted scalar")
    if s[0] == "'":
        body = s[1:]
        if body.endswith("'"):
            body = body[:-1]
        else:
            raise JaibaError("invalid-object", "unclosed quoted scalar")
        return body.replace("''", "'")
    if " #" in s:
        s = s.split(" #", 1)[0].rstrip()
    return s


def yaml_scalar(value: str) -> str:
    if "\n" in value or "\r" in value:
        raise JaibaError("invalid-object", "value is not a single YAML line")
    if value == "" or value != value.strip() or re.search(r"[:#\"'\\]", value) or value[0] in "-?:,[]{}#&*!|>'\"%@`":
        escaped = value.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    if " " in value or "\t" in value:
        escaped = value.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    return value


def single_line_keys(text: str) -> dict | None:
    found = frontmatter_entries(text)
    if found is None:
        return None
    _region, rows = found
    out = {}
    for index, row in enumerate(rows):
        if not row["key"]:
            continue
        if key_is_multiline(rows, index):
            if row["key"] in out:
                raise JaibaError("invalid-object", "frontmatter key is not a single line")
            out[row["key"]] = None
            continue
        if row["key"] in out:
            raise JaibaError("ambiguous", "frontmatter key is not unique")
        out[row["key"]] = parse_scalar(row["raw_value"])
    return out


def classified_status(text: str):
    keys = single_line_keys(text)
    if keys is None or "status" not in keys:
        return UNCLASSIFIED, None
    value = keys["status"]
    if value is None:
        return UNCLASSIFIED, None
    if value == "draft":
        return DRAFT, "draft"
    return FROZEN, value


def splice_frontmatter_key(text: str, key: str, written: str) -> str:
    found = frontmatter_entries(text)
    if found is None:
        raise JaibaError("invalid-object", "frontmatter is missing or unclosed")
    region, rows = found
    nl = detect_nl(text) or "\n"
    matches = [(i, row) for i, row in enumerate(rows) if row["key"] == key]
    if len(matches) > 1:
        raise JaibaError("ambiguous", "frontmatter key is not unique")
    if matches:
        index, row = matches[0]
        if key_is_multiline(rows, index):
            raise JaibaError("invalid-object", "existing frontmatter value is multi-line")
        line_nl = row["nl"] or nl
        return text[:row["start"]] + f"{key}: {written}" + line_nl + text[row["end"]:]
    insert = f"{key}: {written}{nl}"
    return text[:region["close_start"]] + insert + text[region["close_start"]:]


def assert_projection_agrees(text: str, metadata: dict, obj_type: str) -> None:
    keys = single_line_keys(text)
    if keys is None:
        return
    for key, scalar in keys.items():
        if key not in metadata:
            continue
        if scalar is None or metadata[key] != scalar:
            raise JaibaError("invalid-object", "frontmatter and metadata do not agree")
    if keys.get("type") not in (None, obj_type):
        raise JaibaError("invalid-object", "frontmatter type does not match the object type")


def task_rows(text: str):
    rows = list(iter_lines(text))
    tasks = []
    for index, (start, end, content, nl) in enumerate(rows):
        if content.startswith("- [") and not TASK_LINE_RE.match(content):
            raise JaibaError("invalid-object", "non-canonical checkbox")
        match = TASK_LINE_RE.match(content)
        if match:
            tasks.append({
                "index": index,
                "start": start,
                "line_end": end,
                "id": match.group(2),
                "mark": match.group(1),
                "nl": nl,
            })
    by_id = {}
    for task in tasks:
        by_id.setdefault(task["id"], []).append(task)
    for tid, group in by_id.items():
        if len(group) > 1:
            raise JaibaError("ambiguous", f"task {tid} is not unique")
    return tasks, by_id


def block_end(text: str, start: int, tasks, headings) -> int:
    candidates = [len(text)]
    for task in tasks:
        if task["start"] > start:
            candidates.append(task["start"])
            break
    for heading in headings:
        if heading["start"] > start:
            candidates.append(heading["start"])
            break
    return min(candidates)


def checkbox_in_block(block: str):
    hits = []
    for _s, _e, content, _nl in iter_lines(block):
        if content.startswith("- [") and not TASK_LINE_RE.match(content):
            raise JaibaError("invalid-object", "non-canonical checkbox in block")
        match = TASK_LINE_RE.match(content)
        if match:
            hits.append(match.group(2))
    if len(hits) != 1:
        raise JaibaError("invalid-object", "block must contain exactly one task checkbox")
    return hits[0]


def apply_check(text: str, ids, checked: bool) -> str:
    if not isinstance(ids, list) or not ids:
        raise JaibaError("invalid-object", "ids must be a non-empty list")
    _tasks, by_id = task_rows(text)
    new = text
    mark = "x" if checked else " "
    for tid in ids:
        if not isinstance(tid, str) or not TASK_ID_RE.fullmatch(tid):
            raise JaibaError("invalid-object", "token is not a task id")
        group = by_id.get(tid)
        if not group:
            raise JaibaError("invalid-object", "task id has no checkbox line")
        at = group[0]["start"] + 3
        if new[at] not in " xX":
            raise JaibaError("invalid-object", "checkbox mark drifted")
        new = new[:at] + mark + new[at + 1:]
    return new


def apply_add_task(text: str, after: str, block: str) -> str:
    if not isinstance(after, str) or after == "" or not isinstance(block, str):
        raise JaibaError("invalid-object", "add-task parameters must be strings")
    nl = require_nl(text, block)
    new_id = checkbox_in_block(block)
    tasks, by_id = task_rows(text)
    if new_id in by_id:
        raise JaibaError("conflict", "task id is already present")
    headings = heading_spans(text)
    if TASK_ID_RE.fullmatch(after):
        group = by_id.get(after)
        if not group:
            raise JaibaError("invalid-object", "anchor task not found")
        insert_at = block_end(text, group[0]["start"], tasks, headings)
    else:
        _head, _body_start, insert_at = section_bounds(text, after)
    piece = block
    piece = prepend_break_if_needed(text, insert_at, piece, nl)
    piece = ensure_following_break(piece, insert_at < len(text), nl)
    return text[:insert_at] + piece + text[insert_at:]


def apply_amend_task(text: str, tid: str, block: str) -> str:
    if not isinstance(tid, str) or not TASK_ID_RE.fullmatch(tid) or not isinstance(block, str):
        raise JaibaError("invalid-object", "amend-task parameters are malformed")
    nl = require_nl(text, block)
    block_id = checkbox_in_block(block)
    if block_id != tid:
        raise JaibaError("invalid-object", "amend-task block id does not match id")
    tasks, by_id = task_rows(text)
    group = by_id.get(tid)
    if not group:
        raise JaibaError("invalid-object", "task id has no checkbox line")
    headings = heading_spans(text)
    start = group[0]["start"]
    end = block_end(text, start, tasks, headings)
    piece = ensure_following_break(block, end < len(text), nl)
    return text[:start] + piece + text[end:]


def find_yaml_fences(text: str):
    fences = []
    open_start = None
    open_body = None
    for start, end, content, _nl in iter_lines(text):
        if open_start is None:
            if FENCE_OPEN_RE.match(content):
                open_start = start
                open_body = end
            continue
        if FENCE_CLOSE_RE.match(content):
            fences.append({
                "start": open_start,
                "end": end,
                "body_start": open_body,
                "body_end": start,
            })
            open_start = None
    if open_start is not None:
        raise JaibaError("invalid-object", "criteria fence is unclosed")
    return fences


def unique_fence(text: str):
    fences = find_yaml_fences(text)
    if not fences:
        raise JaibaError("invalid-object", "criteria block not found")
    if len(fences) > 1:
        raise JaibaError("ambiguous", "criteria block is not unique")
    return fences[0]


def fence_blob(text: str):
    try:
        fences = find_yaml_fences(text)
    except JaibaError:
        return "unreadable"
    if not fences:
        return None
    if len(fences) > 1:
        return "unreadable"
    fence = fences[0]
    return text[fence["start"]:fence["end"]]


def parse_items(text: str, fence: dict):
    body = text[fence["body_start"]:fence["body_end"]]
    criteria = []
    items = []
    rows = list(iter_lines(body))
    for start, end, content, _nl in rows:
        if re.match(r"^[ \t]*- id:[ \t]*$", content) or (content.strip().startswith("- id:") and not ITEM_RE.match(content)):
            raise JaibaError("invalid-object", "criteria block is outside the subset")
        if re.match(r"^[ \t]*- \{", content) or re.match(r"^[ \t]*\{", content):
            raise JaibaError("invalid-object", "criteria block is outside the subset")
        cmatch = CRITERIA_RE.match(content)
        if cmatch:
            criteria.append(cmatch.group(1))
        imatch = ITEM_RE.match(content)
        if imatch:
            items.append({
                "rel": start,
                "abs": fence["body_start"] + start,
                "id": imatch.group(2),
                "indent": imatch.group(1),
                "line_end": fence["body_start"] + end,
            })
    if len(criteria) != 1:
        raise JaibaError("invalid-object", "criteria block is outside the subset")
    if any("\t" in item["indent"] for item in items):
        raise JaibaError("invalid-object", "criteria indentation is not spaces")
    indents = {item["indent"] for item in items}
    if len(indents) > 1:
        raise JaibaError("invalid-object", "criteria items do not share one indentation")
    ids = [item["id"] for item in items]
    if len(ids) != len(set(ids)):
        raise JaibaError("ambiguous", "criterion id is not unique")
    for index, item in enumerate(items):
        nxt = items[index + 1]["abs"] if index + 1 < len(items) else fence["body_end"]
        item["end"] = nxt
    indent = items[0]["indent"] if items else criteria[0] + "  "
    return items, indent


def shift_item(yaml: str, target_indent: str, nl: str):
    if not isinstance(yaml, str) or yaml == "":
        raise JaibaError("invalid-object", "yaml must be a non-empty string")
    if "\t" in target_indent:
        raise JaibaError("invalid-object", "criteria indentation is not spaces")
    if "\n" in yaml or "\r" in yaml:
        style = detect_nl(yaml)
        if style is None or style != nl:
            raise JaibaError("invalid-object", "splice newline does not match the document")
    if yaml.endswith("\r\n"):
        lines = yaml[:-2].split("\r\n")
    elif yaml.endswith("\n"):
        lines = yaml[:-1].split("\n")
    elif "\r\n" in yaml:
        lines = yaml.split("\r\n")
    elif "\n" in yaml:
        lines = yaml.split("\n")
    else:
        lines = [yaml]
    if not lines or lines == [""]:
        raise JaibaError("invalid-object", "yaml must contain one criterion")
    first = lines[0]
    if re.match(r"^[ \t]*id:", first) and not re.match(r"^[ \t]*- id:", first):
        match = re.match(r"^([ \t]*)id:", first)
        lines[0] = match.group(1) + "- id:" + first[match.end():]
        first = lines[0]
    match = re.match(r"^([ \t]*)- id: (\S+)[ \t]*$", first)
    if not match:
        raise JaibaError("invalid-object", "yaml does not start with one criterion id")
    if "\t" in match.group(1):
        raise JaibaError("invalid-object", "criteria indentation is not spaces")
    extra = [line for line in lines[1:] if ITEM_RE.match(line)]
    if extra:
        raise JaibaError("invalid-object", "yaml must contain exactly one criterion")
    delta = len(target_indent) - len(match.group(1))
    shifted = []
    for line in lines:
        if line == "":
            shifted.append(line)
            continue
        if delta < 0:
            drop = -delta
            if line[:drop] != " " * drop:
                raise JaibaError("invalid-object", "cannot shift criterion indentation")
            line = line[drop:]
        elif delta > 0:
            line = (" " * delta) + line
        shifted.append(line)
    piece = nl.join(shifted)
    if not piece.endswith("\n"):
        piece += nl
    return match.group(2), piece


def item_status_indent(text: str, item: dict) -> str:
    for _s, _e, content, _nl in iter_lines(text[item["abs"]:item["end"]]):
        if ITEM_RE.match(content):
            continue
        match = re.match(r"^([ \t]+)[^ \t].*:", content)
        if match and "status" != content.strip().split(":", 1)[0]:
            return match.group(1)
        if re.match(r"^([ \t]*)status:", content):
            continue
        key = re.match(r"^([ \t]*)([^:\s]+):", content)
        if key and key.group(2) != "status" and not content.lstrip().startswith("- id:"):
            return key.group(1) if key.group(1) else item["indent"] + "  "
    return item["indent"] + "  "


def apply_add_criterion(text: str, yaml: str) -> str:
    nl = require_nl(text, yaml)
    fence = unique_fence(text)
    items, indent = parse_items(text, fence)
    item_id, piece = shift_item(yaml, indent, nl)
    if any(item["id"] == item_id for item in items):
        raise JaibaError("conflict", "criterion id is already present")
    at = items[-1]["end"] if items else fence["body_end"]
    if at > 0 and text[at - 1] != "\n":
        piece = nl + piece
    if not piece.endswith("\n"):
        piece += nl
    return text[:at] + piece + text[at:]


def apply_update_criterion(text: str, tid: str, yaml: str) -> str:
    nl = require_nl(text, yaml)
    fence = unique_fence(text)
    items, indent = parse_items(text, fence)
    item_id, piece = shift_item(yaml, indent, nl)
    if item_id != tid:
        raise JaibaError("invalid-object", "update-criterion cannot change id")
    match = next((item for item in items if item["id"] == tid), None)
    if match is None:
        raise JaibaError("invalid-object", "criterion id not found")
    if not piece.endswith("\n"):
        piece += nl
    return text[:match["abs"]] + piece + text[match["end"]:]


def apply_remove_criterion(text: str, tid: str) -> str:
    fence = unique_fence(text)
    items, _indent = parse_items(text, fence)
    match = next((item for item in items if item["id"] == tid), None)
    if match is None:
        raise JaibaError("invalid-object", "criterion id not found")
    return text[:match["abs"]] + text[match["end"]:]


def apply_set_status(text: str, tid: str, status: str) -> str:
    if not isinstance(status, str) or "\n" in status or "\r" in status or status == "":
        raise JaibaError("invalid-object", "status is not a single-line scalar")
    written = yaml_scalar(status)
    if parse_scalar(written) != status:
        raise JaibaError("invalid-object", "status cannot be spliced as one scalar")
    nl = require_nl(text)
    fence = unique_fence(text)
    items, _indent = parse_items(text, fence)
    match = next((item for item in items if item["id"] == tid), None)
    if match is None:
        raise JaibaError("invalid-object", "criterion id not found")
    status_lines = []
    for start, end, content, line_nl in iter_lines(text[match["abs"]:match["end"]]):
        sm = STATUS_RE.match(content)
        if sm and not content.lstrip().startswith("- "):
            status_lines.append((match["abs"] + start, match["abs"] + end, sm.group(1), line_nl or nl))
    if len(status_lines) > 1:
        raise JaibaError("invalid-object", "criterion status is not a single line")
    if status_lines:
        start, end, indent, line_nl = status_lines[0]
        return text[:start] + f"{indent}status: {written}" + line_nl + text[end:]
    indent = item_status_indent(text, match)
    insert = f"{indent}status: {written}{nl}"
    at = match["end"]
    if at > 0 and text[at - 1] != "\n":
        insert = nl + insert
    return text[:at] + insert + text[at:]


def guard_frozen_fence(before, after_text: str, mode: str) -> None:
    if mode == DRAFT:
        return
    if before is None:
        return
    if before == "unreadable":
        raise JaibaError("invalid-object", "criteria fence cannot be compared")
    after = fence_blob(after_text)
    if after == "unreadable":
        raise JaibaError("invalid-object", "criteria fence cannot be compared")
    if before != after:
        raise JaibaError("conflict", "frozen criteria fence would change")


def normalize_op(op, obj_type: str) -> dict:
    if not isinstance(op, dict) or "op" not in op or not isinstance(op["op"], str):
        raise JaibaError("invalid-object", "op must name a closed operation")
    name = op["op"]
    if name not in PARAMS:
        raise JaibaError("invalid-object", f"unknown op {name}")
    if obj_type not in LEGAL or name not in LEGAL[obj_type]:
        raise JaibaError("invalid-object", f"op {name} is not legal for {obj_type}")
    fields = {k: v for k, v in op.items() if k != "op"}
    if set(fields) != PARAMS[name]:
        raise JaibaError("invalid-object", f"op {name} parameters do not match the closed set")
    if name in {"check", "uncheck"}:
        ids = fields["ids"]
        if not isinstance(ids, list) or not ids or not all(isinstance(i, str) for i in ids):
            raise JaibaError("invalid-object", "ids must be a non-empty list of task ids")
    for key, value in fields.items():
        if key == "ids":
            continue
        if not isinstance(value, str):
            raise JaibaError("invalid-object", f"{key} must be a string")
    if name == "set-frontmatter":
        if fields["key"] == "type":
            raise JaibaError("invalid-object", "type cannot be changed")
        if not KEY_RE.fullmatch(fields["key"]):
            raise JaibaError("invalid-object", "frontmatter key is not a single top-level name")
        if "\n" in fields["value"] or "\r" in fields["value"]:
            raise JaibaError("invalid-object", "value is not a single YAML line")
    return {"op": name, **fields}


def ops_fingerprint(address, ops: list) -> str:
    payload = {"address": normalize_address(address), "ops": ops}
    return sha256_hex(canonical_json_bytes(payload))


def apply_ops(text: str, metadata: dict, obj_type: str, ops: list):
    mode, pre_scalar = classified_status(text)
    keys = single_line_keys(text)
    if keys and keys.get("type") not in (None, obj_type):
        raise JaibaError("invalid-object", "frontmatter type does not match the object type")
    meta = copy.deepcopy(metadata)
    current = text
    for index, op in enumerate(ops):
        try:
            current, meta, mode = apply_one(current, meta, obj_type, op, mode, pre_scalar)
        except JaibaError as exc:
            exc.evidence = {**exc.evidence, "op_index": index, "op": op.get("op")}
            raise
    assert_projection_agrees(current, meta, obj_type)
    return current, meta


def apply_one(text, metadata, obj_type, op, mode, pre_scalar):
    name = op["op"]
    if name == "check":
        return apply_check(text, op["ids"], True), metadata, mode
    if name == "uncheck":
        return apply_check(text, op["ids"], False), metadata, mode
    if name == "add-task":
        return apply_add_task(text, op["after"], op["block"]), metadata, mode
    if name == "amend-task":
        return apply_amend_task(text, op["id"], op["block"]), metadata, mode
    if name == "append-entry":
        return append_entry(text, op["content"]), metadata, mode
    if name == "set-frontmatter":
        value = op["value"]
        written = yaml_scalar(value)
        if parse_scalar(written) != value:
            raise JaibaError("invalid-object", "value cannot be represented as one YAML line")
        if op["key"] == "status" and value == "draft" and pre_scalar not in (None, "draft"):
            raise JaibaError("conflict", "cannot set status back to draft")
        new_text = splice_frontmatter_key(text, op["key"], written)
        new_meta = copy.deepcopy(metadata)
        new_meta[op["key"]] = value
        new_mode = FROZEN if op["key"] == "status" and value != "draft" else mode
        return new_text, new_meta, new_mode
    before = fence_blob(text) if obj_type == "prd" else None
    if name == "replace-section":
        new_text = replace_section(text, op["heading"], op["content"])
    elif name == "append-section":
        new_text = append_section(text, op["after"], op["heading"], op["content"])
    elif name == "append-to-section":
        new_text = append_to_section(text, op["heading"], op["content"])
    elif name == "remove-section":
        new_text = remove_section(text, op["heading"])
    elif name == "add-criterion":
        new_text = apply_add_criterion(text, op["yaml"])
    elif name == "update-criterion":
        present = criterion_present(text, op["id"])
        guard_destructive(mode, present)
        new_text = apply_update_criterion(text, op["id"], op["yaml"])
    elif name == "remove-criterion":
        present = criterion_present(text, op["id"])
        guard_destructive(mode, present)
        new_text = apply_remove_criterion(text, op["id"])
    elif name == "set-criterion-status":
        new_text = apply_set_status(text, op["id"], op["status"])
    else:
        raise JaibaError("invalid-object", f"unknown op {name}")
    if obj_type == "prd" and name in PLAN_OPS:
        guard_frozen_fence(before, new_text, mode)
    return new_text, metadata, mode


def criterion_present(text: str, tid: str) -> bool:
    try:
        fence = unique_fence(text)
        items, _indent = parse_items(text, fence)
    except JaibaError:
        return False
    return any(item["id"] == tid for item in items)


def guard_destructive(mode: str, present: bool) -> None:
    if mode == DRAFT:
        return
    if mode == UNCLASSIFIED:
        raise JaibaError("invalid-object", "document status is not a draft scalar")
    if present:
        raise JaibaError("conflict", "criterion id is permanent")
    raise JaibaError("invalid-object", "criterion id not found")


def as_base(raw: dict) -> dict:
    if not isinstance(raw, dict):
        raise JaibaError("invalid-object", "base must be an object")
    kind = raw.get("kind")
    if kind not in (None, "object", "exec-base"):
        raise JaibaError("invalid-object", "base kind is not an executive object")
    proj = logical_projection(raw)
    if proj["address"]["category"] != "executive":
        raise JaibaError("invalid-object", "patch applies only to executive objects")
    if proj["type"] not in EXECUTIVE_TYPES:
        raise JaibaError("invalid-object", "type is not an executive artifact")
    base_rev = fingerprint({"address": proj["address"], "type": proj["type"], "content": proj["content"], "metadata": proj["metadata"], "relations": proj["relations"]})
    if "base_revision" in raw and raw["base_revision"] != base_rev:
        raise JaibaError("invalid-object", "base_revision does not match the base object")
    return {
        "kind": "exec-base",
        "address": proj["address"],
        "type": proj["type"],
        "content": proj["content"],
        "metadata": proj["metadata"],
        "relations": proj["relations"],
        "revision": base_rev,
        "base_revision": base_rev,
    }


def normalize_delta(raw, expected_address=None) -> dict:
    if not isinstance(raw, dict):
        raise JaibaError("invalid-object", "delta must be an object")
    if raw.get("kind") not in (None, "exec-delta"):
        raise JaibaError("invalid-object", "delta kind must be exec-delta")
    address = normalize_address(raw.get("address"))
    if expected_address is not None and address != expected_address:
        raise JaibaError("invalid-object", "delta address does not match the base")
    if address["category"] != "executive":
        raise JaibaError("invalid-object", "delta address must be executive")
    seq = parse_seq(raw.get("seq"), allow_zero=False)
    request_id = raw.get("request_id", raw.get("request-id"))
    if not isinstance(request_id, str) or request_id == "":
        raise JaibaError("invalid-object", "request_id must be a non-empty string")
    ops = raw.get("ops")
    if not isinstance(ops, list) or not ops:
        raise JaibaError("invalid-object", "ops must be a non-empty list")
    return {"kind": "exec-delta", "address": address, "seq": seq, "request_id": request_id, "ops": ops}


def sort_deltas(deltas: list, address) -> list:
    norm = []
    seen_seq = set()
    seen_req = set()
    for raw in deltas:
        delta = normalize_delta(raw, address)
        if delta["seq"] in seen_seq:
            raise JaibaError("invalid-object", "duplicate delta sequence", {"seq": delta["seq"]})
        if delta["request_id"] in seen_req:
            raise JaibaError("invalid-object", "duplicate request_id", {"seq": delta["seq"]})
        seen_seq.add(delta["seq"])
        seen_req.add(delta["request_id"])
        norm.append(delta)
    norm.sort(key=lambda item: item["seq"])
    for index, delta in enumerate(norm, start=1):
        if delta["seq"] != index:
            raise JaibaError("invalid-object", "delta sequence gap", {"seq": delta["seq"]})
    return norm


def materialize_state(base_raw: dict, delta_raws: list) -> dict:
    base = as_base(base_raw)
    deltas = sort_deltas(delta_raws or [], base["address"])
    content = base["content"]
    metadata = copy.deepcopy(base["metadata"])
    relations = copy.deepcopy(base["relations"])
    obj_type = base["type"]
    for delta in deltas:
        try:
            ops = [normalize_op(op, obj_type) for op in delta["ops"]]
            content, metadata = apply_ops(content, metadata, obj_type, ops)
        except JaibaError as exc:
            exc.evidence = {**exc.evidence, "seq": delta["seq"]}
            raise
    obj = {
        "kind": "object",
        "address": base["address"],
        "type": obj_type,
        "content": content,
        "metadata": metadata,
        "relations": relations,
    }
    obj["revision"] = fingerprint(obj)
    head = {"seq": deltas[-1]["seq"] if deltas else 0, "chain_digest": chain_digest(base["base_revision"], deltas)}
    return {
        "object": obj,
        "head": head,
        "base_revision": base["base_revision"],
        "base": base,
        "deltas": deltas,
    }


def materialized_object(state: dict) -> dict:
    return state["object"]


def upsert_slot(head_record, slot: dict) -> dict:
    if head_record is None:
        address = slot["address"]
        record = {
            "kind": "context-head",
            "namespace": address["namespace"],
            "project-id": address["project-id"],
            "context-id": address["context-id"],
            "slots": {},
        }
    else:
        if not isinstance(head_record, dict) or head_record.get("kind") != "context-head":
            raise JaibaError("invalid-object", "context-head is malformed")
        record = copy.deepcopy(head_record)
        record.setdefault("slots", {})
        if not isinstance(record["slots"], dict):
            raise JaibaError("invalid-object", "context-head slots must be an object")
    key = address_slot_key(slot["address"])
    record["slots"][key] = {
        "address": slot["address"],
        "type": slot["type"],
        "seq": slot["seq"],
        "chain_digest": slot["chain_digest"],
        "revision": slot["revision"],
    }
    return record


def build_delta(doc: dict) -> dict:
    if not isinstance(doc, dict):
        raise JaibaError("invalid-object", "delta input must be an object")
    if doc.get("archetype", "record-store") != "record-store":
        raise JaibaError("missing-capability", "this codec stores deltas only for record-store")
    if "base" not in doc:
        raise JaibaError("not-found", "base is absent")
    state = materialize_state(doc["base"], doc.get("deltas") or [])
    base = state["base"]
    obj_type = base["type"]
    request_id = doc.get("request_id", doc.get("request-id"))
    if not isinstance(request_id, str) or request_id == "":
        raise JaibaError("invalid-object", "request_id must be a non-empty string")
    ops_in = doc.get("ops")
    if not isinstance(ops_in, list) or not ops_in:
        raise JaibaError("invalid-object", "ops must be a non-empty list")
    ops = [normalize_op(op, obj_type) for op in ops_in]
    payload = ops_fingerprint(base["address"], ops)
    for existing in state["deltas"]:
        if existing["request_id"] != request_id:
            continue
        existing_ops = [normalize_op(op, obj_type) for op in existing["ops"]]
        if ops_fingerprint(existing["address"], existing_ops) == payload:
            slot = {
                "address": base["address"],
                "type": obj_type,
                "seq": state["head"]["seq"],
                "chain_digest": state["head"]["chain_digest"],
                "revision": state["object"]["revision"],
            }
            return {
                "idempotent": True,
                "delta": existing,
                "object": state["object"],
                "head": state["head"],
                "slot": slot,
                "base_revision": state["base_revision"],
            }
        raise JaibaError("conflict", "request_id reused with a different payload")
    if "expected_head" not in doc and "expected-head" not in doc:
        raise JaibaError("invalid-object", "expected-head is missing")
    expected = parse_head(doc.get("expected_head", doc.get("expected-head")))
    current = (state["head"]["seq"], state["head"]["chain_digest"])
    if expected != current:
        raise JaibaError("conflict", "expected-head does not match the current head")
    new_seq = state["head"]["seq"] + 1
    if "seq" in doc and parse_seq(doc["seq"], allow_zero=False) != new_seq:
        raise JaibaError("invalid-object", "delta seq does not follow the current head")
    content, metadata = apply_ops(state["object"]["content"], state["object"]["metadata"], obj_type, ops)
    delta = {
        "kind": "exec-delta",
        "address": base["address"],
        "seq": new_seq,
        "request_id": request_id,
        "ops": ops,
    }
    folded = materialize_state(state["base"], state["deltas"] + [delta])
    if folded["object"]["content"] != content or folded["object"]["metadata"] != metadata:
        raise JaibaError("invalid-object", "materialized delta does not match the applied ops")
    slot = {
        "address": base["address"],
        "type": obj_type,
        "seq": folded["head"]["seq"],
        "chain_digest": folded["head"]["chain_digest"],
        "revision": folded["object"]["revision"],
    }
    result = {
        "idempotent": False,
        "delta": delta,
        "object": folded["object"],
        "head": folded["head"],
        "slot": slot,
        "base_revision": folded["base_revision"],
    }
    if "context_head" in doc:
        result["context_head"] = upsert_slot(doc.get("context_head"), slot)
    if "ns16" in doc:
        encoded = encode_payload(canonical_json_bytes(delta), doc["ns16"], ("del", (base["address"], new_seq)))
        result["topic_key"] = encoded.get("topic_key") or encoded.get("chunked_object_topic_key")
        result["wire"] = encoded.get("wire")
        result["sha256"] = encoded.get("sha256") or encoded.get("logical_sha256")
        result["direct"] = encoded["direct"]
        if not encoded["direct"]:
            result["chunks"] = encoded["chunks"]
            result["chunked_object_wire"] = encoded["chunked_object_wire"]
    return result


def split_chunks(raw: bytes) -> list[bytes]:
    if len(raw) <= DIRECT_MAX:
        return [raw]
    return [raw[i:i + DIRECT_MAX] for i in range(0, len(raw), DIRECT_MAX)]


def encode_payload(raw: bytes, ns16: str | None = None, topic: tuple | None = None) -> dict:
    digest = sha256_hex(raw)
    if len(raw) <= DIRECT_MAX:
        wire = encode_wire(raw)
        out = {
            "ok": True,
            "protocol": PROTOCOL,
            "prefix": "JAIBA4",
            "direct": True,
            "sha256": digest,
            "raw_bytes": len(raw),
            "wire": wire,
        }
        if ns16 and topic:
            out["topic_key"] = topic_key(topic[0], ns16, topic[1])
        return out
    parts = split_chunks(raw)
    chunks = []
    for index, part in enumerate(parts):
        entry = {
            "index": index,
            "bytes": len(part),
            "sha256": sha256_hex(part),
            "wire": encode_wire(part),
        }
        if ns16:
            entry["topic_key"] = topic_key("chk", ns16, (digest, index))
        chunks.append(entry)
    manifest = {
        "kind": "chunked-object",
        "logical_sha256": digest,
        "logical_bytes": len(raw),
        "chunks": [
            {k: entry[k] for k in ("index", "bytes", "sha256") if k in entry}
            | ({"topic_key": entry["topic_key"]} if "topic_key" in entry else {})
            for entry in chunks
        ],
    }
    manifest_raw = canonical_json_bytes(manifest)
    if len(manifest_raw) > DIRECT_MAX:
        raise JaibaError("limit-exceeded", "chunked-object manifest exceeds the direct threshold")
    out = {
        "ok": True,
        "protocol": PROTOCOL,
        "prefix": "JAIBA4",
        "direct": False,
        "logical_sha256": digest,
        "logical_bytes": len(raw),
        "chunks": chunks,
        "chunked_object": manifest,
        "chunked_object_wire": encode_wire(manifest_raw),
        "chunked_object_sha256": sha256_hex(manifest_raw),
    }
    if ns16 and topic:
        out["chunked_object_topic_key"] = topic_key(topic[0], ns16, topic[1])
    return out


def cmd_encode(args) -> dict:
    data = read_bytes(args.input)
    if args.raw:
        raw = data
    else:
        value = parse_json_bytes(data)
        if not isinstance(value, dict):
            raise JaibaError("invalid-object", "encode input must be a JSON object")
        raw = canonical_json_bytes(value)
    address = parse_json_bytes(args.address.encode("utf-8")) if args.address else None
    topic = None
    if args.ns16 and args.topic_kind:
        if args.topic_kind == "ctx":
            if address:
                norm = normalize_address(address)
                ident = (norm["namespace"], norm["project-id"], norm["context-id"])
            else:
                if not args.project_id or not args.context_id or not args.namespace:
                    raise JaibaError("invalid-object", "ctx topic requires namespace, project-id and context-id")
                ident = (args.namespace, args.project_id, args.context_id)
            topic = ("ctx", ident)
        elif args.topic_kind == "cat":
            if not args.project_id:
                raise JaibaError("invalid-object", "cat topic requires project-id")
            topic = ("cat", args.project_id)
        elif args.topic_kind in {"obj", "base"}:
            if address is None:
                raise JaibaError("invalid-object", "address is required for this topic kind")
            topic = (args.topic_kind, address)
        elif args.topic_kind == "del":
            if address is None or args.seq is None:
                raise JaibaError("invalid-object", "del topic requires address and seq")
            topic = ("del", (address, args.seq))
        elif args.topic_kind == "chk":
            topic = None
        else:
            raise JaibaError("invalid-object", "unknown topic kind")
    return encode_payload(raw, args.ns16, topic)


def cmd_decode(args) -> dict:
    data = read_bytes(args.input)
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise JaibaError("invalid-object", "input is not UTF-8") from exc
    if "... [truncated]" in text:
        raise JaibaError("verification-failed", "truncated read")
    stripped = text.strip("\r\n")
    if "\n" not in stripped:
        line = stripped
    else:
        line = extract_wire(text)
    if args.project or args.scope:
        project = label_value(text, "Project")
        scope = label_value(text, "Scope")
        if args.project and project != args.project:
            raise JaibaError("verification-failed", "foreign Project")
        if args.scope and scope != args.scope:
            raise JaibaError("verification-failed", "foreign Scope")
        if project is None or scope is None:
            raise JaibaError("verification-failed", "Project or Scope line missing")
    prefix, raw = decode_wire(line)
    out = {
        "ok": True,
        "prefix": prefix[:-1],
        "sha256": sha256_hex(raw),
        "raw_bytes": len(raw),
        "payload_b64": base64.b64encode(raw).decode("ascii"),
    }
    try:
        out["json"] = json.loads(raw.decode("utf-8"))
    except Exception:
        out["json"] = None
    return out


def cmd_delta(args) -> dict:
    doc = parse_json_bytes(read_bytes(args.input))
    result = build_delta(doc)
    result["ok"] = True
    return result


def cmd_materialize(args) -> dict:
    doc = parse_json_bytes(read_bytes(args.input))
    if not isinstance(doc, dict) or "base" not in doc:
        raise JaibaError("invalid-object", "materialize requires a base")
    state = materialize_state(doc["base"], doc.get("deltas") or [])
    return {
        "ok": True,
        "object": state["object"],
        "head": state["head"],
        "base_revision": state["base_revision"],
    }


def cmd_render(args) -> str:
    doc = parse_json_bytes(read_bytes(args.input))
    if isinstance(doc, dict) and "base" in doc and "content" not in doc and "object" not in doc:
        doc = materialize_state(doc["base"], doc.get("deltas") or [])["object"]
    elif isinstance(doc, dict) and "object" in doc and isinstance(doc["object"], dict) and "content" in doc["object"]:
        doc = doc["object"]
    if not isinstance(doc, dict) or not isinstance(doc.get("content"), str):
        raise JaibaError("invalid-object", "render requires materialized content")
    return doc["content"]


def canonical_work_root(work_root: str) -> str:
    if not isinstance(work_root, str) or work_root == "":
        raise JaibaError("invalid-object", "work root is empty")
    if "://" in work_root:
        raise JaibaError("invalid-object", "a URI is not a work root")
    if not os.path.isabs(work_root):
        raise JaibaError("invalid-object", "relative path is not a canonical work root")
    if not os.path.isdir(work_root):
        raise JaibaError("invalid-object", "work root is not a directory")
    real_a = os.path.realpath(work_root)
    try:
        real_b = str(Path(work_root).resolve(strict=True))
    except OSError as exc:
        raise JaibaError("invalid-object", "work root does not resolve") from exc
    def norm(path: str) -> str:
        text = path.replace("\\", "/") if os.sep == "\\" else path
        while "//" in text:
            text = text.replace("//", "/")
        if text != "/" and text.endswith("/"):
            text = text[:-1]
        return text
    left, right = norm(real_a), norm(real_b)
    if left != right or not os.path.isdir(left):
        raise JaibaError("invalid-object", "work root resolutions disagree")
    return left


def digest_canonical(canonical: str) -> str:
    return sha256_hex(canonical.encode("utf-8"))


def cmd_binding_path(args) -> str:
    canonical = canonical_work_root(args.work_root)
    digest = digest_canonical(canonical)
    home = str(Path.home())
    return str(Path(home) / ".jaiba" / "memory" / "bindings" / f"{digest}.yaml")


def measure_record_bytes(record) -> int | None:
    if record is None:
        return None
    if isinstance(record, str):
        return len(record.encode("utf-8"))
    if isinstance(record, dict) and "raw_b64" in record:
        return len(base64.b64decode(record["raw_b64"], validate=True))
    if isinstance(record, (dict, list)):
        return len(canonical_json_bytes(record))
    return None


def cmd_cost(args) -> dict:
    operation = args.operation
    raw_bytes = args.bytes
    head_bytes = args.head_bytes
    chunks = args.chunks
    if args.input:
        doc = parse_json_bytes(read_bytes(args.input))
        if isinstance(doc, dict):
            operation = doc.get("operation", operation)
            raw_bytes = doc.get("bytes", raw_bytes)
            head_bytes = doc.get("head_bytes", head_bytes)
            chunks = doc.get("chunks", chunks)
            if raw_bytes is None and "record" in doc:
                raw_bytes = measure_record_bytes(doc["record"])
            if head_bytes is None and "head" in doc:
                head_bytes = measure_record_bytes(doc["head"])
    if not operation:
        raise JaibaError("invalid-object", "cost requires an operation")
    if raw_bytes is not None and (isinstance(raw_bytes, bool) or not isinstance(raw_bytes, int) or raw_bytes < 0):
        raise JaibaError("invalid-object", "bytes must be a non-negative integer")
    if head_bytes is not None and (isinstance(head_bytes, bool) or not isinstance(head_bytes, int) or head_bytes < 0):
        raise JaibaError("invalid-object", "head_bytes must be a non-negative integer")
    notes = {
        "encode": "local wire only; no backend call",
        "decode": "local decode only; no backend call",
        "delta": "local validation; one delta record is described, not stored",
        "materialize": "local fold; no backend call",
        "render": "local markdown; no backend call",
        "binding-path": "path math only; the binding file is not created",
        "read": "verified catalogue get plus object get",
        "create": "probe topic, save object, get object, save catalogue, get catalogue",
        "update": "update object, get object, update catalogue, get catalogue, plus the caller's pre-read",
        "patch": "one exec-delta plus one context-head; base and catalogue are not rewritten",
        "compact": "new base plus context-head when active deltas exist; no-op writes nothing",
        "append-log": "probe close id, save log, get log, update catalogue, get catalogue",
        "catalog": "one verified catalogue read",
        "archive": "verified closing-log read; no destructive write",
        "clear-work": "inventory-sized; unmeasured without a frozen inventory",
        "batch-prepare": "local argument assembly; no backend call",
        "batch-verify": "local comparison; no backend call",
    }
    if operation not in notes and operation not in {"create-chunked", "read-chunked", "patch-chunked"}:
        raise JaibaError("invalid-object", f"unknown cost operation {operation}")
    if operation == "create" and raw_bytes is not None and raw_bytes > DIRECT_MAX:
        operation = "create-chunked"
    if operation == "read" and chunks:
        operation = "read-chunked"
    if operation == "patch" and raw_bytes is not None and raw_bytes > DIRECT_MAX:
        operation = "patch-chunked"
    chunk_count = chunks
    if chunk_count is None and raw_bytes is not None and raw_bytes > DIRECT_MAX:
        chunk_count = (raw_bytes + DIRECT_MAX - 1) // DIRECT_MAX
    recipes = {
        "encode": (1 if not (raw_bytes and raw_bytes > DIRECT_MAX) else (chunk_count or 0) + 1, 0),
        "decode": (0, 0),
        "delta": (1, 0),
        "materialize": (0, 0),
        "render": (0, 0),
        "binding-path": (0, 0),
        "read": (2, 2),
        "read-chunked": ((2 + chunk_count) if chunk_count is not None else "unknown", (2 + chunk_count) if chunk_count is not None else "unknown"),
        "create": (2, 5),
        "create-chunked": ((chunk_count + 2) if chunk_count is not None else "unknown", (3 * ((chunk_count or 0) + 1) + 2) if chunk_count is not None else "unknown"),
        "update": (2, 5),
        "patch": (2, 5),
        "patch-chunked": ((chunk_count + 2) if chunk_count is not None else "unknown", "unknown"),
        "compact": (2, 4),
        "append-log": (2, 5),
        "catalog": (1, 1),
        "archive": (1, 1),
        "clear-work": ("unknown", "unknown"),
        "batch-prepare": (0, 0),
        "batch-verify": (0, 0),
    }
    records, calls = recipes[operation]
    data = "unknown"
    control = "unknown"
    transmitted = "unknown"
    if operation == "patch" and raw_bytes is not None and head_bytes is not None:
        data = raw_bytes + head_bytes
        control = wire_len(raw_bytes) - raw_bytes + wire_len(head_bytes) - head_bytes
        transmitted = wire_len(raw_bytes) + wire_len(head_bytes)
    elif raw_bytes is not None and operation in {"encode", "delta", "create", "update", "append-log"} and raw_bytes <= DIRECT_MAX:
        data = raw_bytes
        control = wire_len(raw_bytes) - raw_bytes
        transmitted = wire_len(raw_bytes)
    elif raw_bytes is not None and chunk_count is not None and operation in {"encode", "create-chunked"}:
        data = raw_bytes
        control = "unknown"
        transmitted = "unknown"
    return {
        "ok": True,
        "operation": operation,
        "records": records,
        "calls": calls,
        "bytes": {"data": data, "control": control, "transmitted": transmitted},
        "notes": notes.get(operation, notes.get(operation.replace("-chunked", ""), "chunked path; sizes are computed from the supplied byte count, not probed")),
        "threshold_raw_bytes": DIRECT_MAX,
    }


def save_arguments(project: str, title: str, wire: str, key: str) -> dict:
    return {
        "title": title,
        "content": wire,
        "project": project,
        "scope": "project",
        "topic_key": key,
        "type": "manual",
        "capture_prompt": False,
    }


def derive_topic(ns16: str, record: dict, action: dict) -> str:
    if "topic_key" in action:
        key = action["topic_key"]
        if not isinstance(key, str) or len(key) > TOPIC_MAX or not key.startswith(f"jaiba/v4/{ns16}/"):
            raise JaibaError("invalid-object", "topic_key is not in the reserved prefix")
        return key
    kind = action.get("topic_kind") or (record.get("kind") if isinstance(record, dict) else None)
    mapping = {
        "catalog": "cat",
        "object": "obj",
        "exec-base": "base",
        "exec-delta": "del",
        "context-head": "ctx",
        "chunked-object": action.get("topic_kind") or "obj",
    }
    topic_kind = mapping.get(kind, kind)
    if topic_kind == "cat":
        return topic_key("cat", ns16, action.get("project_id") or record.get("project-id") or record.get("project_id"))
    if topic_kind in {"obj", "base"}:
        return topic_key(topic_kind, ns16, record.get("address") or action.get("address"))
    if topic_kind == "del":
        return topic_key("del", ns16, (record.get("address") or action.get("address"), record.get("seq") if isinstance(record, dict) else action.get("seq")))
    if topic_kind == "ctx":
        if isinstance(record, dict) and record.get("kind") == "context-head":
            return topic_key("ctx", ns16, (record["namespace"], record["project-id"], record["context-id"]))
        address = action.get("address") or (record.get("address") if isinstance(record, dict) else None)
        if address:
            norm = normalize_address(address)
            return topic_key("ctx", ns16, (norm["namespace"], norm["project-id"], norm["context-id"]))
        return topic_key("ctx", ns16, (action["namespace"], action["project_id"], action["context_id"]))
    raise JaibaError("invalid-object", "cannot derive topic_key")


def cmd_batch_prepare(doc: dict) -> dict:
    if not isinstance(doc, dict):
        raise JaibaError("invalid-object", "batch must be an object")
    if doc.get("transport", "agent-relay") != "agent-relay":
        raise JaibaError("missing-capability", "this script only prepares agent-relay calls")
    project = doc.get("backend_project")
    ns16 = doc.get("ns16")
    actions = doc.get("actions")
    if not isinstance(project, str) or project == "":
        raise JaibaError("invalid-object", "backend_project is required")
    check_ns16(ns16)
    if not isinstance(actions, list) or not actions:
        raise JaibaError("invalid-object", "actions must be a non-empty list")
    steps = []
    for index, action in enumerate(actions):
        if not isinstance(action, dict) or action.get("action") not in {"save", "update", "read"}:
            raise JaibaError("invalid-object", "action must be save, update, or read")
        step_id = f"a{index}"
        if action["action"] == "read":
            if not isinstance(action.get("obs_id"), int) or isinstance(action.get("obs_id"), bool):
                raise JaibaError("invalid-object", "read requires a numeric obs_id")
            steps.append({
                "step": step_id + "-read",
                "tool": "mem_get_observation",
                "arguments": {"id": action["obs_id"]},
                "expect": {"sha256": action.get("expect_sha256"), "project": project, "scope": "project"},
            })
            continue
        record = action.get("record")
        if "raw_b64" in action:
            raw = base64.b64decode(action["raw_b64"], validate=True)
        elif isinstance(record, dict):
            raw = canonical_json_bytes(record)
        else:
            raise JaibaError("invalid-object", "save/update requires a record")
        if len(raw) <= DIRECT_MAX:
            encoded = encode_wire(raw)
            key = derive_topic(ns16, record if isinstance(record, dict) else {}, action)
            title = action.get("title") or f"jaiba {action.get('topic_kind') or (record.get('kind') if isinstance(record, dict) else 'record')} {key}"
            if action["action"] == "save":
                steps.append({
                    "step": step_id + "-probe",
                    "tool": "mem_search",
                    "arguments": {"query": key, "project": project, "scope": "project", "limit": 5},
                    "purpose": "probe-before-save",
                    "note": "Search is not catalogue absence. A topic_key hit must be read back; matching sha256 is adopted; a different digest stops as conflict. Do not call mem_judge.",
                })
                steps.append({
                    "step": step_id + "-save",
                    "tool": "mem_save",
                    "arguments": save_arguments(project, title, encoded, key),
                    "expect": {"sha256": sha256_hex(raw), "wire": encoded, "topic_key": key},
                })
                steps.append({
                    "step": step_id + "-readback",
                    "tool": "mem_get_observation",
                    "arguments": {"id": {"$ref": step_id + "-save.id"}},
                    "expect": {"sha256": sha256_hex(raw), "wire": encoded, "project": project, "scope": "project"},
                })
            else:
                if not isinstance(action.get("obs_id"), int) or isinstance(action.get("obs_id"), bool):
                    raise JaibaError("invalid-object", "update requires a numeric obs_id")
                steps.append({
                    "step": step_id + "-update",
                    "tool": "mem_update",
                    "arguments": {
                        "id": action["obs_id"],
                        "expected_project": project,
                        "content": encoded,
                    },
                    "expect": {"sha256": sha256_hex(raw), "wire": encoded, "topic_key": key},
                })
                steps.append({
                    "step": step_id + "-readback",
                    "tool": "mem_get_observation",
                    "arguments": {"id": action["obs_id"]},
                    "expect": {"sha256": sha256_hex(raw), "wire": encoded, "project": project, "scope": "project"},
                })
            continue
        parts = split_chunks(raw)
        logical = sha256_hex(raw)
        deferred_chunks = []
        for cindex, part in enumerate(parts):
            key = topic_key("chk", ns16, (logical, cindex))
            wire = encode_wire(part)
            cid = f"{step_id}-c{cindex}"
            steps.append({
                "step": cid + "-probe",
                "tool": "mem_search",
                "arguments": {"query": key, "project": project, "scope": "project", "limit": 5},
                "purpose": "probe-before-save",
            })
            steps.append({
                "step": cid + "-save",
                "tool": "mem_save",
                "arguments": save_arguments(project, action.get("title") or f"jaiba chunk {key}", wire, key),
                "expect": {"sha256": sha256_hex(part), "wire": wire, "topic_key": key},
            })
            steps.append({
                "step": cid + "-readback",
                "tool": "mem_get_observation",
                "arguments": {"id": {"$ref": cid + "-save.id"}},
                "expect": {"sha256": sha256_hex(part), "wire": wire, "project": project, "scope": "project"},
            })
            deferred_chunks.append({
                "index": cindex,
                "obs_id": {"$ref": cid + "-save.id"},
                "topic_key": key,
                "bytes": len(part),
                "sha256": sha256_hex(part),
            })
        steps.append({
            "step": step_id + "-chunked-object-deferred",
            "tool": None,
            "deferred": {
                "kind": "chunked-object",
                "logical_sha256": logical,
                "logical_bytes": len(raw),
                "chunks": deferred_chunks,
                "topic_key": derive_topic(ns16, record if isinstance(record, dict) else {}, action) if isinstance(record, dict) or action.get("topic_kind") else None,
            },
            "note": "Substitute numeric obs_id values, then call batch-prepare again to save the chunked-object. This step is not a backend call.",
        })
    return {
        "ok": True,
        "transport": "agent-relay",
        "backend_io": False,
        "steps": steps,
        "notes": [
            "Bytes transit the model. This script did not open the backend.",
            "Ignore judgment_required. Do not call mem_judge, mem_delete, or mem_save for narrative notes.",
        ],
    }


def cmd_batch_verify(doc: dict) -> dict:
    if not isinstance(doc, dict):
        raise JaibaError("invalid-object", "batch-verify input must be an object")
    expected = doc.get("expected")
    observed = doc.get("observed")
    if not isinstance(expected, list) or not isinstance(observed, list):
        raise JaibaError("invalid-object", "expected and observed must be lists")
    by_step = {}
    for item in observed:
        if isinstance(item, dict) and "step" in item:
            by_step.setdefault(item["step"], item)
    mismatches = []
    verified = []
    for exp in expected:
        if not isinstance(exp, dict) or "step" not in exp:
            raise JaibaError("invalid-object", "expected entry requires step")
        obs = by_step.get(exp["step"])
        if obs is None:
            mismatches.append({"step": exp["step"], "code": "missing-readback"})
            continue
        if isinstance(obs.get("json"), dict):
            trunc = obs["json"].get("truncation")
            if obs["json"].get("truncated") is True or (isinstance(trunc, dict) and trunc.get("truncated") is True):
                mismatches.append({"step": exp["step"], "code": "truncation"})
                continue
        text = obs.get("text") or obs.get("content") or ""
        wire = obs.get("wire")
        try:
            if not wire:
                if not isinstance(text, str) or text == "":
                    raise JaibaError("verification-failed", "observed read is empty")
                wire = text.strip() if text.strip().startswith(ACCEPTED_PREFIXES) and "\n" not in text.strip() else extract_wire(text)
            prefix, raw = decode_wire(wire)
            if exp.get("project") or exp.get("scope"):
                source = text if isinstance(text, str) and text else ""
                project = label_value(source, "Project") if source else None
                scope = label_value(source, "Scope") if source else None
                if exp.get("project") and project != exp["project"]:
                    raise JaibaError("verification-failed", "foreign Project")
                if exp.get("scope") and scope != exp["scope"]:
                    raise JaibaError("verification-failed", "foreign Scope")
            if exp.get("sha256") and sha256_hex(raw) != exp["sha256"]:
                raise JaibaError("verification-failed", "sha256 mismatch")
            if exp.get("wire") and wire != exp["wire"]:
                raise JaibaError("verification-failed", "wire mismatch")
            if exp.get("prefix") and prefix[:-1] != exp["prefix"]:
                raise JaibaError("verification-failed", "prefix mismatch")
        except JaibaError as exc:
            code = "digest-mismatch" if "sha256" in exc.detail else "wire-mismatch" if "wire mismatch" in exc.detail else "foreign-project" if "Project" in exc.detail else "foreign-scope" if "Scope" in exc.detail else exc.code
            mismatches.append({"step": exp["step"], "code": code, "detail": exc.detail})
            continue
        verified.append(exp["step"])
    if mismatches:
        raise JaibaError("verification-failed", "readback did not match", {"mismatches": mismatches, "verified": verified})
    return {"ok": True, "verified": verified, "transport": "agent-relay"}


def read_bytes(path: str | None) -> bytes:
    if path:
        return Path(path).read_bytes()
    return sys.stdin.buffer.read()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="jaiba_engram.py", description="JAIBA4 Engram codec (agent-relay, stdlib only)")
    sub = parser.add_subparsers(dest="command", required=True)

    encode = sub.add_parser("encode", help="canonical JAIBA4 wire of one record")
    encode.add_argument("--input", help="JSON or raw bytes; default stdin")
    encode.add_argument("--raw", action="store_true", help="wrap exact bytes; do not parse JSON")
    encode.add_argument("--ns16")
    encode.add_argument("--topic-kind", choices=["cat", "obj", "chk", "ctx", "base", "del"])
    encode.add_argument("--project-id")
    encode.add_argument("--namespace")
    encode.add_argument("--context-id")
    encode.add_argument("--address", help="JSON address object")
    encode.add_argument("--seq", type=int)
    encode.set_defaults(func=cmd_encode, json_out=True)

    decode = sub.add_parser("decode", help="decode one JAIBA4 or legacy JAIBA3 wire")
    decode.add_argument("--input", help="wire line or observation text; default stdin")
    decode.add_argument("--project")
    decode.add_argument("--scope")
    decode.set_defaults(func=cmd_decode, json_out=True)

    delta = sub.add_parser("delta", help="validate ops and construct one exec-delta")
    delta.add_argument("--input", help="JSON request; default stdin")
    delta.set_defaults(func=cmd_delta, json_out=True)

    materialize = sub.add_parser("materialize", help="fold base and ordered deltas")
    materialize.add_argument("--input", help="JSON {base, deltas}; default stdin")
    materialize.set_defaults(func=cmd_materialize, json_out=True)

    render = sub.add_parser("render", help="print materialized markdown content")
    render.add_argument("--input", help="logical object or {base, deltas}; default stdin")
    render.set_defaults(func=cmd_render, json_out=False)

    binding = sub.add_parser("binding-path", help="print the canonical binding path; create nothing")
    binding.add_argument("--work-root", required=True)
    binding.set_defaults(func=cmd_binding_path, json_out=False)

    cost = sub.add_parser("cost", help="recipe cost; unmeasured bytes stay unknown")
    cost.add_argument("--operation")
    cost.add_argument("--bytes", type=int)
    cost.add_argument("--head-bytes", type=int)
    cost.add_argument("--chunks", type=int)
    cost.add_argument("--input", help="optional JSON cost request")
    cost.set_defaults(func=cmd_cost, json_out=True)

    prepare = sub.add_parser("batch-prepare", help="emit agent-relay tool arguments; no backend I/O")
    prepare.add_argument("--input", help="batch JSON; default stdin")
    prepare.set_defaults(func=lambda args: cmd_batch_prepare(parse_json_bytes(read_bytes(args.input))), json_out=True)

    verify = sub.add_parser("batch-verify", help="compare expected receipts with observed reads")
    verify.add_argument("--input", help="JSON {expected, observed}; default stdin")
    verify.set_defaults(func=lambda args: cmd_batch_verify(parse_json_bytes(read_bytes(args.input))), json_out=True)
    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        result = args.func(args)
    except JaibaError as exc:
        emit_err(exc)
        return 1
    if getattr(args, "json_out", True):
        emit(result)
    else:
        sys.stdout.write(result)
        if args.command == "binding-path":
            sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
    except JaibaError as exc:
        emit_err(exc)
        sys.exit(1)
    except Exception as exc:
        sys.stderr.write(json.dumps({"ok": False, "error": "internal", "detail": f"{type(exc).__name__}: {exc}"}) + "\n")
        sys.exit(2)
