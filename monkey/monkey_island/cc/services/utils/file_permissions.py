import os


def has_sufficient_permissions(path: str, required_permissions: str) -> bool:
    file_mode = os.stat(path).st_mode
    file_permissions = oct(file_mode & 0o777)

    return file_permissions == required_permissions
