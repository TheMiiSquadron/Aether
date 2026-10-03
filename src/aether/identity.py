"""Persistent local Aether device identity primitives."""

from __future__ import annotations

import base64
import binascii
import hashlib
from dataclasses import dataclass, field
from datetime import datetime, timezone

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

DEVICE_ID_DOMAIN = b"aether-device-id-v1\0ed25519\0"
DEVICE_ID_ALGORITHM = "ed25519"
IDENTITY_KIND = "persistent-local"


class DeviceIdentityError(RuntimeError):
    """Raised when local device identity cannot be loaded or validated."""


def encode_base64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


def decode_base64url(value: str) -> bytes:
    try:
        padding = "=" * (-len(value) % 4)
        decoded = base64.b64decode(
            (value + padding).encode("ascii"), altchars=b"-_", validate=True
        )
        if encode_base64url(decoded) != value:
            raise ValueError("Noncanonical encoding")
        return decoded
    except (ValueError, TypeError, UnicodeError, binascii.Error):
        raise DeviceIdentityError("Invalid public-key encoding") from None


def derive_device_id(raw_public_key: bytes) -> str:
    digest = hashlib.sha256(DEVICE_ID_DOMAIN + raw_public_key).digest()
    return f"urn:aether:device:v1:{DEVICE_ID_ALGORITHM}:{encode_base64url(digest)}"


def public_key_fingerprint(raw_public_key: bytes) -> str:
    digest = hashlib.sha256(raw_public_key).digest()
    return f"sha256:{encode_base64url(digest)}"


@dataclass(frozen=True, slots=True)
class DeviceIdentity:
    """Public identity for a local Aether device.

    Private key material is intentionally not part of this dataclass and must
    remain behind the identity store/key-handle boundary.
    """

    device_id: str
    identity_kind: str
    algorithm: str
    public_key: str
    public_key_fingerprint: str
    created_at: str
    storage_backend: str

    @classmethod
    def from_public_key(
        cls,
        raw_public_key: bytes,
        *,
        created_at: str | None = None,
        storage_backend: str,
    ) -> "DeviceIdentity":
        if len(raw_public_key) != 32:
            raise DeviceIdentityError("Ed25519 public key must contain exactly 32 bytes")
        return cls(
            device_id=derive_device_id(raw_public_key),
            identity_kind=IDENTITY_KIND,
            algorithm=DEVICE_ID_ALGORITHM,
            public_key=encode_base64url(raw_public_key),
            public_key_fingerprint=public_key_fingerprint(raw_public_key),
            created_at=created_at or datetime.now(timezone.utc).isoformat(),
            storage_backend=storage_backend,
        )

    def to_metadata(self) -> dict[str, object]:
        return {
            "schema_version": 1,
            "device_id": self.device_id,
            "identity_kind": self.identity_kind,
            "algorithm": self.algorithm,
            "public_key": self.public_key,
            "public_key_fingerprint": self.public_key_fingerprint,
            "created_at": self.created_at,
            "storage_backend": self.storage_backend,
        }

    @classmethod
    def from_metadata(
        cls, metadata: dict[str, object], *, storage_backend: str
    ) -> "DeviceIdentity":
        required = {
            "device_id",
            "identity_kind",
            "algorithm",
            "public_key",
            "public_key_fingerprint",
            "created_at",
            "storage_backend",
        }
        missing = required.difference(metadata)
        if missing:
            raise DeviceIdentityError(
                f"Identity metadata is missing required fields: {sorted(missing)}"
            )
        if type(metadata.get("schema_version")) is not int or metadata["schema_version"] != 1:
            raise DeviceIdentityError("Unsupported identity metadata schema version")

        identity = cls(
            device_id=_metadata_string(metadata, "device_id"),
            identity_kind=_metadata_string(metadata, "identity_kind"),
            algorithm=_metadata_string(metadata, "algorithm"),
            public_key=_metadata_string(metadata, "public_key"),
            public_key_fingerprint=_metadata_string(metadata, "public_key_fingerprint"),
            created_at=_metadata_string(metadata, "created_at"),
            storage_backend=storage_backend,
        )
        try:
            if datetime.fromisoformat(identity.created_at).utcoffset() is None:
                raise ValueError("Missing timezone")
        except ValueError:
            raise DeviceIdentityError("Invalid identity creation timestamp") from None
        identity.validate_public_material()
        return identity

    def validate_public_material(self) -> None:
        if self.identity_kind != IDENTITY_KIND:
            raise DeviceIdentityError("Unexpected identity kind")
        if self.algorithm != DEVICE_ID_ALGORITHM:
            raise DeviceIdentityError("Unsupported identity algorithm")

        raw_public_key = decode_base64url(self.public_key)
        if len(raw_public_key) != 32:
            raise DeviceIdentityError("Ed25519 public key must contain exactly 32 bytes")
        expected_device_id = derive_device_id(raw_public_key)
        if self.device_id != expected_device_id:
            raise DeviceIdentityError("Identity metadata device_id does not match public key")

        expected_fingerprint = public_key_fingerprint(raw_public_key)
        if self.public_key_fingerprint != expected_fingerprint:
            raise DeviceIdentityError(
                "Identity metadata fingerprint does not match public key"
            )

    def to_report(self) -> dict[str, object]:
        return {
            "device_id": self.device_id,
            "identity_kind": self.identity_kind,
            "identity_algorithm": self.algorithm,
            "public_key": self.public_key,
            "public_key_fingerprint": self.public_key_fingerprint,
            "identity_created_at": self.created_at,
            "identity_storage_backend": self.storage_backend,
        }


@dataclass(frozen=True, slots=True)
class LocalDeviceIdentity:
    """Local identity with an in-memory private signing key handle."""

    public_identity: DeviceIdentity
    private_key: Ed25519PrivateKey = field(repr=False)

    @classmethod
    def generate(cls, *, storage_backend: str) -> "LocalDeviceIdentity":
        private_key = Ed25519PrivateKey.generate()
        raw_public_key = public_key_bytes(private_key)
        return cls(
            public_identity=DeviceIdentity.from_public_key(
                raw_public_key,
                storage_backend=storage_backend,
            ),
            private_key=private_key,
        )

    def sign(self, message: bytes) -> bytes:
        return self.private_key.sign(message)


def public_key_bytes(private_key: Ed25519PrivateKey) -> bytes:
    return private_key.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )


def _metadata_string(metadata: dict[str, object], field_name: str) -> str:
    value = metadata[field_name]
    if not isinstance(value, str):
        raise DeviceIdentityError(f"Identity metadata field is not a string: {field_name}")
    return value
