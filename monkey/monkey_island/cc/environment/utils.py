import logging
import os
import platform


def is_windows_os() -> bool:
    return platform.system() == "Windows"


if is_windows_os():
    from monkey_island.cc.environment.windows_permissions import (  # noqa: E402
        set_full_folder_access,
    )
else:
    from monkey_island.cc.environment.linux_permissions import set_perms_to_owner_only  # noqa: E402

LOG = logging.getLogger(__name__)


def create_secure_directory(path: str, create_parent_dirs: bool):
    if not os.path.isdir(path):
        create_directory(path, create_parent_dirs)
        set_secure_permissions(path)


def create_directory(path: str, create_parent_dirs: bool):
    try:
        if create_parent_dirs:
            os.makedirs(path)
        else:
            os.mkdir(path)
    except Exception as ex:
        LOG.error(
            f'Could not create a directory at "{path}" (maybe `$HOME` could not be '
            f"resolved?): {str(ex)}"
        )
        raise ex


def set_secure_permissions(dir_path: str):
    try:
        if is_windows_os():
            set_full_folder_access(folder_path=dir_path)
        else:
            set_perms_to_owner_only(path=dir_path)
    except Exception as ex:
        LOG.error(f"Permissions could not be " f"set successfully for {dir_path}: {str(ex)}")
        raise ex
