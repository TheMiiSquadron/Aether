from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from aether.config import RuntimeConfig
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
    def test_start_constructs_local_device_report(self) -> None:
        runtime = AetherRuntime(
            RuntimeConfig(aether_version="test-version"),
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
        self.assertEqual(device["identity_kind"], "ephemeral-runtime")
        self.assertTrue(device["device_id"].startswith("urn:aether:device:ephemeral:"))

    def test_shutdown_stops_runtime_cleanly(self) -> None:
        runtime = AetherRuntime(
            RuntimeConfig(),
            platform_provider=FakePlatformInfoProvider(),
        )
        runtime.start()

        report = runtime.shutdown()

        self.assertEqual(runtime.state, RuntimeState.STOPPED)
        self.assertEqual(report, {"runtime": {"state": "stopped"}})

    def test_start_is_idempotent_while_running(self) -> None:
        runtime = AetherRuntime(
            RuntimeConfig(),
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
