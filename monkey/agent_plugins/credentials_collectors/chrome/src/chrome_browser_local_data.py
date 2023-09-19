import json
import logging
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Collection, Iterator, Set

logger = logging.getLogger(__name__)


@dataclass(kw_only=True)
class ChromeBrowserLocalState:
    profile_names: Set[str] = field(default_factory=set)


@contextmanager
def read_local_state(local_state_file_path: Path):
    """
    Parse the local state file for a Chrome-based browser
    """

    try:
        with open(local_state_file_path) as f:
            local_state_object = json.load(f)
            yield local_state_object
    except FileNotFoundError:
        logger.error(f'Couldn\'t find local state file at "{local_state_file_path}"')
    except json.decoder.JSONDecodeError as err:
        logger.error(f'Couldn\'t deserialize JSON file at "{local_state_file_path}": {err}')


class ChromeBrowserLocalData:
    """
    The local data for a Chrome-based browser

    :param local_data_directory_path: Path to the browser's local data directory
    """

    def __init__(self, local_data_directory_path: Path, profile_names: Collection[str]):
        self._local_data_directory_path = local_data_directory_path
        self._profile_names = profile_names

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
