import base64
import json
import logging
from pathlib import PurePath
from typing import Collection, Optional, Set

logger = logging.getLogger(__name__)


class ChromeBrowserLocalState:
    """
    The local state for a Chrome-based browser

    This is stored in a file named "Local State" in the browser's local data directory

    :param local_state_file_path: Path to the browser's local state file
    """

    def __init__(self, local_state_file_path: PurePath):
        self._browser_profile_names: Set[str] = set()
        self._master_key: Optional[bytes] = None
        self._parse_local_state_file(local_state_file_path)

    def _parse_local_state_file(self, local_state_file_path: PurePath):
        with open(local_state_file_path) as f:
            try:
                local_state_object = json.load(f)
            except json.decoder.JSONDecodeError as err:
                logger.error(f'Couldn\'t deserialize JSON file at "{local_state_file_path}": {err}')
                local_state_object = {}

            try:
                self._browser_profile_names = set(
                    local_state_object["profile"]["info_cache"].keys()
                )
            except KeyError as err:
                logger.error(
                    "Exception encountered while trying to load user profiles "
                    f"from browser's local state: {err}"
                )
                self._browser_profile_names = set()

            try:
                self._master_key = base64.b64decode(local_state_object["os_crypt"]["encrypted_key"])
            except KeyError as err:
                logger.error(
                    "Exception encountered while trying to get master key "
                    f"from browser's local state: {err}"
                )
                self.master_key = None

    def get_profile_names(self) -> Collection[str]:
        return self._browser_profile_names

    def get_master_key(self) -> Optional[bytes]:
        return self._master_key
