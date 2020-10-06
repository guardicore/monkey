import http.client

import flask_restful
from flask import Response, jsonify

from monkey_island.cc.models.zero_trust.scoutsuite_data_json import ScoutSuiteDataJson
from monkey_island.cc.resources.auth.auth import jwt_required
from monkey_island.cc.services.reporting.report import ReportService
from monkey_island.cc.services.zero_trust.finding_service import FindingService
from monkey_island.cc.services.zero_trust.zero_trust_service import ZeroTrustService

ZERO_TRUST_REPORT_TYPE = "zero_trust"
SECURITY_REPORT_TYPE = "security"
REPORT_TYPES = [SECURITY_REPORT_TYPE, ZERO_TRUST_REPORT_TYPE]

REPORT_DATA_PILLARS = "pillars"
REPORT_DATA_FINDINGS = "findings"
REPORT_DATA_PRINCIPLES_STATUS = "principles"
REPORT_DATA_SCOUTSUITE = "scoutsuite"

__author__ = ["itay.mizeretz", "shay.nehmad"]


class Report(flask_restful.Resource):

    @jwt_required
    def get(self, report_type=SECURITY_REPORT_TYPE, report_data=None):
        if report_type == SECURITY_REPORT_TYPE:
            return ReportService.get_report()
        elif report_type == ZERO_TRUST_REPORT_TYPE:
            if report_data == REPORT_DATA_PILLARS:
                return jsonify({
                    "statusesToPillars": ZeroTrustService.get_statuses_to_pillars(),
                    "pillarsToStatuses": ZeroTrustService.get_pillars_to_statuses(),
                    "grades": ZeroTrustService.get_pillars_grades()
                })
            elif report_data == REPORT_DATA_PRINCIPLES_STATUS:
                return jsonify(ZeroTrustService.get_principles_status())
            elif report_data == REPORT_DATA_FINDINGS:
                return jsonify(FindingService.get_all_findings())
            elif report_data == REPORT_DATA_SCOUTSUITE:
                try:
                    data = ScoutSuiteDataJson.objects.get().scoutsuite_data
                except Exception:
                    data = "{}"
                return Response(data, mimetype='application/json')

        flask_restful.abort(http.client.NOT_FOUND)
