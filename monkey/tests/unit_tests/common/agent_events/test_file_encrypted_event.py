from ipaddress import IPv4Address
from pathlib import PurePath
from uuid import UUID

import pytest

from common.agent_events import FileEncryptedEvent

TARGET_IP_STR = "192.168.1.10"
AGENT_ID = UUID("012e7238-7b81-4108-8c7f-0787bc3f3c10")
TIMESTAMP = 1664371327.4067292
FILE_ENCRYPTED_PATH = PurePath("/home/ubuntu/encrypted.txt")

FILE_ENCRYPTED_EVENT = FileEncryptedEvent(
    source=AGENT_ID,
    timestamp=TIMESTAMP,
    target=IPv4Address(TARGET_IP_STR),
    file_path=PurePath(FILE_ENCRYPTED_PATH),
    success=True,
)

FILE_ENCRYPTED_OBJECT_DICT = {
    "source": AGENT_ID,
    "timestamp": TIMESTAMP,
    "target": IPv4Address(TARGET_IP_STR),
    "file_path": FILE_ENCRYPTED_PATH,
    "success": True,
    "error_message": "",
}

FILE_ENCRYPTED_SIMPLE_DICT = {
    "source": str(AGENT_ID),
    "timestamp": TIMESTAMP,
    "target": TARGET_IP_STR,
    "file_path": FILE_ENCRYPTED_PATH,
    "success": "true",
    "error_message": "",
}


@pytest.mark.parametrize(
    "file_encrypted_event_dict", [FILE_ENCRYPTED_OBJECT_DICT, FILE_ENCRYPTED_SIMPLE_DICT]
)
def test_constructor(file_encrypted_event_dict):
    assert FileEncryptedEvent(**file_encrypted_event_dict) == FILE_ENCRYPTED_EVENT


@pytest.mark.parametrize(
    "key, value",
    [
        ("file_path", None),
        ("success", "not-a-bool"),
        ("error_message", None),
    ],
)
def test_construct_invalid_field__type_error(key, value):
    invalid_type_dict = FILE_ENCRYPTED_SIMPLE_DICT.copy()
    invalid_type_dict[key] = value

    with pytest.raises(TypeError):
        FileEncryptedEvent(**invalid_type_dict)


@pytest.mark.parametrize(
    "key, value",
    [
        ("target", "not-an-ip"),
    ],
)
def test_construct_invalid_field__value_error(key, value):
    invalid_type_dict = FILE_ENCRYPTED_SIMPLE_DICT.copy()
    invalid_type_dict[key] = value

    with pytest.raises(ValueError):
        FileEncryptedEvent(**invalid_type_dict)


def test_construct__extra_fields_forbidden():
    extra_field_dict = FILE_ENCRYPTED_SIMPLE_DICT.copy()
    extra_field_dict["extra_field"] = 99  # red balloons

    with pytest.raises(ValueError):
        FileEncryptedEvent(**extra_field_dict)
