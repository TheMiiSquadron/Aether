"""OS-backed locking for the Foundation local file identity store."""

from __future__ import annotations

import os
import stat
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path


@contextmanager
def identity_file_lock(path: Path) -> Iterator[None]:
    """Lock a stable file; never unlink it or replace its inode.

    Closing the descriptor releases the OS lock, including on process exit.
    Windows LK_LOCK retries for a bounded interval, then raises OSError.
    This requires a local filesystem with working OS file locks.
    """

    flags = os.O_CREAT | os.O_RDWR | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(path, flags, 0o600)
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
            raise OSError("Unsafe identity lock file type")
        if os.name == "posix" and info.st_uid != os.getuid():
            raise OSError("Unsafe identity lock file ownership")
        if os.name == "posix":
            import fcntl

            fcntl.flock(fd, fcntl.LOCK_EX)
        elif os.name == "nt":
            import msvcrt

            os.lseek(fd, 0, os.SEEK_SET)
            msvcrt.locking(fd, msvcrt.LK_LOCK, 1)
        else:
            raise OSError("Unsupported identity file locking platform")
        yield
    finally:
        os.close(fd)
