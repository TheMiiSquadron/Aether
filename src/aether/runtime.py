"""Runtime lifecycle for the Aether Foundation scaffold."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum

from aether.config import RuntimeConfig
from aether.device import AetherDevice, DeviceIdentity, DeviceRole
from aether.platform_info import PlatformInfoProvider, StandardPlatformInfoProvider

LOGGER = logging.getLogger(__name__)


class RuntimeState(StrEnum):
    STOPPED = "stopped"
    RUNNING = "running"


@dataclass(slots=True)
class AetherRuntime:
    """Minimal local runtime lifecycle."""

    config: RuntimeConfig
    platform_provider: PlatformInfoProvider | None = None
    state: RuntimeState = field(init=False)
    local_device: AetherDevice | None = field(init=False)
    started_at: datetime | None = field(init=False)

    def __post_init__(self) -> None:
        if self.platform_provider is None:
            self.platform_provider = StandardPlatformInfoProvider()
        self.state = RuntimeState.STOPPED
        self.local_device: AetherDevice | None = None
        self.started_at: datetime | None = None

    def start(self) -> dict[str, object]:
        if self.state is RuntimeState.RUNNING and self.local_device is not None:
            return self.startup_report()

        platform_info = self.platform_provider.get_platform_info()
        self.local_device = AetherDevice(
            identity=DeviceIdentity.ephemeral(),
            display_name=platform_info.display_name,
            platform=platform_info.platform,
            platform_version=platform_info.platform_version,
            architecture=platform_info.architecture,
            hostname=platform_info.hostname,
            role=DeviceRole.NODE,
            aether_version=self.config.aether_version,
        )
        self.started_at = datetime.now(timezone.utc)
        self.state = RuntimeState.RUNNING
        LOGGER.info("Aether runtime started")
        return self.startup_report()

    def startup_report(self) -> dict[str, object]:
        if self.local_device is None or self.started_at is None:
            return {
                "runtime": {
                    "state": self.state.value,
                    "aether_version": self.config.aether_version,
                    "started_at": None,
                },
                "local_device": None,
                "system": None,
            }

        return {
            "runtime": {
                "state": self.state.value,
                "aether_version": self.config.aether_version,
                "started_at": self.started_at.isoformat(),
            },
            "local_device": self.local_device.to_report(),
            "system": None,
        }

    def shutdown(self) -> dict[str, object]:
        if self.state is RuntimeState.STOPPED:
            return {"runtime": {"state": self.state.value}}

        self.state = RuntimeState.STOPPED
        LOGGER.info("Aether runtime stopped")
        return {"runtime": {"state": self.state.value}}
