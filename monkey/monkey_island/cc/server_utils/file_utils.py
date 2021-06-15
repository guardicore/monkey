import logging
import os
import platform
import stat

LOG = logging.getLogger(__name__)


def is_windows_os() -> bool:
    return platform.system() == "Windows"


if is_windows_os():
    import win32file
    import win32job
    import win32security

    import monkey_island.cc.server_utils.windows_permissions as windows_permissions


def expand_path(path: str) -> str:
    return os.path.expandvars(os.path.expanduser(path))


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
        os.mkdir(path, mode=stat.S_IRWXU)

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


def get_file_descriptor_for_new_secure_file(path: str) -> int:
    if is_windows_os():
        return _get_file_descriptor_for_new_secure_file_windows(path)
    else:
        return _get_file_descriptor_for_new_secure_file_linux(path)


def _get_file_descriptor_for_new_secure_file_linux(path: str) -> int:
    try:
        mode = stat.S_IRUSR | stat.S_IWUSR
        flags = (
            os.O_RDWR | os.O_CREAT | os.O_EXCL
        )  # read/write, create new, throw error if file exists
        fd = os.open(path, flags, mode)

        return fd

    except Exception as ex:
        LOG.error(f'Could not create a file at "{path}": {str(ex)}')
        raise ex


def _get_file_descriptor_for_new_secure_file_windows(path: str) -> int:
    try:
        file_access = win32file.GENERIC_READ | win32file.GENERIC_WRITE
        # subsequent open operations on the object will succeed only if read access is requested
        file_sharing = win32file.FILE_SHARE_READ
        security_attributes = win32security.SECURITY_ATTRIBUTES()
        security_attributes.SECURITY_DESCRIPTOR = (
            windows_permissions.get_security_descriptor_for_owner_only_perms()
        )
        file_creation = win32file.CREATE_NEW  # fails if file exists
        file_attributes = win32file.FILE_FLAG_BACKUP_SEMANTICS

        fd = win32file.CreateFile(
            path,
            file_access,
            file_sharing,
            security_attributes,
            file_creation,
            file_attributes,
            _get_null_value_for_win32(),
        )

        return fd

    except Exception as ex:
        LOG.error(f'Could not create a file at "{path}": {str(ex)}')
        raise ex


def _get_null_value_for_win32() -> None:
    # https://stackoverflow.com/questions/46800142/in-python-with-pywin32-win32job-the-createjobobject-function-how-do-i-pass-nu  # noqa: E501
    return win32job.CreateJobObject(None, "")
