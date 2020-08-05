import logging

import flask_restful

from monkey_island.cc.resources.auth.auth import jwt_required
from monkey_island.cc.services.attack.attack_report import AttackReportService
from monkey_island.cc.services.reporting.report import ReportService

NOT_ALL_REPORTS_DELETED = "Not all reports have been cleared from the DB!"

logger = logging.getLogger(__name__)


class ClearCaches(flask_restful.Resource):
    """
    Used for timing tests - we want to get actual execution time of functions in BlackBox without caching -
    so we use this to clear the caches.
    :note: DO NOT CALL THIS IN PRODUCTION CODE as this will slow down the user experience.
    """
    @jwt_required
    def get(self, **kw):
        try:
            logger.warning("Trying to clear caches! Make sure this is not production")
            ReportService.delete_saved_report_if_exists()
            AttackReportService.delete_saved_report_if_exists()
            # TODO: Monkey.clear_caches(), clear LRU caches of function in the Monkey object
        except RuntimeError as e:
            logger.exception(e)
            flask_restful.abort(500, error_info=str(e))

        if ReportService.is_report_generated() or AttackReportService.is_report_generated():
            logger.error(NOT_ALL_REPORTS_DELETED)
            flask_restful.abort(500, error_info=NOT_ALL_REPORTS_DELETED)

        return {"success": "true"}
