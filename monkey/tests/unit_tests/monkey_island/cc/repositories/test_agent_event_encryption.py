import uuid
from typing import Dict, Sequence

import pytest
from monkeyevents import AbstractAgentEvent, PydanticAgentEventSerializer

from monkey_island.cc.repositories.agent_event_encryption import decrypt_event, encrypt_event


class FakeAgentEvent(AbstractAgentEvent):
    data: str
    list_data: Sequence[str]
    dict_data: Dict[str, str]


EVENT = FakeAgentEvent(
    source=uuid.uuid4(), data="foo", list_data=["abc", "def"], dict_data={"abc": "def"}
)


@pytest.fixture
def key_file(tmp_path):
    return tmp_path / "test_key.bin"


@pytest.fixture
def serializer():
    return PydanticAgentEventSerializer(FakeAgentEvent)


def test_agent_event_encryption__encrypts(repository_encryptor, serializer):
    data = serializer.serialize(EVENT)
    encrypted_data = encrypt_event(repository_encryptor.encrypt, data)

    # Encrypted fields have the "encrypted_" prefix
    assert "encrypted_data" in encrypted_data
    assert encrypted_data["encrypted_data"] is not EVENT.data
    assert encrypted_data["encrypted_list_data"] is not EVENT.list_data
    assert encrypted_data["encrypted_dict_data"] is not EVENT.dict_data


def test_agent_event_encryption__decrypts(repository_encryptor, serializer):
    data = serializer.serialize(EVENT)
    encrypted_data = encrypt_event(repository_encryptor.encrypt, data)

    decrypted_data = decrypt_event(repository_encryptor.decrypt, encrypted_data)
    deserialized_event = serializer.deserialize(decrypted_data)

    assert deserialized_event == EVENT


def test_agent_event_encryption__encryption_throws(repository_encryptor):
    data = "Not a dict."

    with pytest.raises(TypeError):
        encrypt_event(repository_encryptor.encrypt, data, fields=[])


def test_agent_event_encryption__decryption_throws(repository_encryptor):
    data = "Not a dict."

    with pytest.raises(TypeError):
        decrypt_event(repository_encryptor.decrypt, data)
