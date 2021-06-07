from __future__ import annotations

import os

from common.utils.exceptions import InsecurePermissionsError
from monkey_island.cc.server_utils.consts import (
    DEFAULT_CERTIFICATE_PATHS,
    DEFAULT_CRT_PATH,
    DEFAULT_DATA_DIR,
    DEFAULT_KEY_PATH,
    DEFAULT_LOG_LEVEL,
    DEFAULT_START_MONGO_DB,
)
from monkey_island.cc.server_utils.file_utils import expand_path, has_expected_permissions


class IslandConfigOptions:
    def __init__(self, config_contents: dict):
        self.data_dir = expand_path(config_contents.get("data_dir", DEFAULT_DATA_DIR))

        self.log_level = config_contents.get("log_level", DEFAULT_LOG_LEVEL)

        self.start_mongodb = config_contents.get(
            "mongodb", {"start_mongodb": DEFAULT_START_MONGO_DB}
        ).get("start_mongodb", DEFAULT_START_MONGO_DB)

        self.crt_path = expand_path(
            config_contents.get("ssl_certificate", DEFAULT_CERTIFICATE_PATHS).get(
                "ssl_certificate_file", DEFAULT_CRT_PATH
            )
        )
        self.key_path = expand_path(
            config_contents.get("ssl_certificate", DEFAULT_CERTIFICATE_PATHS).get(
                "ssl_certificate_key_file", DEFAULT_KEY_PATH
            )
        )


def raise_on_invalid_options(options: IslandConfigOptions):
    _raise_if_not_isfile(options.crt_path)
    _raise_if_incorrect_permissions(options.crt_path, 0o400)

    _raise_if_not_isfile(options.key_path)
    _raise_if_incorrect_permissions(options.key_path, 0o400)


def _raise_if_not_isfile(f: str):
    if not os.path.isfile(f):
        raise FileNotFoundError(f"{f} does not exist or is not a regular file.")


def _raise_if_incorrect_permissions(f: str, expected_permissions: int):
    if not has_expected_permissions(f, expected_permissions):
        raise InsecurePermissionsError(
            f"The file {f} has incorrect permissions. Expected: {oct(expected_permissions)}"
        )
