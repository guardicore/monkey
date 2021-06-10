import logging
import os
import platform


def is_windows_os() -> bool:
    return platform.system() == "Windows"


if is_windows_os():
    import win32file
    import win32security

    import monkey_island.cc.environment.windows_permissions as windows_permissions

LOG = logging.getLogger(__name__)


def create_secure_directory(path: str):
    if not os.path.isdir(path):
        if is_windows_os():
            _create_secure_directory_windows(path)
        else:
            _create_secure_directory_linux(path)


def _create_secure_directory_linux(path: str):
    try:
        # Don't split directory creation and permission setting
        # because it will temporarily create an accessible directory which anyone can use.
        os.mkdir(path, mode=0o700)
    except Exception as ex:
        LOG.error(
            f'Could not create a directory at "{path}" (maybe environmental variables could not be '
            f"resolved?): {str(ex)}"
        )
        raise ex


def _create_secure_directory_windows(path: str):
    try:
        security_attributes = win32security.SECURITY_ATTRIBUTES()
        security_attributes.SECURITY_DESCRIPTOR = (
            windows_permissions.get_security_descriptor_for_owner_only_perms()
        )
        win32file.CreateDirectory(path, security_attributes)
    except Exception as ex:
        LOG.error(
            f'Could not create a directory at "{path}": {str(ex)}"
        )
        raise ex
