from datetime import datetime
from enum import Enum

import bson
from bson.json_util import dumps
from flask import make_response


def _normalize_obj(obj):
    if ("_id" in obj) and ("id" not in obj):
        obj["id"] = obj["_id"]
        del obj["_id"]

    for key, value in list(obj.items()):
        obj[key] = _normalize_value(value)
    return obj


def _normalize_value(value):
    if isinstance(value, list):
        for i in range(0, len(value)):
            value[i] = _normalize_value(value[i])
    if type(value) == dict:
        return _normalize_obj(value)
    if isinstance(value, bson.objectid.ObjectId):
        return str(value)
    if isinstance(value, datetime):
        return str(value)
    if issubclass(type(value), Enum):
        return value.name

    try:
        return value.__dict__
    except AttributeError:
        pass

    return value


def output_json(value, code, headers=None):
    value = _normalize_value(value)
    resp = make_response(dumps(value), code)
    resp.headers.extend(headers or {})
    return resp
