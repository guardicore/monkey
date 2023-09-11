import base64
import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Collection, Iterator, Optional, Set

logger = logging.getLogger(__name__)


@dataclass
class ChromeBrowserLocalState:
    """
    The local state for a Chrome-based browser

    This is stored in a file named "Local State" in the browser's local data directory
    """

    profile_names: Set[str] = field(default_factory=set)
    master_key: Optional[bytes] = None


class ChromeBrowserLocalData:
    """
    The local data for a Chrome-based browser

    :param local_data_directory_path: Path to the browser's local data directory
    """

    def __init__(self, local_data_directory_path: Path):
        self._local_data_directory_path = local_data_directory_path
        local_state = self._parse_local_state_file(local_data_directory_path / "Local State")
        self._profile_names = local_state.profile_names
        self._master_key = local_state.master_key

    @staticmethod
    def _parse_local_state_file(local_state_file_path: Path) -> ChromeBrowserLocalState:
        """
        Parse the local state file for a Chrome-based browser
        """

        local_state = ChromeBrowserLocalState()
        try:
            with open(local_state_file_path) as f:
                local_state_object = json.load(f)
                local_state.profile_names = set(local_state_object["profile"]["info_cache"].keys())
                local_state.master_key = base64.b64decode(
                    local_state_object["os_crypt"]["encrypted_key"]
                )
        except FileNotFoundError:
            logger.error(f'Couldn\'t find local state file at "{local_state_file_path}"')
        except json.decoder.JSONDecodeError as err:
            logger.error(f'Couldn\'t deserialize JSON file at "{local_state_file_path}": {err}')
        except KeyError as err:
            logger.error(
                "Exception encountered while trying to parse the browser's local state state: "
                f"{err}"
            )
        finally:
            return local_state

    @property
    def profile_names(self) -> Collection[str]:
        """
        Get the names of all profiles for this browser
        """

        return self._profile_names

    @property
    def credentials_database_paths(self) -> Iterator[Path]:
        """
        Get the paths to all of the browser's credentials databases
        """

        for profile_name in self._profile_names:
            database_path = Path(self._local_data_directory_path) / profile_name / "Login Data"

            if database_path.exists() and database_path.is_file():
                yield database_path

    @property
    def master_key(self) -> Optional[bytes]:
        """
        Get the master key used to encrypt the browser's credentials databases
        """
        return self._master_key
