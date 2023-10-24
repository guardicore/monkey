from ipaddress import IPv4Address
from uuid import UUID

import pytest

from common.agent_events import PropagationEvent

TARGET_IP_STR = "192.168.1.10"
AGENT_ID = UUID("012e7238-7b81-4108-8c7f-0787bc3f3c10")
TIMESTAMP = 1664371327.4067292

PROPAGATION_EVENT = PropagationEvent(
    source=AGENT_ID,
    timestamp=TIMESTAMP,
    target=IPv4Address(TARGET_IP_STR),
    success=True,
    exploiter_name="SSHExploiter",
)

PROPAGATION_OBJECT_DICT = {
    "source": AGENT_ID,
    "timestamp": TIMESTAMP,
    "target": IPv4Address(TARGET_IP_STR),
    "success": True,
    "exploiter_name": "SSHExploiter",
    "error_message": "",
}

PROPAGATION_SIMPLE_DICT = {
    "source": str(AGENT_ID),
    "timestamp": TIMESTAMP,
    "target": TARGET_IP_STR,
    "success": "true",
    "exploiter_name": "SSHExploiter",
    "error_message": "",
}


@pytest.mark.parametrize(
    "propagation_event_dict", [PROPAGATION_OBJECT_DICT, PROPAGATION_SIMPLE_DICT]
)
def test_constructor(propagation_event_dict):
    assert PropagationEvent(**propagation_event_dict) == PROPAGATION_EVENT


@pytest.mark.parametrize(
    "key, value",
    [
        ("exploiter_name", None),
        ("error_message", None),
    ],
)
def test_construct_invalid_field__type_error(key, value):
    invalid_type_dict = PROPAGATION_SIMPLE_DICT.copy()
    invalid_type_dict[key] = value

    with pytest.raises(TypeError):
        PropagationEvent(**invalid_type_dict)


@pytest.mark.parametrize(
    "key, value",
    [
        ("target", "not-an-ip"),
        ("target", None),
        ("success", "not-a-bool"),
    ],
)
def test_construct_invalid_field__value_error(key, value):
    invalid_type_dict = PROPAGATION_SIMPLE_DICT.copy()
    invalid_type_dict[key] = value

    with pytest.raises(ValueError):
        PropagationEvent(**invalid_type_dict)


def test_construct__extra_fields_forbidden():
    extra_field_dict = PROPAGATION_SIMPLE_DICT.copy()
    extra_field_dict["extra_field"] = 99  # red balloons

    with pytest.raises(ValueError):
        PropagationEvent(**extra_field_dict)
