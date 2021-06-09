import os

from common.utils.exceptions import InsecurePermissionsError
from monkey_island.cc.environment.utils import is_windows_os
from monkey_island.cc.server_utils.file_utils import has_expected_permissions
from monkey_island.cc.setup.island_config_options import IslandConfigOptions


def raise_on_invalid_options(options: IslandConfigOptions):
    _raise_if_not_isfile(options.crt_path)
    _raise_if_incorrect_permissions(options.crt_path, 0o400, 1179817)

    _raise_if_not_isfile(options.key_path)
    _raise_if_incorrect_permissions(options.key_path, 0o400, 1179817)


def _raise_if_not_isfile(f: str):
    if not os.path.isfile(f):
        raise FileNotFoundError(f"{f} does not exist or is not a regular file.")


def _raise_if_incorrect_permissions(
    f: str, linux_expected_permissions: int, windows_expected_permissions: int
):
    expected_permissions = (
        windows_expected_permissions if is_windows_os() else linux_expected_permissions
    )
    if not has_expected_permissions(f, expected_permissions):
        raise InsecurePermissionsError(
            f"The file {f} has incorrect permissions. Expected: {oct(expected_permissions)}"
        )
