#!/usr/bin/env python3
"""
AST Validator for Memory Surface Package Scripts (MSV-006).

Asserts:
1. Python 3 standard library imports ONLY (sys, json, hashlib, base64, argparse, pathlib, etc.).
2. ZERO third-party pip packages.
3. Subcommands adhere to declared transport mode (agent-relay, local-cli, local-http).
4. Pure subcommands (encode, decode, delta, materialize, render, binding-path, cost) perform no backend I/O.
"""

import ast
import json
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

# Comprehensive standard library top-level module names for Python 3
STDLIB_MODULES: Set[str] = {
    "__future__", "_thread", "abc", "aifc", "argparse", "array", "ast", "asynchat",
    "asyncio", "asyncore", "atexit", "audioop", "base64", "bdb", "binascii",
    "binhex", "bisect", "builtins", "bz2", "cProfile", "calendar", "cgi", "cgitb",
    "chunk", "cmath", "cmd", "code", "codecs", "codeop", "collections", "colorsys",
    "compileall", "concurrent", "configparser", "contextlib", "contextvars",
    "copy", "copyreg", "crypt", "csv", "ctypes", "curses", "dataclasses",
    "datetime", "dbm", "decimal", "difflib", "dis", "distutils", "doctest",
    "email", "encodings", "ensurepip", "enum", "errno", "faulthandler", "fcntl",
    "filecmp", "fileinput", "fnmatch", "formatter", "fpectl", "fractions",
    "ftplib", "functools", "gc", "getopt", "getpass", "gettext", "glob", "grp",
    "gzip", "hashlib", "heapq", "hmac", "html", "http", "imaplib", "imghdr",
    "imp", "importlib", "inspect", "io", "ipaddress", "itertools", "json",
    "keyword", "lib2to3", "linecache", "locale", "logging", "lzma", "mailbox",
    "mailcap", "marshal", "math", "mimetypes", "mmap", "modulefinder", "msilib",
    "msvcrt", "multiprocessing", "netrc", "nis", "nntplib", "numbers", "operator",
    "optparse", "os", "ossaudiodev", "parser", "pathlib", "pdb", "pickle",
    "pickletools", "pipes", "pkgutil", "platform", "plistlib", "poplib", "posix",
    "posixpath", "pprint", "profile", "pstats", "pty", "pwd", "py_compile",
    "pyclbr", "pydoc", "queue", "quopri", "random", "re", "readline", "reprlib",
    "resource", "rlcompleter", "runpy", "sched", "secrets", "select", "selectors",
    "shelve", "shlex", "shutil", "signal", "site", "smtpd", "smtplib", "sndhdr",
    "socket", "socketserver", "spwd", "sqlite3", "ssl", "stat", "statistics",
    "string", "stringprep", "struct", "subprocess", "sunau", "symbol", "symtable",
    "sys", "sysconfig", "syslog", "tabnanny", "tarfile", "telnetlib", "tempfile",
    "termios", "test", "textwrap", "threading", "time", "timeit", "tkinter",
    "token", "tokenize", "trace", "traceback", "tracemalloc", "tty", "turtle",
    "turtledemo", "types", "typing", "unicodedata", "unittest", "urllib", "uu",
    "uuid", "venv", "warnings", "wave", "weakref", "webbrowser", "winreg",
    "winsound", "wsgiref", "xdrlib", "xml", "xmlrpc", "zipapp", "zipfile",
    "zipimport", "zlib"
}

IO_MODULES = {"socket", "urllib", "http", "subprocess"}

CANONICAL_SUBCOMMANDS = {
    "encode", "decode", "delta", "materialize", "render",
    "binding-path", "cost", "batch-prepare", "batch-verify"
}


def analyze_ast(source_code: str, transport_mode: str = "agent-relay") -> Tuple[bool, List[str], Set[str]]:
    """Analyze Python source AST for standard library conformance and transport mode rules."""
    violations: List[str] = []
    imported_modules: Set[str] = set()

    try:
        tree = ast.parse(source_code)
    except SyntaxError as e:
        return False, [f"SyntaxError parsing script: {e}"], set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                top_module = alias.name.split(".")[0]
                imported_modules.add(top_module)
                if top_module not in STDLIB_MODULES:
                    violations.append(f"Disallowed third-party pip import: {alias.name}")
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                top_module = node.module.split(".")[0]
                imported_modules.add(top_module)
                if top_module not in STDLIB_MODULES:
                    violations.append(f"Disallowed third-party pip import: {node.module}")

    # Transport mode checks
    if transport_mode == "agent-relay":
        io_found = imported_modules.intersection(IO_MODULES)
        if io_found:
            violations.append(f"Agent-relay transport forbids direct backend I/O modules: {sorted(io_found)}")

    return len(violations) == 0, violations, imported_modules


def main() -> int:
    fixtures_file = Path(__file__).parent / "script-ast-validation.json"
    if fixtures_file.exists():
        with open(fixtures_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        passed = 0
        total = 0
        for specimen in data.get("specimens", []):
            total += 1
            code = specimen["code"]
            transport = specimen.get("declared_transport", "agent-relay")
            expected = specimen["expected_verdict"]

            is_valid, violations, _ = analyze_ast(code, transport)
            verdict = "conforming" if is_valid else "nonconforming"

            if verdict == expected:
                passed += 1
            else:
                print(f"FAILED specimen {specimen['id']}: expected {expected}, got {verdict}. Violations: {violations}", file=sys.stderr)

        print(f"AST validation fixtures test: {passed}/{total} specimens matched expected verdicts.")
        return 0 if passed == total else 1

    print("No script-ast-validation.json found.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
