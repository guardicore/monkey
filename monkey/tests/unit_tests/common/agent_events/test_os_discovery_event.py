from uuid import UUID

import pytest
from monkeytypes import OperatingSystem

from common.agent_events import OSDiscoveryEvent

AGENT_ID = UUID("012e7238-7b81-4108-8c7f-0787bc3f3c10")
TIMESTAMP = 1664371327.4067292
VERSION = "Ubuntu 22.04"

OS_DISCOVERY_EVENT = OSDiscoveryEvent(
    source=AGENT_ID, timestamp=TIMESTAMP, os=OperatingSystem.LINUX, version=VERSION
)

OS_DISCOVERY_OBJECT_DICT = {
    "source": AGENT_ID,
    "timestamp": TIMESTAMP,
    "target": None,
    "tags": [],
    "os": OperatingSystem.LINUX,
    "version": VERSION,
}

OS_DISCOVERY_SIMPLE_DICT = {
    "source": str(AGENT_ID),
    "timestamp": TIMESTAMP,
    "os": "linux",
    "target": None,
    "tags": [],
    "version": VERSION,
}


@pytest.mark.parametrize(
    "event_dict",
    [OS_DISCOVERY_OBJECT_DICT, OS_DISCOVERY_SIMPLE_DICT],
)
def test_constructor(event_dict):
    assert OSDiscoveryEvent(**event_dict) == OS_DISCOVERY_EVENT


def test_constructor__tags_are_frozenset():
    dict_with_tags = OS_DISCOVERY_SIMPLE_DICT.copy()
    dict_with_tags["tags"] = {
        "tag-1",
        "tag-2",
        "tag-3",
    }

    assert isinstance(OSDiscoveryEvent(**dict_with_tags).tags, frozenset)


def test_constructor__extra_fields_forbidden():
    extra_field_dict = OS_DISCOVERY_SIMPLE_DICT.copy()
    extra_field_dict["extra_field"] = 99  # red balloons

    with pytest.raises(ValueError):
        OSDiscoveryEvent(**extra_field_dict)


def test_serialization():
    serialized_event = OS_DISCOVERY_EVENT.model_dump(mode="json")
    assert serialized_event == OS_DISCOVERY_SIMPLE_DICT


def test_construct_invalid_field__type_error():
    invalid_type_dict = OS_DISCOVERY_SIMPLE_DICT.copy()
    invalid_type_dict["version"] = None

    with pytest.raises(TypeError):
        OSDiscoveryEvent(**invalid_type_dict)


@pytest.mark.parametrize(
    "key, value",
    [
        ("os", None),
        ("os", 1),
        ("os", "FakeOS"),
    ],
)
def test_construct_invalid_field__value_error(key, value):
    invalid_type_dict = OS_DISCOVERY_SIMPLE_DICT.copy()
    invalid_type_dict[key] = value

    with pytest.raises(ValueError):
        OSDiscoveryEvent(**invalid_type_dict)
