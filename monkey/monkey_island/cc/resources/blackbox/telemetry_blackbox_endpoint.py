import flask_restful
from bson import json_util
from flask import request

from monkey_island.cc.models.telemetries import get_telemetry_by_query
from monkey_island.cc.resources.auth.auth import jwt_required


class TelemetryBlackboxEndpoint(flask_restful.Resource):
    @jwt_required
    def get(self, **kw):
        find_query = json_util.loads(request.args.get("find_query"))
        return {"results": list(get_telemetry_by_query(find_query))}
