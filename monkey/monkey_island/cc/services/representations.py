from datetime import datetime

import bson
from bson.json_util import dumps
from flask import make_response


def normalize_obj(obj):
    if ('_id' in obj) and ('id' not in obj):
        obj['id'] = obj['_id']
        del obj['_id']

    for key, value in list(obj.items()):
        if isinstance(value, bson.objectid.ObjectId):
            obj[key] = str(value)
        if isinstance(value, datetime):
            obj[key] = str(value)
        if isinstance(value, dict):
            obj[key] = normalize_obj(value)
        if isinstance(value, list):
            for i in range(0, len(value)):
                if isinstance(value[i], dict):
                    value[i] = normalize_obj(value[i])
    return obj


def output_json(obj, code, headers=None):
    obj = normalize_obj(obj)
    resp = make_response(dumps(obj), code)
    resp.headers.extend(headers or {})
    return resp
