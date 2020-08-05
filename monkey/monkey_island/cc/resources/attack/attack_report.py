import flask_restful
from flask import current_app, json

from monkey_island.cc.resources.auth.auth import jwt_required
from monkey_island.cc.services.attack.attack_report import AttackReportService
from monkey_island.cc.services.attack.attack_schema import SCHEMA

__author__ = "VakarisZ"


class AttackReport(flask_restful.Resource):

    @jwt_required
    def get(self):
        response_content = {'techniques': AttackReportService.get_latest_report()['techniques'], 'schema': SCHEMA}
        return current_app.response_class(json.dumps(response_content,
                                                     indent=None,
                                                     separators=(",", ":"),
                                                     sort_keys=False) + "\n",
                                          mimetype=current_app.config['JSONIFY_MIMETYPE'])
