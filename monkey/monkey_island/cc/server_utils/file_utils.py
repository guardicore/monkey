import os


def expand_path(path: str) -> str:
    return os.path.expandvars(os.path.expanduser(path))


def has_expected_permissions(path: str, expected_permissions: int) -> bool:
    file_mode = os.stat(path).st_mode
    file_permissions = file_mode & 0o777

    return file_permissions == expected_permissions
