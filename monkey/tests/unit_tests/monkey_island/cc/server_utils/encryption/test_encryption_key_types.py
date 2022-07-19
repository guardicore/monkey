import pytest

from monkey_island.cc.server_utils.encryption.encryption_key_types import EncryptionKey32Bytes


@pytest.mark.parametrize("key", ["", 2, []])
def test_create_encryption_key_32_bytes__raises_type_error(key):
    with pytest.raises(TypeError):
        EncryptionKey32Bytes(key)


@pytest.mark.parametrize("key", [b"", b"less", b"this is something that is longer than 32"])
def test_create_encryption_key_32_bytes__raises_value_error(key):
    with pytest.raises(ValueError):
        EncryptionKey32Bytes(key)
