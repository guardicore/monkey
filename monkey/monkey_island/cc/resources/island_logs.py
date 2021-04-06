import logging

import flask_restful

from monkey_island.cc.resources.auth.auth import jwt_required
from monkey_island.cc.services.island_logs import IslandLogService

__author__ = "Maor.Rayzin"

logger = logging.getLogger(__name__)


class IslandLog(flask_restful.Resource):
    @jwt_required
    def get(self):
        try:
            return IslandLogService.get_log_file()
        except Exception:
            logger.error('Monkey Island logs failed to download', exc_info=True)
