import json
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

import bson

from monkey_island.cc.services.representations import APIEncoder


@dataclass
class MockClass:
    a: int


obj_id_str = "123456789012345678901234"
bogus_object1 = MockClass(1)
bogus_object2 = MockClass(2)


def test_api_encoder_dicts():
    assert json.dumps({}) == json.dumps({}, cls=APIEncoder)

    assert json.dumps({"a": "a"}) == json.dumps({"a": "a"}, cls=APIEncoder)

    assert json.dumps({"id": 12345}) == json.dumps({"id": 12345}, cls=APIEncoder)

    assert json.dumps({"id": obj_id_str}) == json.dumps(
        {"id": bson.objectid.ObjectId(obj_id_str)}, cls=APIEncoder
    )

    dt = datetime.now()
    expected = {"a": str(dt)}
    result = json.dumps({"a": dt}, cls=APIEncoder)
    assert json.dumps(expected) == result


def test_api_encoder_complex():
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
    assert json.dumps(expected_dict) == json.dumps(bogus_dict, cls=APIEncoder)


def test_api_encoder_list():
    bogus_list = [bson.objectid.ObjectId(obj_id_str), {"a": "b"}, {"object": [bogus_object1]}]

    expected_list = [obj_id_str, {"a": "b"}, {"object": [{"a": 1}]}]
    assert json.dumps(expected_list) == json.dumps(bogus_list, cls=APIEncoder)


def test_api_encoder_enum():
    class BogusEnum(Enum):
        bogus_val = "Bogus"

    my_obj = {"something": "something", "my_enum": BogusEnum.bogus_val}

    assert json.dumps({"something": "something", "my_enum": "bogus_val"}) == json.dumps(
        my_obj, cls=APIEncoder
    )


def test_api_encoder_tuple():
    bogus_tuple = [{"my_tuple": (bogus_object1, bogus_object2, "string")}]
    expected_tuple = [{"my_tuple": ({"a": 1}, {"a": 2}, "string")}]
    assert json.dumps(expected_tuple) == json.dumps(bogus_tuple, cls=APIEncoder)
