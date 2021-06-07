import os

from common.utils.exceptions import InsecurePermissionsError


def ensure_file_existence(file: str) -> None:
    if not os.path.exists(file):
        raise FileNotFoundError(f"File not found at {file}. Exiting.")


def ensure_file_permissions(file: str) -> None:
    if not file_has_expected_permissions(path=file, expected_permissions="0o400"):
        raise InsecurePermissionsError(
            f"{file} has insecure permissions. Required permissions: r--------. Exiting."
        )


def file_has_expected_permissions(path: str, expected_permissions: str) -> bool:
    file_mode = os.stat(path).st_mode
    file_permissions = oct(file_mode & 0o777)

    return file_permissions == expected_permissions
