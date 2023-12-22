import logging
from threading import Event, Thread
from typing import Optional, Tuple

import requests

from .deployment import Deployment

# TODO get redirects instead of using direct links to AWS
LATEST_VERSION_URL = "https://njf01cuupf.execute-api.us-east-1.amazonaws.com/default?deployment={}"
LATEST_VERSION_TIMEOUT = 7

logger = logging.getLogger(__name__)


class Version:
    """
    Information about the Island's version

    Provides the current version, latest version, and download link for the latest version.
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

    @property
    def deployment(self):
        """
        The deployment of the current Island
        """
        return self._deployment

    def _set_version_metadata(self):
        self._latest_version, self._download_url = self._get_version_info()
        self._initialization_complete.set()

    def _get_version_info(self) -> Tuple[str, Optional[str]]:
        url = LATEST_VERSION_URL.format(self._deployment.value)

        try:
            response = requests.get(url, timeout=LATEST_VERSION_TIMEOUT).json()
        except requests.exceptions.RequestException as err:
            logger.warning(f"Failed to fetch version information from {url}: {err}")
            return self._version_number, None

        try:
            download_link = response["download_link"]
            latest_version = response["version"]
        except KeyError:
            logger.error(f"Failed to fetch version information from {url}: {response}")
            return self._version_number, None

        return latest_version, download_link
