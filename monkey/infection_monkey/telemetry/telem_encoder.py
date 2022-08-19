import json

from common import OperatingSystem


class TelemetryJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, OperatingSystem):
            return obj.name
        return json.JSONEncoder.default(self, obj)
