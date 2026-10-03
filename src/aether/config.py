"""Runtime configuration for Aether Foundation."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RuntimeConfig:
    """Configuration used to start a local Aether runtime instance."""

    aether_version: str = "0.1.0"
    log_level: str = "WARNING"
