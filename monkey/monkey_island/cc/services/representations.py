from datetime import datetime
from enum import Enum
from json import JSONEncoder, dumps
from typing import Any

import bson
from flask import make_response
from pydantic import BaseModel


class APIEncoder(JSONEncoder):
    def default(self, value: Any) -> Any:
        # ObjectId is serializible by default, but returns a dict
        # So serialize it first into a plain string
        if isinstance(value, bson.objectid.ObjectId):
            return str(value)
        if isinstance(value, datetime):
            return str(value)
        if issubclass(type(value), Enum):
            return value.name
        if issubclass(type(value), set):
            return list(value)
        if issubclass(type(value), BaseModel):
            return value.to_json_dict()
        try:
            return JSONEncoder.default(self, value)
        except TypeError:
            return value.__dict__


def output_json(value, code, headers=None):
    resp = make_response(dumps(value, cls=APIEncoder), code)
    resp.headers.extend(headers or {})
    return resp
