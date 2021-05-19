import os
import sys

from monkey_island.cc.environment.windows_permissions import set_full_folder_access

is_windows_os = sys.platform.startswith("win")


def create_data_dir(data_dir: str, create_parent_dirs: bool) -> None:
    if not os.path.isdir(data_dir):
        if create_parent_dirs:
            os.makedirs(data_dir, mode=0o700)
        else:
            os.mkdir(data_dir, mode=0o700)
        if is_windows_os:  # `mode=0o700` doesn't work on Windows
            set_full_folder_access(folder_path=data_dir)
