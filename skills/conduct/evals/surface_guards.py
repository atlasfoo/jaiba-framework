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


def _safe_write_exclusive(target: Path, payload: bytes) -> None:
    """Exclusive write all payload bytes to target with loop and cleanup on error."""
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(target, flags, 0o644)
    written_successfully = False
    try:
        total = 0
        while total < len(payload):
            n = os.write(fd, payload[total:])
            if n == 0:
                raise OSError("write returned 0 bytes before payload completed")
            total += n
        os.fsync(fd)
        written_successfully = True
    finally:
        os.close(fd)
        if not written_successfully:
            try:
                target.unlink(missing_ok=True)
            except OSError:
                pass
    if target.stat().st_size != len(payload):
        target.unlink(missing_ok=True)
        raise OSError("written file size does not match accepted payload length")


def accept_chunk_or_reject(payload: bytes, declared_sha256: str, destination: Path) -> None:
    """Accept a chunk only when its bytes match the declared digest.

    On mismatch this raises ``digest-mismatch`` and does not create, open, or
    write ``destination``. A match may exclusive-create the destination; the
    regression path never matches. On short write or write error, any partially
    written destination is removed.
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
    try:
        dest_info = destination.lstat()
        if stat.S_ISLNK(dest_info.st_mode):
            raise GuardRejected("invalid-object", "destination is a symlink")
    except FileNotFoundError:
        pass

    destination.parent.mkdir(parents=True, exist_ok=True)
    if stat.S_ISLNK(destination.parent.lstat().st_mode):
        raise GuardRejected("invalid-object", "destination parent is a symlink")

    _safe_write_exclusive(destination, payload)


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

    A symlink root or intermediate symlink component is ``invalid-object``.
    Symlinks are not followed and no payload is created outside the root.
    All payload bytes are written completely, or the destination is cleaned up.
    """
    if not isinstance(payload, (bytes, bytearray)):
        raise GuardRejected("invalid-object", "payload must be bytes")
    payload = bytes(payload)
    relative = Path(name)
    if relative.is_absolute() or ".." in relative.parts or relative == Path("."):
        raise GuardRejected("invalid-object", "payload name escapes the destination root")
    if any(p in ("", ".", "..") for p in relative.parts):
        raise GuardRejected("invalid-object", "payload name contains invalid path components")

    reject_symlink_root(root)
    root = Path(root)

    # Check each intermediate path component for symlinks before writing
    current = root
    for part in relative.parts[:-1]:
        current = current / part
        try:
            info = current.lstat()
        except FileNotFoundError:
            try:
                os.mkdir(current, 0o755)
            except FileExistsError:
                pass
            info = current.lstat()
        if stat.S_ISLNK(info.st_mode):
            raise GuardRejected("invalid-object", f"path component '{part}' is a symlink")
        if not stat.S_ISDIR(info.st_mode):
            raise GuardRejected("invalid-object", f"path component '{part}' is not a directory")

    target = current / relative.parts[-1]
    try:
        target_info = target.lstat()
        if stat.S_ISLNK(target_info.st_mode):
            raise GuardRejected("invalid-object", "destination target is a symlink")
    except FileNotFoundError:
        pass

    _safe_write_exclusive(target, payload)
    return target
