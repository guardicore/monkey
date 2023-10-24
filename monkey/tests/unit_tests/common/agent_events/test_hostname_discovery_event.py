from uuid import UUID

import pytest

from common.agent_events import HostnameDiscoveryEvent

AGENT_ID = UUID("012e7238-7b81-4108-8c7f-0787bc3f3c10")
TIMESTAMP = 1664371327.4067292
HOSTNAME = "hostname"

HOSTNAME_DISCOVERY_EVENT = HostnameDiscoveryEvent(
    source=AGENT_ID, timestamp=TIMESTAMP, hostname=HOSTNAME
)

HOSTNAME_DISCOVERY_OBJECT_DICT = {
    "source": AGENT_ID,
    "timestamp": TIMESTAMP,
    "target": None,
    "tags": [],
    "hostname": HOSTNAME,
}

HOSTNAME_DISCOVERY_SIMPLE_DICT = {
    "source": str(AGENT_ID),
    "timestamp": TIMESTAMP,
    "target": None,
    "tags": [],
    "hostname": HOSTNAME,
}


@pytest.mark.parametrize(
    "event_dict",
    [HOSTNAME_DISCOVERY_OBJECT_DICT, HOSTNAME_DISCOVERY_SIMPLE_DICT],
)
def test_constructor(event_dict):
    assert HostnameDiscoveryEvent(**event_dict) == HOSTNAME_DISCOVERY_EVENT


def test_constructor__tags_are_frozenset():
    dict_with_tags = HOSTNAME_DISCOVERY_SIMPLE_DICT.copy()
    dict_with_tags["tags"] = {
        "tag-1",
        "tag-2",
        "tag-3",
    }

    assert isinstance(HostnameDiscoveryEvent(**dict_with_tags).tags, frozenset)


def test_constructor__extra_fields_forbidden():
    extra_field_dict = HOSTNAME_DISCOVERY_SIMPLE_DICT.copy()
    extra_field_dict["extra_field"] = 99  # red balloons

    with pytest.raises(ValueError):
        HostnameDiscoveryEvent(**extra_field_dict)


def test_serialization():
    serialized_event = HOSTNAME_DISCOVERY_EVENT.to_json_dict()
    assert serialized_event == HOSTNAME_DISCOVERY_SIMPLE_DICT


@pytest.mark.parametrize(
    "key, value",
    [
        ("hostname", None),
        ("hostname", []),
    ],
)
def test_construct_invalid_field__type_error(key, value):
    invalid_type_dict = HOSTNAME_DISCOVERY_SIMPLE_DICT.copy()
    invalid_type_dict[key] = value

    with pytest.raises(TypeError):
        HostnameDiscoveryEvent(**invalid_type_dict)
