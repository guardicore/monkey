from datetime import datetime, timezone
from uuid import UUID

import pytest
from monkeytypes import IllegalMutationError

from monkey_island.cc.models import Agent

AGENT_ID = UUID("012e7238-7b81-4108-8c7f-0787bc3f3c10")
PARENT_ID = UUID("0fc9afcb-1902-436b-bd5c-1ad194252484")
SHA256 = "6b524293febf78ac659ce4ca368b8fc74df6e14462e12a43e4044eafe2a5f947"

AGENT_OBJECT_DICT = {
    "id": AGENT_ID,
    "machine_id": 2,
    "parent_id": PARENT_ID,
    "registration_time": datetime.fromtimestamp(1660848410, tz=timezone.utc),
    "start_time": datetime.fromtimestamp(1660848408, tz=timezone.utc),
    "sha256": SHA256,
}

AGENT_SIMPLE_DICT = {
    "id": str(AGENT_ID),
    "machine_id": 2,
    "parent_id": str(PARENT_ID),
    "registration_time": "2022-08-18T18:46:50Z",
    "start_time": "2022-08-18T18:46:48Z",
    "sha256": SHA256,
}


def test_constructor__defaults_from_objects():
    a = Agent(**AGENT_OBJECT_DICT)

    assert a.stop_time is None
    assert a.cc_server is None


def test_constructor__defaults_from_simple_dict():
    agent_simple_dict = AGENT_SIMPLE_DICT.copy()
    del agent_simple_dict["parent_id"]
    a = Agent(**agent_simple_dict)

    assert a.parent_id is None
    assert a.stop_time is None
    assert a.cc_server is None


def test_to_dict():
    a = Agent(**AGENT_OBJECT_DICT)
    agent_simple_dict = AGENT_SIMPLE_DICT.copy()
    agent_simple_dict["stop_time"] = None
    agent_simple_dict["cc_server"] = None

    assert a.to_json_dict() == agent_simple_dict


@pytest.mark.parametrize(
    "key, value",
    [
        ("id", 1),
        ("registration_time", None),
        ("start_time", None),
        ("stop_time", []),
        ("parent_id", 2.1),
        ("cc_server", [1]),
        ("sha256", []),
        ("sha256", 1),
        ("cc_server", []),
    ],
)
def test_construct_invalid_field__type_error(key, value):
    invalid_type_dict = AGENT_SIMPLE_DICT.copy()
    invalid_type_dict[key] = value

    with pytest.raises(TypeError):
        Agent(**invalid_type_dict)


@pytest.mark.parametrize(
    "key, value",
    [
        ("machine_id", -1),
        ("machine_id", "not-an-int"),
        ("registration_time", "not-a-datetime"),
        ("start_time", "not-a-datetime"),
        ("stop_time", "not-a-datetime"),
        ("sha256", "abcdef"),  # too short
        ("sha256", "this_string_has_the_right_length_but_includes_non_hex_characters"),
        ("sha256", "1234567812345678123456781234567812345678123456781234567812345678abcdef"),
    ],
)
def test_construct_invalid_field__value_error(key, value):
    invalid_value_dict = AGENT_SIMPLE_DICT.copy()
    invalid_value_dict[key] = value

    with pytest.raises(ValueError):
        Agent(**invalid_value_dict)


def test_id_immutable():
    a = Agent(**AGENT_SIMPLE_DICT)

    with pytest.raises(IllegalMutationError):
        a.id = PARENT_ID


def test_machine_id_immutable():
    a = Agent(**AGENT_SIMPLE_DICT)

    with pytest.raises(IllegalMutationError):
        a.machine_id = 10


def test_registration_time_immutable():
    a = Agent(**AGENT_SIMPLE_DICT)

    with pytest.raises(IllegalMutationError):
        a.registration_time = 100


def test_start_time_immutable():
    a = Agent(**AGENT_SIMPLE_DICT)

    with pytest.raises(IllegalMutationError):
        a.start_time = 100


def test_parent_id_immutable():
    a = Agent(**AGENT_SIMPLE_DICT)

    with pytest.raises(IllegalMutationError):
        a.parent_id = AGENT_ID


def test_stop_time_set_validated():
    a = Agent(**AGENT_SIMPLE_DICT)

    with pytest.raises(ValueError):
        a.stop_time = "testing!"


def test_cc_server_set_validated():
    a = Agent(**AGENT_SIMPLE_DICT)

    with pytest.raises(TypeError):
        a.cc_server = []


def test_sha256_immutable():
    a = Agent(**AGENT_SIMPLE_DICT)

    with pytest.raises(IllegalMutationError):
        a.sha256 = "testing!"
