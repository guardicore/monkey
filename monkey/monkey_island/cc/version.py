import logging
from threading import Event, Thread

import requests
import semantic_version

from .deployment import Deployment

VERSION_SERVER_URL_PREF = "https://updates.infectionmonkey.com"
VERSION_SERVER_CHECK_NEW_URL = VERSION_SERVER_URL_PREF + "?deployment=%s&monkey_version=%s"
VERSION_SERVER_DOWNLOAD_URL = VERSION_SERVER_CHECK_NEW_URL + "&is_download=true"

LATEST_VERSION_TIMEOUT = 7

logger = logging.getLogger(__name__)


class Version:
    """
    Class which get current version, latest version and download link for the latest version
    """

    def __init__(self, version_number: str, deployment: Deployment):
        self._version_number = version_number
        self._latest_version = None
        self._download_url = None
        self._deployment = deployment
        self._initialization_complete = Event()

        Thread(target=self._set_version_metadata, daemon=True).start()

    @property
    def version_number(self):
        """
        The current version of the island
        """
        return self._version_number

    @property
    def latest_version(self):
        """
        Latest available version of the island
        """
        self._initialization_complete.wait()
        return self._latest_version

    @property
    def download_url(self):
        """
        URL for the latest available version
        """
        self._initialization_complete.wait()
        return self._download_url

    def _set_version_metadata(self):
        self._latest_version = self._get_latest_version()
        self._download_url = self._get_download_link()
        self._initialization_complete.set()

    def _get_latest_version(self) -> str:
        url = VERSION_SERVER_CHECK_NEW_URL % (self._deployment.value, self._version_number)

        try:
            reply = requests.get(url, timeout=LATEST_VERSION_TIMEOUT)
        except requests.exceptions.RequestsException as err:
            logger.warning(f"Failed to connect to {VERSION_SERVER_URL_PREF}: {err}")
            return self._version_number

        res = reply.json().get("newer_version", None)

        if res is False:
            return self._version_number

        if not semantic_version.validate(res):
            logger.warning(f"Recieved invalid version {res} from {VERSION_SERVER_URL_PREF}")
            return self._version_number

        return res.strip()

    def _get_download_link(self):
        return VERSION_SERVER_DOWNLOAD_URL % (self._deployment.value, self._version_number)
