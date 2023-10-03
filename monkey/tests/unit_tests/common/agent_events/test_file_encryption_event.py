from ipaddress import IPv4Address
from pathlib import PurePosixPath, PureWindowsPath
from uuid import UUID

import pytest
from monkeytypes import OperatingSystem
from pydantic.errors import IntegerError

from common.agent_events import FileEncryptionEvent

TARGET_IP_STR = "192.168.1.10"
AGENT_ID = UUID("012e7238-7b81-4108-8c7f-0787bc3f3c10")
TIMESTAMP = 1664371327.4067292
LINUX_FILE_ENCRYPTED_PATH = PurePosixPath("/home/ubuntu/encrypted.txt")
WINDOWS_FILE_ENCRYPTED_PATH = PureWindowsPath("C:/Windows/temp/some_file.txt")

LINUX_FILE_ENCRYPTION_EVENT = FileEncryptionEvent(
    source=AGENT_ID,
    timestamp=TIMESTAMP,
    target=IPv4Address(TARGET_IP_STR),
    file_path=LINUX_FILE_ENCRYPTED_PATH,
    success=True,
)

WINDOWS_FILE_ENCRYPTION_EVENT = FileEncryptionEvent(
    source=AGENT_ID,
    timestamp=TIMESTAMP,
    target=IPv4Address(TARGET_IP_STR),
    file_path=WINDOWS_FILE_ENCRYPTED_PATH,
    success=True,
)

LINUX_FILE_ENCRYPTION_OBJECT_DICT = {
    "source": AGENT_ID,
    "timestamp": TIMESTAMP,
    "target": IPv4Address(TARGET_IP_STR),
    "file_path": LINUX_FILE_ENCRYPTED_PATH,
    "success": True,
    "error_message": "",
}

LINUX_FILE_ENCRYPTION_SIMPLE_DICT = {
    "source": str(AGENT_ID),
    "timestamp": TIMESTAMP,
    "target": TARGET_IP_STR,
    "file_path": {"path": str(LINUX_FILE_ENCRYPTED_PATH), "os": OperatingSystem.LINUX.value},
    "success": True,
    "error_message": "",
    "tags": [],
}


@pytest.mark.parametrize(
    "linux_file_encryption_event_dict",
    [LINUX_FILE_ENCRYPTION_OBJECT_DICT, LINUX_FILE_ENCRYPTION_SIMPLE_DICT],
)
def test_constructor(linux_file_encryption_event_dict):
    assert FileEncryptionEvent(**linux_file_encryption_event_dict) == LINUX_FILE_ENCRYPTION_EVENT


def test_serialization():
    serialized_event = LINUX_FILE_ENCRYPTION_EVENT.dict(simplify=True)
    assert serialized_event == LINUX_FILE_ENCRYPTION_SIMPLE_DICT


@pytest.mark.parametrize(
    "key, value",
    [
        ("file_path", None),
        ("file_path", 1234),
        ("file_path", {"path": None, "os": OperatingSystem.WINDOWS.value}),
        ("file_path", {"path": str(LINUX_FILE_ENCRYPTED_PATH), "os": None}),
        ("success", "not-a-bool"),
        ("error_message", None),
    ],
)
def test_construct_invalid_field__type_error(key, value):
    invalid_type_dict = LINUX_FILE_ENCRYPTION_SIMPLE_DICT.copy()
    invalid_type_dict[key] = value

    with pytest.raises(TypeError):
        FileEncryptionEvent(**invalid_type_dict)


@pytest.mark.parametrize(
    "key, value",
    [
        ("file_path", {"bogus_field": "bogus"}),
        ("file_path", {"path": str(LINUX_FILE_ENCRYPTED_PATH), "os": "FakeOS"}),
    ],
)
def test_construct_invalid_field__value_error(key, value):
    invalid_value_dict = LINUX_FILE_ENCRYPTION_SIMPLE_DICT.copy()
    invalid_value_dict[key] = value

    with pytest.raises(ValueError):
        FileEncryptionEvent(**invalid_value_dict)


def test_construct_invalid_field__integer_error():
    invalid_value_dict = LINUX_FILE_ENCRYPTION_SIMPLE_DICT.copy()
    invalid_value_dict["target"] = "not-an-ip-or-integer"

    with pytest.raises(IntegerError):
        FileEncryptionEvent(**invalid_value_dict)


def test_construct__extra_fields_forbidden():
    extra_field_dict = LINUX_FILE_ENCRYPTION_SIMPLE_DICT.copy()
    extra_field_dict["extra_field"] = 99  # red balloons

    with pytest.raises(ValueError):
        FileEncryptionEvent(**extra_field_dict)


@pytest.mark.parametrize(
    "event",
    [LINUX_FILE_ENCRYPTION_EVENT, WINDOWS_FILE_ENCRYPTION_EVENT],
)
def test_file_encryption_event__de_serialization(event):
    serialized_event = event.dict(simplify=True)
    deserialized_event = FileEncryptionEvent(**serialized_event)

    assert isinstance(deserialized_event.file_path, type(event.file_path))
