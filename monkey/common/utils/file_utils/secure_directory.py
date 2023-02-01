import logging
import stat
from pathlib import Path

from ..environment import is_windows_os

if is_windows_os():
    import win32file
    import win32security

    from .. import windows_permissions

logger = logging.getLogger(__name__)


class FailedDirectoryCreationError(Exception):
    pass


def create_secure_directory(path: Path):
    if is_windows_os():
        _check_existing_directory_is_secure = _check_existing_directory_is_secure_windows
        _create_secure_directory = _create_secure_directory_windows
    else:
        _check_existing_directory_is_secure = _check_existing_directory_is_secure_linux
        _create_secure_directory = _create_secure_directory_linux

    if path.exists():
        if not path.is_dir():
            raise FailedDirectoryCreationError(
                f'The path "{path}" already exists and is not a directory'
            )
        _check_existing_directory_is_secure(path)
    else:
        _create_secure_directory(path)


def _check_existing_directory_is_secure_windows(path: Path):
    acl, user_sid = windows_permissions.get_acl_and_sid_from_path(path)

    if acl.GetAceCount() != 1:
        is_secure_and_accessible = False
    else:
        ace = acl.GetExplicitEntriesFromAcl()[0]
        ace_sid = ace["Trustee"]["Identifier"]
        ace_permissions = ace["AccessPermissions"]
        ace_access_mode = ace["AccessMode"]
        ace_inheritance = ace["Inheritance"]

        is_secure_and_accessible = (
            (ace_sid == user_sid)
            & (ace_permissions == windows_permissions.ACCESS_PERMISSIONS_FULL_CONTROL)
            & (ace_access_mode == windows_permissions.ACCESS_MODE_GRANT_ACCESS)
            & (ace_inheritance == windows_permissions.INHERITANCE_OBJECT_AND_CONTAINER)
        )

    if not is_secure_and_accessible:
        raise FailedDirectoryCreationError(
            f'The directory "{path}" already exists and is insecure or unaccessible'
        )


def _create_secure_directory_windows(path: Path):
    try:
        # Don't split directory creation and permission setting
        # because it will temporarily create an accessible directory which anyone can use.
        security_attributes = win32security.SECURITY_ATTRIBUTES()
        security_attributes.SECURITY_DESCRIPTOR = (
            windows_permissions.get_security_descriptor_for_owner_only_perms()
        )
        win32file.CreateDirectory(str(path), security_attributes)

    except Exception as ex:
        message = f'Could not create a directory at "{path}": {str(ex)}'
        logger.error(message)
        raise FailedDirectoryCreationError(message)


def _check_existing_directory_is_secure_linux(path: Path):
    path_mode = path.stat().st_mode

    is_secure = (path_mode & (stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)) == stat.S_IRWXU

    if not is_secure:
        raise FailedDirectoryCreationError(f'The directory "{path}" already exists and is insecure')


def _create_secure_directory_linux(path: Path):
    try:
        # Don't split directory creation and permission setting
        # because it will temporarily create an accessible directory which anyone can use.
        path.mkdir(mode=stat.S_IRWXU)

    except Exception as ex:
        message = f'Could not create a directory at "{path}": {str(ex)}'
        logger.error(message)
        raise FailedDirectoryCreationError(message)
