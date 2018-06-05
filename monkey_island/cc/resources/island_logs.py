import logging

import flask_restful

from cc.auth import jwt_required
from cc.services.island_logs import IslandLogService

__author__ = "Maor.Rayzin"

logger = logging.getLogger(__name__)


class IslandLog(flask_restful.Resource):
    @jwt_required()
    def get(self):
        try:
            return IslandLogService.get_log_file()
        except Exception as e:
            logger.error('Monkey Island logs failed to download', exc_info=True)
