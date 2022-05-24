from flask import jsonify

from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.resources.request_authentication import jwt_required
from monkey_island.cc.services.ransomware import ransomware_report


class RansomwareReport(AbstractResource):
    # API Spec: This is an action and there's no "resource"; RPC-style endpoint?
    urls = ["/api/report/ransomware"]

    @jwt_required
    def get(self):
        return jsonify(
            {
                "propagation_stats": ransomware_report.get_propagation_stats(),
            }
        )
