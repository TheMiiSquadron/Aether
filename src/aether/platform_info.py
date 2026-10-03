"""Safe platform information providers."""

from __future__ import annotations

import platform
import socket
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class PlatformInfo:
    display_name: str
    platform: str
    platform_version: str
    architecture: str
    hostname: str


class PlatformInfoProvider(Protocol):
    def get_platform_info(self) -> PlatformInfo:
        """Return basic information about the local device."""


class StandardPlatformInfoProvider:
    """Cross-platform provider backed by Python standard-library APIs."""

    def get_platform_info(self) -> PlatformInfo:
        hostname = socket.gethostname() or "unknown"
        system = platform.system() or "unknown"
        version = platform.version() or platform.release() or "unknown"
        architecture = platform.machine() or "unknown"

        return PlatformInfo(
            display_name=hostname,
            platform=system,
            platform_version=version,
            architecture=architecture,
            hostname=hostname,
        )
