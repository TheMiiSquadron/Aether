"""Platform-neutral local storage paths for Aether Foundation."""

from __future__ import annotations

import os
import platform
from pathlib import Path


def default_identity_dir() -> Path:
    return default_data_dir() / "identity"


def default_data_dir() -> Path:
    system = platform.system()
    home = Path.home()

    if system == "Darwin":
        return home / "Library" / "Application Support" / "Aether" / "Foundation"

    if system == "Windows":
        local_app_data = os.environ.get("LOCALAPPDATA")
        if local_app_data:
            return Path(local_app_data) / "Aether" / "Foundation"
        return home / "AppData" / "Local" / "Aether" / "Foundation"

    xdg_data_home = os.environ.get("XDG_DATA_HOME")
    if xdg_data_home:
        return Path(xdg_data_home) / "aether" / "foundation"
    return home / ".local" / "share" / "aether" / "foundation"
