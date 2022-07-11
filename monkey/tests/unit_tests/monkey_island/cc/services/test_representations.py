from dataclasses import dataclass
from datetime import datetime
from enum import Enum

import bson

from monkey_island.cc.services.representations import _normalize_value


@dataclass
class MockClass:
    a: int


obj_id_str = "123456789012345678901234"
bogus_object1 = MockClass(1)
bogus_object2 = MockClass(2)


def test_normalize_dicts():
    assert {} == _normalize_value({})

    assert {"a": "a"} == _normalize_value({"a": "a"})

    assert {"id": 12345} == _normalize_value({"id": 12345})

    assert {"id": obj_id_str} == _normalize_value({"id": bson.objectid.ObjectId(obj_id_str)})

    dt = datetime.now()
    expected = {"a": str(dt)}
    result = _normalize_value({"a": dt})
    assert expected == result


def test_normalize_complex():
    bogus_dict = {
        "a": [
            {
                "ba": bson.objectid.ObjectId(obj_id_str),
                "bb": bson.objectid.ObjectId(obj_id_str),
            }
        ],
        "b": {"id": bson.objectid.ObjectId(obj_id_str)},
    }

    expected_dict = {"a": [{"ba": obj_id_str, "bb": obj_id_str}], "b": {"id": obj_id_str}}
    assert expected_dict == _normalize_value(bogus_dict)


def test_normalize_list():
    bogus_list = [bson.objectid.ObjectId(obj_id_str), {"a": "b"}, {"object": [bogus_object1]}]

    expected_list = [obj_id_str, {"a": "b"}, {"object": [{"a": 1}]}]
    assert expected_list == _normalize_value(bogus_list)


def test_normalize_enum():
    class BogusEnum(Enum):
        bogus_val = "Bogus"

    my_obj = {"something": "something", "my_enum": BogusEnum.bogus_val}

    assert {"something": "something", "my_enum": "bogus_val"} == _normalize_value(my_obj)


def test_normalize_tuple():
    bogus_tuple = [{"my_tuple": (bogus_object1, bogus_object2, b"one_two")}]
    expected_tuple = [{"my_tuple": ({"a": 1}, {"a": 2}, b"one_two")}]
    assert expected_tuple == _normalize_value(bogus_tuple)
