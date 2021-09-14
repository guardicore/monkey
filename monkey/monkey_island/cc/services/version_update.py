import json
import logging
from pathlib import Path

import requests

from common.utils.exceptions import VersionServerConnectionError
from common.version import get_version
from monkey_island.cc.server_utils.consts import MONKEY_ISLAND_ABS_PATH

DEPLOYMENT_FILE_PATH = Path(MONKEY_ISLAND_ABS_PATH) / "cc" / "deployment.json"

logger = logging.getLogger(__name__)


class VersionUpdateService:
    VERSION_SERVER_URL_PREF = "https://updates.infectionmonkey.com"
    VERSION_SERVER_CHECK_NEW_URL = VERSION_SERVER_URL_PREF + "?deployment=%s&monkey_version=%s"
    VERSION_SERVER_DOWNLOAD_URL = VERSION_SERVER_CHECK_NEW_URL + "&is_download=true"

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
            except VersionServerConnectionError:
                logger.info("Failed updating version number")

        return VersionUpdateService.newer_version

    @staticmethod
    def _check_new_version():
        """
        Checks if newer monkey version is available
        :return: False if not, version in string format ('1.6.2') otherwise
        """

        url = VersionUpdateService.VERSION_SERVER_CHECK_NEW_URL % (
            VersionUpdateService.get_deployment_from_file(DEPLOYMENT_FILE_PATH),
            get_version(),
        )

        try:
            reply = requests.get(url, timeout=7)
        except requests.exceptions.RequestException:
            logger.info("Can't get latest monkey version, probably no connection to the internet.")
            raise VersionServerConnectionError

        res = reply.json().get("newer_version", None)

        if res is False:
            return res

        [int(x) for x in res.split(".")]  # raises value error if version is invalid format
        return res

    @staticmethod
    def get_download_link():
        return VersionUpdateService.VERSION_SERVER_DOWNLOAD_URL % (
            VersionUpdateService.get_deployment_from_file(DEPLOYMENT_FILE_PATH),
            get_version(),
        )

    @staticmethod
    def get_deployment_from_file(file_path: Path) -> str:
        deployment = "unknown"

        try:
            with open(file_path, "r") as deployment_info_file:
                deployment_info = json.load(deployment_info_file)
                deployment = deployment_info["deployment"]
        except FileNotFoundError as ex:
            logger.debug(f"Deployment file {file_path} is not found. Exception: {ex}")
        except KeyError as ex:
            logger.debug(f"Invalid key in the deployment file. Exception: {ex}")
        except json.JSONDecodeError as ex:
            logger.debug(f"Invalid deployment info file. Exception: {ex}")
        except Exception as ex:
            logger.debug(f"Couldn't get deployment info from {file_path}. Exception: {ex}.")

        return deployment
