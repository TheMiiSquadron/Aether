"""Aether device model primitives.

This module intentionally models only the local installed device needed by the
Foundation scaffold. System enrollment, trust, pairing, host status, networking,
and System ownership are deferred by the architecture documents.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from aether.identity import DeviceIdentity


class DeviceRole(StrEnum):
    """Initial conceptual Aether device roles."""

    NODE = "node"
    ENDPOINT = "endpoint"
    COMPANION = "companion"


@dataclass(frozen=True, slots=True)
class AetherDevice:
    """Local Aether device representation."""

    identity: DeviceIdentity
    display_name: str
    platform: str
    platform_version: str
    architecture: str
    hostname: str
    role: DeviceRole
    aether_version: str
    capabilities: tuple[str, ...] = field(default_factory=tuple)
    enrolled_system_id: str | None = None

    def to_report(self) -> dict[str, object]:
        return self.identity.to_report() | {
            "display_name": self.display_name,
            "platform": self.platform,
            "platform_version": self.platform_version,
            "architecture": self.architecture,
            "hostname": self.hostname,
            "role": self.role.value,
            "aether_version": self.aether_version,
            "capabilities": list(self.capabilities),
            "enrolled_system_id": self.enrolled_system_id,
        }
