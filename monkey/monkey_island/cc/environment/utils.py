import logging
import os
import platform


def is_windows_os() -> bool:
    return platform.system() == "Windows"


if is_windows_os():
    import monkey_island.cc.environment.windows_permissions as windows_permissions

LOG = logging.getLogger(__name__)


def create_secure_directory(path: str, create_parent_dirs: bool):
    if not os.path.isdir(path):
        _create_secure_directory(path, create_parent_dirs)
        set_secure_permissions(path)


def _create_secure_directory(path: str, create_parent_dirs: bool):
    try:
        if create_parent_dirs:
            # Don't split directory creation and permission setting
            # because it will temporarily create an accessible directory which anyone can use.
            os.makedirs(path, mode=0o700)
        else:
            os.mkdir(path, mode=0o700)
    except Exception as ex:
        LOG.error(
            f'Could not create a directory at "{path}" (maybe environmental variables could not be '
            f"resolved?): {str(ex)}"
        )
        raise ex


def set_secure_permissions(dir_path: str):
    try:
        if is_windows_os():
            windows_permissions.set_perms_to_owner_only(folder_path=dir_path)
    except Exception as ex:
        LOG.error(f"Permissions could not be set successfully for {dir_path}: {str(ex)}")
        raise ex
