import logging
import os
import platform


def is_windows_os() -> bool:
    return platform.system() == "Windows"


if is_windows_os():
    import win32file
    import win32job
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
        LOG.error(f'Could not create a directory at "{path}": {str(ex)}')
        raise ex


def _create_secure_directory_windows(path: str):
    try:
        security_attributes = win32security.SECURITY_ATTRIBUTES()
        security_attributes.SECURITY_DESCRIPTOR = (
            windows_permissions.get_security_descriptor_for_owner_only_perms()
        )
        win32file.CreateDirectory(path, security_attributes)

    except Exception as ex:
        LOG.error(f'Could not create a directory at "{path}": {str(ex)}')
        raise ex


def create_secure_file(path: str):
    if not os.path.isfile(path):
        if is_windows_os():
            _create_secure_file_windows(path)
        else:
            _create_secure_file_linux(path)


def _create_secure_file_linux(path: str):
    try:
        flags = (
            os.O_RDWR | os.O_CREAT | os.O_EXCL
        )  # read/write, create new, throw error if file exists
        mode = 0o700  # read/write/execute permissions to owner
        os.close(os.open(path, flags, mode))

    except Exception as ex:
        LOG.error(f'Could not create a file at "{path}": {str(ex)}')
        raise ex


def _create_secure_file_windows(path: str):
    try:
        file_access = win32file.GENERIC_READ | win32file.GENERIC_WRITE
        file_sharing = (
            win32file.FILE_SHARE_READ
        )  # subsequent open operations on the object will succeed only if read access is requested
        security_attributes = win32security.SECURITY_ATTRIBUTES()
        security_attributes.SECURITY_DESCRIPTOR = (
            windows_permissions.get_security_descriptor_for_owner_only_perms()
        )
        file_creation = win32file.CREATE_NEW  # fails if file exists
        file_attributes = win32file.FILE_FLAG_BACKUP_SEMANTICS

        win32file.CloseHandle(
            win32file.CreateFile(
                path,
                file_access,
                file_sharing,
                security_attributes,
                file_creation,
                file_attributes,
                win32job.CreateJobObject(
                    None, ""
                ),  # https://stackoverflow.com/questions/46800142/in-python-with-pywin32-win32job-the-createjobobject-function-how-do-i-pass-nu  # noqa: E501
            )
        )

    except Exception as ex:
        LOG.error(f'Could not create a file at "{path}": {str(ex)}')
        raise ex
