from datetime import datetime
from unittest import TestCase

import bson

from monkey_island.cc.services.representations import normalize_obj


class TestJsonRepresentations(TestCase):
    def test_normalize_obj(self):
        # empty
        self.assertEqual({}, normalize_obj({}))

        # no special content
        self.assertEqual(
            {"a": "a"},
            normalize_obj({"a": "a"})
        )

        # _id field -> id field
        self.assertEqual(
            {"id": 12345},
            normalize_obj({"_id": 12345})
        )

        # obj id field -> str
        obj_id_str = "123456789012345678901234"
        self.assertEqual(
            {"id": obj_id_str},
            normalize_obj({"_id": bson.objectid.ObjectId(obj_id_str)})
        )

        # datetime -> str
        dt = datetime.now()
        expected = {"a": str(dt)}
        result = normalize_obj({"a": dt})
        self.assertEqual(expected, result)

        # dicts and lists
        self.assertEqual({
            "a": [
                {"ba": obj_id_str,
                 "bb": obj_id_str}
            ],
            "b": {"id": obj_id_str}
        },
            normalize_obj({
                "a": [
                    {"ba": bson.objectid.ObjectId(obj_id_str),
                     "bb": bson.objectid.ObjectId(obj_id_str)}
                ],
                "b": {"_id": bson.objectid.ObjectId(obj_id_str)}
            })
        )
