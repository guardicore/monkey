from ipaddress import IPv4Address
from uuid import UUID

import pytest

from common.agent_events import PasswordRestorationEvent

TARGET_IP_STR = "192.168.1.10"
AGENT_ID = UUID("012e7238-7b81-4108-8c7f-0787bc3f3c10")
TIMESTAMP = 1664371327.4067292

PASSWORD_RESTORATION_EVENT = PasswordRestorationEvent(
    source=AGENT_ID,
    timestamp=TIMESTAMP,
    target=IPv4Address(TARGET_IP_STR),
    success=True,
)

PASSWORD_RESTORATION_OBJECT_DICT = {
    "source": AGENT_ID,
    "timestamp": TIMESTAMP,
    "target": IPv4Address(TARGET_IP_STR),
    "success": True,
}

PASSWORD_RESTORATION_SIMPLE_DICT = {
    "source": str(AGENT_ID),
    "timestamp": TIMESTAMP,
    "target": TARGET_IP_STR,
    "success": "true",
}


@pytest.mark.parametrize(
    "password_restoration_event_dict",
    [PASSWORD_RESTORATION_OBJECT_DICT, PASSWORD_RESTORATION_SIMPLE_DICT],
)
def test_constructor(password_restoration_event_dict):
    assert PasswordRestorationEvent(**password_restoration_event_dict) == PASSWORD_RESTORATION_EVENT


@pytest.mark.parametrize(
    "key, value",
    [
        ("target", "not-an-ip"),
        ("target", None),
        ("success", "not-a-bool"),
    ],
)
def test_construct_invalid_field__value_error(key, value):
    invalid_type_dict = PASSWORD_RESTORATION_SIMPLE_DICT.copy()
    invalid_type_dict[key] = value

    with pytest.raises(ValueError):
        PasswordRestorationEvent(**invalid_type_dict)


def test_construct__extra_fields_forbidden():
    extra_field_dict = PASSWORD_RESTORATION_SIMPLE_DICT.copy()
    extra_field_dict["extra_field"] = 99  # red balloons

    with pytest.raises(ValueError):
        PasswordRestorationEvent(**extra_field_dict)
