from pathlib import Path, PurePath
from typing import Collection, Iterator, Optional

from .chrome_browser_local_state import parse_local_state_file


class ChromeBrowserLocalData:
    """
    The local data for a Chrome-based browser

    :param local_data_directory_path: Path to the browser's local data directory
    """

    def __init__(self, local_data_directory_path: PurePath):
        self._local_data_directory_path = local_data_directory_path
        self._local_state = parse_local_state_file(local_data_directory_path / Path("Local State"))

    @property
    def profile_names(self) -> Collection[str]:
        """
        Get the names of all profiles for this browser
        """

        return self._local_state.profile_names

    @property
    def credentials_database_paths(self) -> Iterator[PurePath]:
        """
        Get the paths to all of the browser's credentials databases
        """

        for profile_name in self.profile_names:
            database_path = Path(self._local_data_directory_path) / profile_name / "Login Data"

            if database_path.exists() and database_path.is_file():
                yield database_path

    @property
    def master_key(self) -> Optional[bytes]:
        """
        Get the master key used to encrypt the browser's credentials databases
        """
        return self._local_state.master_key
