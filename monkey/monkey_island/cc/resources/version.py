import logging

from monkey_island.cc import Version
from monkey_island.cc.resources.AbstractResource import AbstractResource

logger = logging.getLogger(__name__)


class Version(AbstractResource):
    urls = ["/api/island/version"]

    def __init__(self, version: Version):
        self._version = version

    # We don't secure this since it doesn't give out any private info and we want UI to know version
    # even when not authenticated
    def get(self):
        return {
            "version_number": self._version.version_number,
            "latest_version": self._version.latest_version,
            "download_link": self._version.download_url,
        }
