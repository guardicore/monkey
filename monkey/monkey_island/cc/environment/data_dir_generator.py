import logging
import os

from monkey_island.cc.environment.utils import is_windows_os
from monkey_island.cc.environment.windows_permissions import set_full_folder_access

LOG = logging.getLogger(__name__)


def create_data_dir(data_dir: str, create_parent_dirs: bool) -> None:
    if not os.path.isdir(data_dir):
        try:
            if create_parent_dirs:
                os.makedirs(data_dir, mode=0o700)
            else:
                os.mkdir(data_dir, mode=0o700)
        except Exception as ex:
            LOG.error(
                f'Could not create data directory at "{data_dir}" (maybe `$HOME` could not be '
                f"resolved?): {str(ex)}"
            )

        if is_windows_os():  # `mode=0o700` doesn't work on Windows
            try:
                set_full_folder_access(folder_path=data_dir)
            except Exception as ex:
                LOG.error(
                    f'Data directory was created at "{data_dir}" but permissions could not be '
                    f"set successfully: {str(ex)}"
                )
