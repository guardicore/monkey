from flask import current_app, json

from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.resources.request_authentication import jwt_required
from monkey_island.cc.services.attack.attack_report import AttackReportService
from monkey_island.cc.services.attack.attack_schema import SCHEMA


class AttackReport(AbstractResource):
    # API Spec: This is an action and there's no "resource"; RPC-style endpoint?
    urls = ["/api/report/attack"]

    @jwt_required
    def get(self):
        response_content = {
            "techniques": AttackReportService.get_latest_report()["techniques"],
            "schema": SCHEMA,
        }
        return current_app.response_class(
            json.dumps(response_content, indent=None, separators=(",", ":"), sort_keys=False)
            + "\n",
            mimetype=current_app.config["JSONIFY_MIMETYPE"],
        )
