import os

from common.utils.exceptions import InsecurePermissionsError
from monkey_island.cc.server_utils.file_utils import has_expected_permissions


def ensure_file_existence(file: str) -> None:
    if not os.path.exists(file):
        raise FileNotFoundError(f"File not found at {file}. Exiting.")


def ensure_file_permissions(file: str) -> None:
    if not has_expected_permissions(path=file, expected_permissions="0o400"):
        raise InsecurePermissionsError(
            f"{file} has insecure permissions. Required permissions: 400. Exiting."
        )
