"""Storage backends for local Aether device identity."""

from __future__ import annotations

import json
import os
import stat
import tempfile
from pathlib import Path
from typing import Protocol

from cryptography.exceptions import UnsupportedAlgorithm
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from aether.identity import (
    DEVICE_ID_ALGORITHM,
    DeviceIdentity,
    DeviceIdentityError,
    LocalDeviceIdentity,
    public_key_bytes,
)
from aether.identity_lock import identity_file_lock


class IdentityStore(Protocol):
    @property
    def storage_backend(self) -> str:
        """Human-readable storage backend name."""

    def load_or_create(self) -> LocalDeviceIdentity:
        """Load the local identity or create it on first launch."""


class FileIdentityStore:
    """Initial Foundation fallback identity store.

    This backend uses local files with restrictive permissions. It is not the
    final long-term secure storage backend for Aether; native secure storage
    backends can replace it behind the IdentityStore interface later.
    POSIX modes are enforced; Windows relies on inherited user-directory ACLs.
    chmod is not used as a substitute for Windows ACL protection.
    """

    storage_backend = "foundation-file-fallback"

    def __init__(self, identity_dir: Path) -> None:
        self.identity_dir = identity_dir
        self.private_key_path = identity_dir / "device_identity.ed25519.pem"
        self.metadata_path = identity_dir / "device_identity.json"
        self.lock_path = identity_dir / ".identity.lock"

    def load_or_create(self) -> LocalDeviceIdentity:
        try:
            self.identity_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
            _ensure_posix_permissions(self.identity_dir, 0o700, directory=True)
            with identity_file_lock(self.lock_path):
                return self._load_or_create_locked()
        except OSError:
            raise DeviceIdentityError("Local device identity storage is unavailable") from None

    def _load_or_create_locked(self) -> LocalDeviceIdentity:
        # lstat preserves evidence of broken symlinks rather than replacing them.
        private_exists = _path_exists(self.private_key_path)
        metadata_exists = _path_exists(self.metadata_path)

        if not private_exists and not metadata_exists:
            identity = LocalDeviceIdentity.generate(storage_backend=self.storage_backend)
            self._persist(identity)
            return identity

        if private_exists != metadata_exists:
            raise DeviceIdentityError(
                "Local device identity state is incomplete; refusing to replace it"
            )

        return self._load()

    def _load(self) -> LocalDeviceIdentity:
        try:
            metadata = json.loads(self.metadata_path.read_text(encoding="utf-8"))
        except (OSError, ValueError, UnicodeError):
            raise DeviceIdentityError("Local device identity metadata is unreadable") from None

        if not isinstance(metadata, dict):
            raise DeviceIdentityError("Local device identity metadata is not an object")

        public_identity = DeviceIdentity.from_metadata(
            metadata, storage_backend=self.storage_backend
        )
        if public_identity.algorithm != DEVICE_ID_ALGORITHM:
            raise DeviceIdentityError("Unsupported local device identity algorithm")

        try:
            _ensure_posix_permissions(self.private_key_path, 0o600)
            flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
            with os.fdopen(os.open(self.private_key_path, flags), "rb") as key_file:
                _ensure_posix_permissions(key_file.fileno(), 0o600)
                private_key_data = key_file.read()
            loaded_key = serialization.load_pem_private_key(
                private_key_data,
                password=None,
            )
        except (OSError, ValueError, TypeError, UnsupportedAlgorithm):
            raise DeviceIdentityError("Local device private key is unreadable") from None

        if not isinstance(loaded_key, Ed25519PrivateKey):
            raise DeviceIdentityError("Local device private key has unexpected type")

        raw_public_key = public_key_bytes(loaded_key)
        derived_identity = DeviceIdentity.from_public_key(
            raw_public_key,
            created_at=public_identity.created_at,
            storage_backend=self.storage_backend,
        )
        if derived_identity != public_identity:
            raise DeviceIdentityError(
                "Local device identity metadata does not match private key"
            )

        return LocalDeviceIdentity(
            public_identity=public_identity,
            private_key=loaded_key,
        )

    def _persist(self, identity: LocalDeviceIdentity) -> None:
        private_key_data = identity.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
        _atomic_write(self.private_key_path, private_key_data, 0o600)

        metadata_data = json.dumps(
            identity.public_identity.to_metadata(),
            indent=2,
            sort_keys=True,
        ).encode("utf-8")
        _atomic_write(self.metadata_path, metadata_data + b"\n", 0o600)


def _atomic_write(path: Path, data: bytes, mode: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent,
    )
    temp_path = Path(temp_name)
    try:
        with os.fdopen(fd, "wb") as temp_file:
            temp_file.write(data)
            temp_file.flush()
            os.fsync(temp_file.fileno())
        _ensure_posix_permissions(temp_path, mode)
        os.replace(temp_path, path)
    except Exception:
        try:
            temp_path.unlink()
        except OSError:
            pass
        raise


def _path_exists(path: Path) -> bool:
    try:
        path.lstat()
        return True
    except FileNotFoundError:
        return False


def _ensure_posix_permissions(
    target: Path | int, mode: int, *, directory: bool = False
) -> None:
    if os.name != "posix":
        return
    try:
        info = os.fstat(target) if isinstance(target, int) else target.lstat()
        expected_type = stat.S_ISDIR if directory else stat.S_ISREG
        if not expected_type(info.st_mode) or info.st_uid != os.getuid():
            raise DeviceIdentityError("Unsafe local device identity storage ownership or type")
        if not directory and info.st_nlink != 1:
            raise DeviceIdentityError("Linked private identity files are not supported")
        if stat.S_IMODE(info.st_mode) != mode:
            if isinstance(target, int):
                os.fchmod(target, mode)
                info = os.fstat(target)
            else:
                target.chmod(mode)
                info = target.lstat()
            if stat.S_IMODE(info.st_mode) != mode:
                raise DeviceIdentityError("Local device identity permissions remain unsafe")
    except OSError:
        raise DeviceIdentityError("Cannot secure local device identity permissions") from None


def private_key_permissions(path: Path) -> str | None:
    """Return an octal POSIX mode string for reporting, if available."""

    if os.name != "posix":
        return None
    return oct(stat.S_IMODE(path.stat().st_mode))
