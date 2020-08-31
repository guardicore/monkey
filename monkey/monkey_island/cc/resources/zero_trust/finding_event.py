import json

import flask_restful

from monkey_island.cc.resources.auth.auth import jwt_required
from monkey_island.cc.services.reporting.zero_trust_service import \
    ZeroTrustService


class ZeroTrustFindingEvent(flask_restful.Resource):

    @jwt_required
    def get(self, finding_id: str):
        return {'events_json': json.dumps(ZeroTrustService.get_events_by_finding(finding_id), default=str)}
