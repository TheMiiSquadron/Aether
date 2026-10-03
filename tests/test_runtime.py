from __future__ import annotations

import base64
import json
import sys
import tempfile
import unittest
from pathlib import Path

from cryptography.hazmat.primitives import serialization

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from aether.config import RuntimeConfig
from aether.identity_store import FileIdentityStore
from aether.platform_info import PlatformInfo
from aether.runtime import AetherRuntime, RuntimeState


class FakePlatformInfoProvider:
    def get_platform_info(self) -> PlatformInfo:
        return PlatformInfo(
            display_name="Test Device",
            platform="TestOS",
            platform_version="1.2.3",
            architecture="test64",
            hostname="test-host",
        )


class RuntimeTests(unittest.TestCase):
    def test_backend_reports_and_logs_exclude_private_material(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            store = FileIdentityStore(Path(temp_dir) / "identity")
            identity = store.load_or_create()
            metadata = identity.public_identity.to_metadata()
            metadata["storage_backend"] = "forged-backend"
            store.metadata_path.write_text(json.dumps(metadata))
            runtime = AetherRuntime(RuntimeConfig(), identity_store=store)
            with self.assertLogs("aether.runtime", level="DEBUG") as logs:
                report = runtime.start()
                runtime.shutdown()
            self.assertEqual(
                report["local_device"]["identity_storage_backend"],
                store.storage_backend,
            )
            self.assertIsNone(report["system"])
            self.assertIsNone(report["local_device"]["enrolled_system_id"])
            public_output = json.dumps(report) + repr(identity) + str(logs.output)
            pem = store.private_key_path.read_text()
            raw = identity.private_key.private_bytes(
                serialization.Encoding.Raw,
                serialization.PrivateFormat.Raw,
                serialization.NoEncryption(),
            )
            for secret in (pem, "PRIVATE KEY", base64.b64encode(raw).decode(), raw.hex()):
                self.assertNotIn(secret, public_output)

    def test_start_constructs_local_device_report(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            runtime = AetherRuntime(
                RuntimeConfig(
                    aether_version="test-version",
                    identity_dir=Path(temp_dir) / "identity",
                ),
                platform_provider=FakePlatformInfoProvider(),
            )

            report = runtime.start()

        self.assertEqual(runtime.state, RuntimeState.RUNNING)
        self.assertEqual(report["runtime"]["state"], "running")
        self.assertEqual(report["runtime"]["aether_version"], "test-version")
        self.assertIsNone(report["system"])

        device = report["local_device"]
        self.assertEqual(device["display_name"], "Test Device")
        self.assertEqual(device["platform"], "TestOS")
        self.assertEqual(device["platform_version"], "1.2.3")
        self.assertEqual(device["architecture"], "test64")
        self.assertEqual(device["hostname"], "test-host")
        self.assertEqual(device["role"], "node")
        self.assertEqual(device["capabilities"], [])
        self.assertIsNone(device["enrolled_system_id"])
        self.assertEqual(device["identity_kind"], "persistent-local")
        self.assertEqual(device["identity_algorithm"], "ed25519")
        self.assertTrue(device["device_id"].startswith("urn:aether:device:v1:ed25519:"))
        self.assertIn("public_key", device)
        self.assertIn("public_key_fingerprint", device)
        self.assertNotIn("private_key", device)

    def test_shutdown_stops_runtime_cleanly(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            runtime = AetherRuntime(
                RuntimeConfig(identity_dir=Path(temp_dir) / "identity"),
                platform_provider=FakePlatformInfoProvider(),
            )
            runtime.start()

            report = runtime.shutdown()

        self.assertEqual(runtime.state, RuntimeState.STOPPED)
        self.assertEqual(report, {"runtime": {"state": "stopped"}})

    def test_start_is_idempotent_while_running(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            runtime = AetherRuntime(
                RuntimeConfig(identity_dir=Path(temp_dir) / "identity"),
                platform_provider=FakePlatformInfoProvider(),
            )

            first_report = runtime.start()
            second_report = runtime.start()

        self.assertEqual(
            first_report["local_device"]["device_id"],
            second_report["local_device"]["device_id"],
        )


if __name__ == "__main__":
    unittest.main()
