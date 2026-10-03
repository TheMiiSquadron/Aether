from __future__ import annotations

import json
import multiprocessing
import os
import stat
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from aether.identity import DeviceIdentityError, encode_base64url
from aether.identity_store import FileIdentityStore


def _initialize_concurrently(identity_dir, barrier, results) -> None:
    class SlowStore(FileIdentityStore):
        def _persist(self, identity):
            # Widen the old race window while all processes start together.
            time.sleep(0.15)
            super()._persist(identity)

    try:
        barrier.wait(timeout=15)
        identity = SlowStore(Path(identity_dir)).load_or_create()
        results.put(identity.public_identity.device_id)
    except Exception as exc:
        results.put(type(exc).__name__)


class FileIdentityStoreTests(unittest.TestCase):
    def test_first_launch_creates_and_restart_reuses_identity(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            store = FileIdentityStore(Path(temp_dir) / "identity")

            first_identity = store.load_or_create().public_identity
            second_identity = FileIdentityStore(Path(temp_dir) / "identity").load_or_create()

        self.assertEqual(first_identity.device_id, second_identity.public_identity.device_id)
        self.assertEqual(first_identity.identity_kind, "persistent-local")
        self.assertEqual(first_identity.algorithm, "ed25519")

    def test_identity_does_not_depend_on_display_name_or_hostname(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            store = FileIdentityStore(Path(temp_dir) / "identity")

            first_identity = store.load_or_create().public_identity
            second_identity = store.load_or_create().public_identity

        self.assertEqual(first_identity.device_id, second_identity.device_id)

    def test_private_key_file_uses_restrictive_posix_permissions(self) -> None:
        if os.name != "posix":
            self.skipTest("POSIX permissions are not available on this platform")

        with tempfile.TemporaryDirectory() as temp_dir:
            store = FileIdentityStore(Path(temp_dir) / "identity")
            store.load_or_create()

            private_mode = stat.S_IMODE(store.private_key_path.stat().st_mode)
            identity_dir_mode = stat.S_IMODE(store.identity_dir.stat().st_mode)

        self.assertEqual(private_mode, 0o600)
        self.assertEqual(identity_dir_mode, 0o700)

    def test_metadata_contains_no_system_membership_or_trust(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            store = FileIdentityStore(Path(temp_dir) / "identity")
            store.load_or_create()

            metadata = json.loads(store.metadata_path.read_text(encoding="utf-8"))

        self.assertNotIn("system_id", metadata)
        self.assertNotIn("enrolled_system_id", metadata)
        self.assertNotIn("trusted", metadata)
        self.assertNotIn("owner", metadata)

    def test_corrupted_metadata_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            store = FileIdentityStore(Path(temp_dir) / "identity")
            store.load_or_create()
            store.metadata_path.write_text("{not-json", encoding="utf-8")

            with self.assertRaises(DeviceIdentityError):
                FileIdentityStore(Path(temp_dir) / "identity").load_or_create()

    def test_missing_private_key_with_metadata_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            store = FileIdentityStore(Path(temp_dir) / "identity")
            store.load_or_create()
            store.private_key_path.unlink()

            with self.assertRaises(DeviceIdentityError):
                FileIdentityStore(Path(temp_dir) / "identity").load_or_create()

    def test_clean_isolated_store_creates_different_identity(self) -> None:
        with tempfile.TemporaryDirectory() as first_dir:
            first_identity = FileIdentityStore(
                Path(first_dir) / "identity"
            ).load_or_create().public_identity

        with tempfile.TemporaryDirectory() as second_dir:
            second_identity = FileIdentityStore(
                Path(second_dir) / "identity"
            ).load_or_create().public_identity

        self.assertNotEqual(first_identity.device_id, second_identity.device_id)

    def test_valid_but_mismatched_public_metadata_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            first = FileIdentityStore(Path(temp_dir) / "first")
            second = FileIdentityStore(Path(temp_dir) / "second")
            first.load_or_create()
            second.load_or_create()
            private_before = first.private_key_path.read_bytes()
            first.metadata_path.write_bytes(second.metadata_path.read_bytes())
            with self.assertRaises(DeviceIdentityError):
                first.load_or_create()
            self.assertEqual(first.private_key_path.read_bytes(), private_before)

    def test_malformed_and_wrong_type_private_keys_fail_closed(self) -> None:
        wrong_key = ec.generate_private_key(ec.SECP256R1()).private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption(),
        )
        for key_data in (b"malformed private PEM", wrong_key):
            with self.subTest(key_type=key_data[:20]):
                with tempfile.TemporaryDirectory() as temp_dir:
                    store = FileIdentityStore(Path(temp_dir) / "identity")
                    store.load_or_create()
                    store.private_key_path.write_bytes(key_data)
                    with self.assertRaises(DeviceIdentityError) as error:
                        store.load_or_create()
                    self.assertNotIn(key_data.decode(), str(error.exception))
                    self.assertIsNone(error.exception.__cause__)
                    self.assertEqual(store.private_key_path.read_bytes(), key_data)

    def test_invalid_metadata_fails_closed(self) -> None:
        mutations = [
            {"schema_version": value} for value in (None, 0, 2, "1", True, 1.0)
        ] + [
            {"public_key": value}
            for value in (
                "!", "\u00e9", "A",
                encode_base64url(b"a" * 31), encode_base64url(b"a" * 33),
            )
        ] + [
            {"algorithm": "rsa"}, {"identity_kind": "trusted"},
            {"created_at": "invalid"}, {"device_id": "wrong"},
            {"public_key_fingerprint": "wrong"},
        ]
        with tempfile.TemporaryDirectory() as temp_dir:
            store = FileIdentityStore(Path(temp_dir) / "identity")
            store.load_or_create()
            original = json.loads(store.metadata_path.read_text())
            for mutation in mutations:
                with self.subTest(mutation=mutation):
                    store.metadata_path.write_text(json.dumps(original | mutation))
                    with self.assertRaises(DeviceIdentityError):
                        store.load_or_create()
            for name in original:
                with self.subTest(missing=name):
                    metadata = original.copy()
                    del metadata[name]
                    store.metadata_path.write_text(json.dumps(metadata))
                    with self.assertRaises(DeviceIdentityError):
                        store.load_or_create()
            for invalid in ([], None, "not an object"):
                store.metadata_path.write_text(json.dumps(invalid))
                with self.assertRaises(DeviceIdentityError):
                    store.load_or_create()
            store.metadata_path.write_bytes(b"\xff")
            with self.assertRaises(DeviceIdentityError):
                store.load_or_create()

    def test_active_store_determines_storage_backend(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            store = FileIdentityStore(Path(temp_dir) / "identity")
            first = store.load_or_create().public_identity
            metadata = first.to_metadata() | {"storage_backend": "native-secure-storage"}
            store.metadata_path.write_text(json.dumps(metadata))
            loaded = store.load_or_create().public_identity
            self.assertEqual(loaded.storage_backend, store.storage_backend)
            self.assertEqual(loaded.device_id, first.device_id)

    @unittest.skipUnless(os.name == "posix", "POSIX permissions required")
    def test_existing_permissions_are_repaired_without_changing_identity(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            store = FileIdentityStore(Path(temp_dir) / "identity")
            original = store.load_or_create().public_identity
            for mode in (0o644, 0o666, 0o000):
                with self.subTest(mode=mode):
                    store.identity_dir.chmod(0o755)
                    store.private_key_path.chmod(mode)
                    self.assertEqual(store.load_or_create().public_identity, original)
                    self.assertEqual(stat.S_IMODE(store.identity_dir.stat().st_mode), 0o700)
                    self.assertEqual(stat.S_IMODE(store.private_key_path.stat().st_mode), 0o600)

    @unittest.skipUnless(os.name == "posix", "POSIX permissions required")
    def test_permission_repair_failures_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            store = FileIdentityStore(Path(temp_dir) / "identity")
            store.load_or_create()
            for target, mode in ((store.identity_dir, 0o755), (store.private_key_path, 0o644)):
                with self.subTest(target=target.name):
                    target.chmod(mode)
                    with patch.object(
                        Path, "chmod", side_effect=PermissionError("sensitive diagnostic")
                    ):
                        with self.assertRaises(DeviceIdentityError) as error:
                            store.load_or_create()
                    self.assertNotIn("sensitive diagnostic", str(error.exception))
                    self.assertIsNone(error.exception.__cause__)
                    target.chmod(0o700 if target == store.identity_dir else 0o600)

    @unittest.skipUnless(os.name == "posix", "POSIX permissions required")
    def test_silent_permission_repair_failure_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            store = FileIdentityStore(Path(temp_dir) / "identity")
            store.load_or_create()
            store.private_key_path.chmod(0o644)
            with patch.object(Path, "chmod"):
                with self.assertRaises(DeviceIdentityError):
                    store.load_or_create()

    def test_missing_metadata_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            store = FileIdentityStore(Path(temp_dir) / "identity")
            store.load_or_create()
            store.metadata_path.unlink()
            with self.assertRaises(DeviceIdentityError):
                store.load_or_create()

    def test_lock_failure_fails_closed_without_creating_keys(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            store = FileIdentityStore(Path(temp_dir) / "identity")
            with patch(
                "aether.identity_store.identity_file_lock",
                side_effect=OSError("lock unavailable"),
            ):
                with self.assertRaises(DeviceIdentityError):
                    store.load_or_create()
            self.assertFalse(store.private_key_path.exists())
            self.assertFalse(store.metadata_path.exists())

    def test_interrupted_metadata_write_preserves_key_and_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            store = FileIdentityStore(Path(temp_dir) / "identity")
            original_replace = os.replace

            def fail_metadata_replace(source, destination):
                if destination == store.metadata_path:
                    raise OSError("simulated write failure")
                return original_replace(source, destination)

            with patch("aether.identity_store.os.replace", side_effect=fail_metadata_replace):
                with self.assertRaises(DeviceIdentityError):
                    store.load_or_create()
            key_before = store.private_key_path.read_bytes()
            self.assertFalse(store.metadata_path.exists())
            self.assertEqual(list(store.identity_dir.glob(".*.tmp")), [])
            with self.assertRaises(DeviceIdentityError):
                store.load_or_create()
            self.assertEqual(store.private_key_path.read_bytes(), key_before)

    @unittest.skipUnless(os.name == "posix", "POSIX filesystem checks required")
    def test_symlinked_private_key_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            store = FileIdentityStore(Path(temp_dir) / "identity")
            store.load_or_create()
            target = Path(temp_dir) / "key.pem"
            store.private_key_path.rename(target)
            store.private_key_path.symlink_to(target)
            with self.assertRaises(DeviceIdentityError):
                store.load_or_create()

    def test_concurrent_first_launch_creates_one_persistent_identity(self) -> None:
        context = multiprocessing.get_context("spawn")
        with tempfile.TemporaryDirectory() as temp_dir:
            identity_dir = Path(temp_dir) / "identity"
            barrier = context.Barrier(4)
            results = context.Queue()
            processes = [
                context.Process(
                    target=_initialize_concurrently,
                    args=(str(identity_dir), barrier, results),
                )
                for _ in range(4)
            ]
            try:
                for process in processes:
                    process.start()
                identifiers = [results.get(timeout=20) for _ in processes]
                for process in processes:
                    process.join(timeout=10)
                    self.assertEqual(process.exitcode, 0)
                stored = FileIdentityStore(identity_dir).load_or_create().public_identity
                self.assertEqual(identifiers, [stored.device_id] * len(processes))
                self.assertEqual(list(identity_dir.glob(".*.tmp")), [])
            finally:
                for process in processes:
                    if process.is_alive():
                        process.terminate()
                        process.join(timeout=5)
                results.close()
                results.join_thread()


if __name__ == "__main__":
    unittest.main()
