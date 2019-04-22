import flask_restful
import logging

from monkey_island.cc.environment.environment import env
from monkey_island.cc.auth import jwt_required
from monkey_island.cc.services.version_update import VersionUpdateService

__author__ = 'itay.mizeretz'

logger = logging.getLogger(__name__)


class VersionUpdate(flask_restful.Resource):
    def __init__(self):
        super(VersionUpdate, self).__init__()

    @jwt_required()
    def get(self):
        return {
            'current_version': env.get_version(),
            'newer_version': VersionUpdateService.get_newer_version(),
            'download_link': VersionUpdateService.get_download_link()
        }
