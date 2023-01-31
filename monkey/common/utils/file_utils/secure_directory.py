import logging
import stat
from pathlib import Path

from ..environment import is_windows_os

if is_windows_os():
    import win32file
    import win32security

    from .. import windows_permissions

logger = logging.getLogger(__name__)


def create_secure_directory(path: Path):
    # TODO: Raise an exception if the directory exists and is not secure. Otherwise, the caller may
    #       think a secure directory was created when it wasn't.
    if not path.is_dir():
        if is_windows_os():
            _create_secure_directory_windows(path)
        else:
            _create_secure_directory_linux(path)


def _create_secure_directory_linux(path: Path):
    try:
        # Don't split directory creation and permission setting
        # because it will temporarily create an accessible directory which anyone can use.
        path.mkdir(mode=stat.S_IRWXU)

    except Exception as ex:
        logger.error(f'Could not create a directory at "{path}": {str(ex)}')
        raise ex


def _create_secure_directory_windows(path: Path):
    try:
        security_attributes = win32security.SECURITY_ATTRIBUTES()
        security_attributes.SECURITY_DESCRIPTOR = (
            windows_permissions.get_security_descriptor_for_owner_only_perms()
        )
        win32file.CreateDirectory(str(path), security_attributes)

    except Exception as ex:
        logger.error(f'Could not create a directory at "{path}": {str(ex)}')
        raise ex
