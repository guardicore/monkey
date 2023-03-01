import logging

from monkey_island.cc import Version as IslandVersion
from monkey_island.cc.flask_utils import AbstractResource, jwt_required

logger = logging.getLogger(__name__)


class Version(AbstractResource):
    urls = ["/api/island/version"]

    def __init__(self, version: IslandVersion):
        self._version = version

    @jwt_required
    def get(self):
        return {
            "version_number": self._version.version_number,
            "latest_version": self._version.latest_version,
            "download_link": self._version.download_url,
        }
