"""Fail-closed guards for corrupt-chunk and symlink-root regressions.

Stdlib only. This is not a backend client and not a conformance claim.
Callers import these functions directly.
"""
from __future__ import annotations

import hashlib
import os
import stat
from pathlib import Path


class GuardRejected(Exception):
    """A specific guard refused the operation before any destination write."""

    def __init__(self, code: str, detail: str = ""):
        self.code = code
        self.detail = detail
        super().__init__(f"{code}: {detail}" if detail else code)


def accept_chunk_or_reject(payload: bytes, declared_sha256: str, destination: Path) -> None:
    """Accept a chunk only when its bytes match the declared digest.

    On mismatch this raises ``digest-mismatch`` and does not create, open, or
    write ``destination``. A match may exclusive-create the destination; the
    regression path never matches.
    """
    if not isinstance(payload, (bytes, bytearray)):
        raise GuardRejected("invalid-object", "chunk payload must be bytes")
    if not isinstance(declared_sha256, str) or len(declared_sha256) != 64:
        raise GuardRejected("invalid-object", "declared digest must be 64 hex characters")
    payload = bytes(payload)
    destination = Path(destination)
    actual = hashlib.sha256(payload).hexdigest()
    if actual != declared_sha256:
        raise GuardRejected(
            "digest-mismatch",
            "chunk sha256 does not match declared digest; destination not written",
        )
    destination.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(destination, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
    try:
        os.write(fd, payload)
    finally:
        os.close(fd)


def reject_symlink_root(root: Path) -> None:
    """Reject a symlink destination before any write. Does not follow the link."""
    root = Path(root)
    try:
        info = root.lstat()
    except FileNotFoundError as exc:
        raise GuardRejected("invalid-object", "destination root is absent") from exc
    if stat.S_ISLNK(info.st_mode):
        raise GuardRejected("invalid-object", "symlink root rejected before write")
    if not stat.S_ISDIR(info.st_mode):
        raise GuardRejected("invalid-object", "destination root is not a real directory")


def write_exclusive(root: Path, name: str, payload: bytes) -> Path:
    """Exclusive-create ``name`` under a real directory root.

    A symlink root is ``invalid-object``. The link is not followed and no
    payload is created. This is the filesystem-surface escape check for a
    migration destination, not a backend call.
    """
    if not isinstance(payload, (bytes, bytearray)):
        raise GuardRejected("invalid-object", "payload must be bytes")
    relative = Path(name)
    if relative.is_absolute() or ".." in relative.parts or relative == Path("."):
        raise GuardRejected("invalid-object", "payload name escapes the destination root")
    reject_symlink_root(root)
    target = Path(root) / relative
    fd = os.open(target, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
    try:
        os.write(fd, bytes(payload))
    finally:
        os.close(fd)
    return target
