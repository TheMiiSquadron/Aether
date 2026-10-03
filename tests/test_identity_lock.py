from __future__ import annotations

import multiprocessing
import os
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from aether.identity_lock import identity_file_lock


def _hold_lock(path, ready, release) -> None:
    with identity_file_lock(Path(path)):
        ready.set()
        release.wait(timeout=20)


class IdentityLockTests(unittest.TestCase):
    def test_exception_releases_lock_and_keeps_stable_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "identity.lock"
            with self.assertRaises(ValueError):
                with identity_file_lock(path):
                    raise ValueError("simulated failure")
            before = path.stat().st_ino
            with identity_file_lock(path):
                self.assertEqual(path.stat().st_ino, before)
            self.assertTrue(path.exists())

    def test_process_exit_releases_lock(self) -> None:
        context = multiprocessing.get_context("spawn")
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "identity.lock"
            ready = context.Event()
            release = context.Event()
            process = context.Process(target=_hold_lock, args=(str(path), ready, release))
            process.start()
            try:
                self.assertTrue(ready.wait(timeout=15))
                process.terminate()
                process.join(timeout=5)
                self.assertFalse(process.is_alive())
                with identity_file_lock(path):
                    self.assertTrue(path.exists())
            finally:
                if process.is_alive():
                    process.terminate()
                process.join(timeout=5)

    def test_windows_adapter_locks_first_byte_and_closes_descriptor(self) -> None:
        # Contract check only; native Windows behavior still needs Windows CI.
        fake_msvcrt = SimpleNamespace(LK_LOCK=1, locking=Mock())
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "identity.lock"
            with (
                patch("aether.identity_lock.os.name", "nt"),
                patch.dict(sys.modules, {"msvcrt": fake_msvcrt}),
            ):
                with identity_file_lock(path):
                    fd, mode, length = fake_msvcrt.locking.call_args.args
                    self.assertEqual((mode, length), (fake_msvcrt.LK_LOCK, 1))
                    self.assertEqual(os.lseek(fd, 0, os.SEEK_CUR), 0)
            with self.assertRaises(OSError):
                os.fstat(fd)


if __name__ == "__main__":
    unittest.main()
