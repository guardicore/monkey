import json

from common import OperatingSystems


class TelemetryJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, OperatingSystems):
            return obj.name
        return json.JSONEncoder.default(self, obj)
