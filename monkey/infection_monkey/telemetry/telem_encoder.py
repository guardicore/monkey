import json

from pydantic import BaseModel, SecretBytes, SecretStr

from common import OperatingSystem


class TelemetryJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, OperatingSystem):
            return obj.name
        if issubclass(type(obj), BaseModel):
            return obj.dict(simplify=True)
        if issubclass(type(obj), (SecretStr, SecretBytes)):
            return obj.get_secret_value()
        return json.JSONEncoder.default(self, obj)
