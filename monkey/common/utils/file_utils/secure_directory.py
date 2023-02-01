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
        _change_existing_directory_to_secure = _change_existing_directory_to_secure_windows
        _create_secure_directory = _create_secure_directory_windows
    else:
        _change_existing_directory_to_secure = _change_existing_directory_to_secure_linux
        _create_secure_directory = _create_secure_directory_linux

    if path.exists():
        _check_path_is_directory(path)
        _change_existing_directory_to_secure(path)
    else:
        _create_secure_directory(path)


def _check_path_is_directory(path: Path):
    if not path.is_dir():
        raise FailedDirectoryCreationError(
            f'The path "{path}" already exists and is not a directory'
        )

    logger.info(f"A directory already exists at {path}")


def _change_existing_directory_to_secure_windows(path: Path):
    try:
        security_descriptor = (
            windows_permissions.get_security_descriptor_for_owner_only_permissions()
        )
        win32security.SetFileSecurity(
            str(path), win32security.DACL_SECURITY_INFORMATION, security_descriptor
        )

    except Exception as err:
        message = (
            "An error occured while changing the existing directory's permissions"
            f"to be secure: {str(err)}"
        )
        logger.exception(message)
        raise FailedDirectoryCreationError(err)


def _create_secure_directory_windows(path: Path):
    try:
        # Don't split directory creation and permission setting
        # because it will temporarily create an accessible directory which anyone can use.
        security_attributes = win32security.SECURITY_ATTRIBUTES()
        security_attributes.SECURITY_DESCRIPTOR = (
            windows_permissions.get_security_descriptor_for_owner_only_permissions()
        )
        win32file.CreateDirectory(str(path), security_attributes)

    except Exception as err:
        message = f"Could not create a secure directory at {path}: {str(err)}"
        logger.error(message)
        raise FailedDirectoryCreationError(message)


def _change_existing_directory_to_secure_linux(path: Path):
    try:
        path.chmod(mode=stat.S_IRWXU)

    except Exception as err:
        message = (
            "An error occured while changing the existing directory's permissions"
            f"to be secure: {str(err)}"
        )
        logger.exception(message)
        raise FailedDirectoryCreationError(err)


def _create_secure_directory_linux(path: Path):
    try:
        # Don't split directory creation and permission setting
        # because it will temporarily create an accessible directory which anyone can use.
        path.mkdir(mode=stat.S_IRWXU)

    except Exception as err:
        message = f"Could not create a secure directory at {path}: {str(err)}"
        logger.error(message)
        raise FailedDirectoryCreationError(message)
