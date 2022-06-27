from datetime import datetime
from enum import Enum

import bson
from bson.json_util import dumps
from flask import make_response


def normalize_obj(obj):
    if ("_id" in obj) and ("id" not in obj):
        obj["id"] = obj["_id"]
        del obj["_id"]

    for key, value in list(obj.items()):
        if isinstance(value, list):
            for i in range(0, len(value)):
                obj[key][i] = _normalize_value(value[i])
        else:
            obj[key] = _normalize_value(value)
    return obj


def _normalize_value(value):
    if type(value) == dict:
        return normalize_obj(value)
    if isinstance(value, bson.objectid.ObjectId):
        return str(value)
    if isinstance(value, datetime):
        return str(value)
    if issubclass(type(value), Enum):
        return value.name
    else:
        return value


def output_json(obj, code, headers=None):
    obj = normalize_obj(obj)
    resp = make_response(dumps(obj), code)
    resp.headers.extend(headers or {})
    return resp
