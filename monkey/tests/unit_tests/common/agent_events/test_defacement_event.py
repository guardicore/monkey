from uuid import UUID

import pytest

from common.agent_events import AgentEventTag, DefacementEvent

AGENT_ID = UUID("012e7238-7b81-4108-8c7f-0787bc3f3c10")
TIMESTAMP = 1664371327.4067292
TAGS: frozenset[AgentEventTag] = frozenset()

DEFACEMENT_TARGET = DefacementEvent.DefacementTarget.INTERNAL
DESCRIPTION = "Changed desktop wallpaper"

DEFACEMENT_EVENT = DefacementEvent(
    source=AGENT_ID,
    timestamp=TIMESTAMP,
    tags=TAGS,
    defacement_target=DEFACEMENT_TARGET,
    description=DESCRIPTION,
)

DEFACEMENT_OBJECT_DICT = {
    "source": AGENT_ID,
    "timestamp": TIMESTAMP,
    "target": None,
    "tags": TAGS,
    "defacement_target": DEFACEMENT_TARGET,
    "description": DESCRIPTION,
}

DEFACEMENT_SIMPLE_DICT = {
    "source": str(AGENT_ID),
    "timestamp": TIMESTAMP,
    "target": None,
    "tags": list(TAGS),
    "defacement_target": "internal",
    "description": DESCRIPTION,
}


@pytest.mark.parametrize(
    "event_dict",
    [DEFACEMENT_OBJECT_DICT, DEFACEMENT_SIMPLE_DICT],
)
def test_constructor(event_dict):
    assert DefacementEvent(**event_dict) == DEFACEMENT_EVENT


def test_constructor__tags_are_frozenset():
    dict_with_tags = DEFACEMENT_SIMPLE_DICT.copy()
    dict_with_tags["tags"] = {
        "tag-1",
        "tag-2",
        "tag-3",
    }

    assert isinstance(DefacementEvent(**dict_with_tags).tags, frozenset)


def test_constructor__extra_fields_forbidden():
    extra_field_dict = DEFACEMENT_SIMPLE_DICT.copy()
    extra_field_dict["extra_field"] = 99  # red balloons

    with pytest.raises(ValueError):
        DefacementEvent(**extra_field_dict)


def test_serialization():
    serialized_event = DEFACEMENT_EVENT.to_json_dict()
    assert serialized_event == DEFACEMENT_SIMPLE_DICT


@pytest.mark.parametrize(
    "key, value",
    [
        ("defacement_target", None),
        ("defacement_target", 1),
        ("defacement_target", "invalid"),
    ],
)
def test_construct_invalid_field__type_error(key, value):
    invalid_type_dict = DEFACEMENT_SIMPLE_DICT.copy()
    invalid_type_dict[key] = value

    with pytest.raises(ValueError):
        DefacementEvent(**invalid_type_dict)
