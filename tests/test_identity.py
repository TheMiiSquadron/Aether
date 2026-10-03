from __future__ import annotations

import hashlib
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from aether.identity import (
    DEVICE_ID_DOMAIN,
    DeviceIdentity,
    DeviceIdentityError,
    LocalDeviceIdentity,
    derive_device_id,
    encode_base64url,
    public_key_fingerprint,
)


class IdentityTests(unittest.TestCase):
    def test_device_id_derivation_is_sha256_domain_separated(self) -> None:
        raw_public_key = bytes(range(32))

        device_id = derive_device_id(raw_public_key)

        self.assertEqual(DEVICE_ID_DOMAIN, b"aether-device-id-v1\0ed25519\0")
        expected_digest = hashlib.sha256(
            b"aether-device-id-v1\0ed25519\0" + raw_public_key
        ).digest()
        self.assertEqual(
            device_id,
            f"urn:aether:device:v1:ed25519:{encode_base64url(expected_digest)}",
        )

    def test_public_key_fingerprint_uses_raw_public_key_sha256(self) -> None:
        raw_public_key = b"a" * 32

        fingerprint = public_key_fingerprint(raw_public_key)

        expected_digest = hashlib.sha256(raw_public_key).digest()
        self.assertEqual(fingerprint, f"sha256:{encode_base64url(expected_digest)}")

    def test_malformed_public_keys_raise_identity_error(self) -> None:
        identity = LocalDeviceIdentity.generate(storage_backend="test").public_identity
        for value in ("!", "\u00e9", "A", identity.public_key + "=", "a" * 43 + "!"):
            with self.subTest(value=value):
                metadata = identity.to_metadata() | {"public_key": value}
                with self.assertRaises(DeviceIdentityError):
                    DeviceIdentity.from_metadata(metadata, storage_backend="test")

    def test_public_key_requires_exactly_32_bytes(self) -> None:
        for length in (0, 31, 33):
            with self.subTest(length=length):
                with self.assertRaises(DeviceIdentityError):
                    DeviceIdentity.from_public_key(b"a" * length, storage_backend="test")

    def test_signatures_verify_and_private_handle_is_excluded_from_repr(self) -> None:
        identity = LocalDeviceIdentity.generate(storage_backend="test")
        message = b"local identity test"
        identity.private_key.public_key().verify(identity.sign(message), message)
        self.assertNotIn("private_key=", repr(identity))


if __name__ == "__main__":
    unittest.main()
