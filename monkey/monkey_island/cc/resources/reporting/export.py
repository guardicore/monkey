import http.client
import logging

import flask_restful
from flask import jsonify

from monkey_island.cc.resources.auth.auth import jwt_required
from monkey_island.cc.services.reporting.exporting.exporter_factory import ExporterFactory
from monkey_island.cc.services.reporting.report import ReportService

logger = logging.getLogger(__name__)


class Export(flask_restful.Resource):
    @jwt_required()
    def get(self, exporter):
        logger.debug(f"Got request to manually export using the {exporter} exporter.")
        try:
            exporter = ExporterFactory.get_exporter(exporter)
            report = ReportService.get_report()
            user_message = exporter.handle_report(report)
            return jsonify(status="OK", extra_info=user_message)
        except NotImplementedError as _:
            logger.error(f"Export called with unknown exporter {exporter}. More info:", exc_info=True)
            return flask_restful.abort(404)
