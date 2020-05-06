import flask_restful
import json

from monkey_island.cc.auth import jwt_required
from monkey_island.cc.services.reporting.zero_trust_service import ZeroTrustService
from monkey_island.cc.testing.profiler_decorator import profile


class ZeroTrustFindingEvent(flask_restful.Resource):

    @jwt_required()
    @profile()
    def get(self, finding_id: str):
        return {'events_json': json.dumps(ZeroTrustService.get_events_by_finding(finding_id), default=str)}
