import uuid

import pytest

from common.agent_event_serializers import PydanticAgentEventSerializer
from common.agent_events import AbstractAgentEvent
from monkey_island.cc.repository.agent_event_encryption import (
    decrypt_event,
    encrypt_event,
    get_fields_to_encrypt,
)
from monkey_island.cc.server_utils.encryption import RepositoryEncryptor


class FakeAgentEvent(AbstractAgentEvent):
    data: str


@pytest.fixture
def key_file(tmp_path):
    return tmp_path / "test_key.bin"


@pytest.fixture
def encryptor(key_file):
    encryptor = RepositoryEncryptor(key_file)
    encryptor.unlock(b"password")
    return encryptor


@pytest.fixture
def serializer():
    return PydanticAgentEventSerializer()


def test_agent_event_encryption__encrypts(encryptor, serializer):
    event = FakeAgentEvent(source=uuid.uuid4(), data="foo")
    data = serializer.serialize(event)
    fields = get_fields_to_encrypt(event)
    encrypted_data = encrypt_event(encryptor.encrypt, data, fields)

    # Encrypted fields have the "encrypted_" prefix
    assert "encrypted_data" in encrypted_data
    assert encrypted_data["encrypted_data"] is not event.data


def test_agent_event_encryption__decrypts(encryptor, serializer):
    event = FakeAgentEvent(source=uuid.uuid4(), data="foo")

    data = serializer.serialize(event)
    fields = get_fields_to_encrypt(event)
    encrypted_data = encrypt_event(encryptor.encrypt, data, fields)

    decrypted_data = decrypt_event(encryptor.decrypt, encrypted_data)
    deserialized_event = serializer.deserialize(decrypted_data)

    assert deserialized_event == event
