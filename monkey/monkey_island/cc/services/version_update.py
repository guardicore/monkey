import logging

import requests

import monkey_island.cc.environment.environment_singleton as env_singleton
from common.version import get_version

__author__ = "itay.mizeretz"

logger = logging.getLogger(__name__)


class VersionUpdateService:
    VERSION_SERVER_URL_PREF = 'https://updates.infectionmonkey.com'
    VERSION_SERVER_CHECK_NEW_URL = VERSION_SERVER_URL_PREF + '?deployment=%s&monkey_version=%s'
    VERSION_SERVER_DOWNLOAD_URL = VERSION_SERVER_CHECK_NEW_URL + '&is_download=true'

    newer_version = None

    def __init__(self):
        pass

    @staticmethod
    def get_newer_version():
        """
        Checks for newer version if never checked before.
        :return: None if failed checking for newer version, result of '_check_new_version' otherwise
        """
        if VersionUpdateService.newer_version is None:
            try:
                VersionUpdateService.newer_version = VersionUpdateService._check_new_version()
            except Exception:
                logger.exception('Failed updating version number')

        return VersionUpdateService.newer_version

    @staticmethod
    def _check_new_version():
        """
        Checks if newer monkey version is available
        :return: False if not, version in string format ('1.6.2') otherwise
        """
        url = VersionUpdateService.VERSION_SERVER_CHECK_NEW_URL % (env_singleton.env.get_deployment(), get_version())

        reply = requests.get(url, timeout=15)

        res = reply.json().get('newer_version', None)

        if res is False:
            return res

        [int(x) for x in res.split('.')]  # raises value error if version is invalid format
        return res

    @staticmethod
    def get_download_link():
        return VersionUpdateService.VERSION_SERVER_DOWNLOAD_URL % (env_singleton.env.get_deployment(), get_version())
