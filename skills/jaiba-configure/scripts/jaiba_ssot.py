#!/usr/bin/env python3
"""JAIBA Global SSOT manager: host detection, legacy harvest, validation, and projection.

Pure Python 3 standard library only (zero external dependencies).
Enforces ADR-010 (§4.5 content-is-data boundaries), ADR-014 (atomic writes),
and ADR-017 (verified effort controls only; researcher never pins a model).
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Any

CANONICAL_ROLES = (
    "executor-high",
    "executor-medium",
    "executor-low",
    "code-analyst",
    "business-analyst",
    "verify",
    "researcher",
)

ROLE_TO_TIER = {
    "executor-high": "high",
    "executor-medium": "medium",
    "code-analyst": "medium",
    "business-analyst": "medium",
    "verify": "medium",
    "executor-low": "low",
}

VALID_TIERS = ("high", "medium", "low")
VALID_NATIVE_PLAN_CLIENTS = ("auto", "on", "off")
MAX_UNTRUSTED_BYTES = 262144
MAX_YAML_DEPTH = 32

HOST_LAYOUTS: dict[str, dict[str, Any]] = {
    "antigravity": {
        "rel_root": ".gemini/config",
        "global_instruction_file": "pointer",
        "exclude_subdirs": (),
    },
    "claude-code": {
        "rel_root": ".claude",
        "global_instruction_file": "CLAUDE.md",
        "exclude_subdirs": (),
    },
    "opencode": {
        "rel_root": ".config/opencode",
        "global_instruction_file": "AGENTS.md",
        "exclude_subdirs": (),
    },
    "cursor": {
        "rel_root": ".cursor",
        "global_instruction_file": "pointer",
        "exclude_subdirs": (),
    },
    "gemini-cli": {
        "rel_root": ".gemini",
        "global_instruction_file": "GEMINI.md",
        "exclude_subdirs": ("config",),
    },
    "windsurf": {
        "rel_root": ".windsurf",
        "global_instruction_file": "pointer",
        "exclude_subdirs": (),
    },
    "github-copilot": {
        "rel_root": ".github/copilot",
        "global_instruction_file": "pointer",
        "exclude_subdirs": (),
    },
    "agents": {
        "rel_root": ".agents",
        "global_instruction_file": "pointer",
        "exclude_subdirs": (),
    },
}

DEFAULT_NEUTRAL_CAVEAT: dict[str, Any] = {
    "host_id": "agents",
    "display_name": "Neutral Fallback (~/.agents/)",
    "config_root": "~/.agents/",
    "subagent_dir": "~/.agents/agents/",
    "global_instruction_file": "pointer",
    "frontmatter_flavor": "standard",
    "emits_name": True,
    "emits_requires": True,
    "emits_mode_subagent": False,
    "emits_permission_map": False,
    "effort_syntax": "none",
    "researcher_model_pin": "forbidden",
    "researcher_effort": "forbidden",
}

CURSOR_EFFORT_RE = re.compile(r"^([^\[\]]+?)\[effort=([^\[\]]+)\]$")
CONTROL_CHAR_RE = re.compile(r"[\x00-\x1f\x7f]")
KEY_TOKEN_RE = re.compile(
    r'^([A-Za-z0-9_.-]+|"(?:[^"\\]|\\.)*"|\'(?:[^\']|\'\')*\'):(?:[ \t]+(.*)|[ \t]*)$'
)
YAML_TAG_RE = re.compile(r"^!{1,2}[A-Za-z0-9_.:/-]+(?:\s|$)")


class SsotError(Exception):
    def __init__(self, code: str, detail: str, evidence: dict[str, Any] | None = None):
        super().__init__(detail)
        self.code = code
        self.detail = detail
        self.evidence = evidence or {}


class YamlError(SsotError):
    def __init__(self, detail: str, line: int | None = None):
        ev = {"line": line} if line is not None else {}
        super().__init__("invalid-yaml", detail, ev)
        self.line = line


def _strip_inline_comment(raw: str) -> str:
    in_sq = False
    in_dq = False
    i = 0
    while i < len(raw):
        ch = raw[i]
        if ch == "\\" and in_dq:
            i += 2
            continue
        if ch == "'" and not in_dq:
            if in_sq and i + 1 < len(raw) and raw[i + 1] == "'":
                i += 2
                continue
            in_sq = not in_sq
        elif ch == '"' and not in_sq:
            in_dq = not in_dq
        elif ch == "#" and not in_sq and not in_dq:
            if i == 0 or raw[i - 1] in (" ", "\t"):
                return raw[:i].rstrip(" \t")
        i += 1
    return raw.rstrip(" \t")


def _unquote_or_parse_scalar(raw: str, line_no: int | None = None) -> Any:
    s = _strip_inline_comment(raw.strip())
    if s == "":
        return None
    if YAML_TAG_RE.match(s):
        raise YamlError(f"unsupported YAML tag in scalar: {s.split()[0]}", line_no)
    if s[0] == "&" or s[0] == "*":
        raise YamlError("YAML anchors/aliases are not supported", line_no)
    if s[0] == '"':
        out: list[str] = []
        i = 1
        while i < len(s):
            ch = s[i]
            if ch == "\\":
                if i + 1 >= len(s):
                    raise YamlError("unclosed double-quoted scalar", line_no)
                nxt = s[i + 1]
                esc = {"n": "\n", "r": "\r", "t": "\t", "\\": "\\", '"': '"', "/": "/"}
                out.append(esc.get(nxt, nxt))
                i += 2
                continue
            if ch == '"':
                trailing = s[i + 1 :].strip()
                if trailing:
                    raise YamlError("unexpected trailing characters after quoted scalar", line_no)
                return "".join(out)
            out.append(ch)
            i += 1
        raise YamlError("unclosed double-quoted scalar", line_no)
    if s[0] == "'":
        out = []
        i = 1
        while i < len(s):
            ch = s[i]
            if ch == "'":
                if i + 1 < len(s) and s[i + 1] == "'":
                    out.append("'")
                    i += 2
                    continue
                trailing = s[i + 1 :].strip()
                if trailing:
                    raise YamlError("unexpected trailing characters after single-quoted scalar", line_no)
                return "".join(out)
            out.append(ch)
            i += 1
        raise YamlError("unclosed single-quoted scalar", line_no)
    if s == "{}":
        return {}
    if s == "[]":
        return []
    if s.startswith("[") and s.endswith("]"):
        return _parse_flow_list(s[1:-1], line_no)
    if s.startswith("{") and s.endswith("}"):
        return _parse_flow_dict(s[1:-1], line_no)
    if s.startswith("[") or s.startswith("{"):
        raise YamlError("unclosed or multiline flow collection is not supported", line_no)

    low = s.lower()
    if low in ("null", "~"):
        return None
    if low == "true":
        return True
    if low == "false":
        return False
    if re.fullmatch(r"-?[0-9]+", s):
        if len(s) > 1 and s.startswith("0") and not s.startswith("-"):
            return s
        return int(s)
    return s


def _split_flow_items(inner: str, line_no: int | None) -> list[str]:
    items: list[str] = []
    buf: list[str] = []
    in_sq = False
    in_dq = False
    depth = 0
    i = 0
    while i < len(inner):
        ch = inner[i]
        if ch == "\\" and in_dq:
            buf.append(ch)
            if i + 1 < len(inner):
                buf.append(inner[i + 1])
                i += 2
                continue
            raise YamlError("dangling escape in flow collection", line_no)
        if ch == "'" and not in_dq:
            in_sq = not in_sq
            buf.append(ch)
        elif ch == '"' and not in_sq:
            in_dq = not in_dq
            buf.append(ch)
        elif not in_sq and not in_dq:
            if ch in ("[", "{"):
                depth += 1
                buf.append(ch)
            elif ch in ("]", "}"):
                depth -= 1
                if depth < 0:
                    raise YamlError("unbalanced brackets in flow collection", line_no)
                buf.append(ch)
            elif ch == "," and depth == 0:
                items.append("".join(buf).strip())
                buf = []
                i += 1
                continue
            else:
                buf.append(ch)
        else:
            buf.append(ch)
        i += 1
    if in_sq or in_dq or depth != 0:
        raise YamlError("unclosed flow collection or quote", line_no)
    tail = "".join(buf).strip()
    if tail:
        items.append(tail)
    return items


def _parse_flow_list(inner: str, line_no: int | None) -> list[Any]:
    if not inner.strip():
        return []
    return [_unquote_or_parse_scalar(part, line_no) for part in _split_flow_items(inner, line_no)]


def _parse_flow_dict(inner: str, line_no: int | None) -> dict[str, Any]:
    if not inner.strip():
        return {}
    out: dict[str, Any] = {}
    for part in _split_flow_items(inner, line_no):
        m = KEY_TOKEN_RE.match(part)
        if not m:
            raise YamlError(f"invalid entry in flow mapping: {part}", line_no)
        key = str(_parse_key_token(m.group(1), line_no))
        if key in out:
            raise YamlError(f"duplicate key '{key}' in flow mapping", line_no)
        raw_val = (m.group(2) or "").strip()
        out[key] = _unquote_or_parse_scalar(raw_val, line_no)
    return out


def _parse_key_token(token: str, line_no: int | None) -> str:
    if (token.startswith('"') and token.endswith('"')) or (
        token.startswith("'") and token.endswith("'")
    ):
        val = _unquote_or_parse_scalar(token, line_no)
        return "" if val is None else str(val)
    return token


def parse_yaml_subset(text: str) -> Any:
    """Parse a deterministic, safe YAML subset into Python primitives."""
    if text.startswith("\ufeff"):
        text = text[1:]
    raw_lines = text.splitlines()
    tokens: list[tuple[int, int, str]] = []
    for idx, line in enumerate(raw_lines, start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        leading = len(line) - len(line.lstrip(" \t"))
        if "\t" in line[:leading]:
            raise YamlError("tabs are not allowed in YAML indentation", idx)
        tokens.append((idx, leading, line[leading:]))

    if not tokens:
        return {}

    def parse_block_scalar(start_pos: int, parent_indent: int, style: str) -> tuple[str, int]:
        chomp = "clip"
        if style.endswith("-"):
            chomp = "strip"
        elif style.endswith("+"):
            chomp = "keep"
        fold = style.startswith(">")
        first_line_no = tokens[start_pos - 1][0]
        # Read raw lines directly after first_line_no to preserve blank lines & exact indentation
        collected: list[str] = []
        block_indent: int | None = None
        raw_idx = first_line_no  # 0-based index of next raw line
        while raw_idx < len(raw_lines):
            rline = raw_lines[raw_idx]
            if rline.strip() == "":
                collected.append("")
                raw_idx += 1
                continue
            r_leading = len(rline) - len(rline.lstrip(" "))
            if "\t" in rline[: len(rline) - len(rline.lstrip(" \t"))]:
                raise YamlError("tabs are not allowed in YAML block scalar", raw_idx + 1)
            if block_indent is None:
                if r_leading <= parent_indent:
                    break
                block_indent = r_leading
            elif r_leading < block_indent:
                break
            collected.append(rline[block_indent:])
            raw_idx += 1

        while collected and collected[-1] == "" and chomp != "keep":
            collected.pop()
        if fold:
            joined = " ".join(part if part != "" else "\n" for part in collected).strip()
        else:
            joined = "\n".join(collected)
        if chomp == "clip" and joined:
            joined += "\n"
        # Advance token cursor past raw_idx (1-based line <= raw_idx)
        pos = start_pos
        while pos < len(tokens) and tokens[pos][0] <= raw_idx:
            pos += 1
        return joined, pos

    def parse_node(pos: int, min_indent: int, depth: int) -> tuple[Any, int]:
        if depth > MAX_YAML_DEPTH:
            raise YamlError("YAML nesting depth exceeds safe limit", tokens[pos][0])
        line_no, indent, content = tokens[pos]
        if indent < min_indent:
            raise YamlError("unexpected indentation", line_no)
        if content.startswith("- ") or content == "-":
            return parse_list(pos, indent, depth)
        if KEY_TOKEN_RE.match(content):
            return parse_dict(pos, indent, depth)
        val = _unquote_or_parse_scalar(content, line_no)
        return val, pos + 1

    def parse_list(pos: int, list_indent: int, depth: int) -> tuple[list[Any], int]:
        out: list[Any] = []
        while pos < len(tokens):
            line_no, indent, content = tokens[pos]
            if indent < list_indent:
                break
            if indent > list_indent:
                raise YamlError("unexpected indentation in list", line_no)
            if not (content.startswith("- ") or content == "-"):
                break
            rest = content[1:].lstrip(" ") if content != "-" else ""
            rest_clean = _strip_inline_comment(rest)
            if rest_clean == "":
                pos += 1
                if pos < len(tokens) and tokens[pos][1] > list_indent:
                    val, pos = parse_node(pos, tokens[pos][1], depth + 1)
                    out.append(val)
                else:
                    out.append(None)
                continue
            if rest_clean in ("|", "|-", "|+", ">", ">-", ">+"):
                val, pos = parse_block_scalar(pos + 1, list_indent, rest_clean)
                out.append(val)
                continue
            m = KEY_TOKEN_RE.match(rest)
            if m:
                # Inline mapping item inside list: `- key: val`
                item_indent = list_indent + 2
                item: dict[str, Any] = {}
                key = _parse_key_token(m.group(1), line_no)
                raw_val = m.group(2)
                raw_clean = _strip_inline_comment(raw_val.strip()) if raw_val is not None else ""
                if raw_clean in ("|", "|-", "|+", ">", ">-", ">+"):
                    val, pos = parse_block_scalar(pos + 1, item_indent, raw_clean)
                    item[key] = val
                elif raw_clean == "":
                    pos += 1
                    if pos < len(tokens) and tokens[pos][1] > item_indent:
                        val, pos = parse_node(pos, tokens[pos][1], depth + 1)
                        item[key] = val
                    else:
                        item[key] = None
                else:
                    item[key] = _unquote_or_parse_scalar(raw_val, line_no)
                    pos += 1
                if pos < len(tokens) and tokens[pos][1] >= item_indent:
                    extra, pos = parse_dict(pos, tokens[pos][1], depth + 1)
                    for k, v in extra.items():
                        if k in item:
                            raise YamlError(f"duplicate key '{k}' in list mapping", tokens[pos - 1][0])
                        item[k] = v
                out.append(item)
                continue
            out.append(_unquote_or_parse_scalar(rest, line_no))
            pos += 1
        return out, pos

    def parse_dict(pos: int, dict_indent: int, depth: int) -> tuple[dict[str, Any], int]:
        out: dict[str, Any] = {}
        while pos < len(tokens):
            line_no, indent, content = tokens[pos]
            if indent < dict_indent:
                break
            if indent > dict_indent:
                raise YamlError("unexpected indentation in mapping", line_no)
            if content.startswith("- ") or content == "-":
                break
            m = KEY_TOKEN_RE.match(content)
            if not m:
                raise YamlError(f"expected mapping key: {content}", line_no)
            key = _parse_key_token(m.group(1), line_no)
            if key in out:
                raise YamlError(f"duplicate mapping key '{key}'", line_no)
            raw_val = m.group(2)
            raw_clean = _strip_inline_comment(raw_val.strip()) if raw_val is not None else ""
            if raw_clean in ("|", "|-", "|+", ">", ">-", ">+"):
                val, pos = parse_block_scalar(pos + 1, dict_indent, raw_clean)
                out[key] = val
                continue
            if raw_clean == "":
                pos += 1
                if pos < len(tokens) and tokens[pos][1] > dict_indent:
                    val, pos = parse_node(pos, tokens[pos][1], depth + 1)
                    out[key] = val
                elif (
                    pos < len(tokens)
                    and tokens[pos][1] == dict_indent
                    and (tokens[pos][2].startswith("- ") or tokens[pos][2] == "-")
                ):
                    val, pos = parse_list(pos, dict_indent, depth + 1)
                    out[key] = val
                else:
                    out[key] = None
                continue
            out[key] = _unquote_or_parse_scalar(raw_val, line_no)
            pos += 1
        return out, pos

    result, next_pos = parse_node(0, tokens[0][1], 0)
    if next_pos < len(tokens):
        raise YamlError("trailing content at top level", tokens[next_pos][0])
    return result


YAML_RESERVED_PLAIN = {"true", "false", "null", "~", "on", "off", "yes", "no"}


def format_yaml_scalar(value: Any, force_quote: bool = False) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    text = str(value)
    if "\n" in text or "\r" in text:
        escaped = (
            text.replace("\\", "\\\\")
            .replace('"', '\\"')
            .replace("\n", "\\n")
            .replace("\r", "\\r")
        )
        return f'"{escaped}"'
    needs_quote = force_quote
    if not needs_quote:
        if text == "" or text != text.strip():
            needs_quote = True
        elif text.lower() in YAML_RESERVED_PLAIN:
            needs_quote = True
        elif re.fullmatch(r"-?[0-9]+(?:\.[0-9]+)?", text):
            needs_quote = True
        elif text[0] in "-?:,[]{}#&*!|>'\"%@`":
            needs_quote = True
        elif ": " in text or text.endswith(":") or " #" in text or "#" in text or '"' in text or "\\" in text:
            needs_quote = True
    if needs_quote:
        escaped = text.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    return text


def dump_yaml(data: Any, indent: int = 0, force_quote_keys: set[str] | None = None) -> str:
    """Serialize Python dicts/lists/scalars to deterministic 2-space indented YAML."""
    lines = _dump_yaml_lines(data, indent, force_quote_keys or set())
    return "\n".join(lines) + ("\n" if lines else "")


def _dump_yaml_lines(data: Any, indent: int, force_quote_keys: set[str]) -> list[str]:
    pad = " " * indent
    lines: list[str] = []
    if isinstance(data, dict):
        if not data:
            lines.append(f"{pad}{{}}")
            return lines
        for key, val in data.items():
            key_str = str(key)
            if not re.fullmatch(r"[A-Za-z0-9_.-]+", key_str):
                key_str = format_yaml_scalar(key_str, force_quote=True)
            fq = str(key) in force_quote_keys
            if isinstance(val, dict):
                if not val:
                    lines.append(f"{pad}{key_str}: {{}}")
                else:
                    lines.append(f"{pad}{key_str}:")
                    lines.extend(_dump_yaml_lines(val, indent + 2, force_quote_keys))
            elif isinstance(val, list):
                if not val:
                    lines.append(f"{pad}{key_str}: []")
                else:
                    lines.append(f"{pad}{key_str}:")
                    lines.extend(_dump_yaml_lines(val, indent + 2, force_quote_keys))
            elif val is None:
                lines.append(f"{pad}{key_str}: null")
            else:
                lines.append(f"{pad}{key_str}: {format_yaml_scalar(val, force_quote=fq)}")
        return lines
    if isinstance(data, list):
        if not data:
            lines.append(f"{pad}[]")
            return lines
        for item in data:
            if isinstance(item, dict):
                if not item:
                    lines.append(f"{pad}- {{}}")
                else:
                    sub = _dump_yaml_lines(item, indent + 2, force_quote_keys)
                    first = sub[0].lstrip(" ")
                    lines.append(f"{pad}- {first}")
                    lines.extend(sub[1:])
            elif isinstance(item, list):
                lines.append(f"{pad}-")
                lines.extend(_dump_yaml_lines(item, indent + 2, force_quote_keys))
            else:
                lines.append(f"{pad}- {format_yaml_scalar(item)}")
        return lines
    lines.append(f"{pad}{format_yaml_scalar(data)}")
    return lines


def split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Split a Markdown document into (frontmatter_dict, body)."""
    if text.startswith("\ufeff"):
        text = text[1:]
    lines = text.splitlines(keepends=True)
    if not lines:
        raise SsotError("missing-frontmatter", "file is empty")
    if lines[0].rstrip("\r\n").rstrip(" \t") != "---":
        raise SsotError("missing-frontmatter", "missing opening '---' frontmatter delimiter")
    close_idx: int | None = None
    for idx in range(1, len(lines)):
        marker = lines[idx].rstrip("\r\n").rstrip(" \t")
        if marker in ("---", "..."):
            close_idx = idx
            break
    if close_idx is None:
        raise SsotError("unclosed-frontmatter", "missing closing '---' frontmatter delimiter")
    fm_text = "".join(lines[1:close_idx])
    parsed = parse_yaml_subset(fm_text)
    if parsed is None:
        parsed = {}
    if not isinstance(parsed, dict):
        raise SsotError("invalid-frontmatter", "frontmatter must be a YAML mapping")
    body = "".join(lines[close_idx + 1 :])
    return parsed, body


def render_markdown(frontmatter: dict[str, Any], body: str, force_quote_keys: set[str] | None = None) -> str:
    fm_yaml = dump_yaml(frontmatter, indent=0, force_quote_keys=force_quote_keys)
    clean_body = body.lstrip("\r\n").replace("\r\n", "\n")
    if clean_body and not clean_body.endswith("\n"):
        clean_body += "\n"
    if clean_body:
        return f"---\n{fm_yaml}---\n\n{clean_body}"
    return f"---\n{fm_yaml}---\n"


def read_bounded_text(path: Path, max_bytes: int = MAX_UNTRUSTED_BYTES) -> str:
    raw = path.read_bytes()
    if len(raw) > max_bytes:
        raise SsotError(
            "file-too-large",
            f"{path} exceeds {max_bytes} bytes safety limit ({len(raw)} bytes)",
        )
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise SsotError("invalid-encoding", f"{path} is not valid UTF-8") from exc


def atomic_write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.tmp.", dir=str(path.parent))
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(content)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp_path, path)
    except Exception:
        if tmp_path.exists():
            try:
                tmp_path.unlink()
            except OSError:
                pass
        raise


def atomic_symlink(target: Path, link_path: Path) -> None:
    link_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = link_path.parent / f".{link_path.name}.tmp.{os.getpid()}.{id(link_path)}"
    if tmp_path.exists() or tmp_path.is_symlink():
        tmp_path.unlink()
    try:
        os.symlink(str(target), str(tmp_path))
        os.replace(tmp_path, link_path)
    except Exception:
        if tmp_path.exists() or tmp_path.is_symlink():
            try:
                tmp_path.unlink()
            except OSError:
                pass
        raise


def resolve_home_path(raw: str, home: Path) -> Path:
    if raw == "~":
        return home
    if raw.startswith("~/"):
        return home / raw[2:]
    return Path(raw).expanduser()


def portable_home_str(path: Path, home: Path, trailing_slash: bool = True) -> str:
    try:
        rel = path.resolve(strict=False).relative_to(home.resolve(strict=False))
        base = "~/" + rel.as_posix() if str(rel) != "." else "~"
    except ValueError:
        base = path.as_posix()
    if trailing_slash and not base.endswith("/"):
        base += "/"
    return base


def load_caveats(caveats_dir: Path) -> tuple[dict[str, dict[str, Any]], dict[str, str]]:
    """Load caveat rules from caveats_dir/*.md frontmatter."""
    if not caveats_dir.is_dir():
        raise SsotError("missing-caveats", f"caveats directory not found: {caveats_dir}")
    caveats: dict[str, dict[str, Any]] = {}
    aliases: dict[str, str] = {}

    index_path = caveats_dir / "index.md"
    if index_path.is_file():
        idx_fm, _ = split_frontmatter(read_bounded_text(index_path))
        neutral = dict(DEFAULT_NEUTRAL_CAVEAT)
        nf = idx_fm.get("neutral_fallback")
        if isinstance(nf, dict):
            for k in ("config_root", "subagent_dir", "global_instruction_file", "frontmatter_flavor", "effort_syntax"):
                if k in nf and nf[k] is not None:
                    neutral[k] = nf[k]
        caveats["agents"] = neutral
    else:
        caveats["agents"] = dict(DEFAULT_NEUTRAL_CAVEAT)

    for md_path in sorted(caveats_dir.glob("*.md")):
        if md_path.name == "index.md":
            continue
        fm, _ = split_frontmatter(read_bounded_text(md_path))
        host_id = fm.get("host_id")
        if not isinstance(host_id, str) or not host_id:
            raise SsotError("invalid-caveat", f"missing host_id in {md_path}")
        caveats[host_id] = fm
        aliases[host_id] = host_id
        raw_aliases = fm.get("aliases")
        if isinstance(raw_aliases, list):
            for alias in raw_aliases:
                if isinstance(alias, str) and alias:
                    aliases[alias] = host_id
    aliases["agents"] = "agents"
    aliases["neutral"] = "agents"
    return caveats, aliases


def normalize_host_id(raw_host: str, aliases: dict[str, str]) -> str | None:
    return aliases.get(raw_host.strip())


def host_root_from_layout(host_id: str, home: Path) -> Path:
    layout = HOST_LAYOUTS.get(host_id)
    if not layout:
        raise SsotError("unknown-host", f"unknown host_id: {host_id}")
    return home / layout["rel_root"]


def check_host_exists(host_id: str, home: Path) -> tuple[bool, Path]:
    root = host_root_from_layout(host_id, home)
    if not root.is_dir():
        return False, root
    excludes = set(HOST_LAYOUTS[host_id]["exclude_subdirs"])
    if excludes:
        try:
            children = {p.name for p in root.iterdir()}
        except OSError:
            return False, root
        # If the directory exists solely to contain excluded subdirs (e.g. ~/.gemini/config for Antigravity)
        if children and children.issubset(excludes):
            return False, root
    return True, root


def inspect_host(host_id: str, home: Path) -> dict[str, Any]:
    exists, root = check_host_exists(host_id, home)
    layout = HOST_LAYOUTS[host_id]
    contract_path = root / "jaiba-contract.md"
    cfg_path = root / "jaiba-configure.yaml"
    agents_dir = root / "agents"
    skills_dir = root / "skills"
    gif = layout["global_instruction_file"]
    gif_exists = (root / gif).is_file() if gif != "pointer" else False

    jaiba_agents: list[str] = []
    third_party_agents: list[str] = []
    if exists and agents_dir.is_dir():
        canonical_filenames = {f"{r}.md": r for r in CANONICAL_ROLES}
        try:
            entries = sorted(agents_dir.iterdir(), key=lambda p: p.name)
        except OSError:
            entries = []
        for entry in entries:
            if entry.name in canonical_filenames:
                jaiba_agents.append(canonical_filenames[entry.name])
            elif entry.name.endswith(".md") and not entry.is_dir():
                third_party_agents.append(entry.name)

    contract_exists = exists and (contract_path.is_file() or contract_path.is_symlink())
    contract_is_symlink = exists and contract_path.is_symlink()
    contract_target = os.readlink(contract_path) if contract_is_symlink else None

    return {
        "host_id": host_id,
        "config_root": str(root),
        "portable_config_root": portable_home_str(root, home),
        "exists": exists,
        "legacy_markers": {
            "jaiba_contract": contract_exists,
            "jaiba_contract_is_symlink": contract_is_symlink,
            "jaiba_contract_target": contract_target,
            "jaiba_configure_yaml": exists and cfg_path.is_file(),
            "jaiba_agents_count": len(jaiba_agents),
            "jaiba_agents": jaiba_agents,
            "third_party_agents_count": len(third_party_agents),
            "third_party_agents": third_party_agents,
            "skills_dir_exists": exists and skills_dir.is_dir(),
            "global_instruction_file_exists": gif_exists,
        },
    }


def cmd_detect_hosts(args: argparse.Namespace) -> dict[str, Any]:
    home = Path(args.home)
    ssot_root = Path(args.ssot_root)
    caveats_dir = Path(args.caveats_dir)
    caveats, _aliases = load_caveats(caveats_dir)

    host_ids = [h for h in HOST_LAYOUTS if h in caveats]
    hosts = [inspect_host(hid, home) for hid in host_ids]
    ssot_info = {
        "ssot_root": str(ssot_root),
        "exists": ssot_root.is_dir(),
        "config_yaml": (ssot_root / "config.yaml").is_file(),
        "mappings_yaml": (ssot_root / "mappings.yaml").is_file(),
        "contract": (ssot_root / "contract" / "jaiba-contract.md").is_file(),
        "base_agents_dir": (ssot_root / "agents" / "base").is_dir(),
    }
    return {
        "ok": True,
        "command": "detect-hosts",
        "home": str(home),
        "ssot": ssot_info,
        "hosts": hosts,
    }


def _check_safe_scalar(val: Any, field_name: str) -> tuple[str | None, str | None]:
    if val is None:
        return None, None
    if not isinstance(val, str):
        return None, f"{field_name} must be a string, got {type(val).__name__}"
    cleaned = val.strip()
    if cleaned == "":
        return None, None
    if CONTROL_CHAR_RE.search(cleaned):
        return None, f"{field_name} contains control characters"
    if any(ch.isspace() for ch in cleaned):
        return None, f"{field_name} contains unexpected whitespace"
    return cleaned, None


def _validate_single_entry(
    host_id: str,
    role: str | None,
    model: Any,
    effort: Any,
    caveats: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if host_id not in caveats:
        errors.append({"host": host_id, "role": role, "error": "unknown-host", "detail": f"Host '{host_id}' has no caveat definition"})
        return errors

    caveat = caveats[host_id]
    if role is not None and role not in CANONICAL_ROLES:
        errors.append({"host": host_id, "role": role, "error": "unknown-role", "detail": f"Role '{role}' is not one of the 7 canonical JAIBA roles"})

    model_str, model_err = _check_safe_scalar(model, "model")
    if model_err:
        errors.append({"host": host_id, "role": role, "error": "invalid-model", "detail": model_err})
    effort_str, effort_err = _check_safe_scalar(effort, "effort")
    if effort_err:
        errors.append({"host": host_id, "role": role, "error": "invalid-effort", "detail": effort_err})

    if role == "researcher":
        if model_str is not None:
            errors.append({
                "host": host_id,
                "role": "researcher",
                "error": "researcher-model-pin-forbidden",
                "detail": "ADR-017: 'researcher' must never have a 'model:' pin on any host",
            })
        if effort_str is not None:
            errors.append({
                "host": host_id,
                "role": "researcher",
                "error": "researcher-effort-forbidden",
                "detail": "ADR-017: 'researcher' must never have an effort control on any host",
            })
        return errors

    # Model catalog check (Antigravity exception)
    selectable_models = caveat.get("selectable_models")
    if isinstance(selectable_models, list) and model_str is not None:
        allowed_models = {str(m) for m in selectable_models}
        if model_str not in allowed_models:
            errors.append({
                "host": host_id,
                "role": role,
                "error": "invalid-host-model",
                "detail": f"Host '{host_id}' only allows selectable models {sorted(allowed_models)}, got '{model_str}'",
            })

    # Effort syntax rules from caveat
    effort_syntax = str(caveat.get("effort_syntax") or "none")
    if effort_str is not None:
        if effort_syntax == "none":
            errors.append({
                "host": host_id,
                "role": role,
                "error": "effort-unsupported",
                "detail": f"ADR-017: host '{host_id}' has effort_syntax=none; effort '{effort_str}' is not supported",
            })
        else:
            if model_str is None or model_str == "inherit":
                errors.append({
                    "host": host_id,
                    "role": role,
                    "error": "effort-without-model",
                    "detail": f"Host '{host_id}' does not allow effort '{effort_str}' when model is unset or inherit",
                })
            forbidden = caveat.get("effort_forbidden_values")
            if isinstance(forbidden, list) and effort_str in {str(x) for x in forbidden}:
                errors.append({
                    "host": host_id,
                    "role": role,
                    "error": "forbidden-effort-value",
                    "detail": f"Effort value '{effort_str}' is explicitly forbidden on host '{host_id}'",
                })
            documented = caveat.get("effort_documented_values")
            if isinstance(documented, list):
                allowed_eff = {str(x) for x in documented}
                if effort_str not in allowed_eff:
                    errors.append({
                        "host": host_id,
                        "role": role,
                        "error": "undocumented-effort-value",
                        "detail": f"Host '{host_id}' only documents effort values {sorted(allowed_eff)}, got '{effort_str}'",
                    })
            if host_id == "cursor":
                if "[" in effort_str or "]" in effort_str:
                    errors.append({
                        "host": host_id,
                        "role": role,
                        "error": "invalid-effort-syntax",
                        "detail": "Cursor effort value cannot contain '[' or ']'",
                    })
                if model_str and ("[effort=" in model_str or "[" in model_str or "]" in model_str):
                    errors.append({
                        "host": host_id,
                        "role": role,
                        "error": "ambiguous-cursor-model",
                        "detail": "Store base model ID in 'model' and effort value in 'effort' separately in mappings.yaml",
                    })
    elif host_id == "cursor" and model_str and ("[effort=" in model_str or "[" in model_str or "]" in model_str):
        m = CURSOR_EFFORT_RE.match(model_str)
        if not m:
            errors.append({
                "host": host_id,
                "role": role,
                "error": "invalid-cursor-model-syntax",
                "detail": f"Malformed Cursor inline effort syntax in model '{model_str}'",
            })

    return errors


def _resolve_role_mapping(host_cfg: dict[str, Any], role: str) -> tuple[str | None, str | None]:
    if not isinstance(host_cfg, dict):
        return None, None
    entry: Any = None
    roles_map = host_cfg.get("roles")
    if isinstance(roles_map, dict) and role in roles_map:
        entry = roles_map[role]
    elif role in host_cfg:
        entry = host_cfg[role]
    else:
        tier = ROLE_TO_TIER.get(role)
        tiers_map = host_cfg.get("tiers")
        if tier and isinstance(tiers_map, dict) and tier in tiers_map:
            entry = tiers_map[tier]

    if not isinstance(entry, dict):
        return None, None
    model = entry.get("model")
    effort = entry.get("effort")
    m_str = model.strip() if isinstance(model, str) and model.strip() else None
    e_str = effort.strip() if isinstance(effort, str) and effort.strip() else None
    return m_str, e_str


def validate_mappings_data(
    mappings: dict[str, Any],
    caveats: dict[str, dict[str, Any]],
    aliases: dict[str, str],
    only_hosts: set[str] | None = None,
) -> tuple[list[dict[str, Any]], int]:
    errors: list[dict[str, Any]] = []
    checked = 0
    if not isinstance(mappings, dict):
        errors.append({"error": "invalid-mappings", "detail": "mappings.yaml root must be a YAML mapping"})
        return errors, checked

    hosts_section = mappings.get("hosts")
    if hosts_section is None:
        return errors, checked
    if not isinstance(hosts_section, dict):
        errors.append({"error": "invalid-mappings", "detail": "'hosts' section in mappings.yaml must be a mapping"})
        return errors, checked

    for raw_host, host_cfg in hosts_section.items():
        host_id = normalize_host_id(str(raw_host), aliases)
        if host_id is None:
            if only_hosts is None or str(raw_host) in only_hosts:
                errors.append({"host": str(raw_host), "role": None, "error": "unknown-host", "detail": f"Unknown host '{raw_host}' in mappings.yaml"})
            continue
        if only_hosts is not None and host_id not in only_hosts:
            continue
        if not isinstance(host_cfg, dict):
            errors.append({"host": host_id, "role": None, "error": "invalid-host-mapping", "detail": f"Mapping for host '{host_id}' must be a YAML mapping"})
            continue

        roles_map = host_cfg.get("roles")
        if roles_map is not None:
            if not isinstance(roles_map, dict):
                errors.append({"host": host_id, "role": None, "error": "invalid-roles-map", "detail": f"'roles' for host '{host_id}' must be a mapping"})
            else:
                for role, r_cfg in roles_map.items():
                    checked += 1
                    if not isinstance(r_cfg, dict):
                        errors.append({"host": host_id, "role": str(role), "error": "invalid-role-entry", "detail": "Role entry must be a mapping"})
                        continue
                    errors.extend(_validate_single_entry(host_id, str(role), r_cfg.get("model"), r_cfg.get("effort"), caveats))

        for role in CANONICAL_ROLES:
            if role in host_cfg:
                checked += 1
                r_cfg = host_cfg[role]
                if not isinstance(r_cfg, dict):
                    errors.append({"host": host_id, "role": role, "error": "invalid-role-entry", "detail": "Role entry must be a mapping"})
                    continue
                errors.extend(_validate_single_entry(host_id, role, r_cfg.get("model"), r_cfg.get("effort"), caveats))

        tiers_map = host_cfg.get("tiers")
        if tiers_map is not None:
            if not isinstance(tiers_map, dict):
                errors.append({"host": host_id, "role": None, "error": "invalid-tiers-map", "detail": f"'tiers' for host '{host_id}' must be a mapping"})
            else:
                for tier_name, t_cfg in tiers_map.items():
                    checked += 1
                    if tier_name == "researcher":
                        errors.append({
                            "host": host_id,
                            "role": "researcher",
                            "error": "researcher-tier-forbidden",
                            "detail": "ADR-017: 'researcher' cannot be configured as a tier",
                        })
                        continue
                    if tier_name not in VALID_TIERS:
                        errors.append({
                            "host": host_id,
                            "role": None,
                            "error": "unknown-tier",
                            "detail": f"Unknown tier '{tier_name}' (expected one of {VALID_TIERS})",
                        })
                        continue
                    if not isinstance(t_cfg, dict):
                        errors.append({"host": host_id, "role": None, "error": "invalid-tier-entry", "detail": "Tier entry must be a mapping"})
                        continue
                    errors.extend(_validate_single_entry(host_id, None, t_cfg.get("model"), t_cfg.get("effort"), caveats))

    return errors, checked


def cmd_validate_mapping(args: argparse.Namespace) -> tuple[dict[str, Any], int]:
    caveats, aliases = load_caveats(Path(args.caveats_dir))

    if args.host is not None:
        host_id = normalize_host_id(args.host, aliases) or args.host
        errs = _validate_single_entry(host_id, args.role, args.model, args.effort, caveats)
        ok = len(errs) == 0
        return {
            "ok": ok,
            "command": "validate-mapping",
            "mode": "inline",
            "host": host_id,
            "role": args.role,
            "errors": errs,
        }, (0 if ok else 2)

    mappings_path = Path(args.mappings) if args.mappings else (Path(args.ssot_root) / "mappings.yaml")
    if not mappings_path.is_file():
        return {
            "ok": False,
            "command": "validate-mapping",
            "mode": "file",
            "mappings_path": str(mappings_path),
            "errors": [{"error": "missing-file", "detail": f"Mappings file not found: {mappings_path}"}],
        }, 2

    try:
        parsed = parse_yaml_subset(read_bounded_text(mappings_path))
    except SsotError as exc:
        return {
            "ok": False,
            "command": "validate-mapping",
            "mode": "file",
            "mappings_path": str(mappings_path),
            "errors": [{"error": exc.code, "detail": exc.detail}],
        }, 2

    if parsed is None:
        parsed = {}
    errs, checked = validate_mappings_data(parsed, caveats, aliases)
    ok = len(errs) == 0
    return {
        "ok": ok,
        "command": "validate-mapping",
        "mode": "file",
        "mappings_path": str(mappings_path),
        "checked_entries": checked,
        "errors": errs,
    }, (0 if ok else 2)


def _parse_hosts_filter(raw_hosts: list[str] | None, aliases: dict[str, str]) -> list[str]:
    if not raw_hosts:
        return list(HOST_LAYOUTS.keys())
    selected: list[str] = []
    for chunk in raw_hosts:
        for part in chunk.split(","):
            token = part.strip()
            if not token:
                continue
            norm = normalize_host_id(token, aliases)
            if norm is None:
                raise SsotError("unknown-host", f"unknown host in --hosts filter: {token}")
            if norm not in selected:
                selected.append(norm)
    return selected


def _load_or_empty_yaml(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    data = parse_yaml_subset(read_bounded_text(path))
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise SsotError("invalid-yaml", f"{path} root must be a YAML mapping")
    return data


def cmd_harvest_legacy(args: argparse.Namespace) -> dict[str, Any]:
    home = Path(args.home)
    ssot_root = Path(args.ssot_root)
    caveats, aliases = load_caveats(Path(args.caveats_dir))
    target_hosts = _parse_hosts_filter(args.hosts, aliases)

    findings: list[dict[str, Any]] = []
    harvested_hosts: dict[str, Any] = {}
    harvested_adapters: list[dict[str, Any]] = []
    preserved_third_party: dict[str, list[str]] = {}
    plan_clients_found: dict[str, str] = {}

    for host_id in target_hosts:
        info = inspect_host(host_id, home)
        if not info["exists"]:
            continue
        root = Path(info["config_root"])
        agents_dir = root / "agents"
        third_party = info["legacy_markers"]["third_party_agents"]
        if third_party:
            preserved_third_party[host_id] = third_party

        host_roles: dict[str, dict[str, Any]] = {}
        if agents_dir.is_dir():
            for role in CANONICAL_ROLES:
                agent_path = agents_dir / f"{role}.md"
                if not agent_path.is_file():
                    continue
                try:
                    fm, _body = split_frontmatter(read_bounded_text(agent_path))
                except SsotError as exc:
                    findings.append({
                        "host": host_id,
                        "role": role,
                        "file": str(agent_path),
                        "kind": "malformed-frontmatter",
                        "code": exc.code,
                        "detail": exc.detail,
                    })
                    continue

                raw_model = fm.get("model")
                raw_effort = fm.get("effort")
                model_val: str | None = None
                effort_val: str | None = None

                if raw_model is not None:
                    m_str, m_err = _check_safe_scalar(raw_model, "model")
                    if m_err:
                        findings.append({
                            "host": host_id,
                            "role": role,
                            "file": str(agent_path),
                            "kind": "invalid-model",
                            "detail": m_err,
                        })
                    elif m_str is not None:
                        if host_id == "cursor" and ("[" in m_str or "]" in m_str):
                            cm = CURSOR_EFFORT_RE.match(m_str)
                            if cm:
                                model_val = cm.group(1).strip()
                                effort_val = cm.group(2).strip()
                            else:
                                findings.append({
                                    "host": host_id,
                                    "role": role,
                                    "file": str(agent_path),
                                    "kind": "malformed-cursor-effort",
                                    "detail": f"Invalid Cursor inline effort syntax in model '{m_str}'",
                                })
                        else:
                            model_val = m_str

                if raw_effort is not None:
                    e_str, e_err = _check_safe_scalar(raw_effort, "effort")
                    if e_err:
                        findings.append({
                            "host": host_id,
                            "role": role,
                            "file": str(agent_path),
                            "kind": "invalid-effort",
                            "detail": e_err,
                        })
                    elif e_str is not None:
                        if effort_val is not None and effort_val != e_str:
                            findings.append({
                                "host": host_id,
                                "role": role,
                                "file": str(agent_path),
                                "kind": "conflicting-effort",
                                "detail": f"Conflicting inline '{effort_val}' and top-level '{e_str}'",
                            })
                        else:
                            effort_val = e_str

                if role == "researcher":
                    if model_val is not None or effort_val is not None:
                        findings.append({
                            "host": host_id,
                            "role": "researcher",
                            "file": str(agent_path),
                            "kind": "invalid-researcher-pin",
                            "detail": "ADR-017: researcher must not carry model or effort; omitted from harvested mappings",
                        })
                    continue

                if model_val == "inherit" and host_id != "antigravity":
                    model_val = None

                entry_errors = _validate_single_entry(host_id, role, model_val, effort_val, caveats)
                if entry_errors:
                    for e in entry_errors:
                        findings.append({
                            "host": host_id,
                            "role": role,
                            "file": str(agent_path),
                            "kind": e["error"],
                            "detail": e["detail"],
                        })
                    # Drop only the invalid fields so valid model survives if only effort was unsupported
                    filtered_errs_no_eff = _validate_single_entry(host_id, role, model_val, None, caveats)
                    if not filtered_errs_no_eff and effort_val is not None:
                        effort_val = None
                    else:
                        continue

                if model_val is not None or effort_val is not None:
                    role_rec: dict[str, Any] = {}
                    if model_val is not None:
                        role_rec["model"] = model_val
                    if effort_val is not None:
                        role_rec["effort"] = effort_val
                    role_rec["provenance"] = "harvested"
                    host_roles[role] = role_rec

        # Harvest jaiba-configure.yaml
        cfg_file = root / "jaiba-configure.yaml"
        if cfg_file.is_file():
            try:
                legacy_cfg = parse_yaml_subset(read_bounded_text(cfg_file))
                if not isinstance(legacy_cfg, dict):
                    raise SsotError("invalid-yaml", "jaiba-configure.yaml root must be a mapping")
                if "native-plan-client" in legacy_cfg:
                    npc = legacy_cfg["native-plan-client"]
                    if isinstance(npc, str) and npc in VALID_NATIVE_PLAN_CLIENTS:
                        plan_clients_found[host_id] = npc
                    else:
                        findings.append({
                            "host": host_id,
                            "file": str(cfg_file),
                            "kind": "invalid-native-plan-client",
                            "detail": f"Expected one of {VALID_NATIVE_PLAN_CLIENTS}, got {npc!r}",
                        })
            except SsotError as exc:
                findings.append({
                    "host": host_id,
                    "file": str(cfg_file),
                    "kind": "malformed-jaiba-configure-yaml",
                    "code": exc.code,
                    "detail": exc.detail,
                })

        # Harvest memory-surface adapters from <host>/skills/*/SKILL.md
        skills_dir = root / "skills"
        if skills_dir.is_dir():
            try:
                skill_dirs = sorted(skills_dir.iterdir(), key=lambda p: p.name)
            except OSError:
                skill_dirs = []
            for sdir in skill_dirs:
                if not sdir.is_dir():
                    continue
                skill_md = sdir / "SKILL.md"
                if not skill_md.is_file():
                    continue
                try:
                    sfm, _ = split_frontmatter(read_bounded_text(skill_md))
                except SsotError as exc:
                    findings.append({
                        "host": host_id,
                        "file": str(skill_md),
                        "kind": "malformed-skill-frontmatter",
                        "code": exc.code,
                        "detail": exc.detail,
                    })
                    continue
                category = sfm.get("category")
                if category in ("memory-surface", "memory-surface-draft"):
                    adapter_rec = {
                        "adapter-id": str(sfm.get("adapter-id") or sfm.get("name") or sdir.name),
                        "name": str(sfm.get("name") or sdir.name),
                        "category": str(category),
                        "version": str(sfm.get("version") or "unknown"),
                        "contract-id": str(sfm.get("contract-id") or ""),
                        "contract-version": str(sfm.get("contract-version") or ""),
                        "source-host": host_id,
                        "source-path": portable_home_str(sdir, home, trailing_slash=False),
                    }
                    harvested_adapters.append(adapter_rec)

        markers = info["legacy_markers"]
        has_legacy = (
            markers["jaiba_contract"]
            or markers["jaiba_configure_yaml"]
            or markers["jaiba_agents_count"] > 0
        )
        harvested_hosts[host_id] = {
            "portable_config_root": info["portable_config_root"],
            "has_legacy_markers": has_legacy,
            "native_plan_client": plan_clients_found.get(host_id),
            "roles": host_roles,
        }

    # Build merged config.yaml and mappings.yaml structures
    config_path = ssot_root / "config.yaml"
    mappings_path = ssot_root / "mappings.yaml"
    existing_cfg = _load_or_empty_yaml(config_path)
    existing_map = _load_or_empty_yaml(mappings_path)

    merged_cfg: dict[str, Any] = dict(existing_cfg)
    merged_cfg.setdefault("schema_version", 1)

    npc_values = set(plan_clients_found.values())
    if "native-plan-client" not in merged_cfg:
        if len(npc_values) == 1:
            merged_cfg["native-plan-client"] = next(iter(npc_values))
        else:
            merged_cfg["native-plan-client"] = "auto"

    cfg_hosts = dict(merged_cfg.get("hosts") or {})
    for host_id, hdata in harvested_hosts.items():
        prev = dict(cfg_hosts.get(host_id) or {})
        if "enabled" not in prev:
            prev["enabled"] = bool(hdata["has_legacy_markers"])
        prev.setdefault("config-root", hdata["portable_config_root"])
        if hdata["native_plan_client"] is not None:
            prev["native-plan-client"] = hdata["native_plan_client"]
        cfg_hosts[host_id] = prev
    merged_cfg["hosts"] = cfg_hosts

    if harvested_adapters:
        existing_adapters = list(merged_cfg.get("memory-adapters") or [])
        seen_keys = {
            (a.get("adapter-id"), a.get("version"), a.get("source-host"))
            for a in existing_adapters
            if isinstance(a, dict)
        }
        for ad in harvested_adapters:
            key = (ad["adapter-id"], ad["version"], ad["source-host"])
            if key not in seen_keys:
                existing_adapters.append(ad)
                seen_keys.add(key)
        merged_cfg["memory-adapters"] = existing_adapters

    merged_map: dict[str, Any] = dict(existing_map)
    merged_map.setdefault("schema_version", 1)
    map_hosts = dict(merged_map.get("hosts") or {})
    for host_id, hdata in harvested_hosts.items():
        if not hdata["roles"]:
            continue
        prev_h = dict(map_hosts.get(host_id) or {})
        prev_roles = dict(prev_h.get("roles") or {})
        for role, r_rec in hdata["roles"].items():
            prev_roles[role] = r_rec
        prev_h["roles"] = prev_roles
        map_hosts[host_id] = prev_h
    merged_map["hosts"] = map_hosts
    merged_map.setdefault("tier-affinity", {})
    merged_map.setdefault("cross-agent-bridge", {})

    written_files: list[str] = []
    if args.write:
        ssot_root.mkdir(parents=True, exist_ok=True)
        atomic_write_text(config_path, dump_yaml(merged_cfg, force_quote_keys={"native-plan-client"}))
        atomic_write_text(mappings_path, dump_yaml(merged_map))
        written_files = [str(config_path), str(mappings_path)]

    return {
        "ok": True,
        "command": "harvest-legacy",
        "write": bool(args.write),
        "written_files": written_files,
        "harvested_hosts": harvested_hosts,
        "memory_adapters": harvested_adapters,
        "preserved_third_party": preserved_third_party,
        "findings": findings,
        "proposed_config": merged_cfg,
        "proposed_mappings": merged_map,
    }


def _synthesize_frontmatter(
    role: str,
    base_fm: dict[str, Any],
    host_id: str,
    caveat: dict[str, Any],
    model: str | None,
    effort: str | None,
) -> tuple[dict[str, Any], set[str]]:
    description = str(base_fm.get("description") or "")
    requires = base_fm.get("requires")
    flavor = str(caveat.get("frontmatter_flavor") or "standard")
    emits_mode = bool(caveat.get("emits_mode_subagent")) or flavor == "opencode"
    emits_perm = bool(caveat.get("emits_permission_map")) or flavor == "opencode"
    emits_name = caveat.get("emits_name", True)
    emits_requires = caveat.get("emits_requires", True)

    eff_model: str | None = None
    eff_effort: str | None = None
    if role != "researcher" and model is not None and model != "inherit":
        eff_model = model
        if effort is not None and str(caveat.get("effort_syntax") or "none") != "none":
            eff_effort = effort

    out: dict[str, Any] = {}
    quote_keys: set[str] = set()

    if emits_mode and emits_perm:
        # OpenCode native projection
        out["description"] = description
        quote_keys.add("description")
        out["mode"] = "subagent"
        if eff_model is not None:
            out["model"] = eff_model
        perms_all = caveat.get("permissions_by_role") or {}
        if not isinstance(perms_all, dict) or role not in perms_all:
            raise SsotError("missing-permission-map", f"OpenCode caveat missing permissions_by_role for '{role}'")
        out["permission"] = perms_all[role]
        return out, quote_keys

    if emits_name:
        out["name"] = str(base_fm.get("name") or role)
    out["description"] = description
    if emits_requires and isinstance(requires, list) and requires:
        out["requires"] = requires

    if eff_model is not None:
        if host_id == "cursor" and eff_effort is not None:
            out["model"] = f"{eff_model}[effort={eff_effort}]"
        else:
            out["model"] = eff_model
            if host_id == "claude-code" and eff_effort is not None:
                out["effort"] = eff_effort

    return out, quote_keys


def _unique_backup_path(target: Path, today_str: str) -> Path:
    candidate = Path(f"{target}.bak-{today_str}")
    if not candidate.exists():
        return candidate
    idx = 1
    while True:
        numbered = Path(f"{target}.bak-{today_str}.{idx}")
        if not numbered.exists():
            return numbered
        idx += 1


def _resolve_base_agents_dir(args: argparse.Namespace) -> Path:
    if args.base_agents_dir:
        return Path(args.base_agents_dir)
    ssot_base = Path(args.ssot_root) / "agents" / "base"
    if ssot_base.is_dir():
        return ssot_base
    return Path(__file__).resolve().parent.parent / "assets" / "agents"


def cmd_project(args: argparse.Namespace) -> tuple[dict[str, Any], int]:
    home = Path(args.home)
    ssot_root = Path(args.ssot_root)
    caveats, aliases = load_caveats(Path(args.caveats_dir))
    base_agents_dir = _resolve_base_agents_dir(args)

    config_path = Path(args.config) if args.config else (ssot_root / "config.yaml")
    if not config_path.is_file():
        return {
            "ok": False,
            "command": "project",
            "errors": [{"error": "missing-config", "detail": f"Config file not found: {config_path}"}],
        }, 2

    try:
        config_data = parse_yaml_subset(read_bounded_text(config_path))
    except SsotError as exc:
        return {
            "ok": False,
            "command": "project",
            "errors": [{"error": exc.code, "detail": exc.detail}],
        }, 2

    if not isinstance(config_data, dict):
        return {
            "ok": False,
            "command": "project",
            "errors": [{"error": "invalid-config", "detail": "config.yaml root must be a YAML mapping"}],
        }, 2

    mappings_path = Path(args.mappings) if args.mappings else (ssot_root / "mappings.yaml")
    if args.mappings and not mappings_path.is_file():
        return {
            "ok": False,
            "command": "project",
            "errors": [{"error": "missing-mappings", "detail": f"Mappings file not found: {mappings_path}"}],
        }, 2

    if mappings_path.is_file():
        try:
            mappings_data = parse_yaml_subset(read_bounded_text(mappings_path)) or {}
        except SsotError as exc:
            return {
                "ok": False,
                "command": "project",
                "errors": [{"error": exc.code, "detail": exc.detail}],
            }, 2
    else:
        mappings_data = {}

    cfg_hosts = config_data.get("hosts")
    if not isinstance(cfg_hosts, dict):
        return {
            "ok": False,
            "command": "project",
            "errors": [{"error": "invalid-config", "detail": "config.yaml must define a 'hosts' mapping"}],
        }, 2

    enabled_hosts: list[tuple[str, Path]] = []
    disabled_hosts: list[str] = []
    for raw_host, h_cfg in cfg_hosts.items():
        host_id = normalize_host_id(str(raw_host), aliases)
        if host_id is None or host_id not in caveats:
            return {
                "ok": False,
                "command": "project",
                "errors": [{"error": "unknown-host", "detail": f"Unknown host '{raw_host}' in config.yaml"}],
            }, 2
        if not isinstance(h_cfg, dict):
            return {
                "ok": False,
                "command": "project",
                "errors": [{"error": "invalid-config", "detail": f"Host entry '{raw_host}' must be a mapping"}],
            }, 2
        if h_cfg.get("enabled") is True:
            raw_root = h_cfg.get("config-root") or h_cfg.get("config_root")
            if isinstance(raw_root, str) and raw_root.strip():
                h_root = resolve_home_path(raw_root.strip(), home)
            else:
                h_root = host_root_from_layout(host_id, home)
            enabled_hosts.append((host_id, h_root))
        else:
            disabled_hosts.append(host_id)

    enabled_ids = {hid for hid, _ in enabled_hosts}
    # Fail-closed validation of all enabled hosts BEFORE writing anything
    val_errors, _checked = validate_mappings_data(mappings_data, caveats, aliases, only_hosts=enabled_ids)
    if val_errors:
        return {
            "ok": False,
            "command": "project",
            "errors": val_errors,
        }, 2

    # Load all 7 canonical base agent templates before writing anything
    base_templates: dict[str, tuple[dict[str, Any], str]] = {}
    for role in CANONICAL_ROLES:
        tpl_path = base_agents_dir / f"{role}.md"
        if not tpl_path.is_file():
            return {
                "ok": False,
                "command": "project",
                "errors": [{"error": "missing-base-template", "detail": f"Base template not found: {tpl_path}"}],
            }, 2
        base_templates[role] = split_frontmatter(read_bounded_text(tpl_path))

    # Ensure SSOT contract exists (seed from packaged asset if absent)
    ssot_contract = ssot_root / "contract" / "jaiba-contract.md"
    packaged_contract = Path(__file__).resolve().parent.parent / "assets" / "jaiba-contract.md"
    seeded_contract = False
    if not ssot_contract.is_file():
        if not packaged_contract.is_file():
            return {
                "ok": False,
                "command": "project",
                "errors": [{"error": "missing-contract", "detail": f"Contract not found at {ssot_contract} or {packaged_contract}"}],
            }, 2
        contract_text = read_bounded_text(packaged_contract)
        if not args.dry_run:
            atomic_write_text(ssot_contract, contract_text)
        seeded_contract = True
    else:
        contract_text = read_bounded_text(ssot_contract)

    today_str = dt.date.today().isoformat()
    map_hosts = mappings_data.get("hosts") if isinstance(mappings_data, dict) else {}
    if not isinstance(map_hosts, dict):
        map_hosts = {}

    # Resolve host mappings considering alias keys in mappings.yaml too
    resolved_map_by_host: dict[str, dict[str, Any]] = {}
    for raw_k, val in map_hosts.items():
        norm_k = normalize_host_id(str(raw_k), aliases)
        if norm_k and isinstance(val, dict):
            resolved_map_by_host[norm_k] = val

    host_reports: list[dict[str, Any]] = []
    for host_id, h_root in enabled_hosts:
        caveat = caveats[host_id]
        h_map = resolved_map_by_host.get(host_id, {})
        agents_dir = h_root / "agents"
        agent_actions: list[dict[str, Any]] = []
        backups: list[str] = []

        for role in CANONICAL_ROLES:
            base_fm, body = base_templates[role]
            model_val, effort_val = _resolve_role_mapping(h_map, role)
            proj_fm, quote_keys = _synthesize_frontmatter(role, base_fm, host_id, caveat, model_val, effort_val)
            rendered = render_markdown(proj_fm, body, force_quote_keys=quote_keys)
            target_file = agents_dir / f"{role}.md"

            if target_file.is_file() and not target_file.is_symlink():
                existing_text = target_file.read_text(encoding="utf-8", errors="replace")
                if existing_text == rendered:
                    agent_actions.append({"role": role, "path": str(target_file), "action": "unchanged"})
                    continue
                if args.backup:
                    bak_path = _unique_backup_path(target_file, today_str)
                    if not args.dry_run:
                        atomic_write_text(bak_path, existing_text)
                    backups.append(str(bak_path))
                action = "updated"
            else:
                action = "created"

            if not args.dry_run:
                atomic_write_text(target_file, rendered)
            agent_actions.append({"role": role, "path": str(target_file), "action": action})

        # Contract projection
        target_contract = h_root / "jaiba-contract.md"
        desired_mode = args.contract_mode
        contract_report: dict[str, Any] = {"path": str(target_contract), "mode": desired_mode}

        if desired_mode == "symlink":
            already_linked = False
            if target_contract.is_symlink():
                try:
                    if Path(os.readlink(target_contract)) == ssot_contract or target_contract.resolve() == ssot_contract.resolve():
                        already_linked = True
                except OSError:
                    already_linked = False
            if already_linked:
                contract_report["action"] = "unchanged"
            else:
                if target_contract.is_file() and not target_contract.is_symlink():
                    existing_c = target_contract.read_text(encoding="utf-8", errors="replace")
                    if existing_c != contract_text and args.backup:
                        bak_c = _unique_backup_path(target_contract, today_str)
                        if not args.dry_run:
                            atomic_write_text(bak_c, existing_c)
                        backups.append(str(bak_c))
                if not args.dry_run:
                    try:
                        atomic_symlink(ssot_contract, target_contract)
                        contract_report["action"] = "symlinked"
                        contract_report["target"] = str(ssot_contract)
                    except OSError as exc:
                        atomic_write_text(target_contract, contract_text)
                        contract_report["action"] = "copied-fallback"
                        contract_report["fallback_reason"] = str(exc)
                else:
                    contract_report["action"] = "would-symlink"
                    contract_report["target"] = str(ssot_contract)
        else:
            if target_contract.is_file() and not target_contract.is_symlink():
                existing_c = target_contract.read_text(encoding="utf-8", errors="replace")
                if existing_c == contract_text:
                    contract_report["action"] = "unchanged"
                else:
                    if args.backup:
                        bak_c = _unique_backup_path(target_contract, today_str)
                        if not args.dry_run:
                            atomic_write_text(bak_c, existing_c)
                        backups.append(str(bak_c))
                    if not args.dry_run:
                        atomic_write_text(target_contract, contract_text)
                    contract_report["action"] = "copied"
            else:
                if not args.dry_run:
                    atomic_write_text(target_contract, contract_text)
                contract_report["action"] = "copied"

        host_reports.append({
            "host_id": host_id,
            "config_root": str(h_root),
            "agents": agent_actions,
            "contract": contract_report,
            "backups": backups,
        })

    return {
        "ok": True,
        "command": "project",
        "dry_run": bool(args.dry_run),
        "seeded_ssot_contract": seeded_contract,
        "enabled_hosts": [hid for hid, _ in enabled_hosts],
        "disabled_hosts_untouched": disabled_hosts,
        "projections": host_reports,
    }, 0


def build_parser() -> argparse.ArgumentParser:
    default_caveats = str(Path(__file__).resolve().parent.parent / "references" / "caveats")

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--home", default=argparse.SUPPRESS, help="Override home directory (default: Path.home())")
    common.add_argument("--ssot-root", default=argparse.SUPPRESS, help="Override SSOT root (default: <home>/.jaiba)")
    common.add_argument("--caveats-dir", default=argparse.SUPPRESS, help="Override caveats directory")
    common.add_argument("--base-agents-dir", default=argparse.SUPPRESS, help="Override base agent templates directory")
    common.add_argument("--json", action="store_true", default=argparse.SUPPRESS, help="Emit JSON output (default)")

    parser = argparse.ArgumentParser(description="JAIBA Global SSOT host manager (pure Python 3 stdlib)")
    parser.add_argument("--home", default=None, help="Override home directory (default: Path.home())")
    parser.add_argument("--ssot-root", default=None, help="Override SSOT root (default: <home>/.jaiba)")
    parser.add_argument("--caveats-dir", default=default_caveats, help="Override caveats directory")
    parser.add_argument("--base-agents-dir", default=None, help="Override base agent templates directory")
    parser.add_argument("--json", action="store_true", help="Emit JSON output (default)")

    sub = parser.add_subparsers(dest="subcommand", required=True)

    sub.add_parser("detect-hosts", parents=[common], help="Detect known host config roots and JAIBA legacy markers")

    p_harvest = sub.add_parser("harvest-legacy", parents=[common], help="Harvest legacy per-host configs safely")
    p_harvest.add_argument("--hosts", nargs="*", default=None, help="Optional host filter (comma-separated or multiple)")
    p_harvest.add_argument("--write", action="store_true", help="Atomically write/merge config.yaml and mappings.yaml")

    p_val = sub.add_parser("validate-mapping", parents=[common], help="Validate host model/effort mappings against caveats")
    p_val.add_argument("--mappings", default=None, help="Path to mappings.yaml (default: <ssot-root>/mappings.yaml)")
    p_val.add_argument("--host", default=None, help="Inline host ID to validate")
    p_val.add_argument("--role", default=None, help="Inline role name to validate")
    p_val.add_argument("--model", default=None, help="Inline model ID to validate")
    p_val.add_argument("--effort", default=None, help="Inline effort value to validate")

    p_proj = sub.add_parser("project", parents=[common], help="Project host-native subagents and contract links to enabled hosts")
    p_proj.add_argument("--config", default=None, help="Path to config.yaml (default: <ssot-root>/config.yaml)")
    p_proj.add_argument("--mappings", default=None, help="Path to mappings.yaml (default: <ssot-root>/mappings.yaml)")
    p_proj.add_argument("--dry-run", action="store_true", help="Compute projection without writing files")
    p_proj.add_argument("--backup", action=argparse.BooleanOptionalAction, default=True, help="Back up differing JAIBA files before overwrite")
    p_proj.add_argument("--contract-mode", choices=("symlink", "copy"), default="symlink", help="How to project jaiba-contract.md")

    return parser


def main(argv: list[str] | None = None) -> int:
    import json

    parser = build_parser()
    args = parser.parse_args(argv)
    home = Path(args.home) if args.home else Path.home()
    args.home = str(home)
    if not args.ssot_root:
        args.ssot_root = str(home / ".jaiba")

    try:
        if args.subcommand == "detect-hosts":
            payload, code = cmd_detect_hosts(args), 0
        elif args.subcommand == "harvest-legacy":
            payload, code = cmd_harvest_legacy(args), 0
        elif args.subcommand == "validate-mapping":
            payload, code = cmd_validate_mapping(args)
        elif args.subcommand == "project":
            payload, code = cmd_project(args)
        else:
            raise SsotError("unknown-subcommand", f"unsupported subcommand: {args.subcommand}")
    except SsotError as exc:
        payload = {"ok": False, "error": exc.code, "detail": exc.detail}
        if exc.evidence:
            payload["evidence"] = exc.evidence
        code = 2

    sys.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
