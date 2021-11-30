from __future__ import annotations

from dpath import util

from common.utils.file_utils import expand_path
from monkey_island.cc.server_utils.consts import (
    DEFAULT_CERTIFICATE_PATHS,
    DEFAULT_CRT_PATH,
    DEFAULT_DATA_DIR,
    DEFAULT_KEY_PATH,
    DEFAULT_LOG_LEVEL,
    DEFAULT_START_MONGO_DB,
)

_DATA_DIR = "data_dir"
_SSL_CERT = "ssl_certificate"
_SSL_CERT_FILE = "ssl_certificate_file"
_SSL_CERT_KEY = "ssl_certificate_key_file"
_MONGODB = "mongodb"
_START_MONGODB = "start_mongodb"
_LOG_LEVEL = "log_level"


class IslandConfigOptions:
    def __init__(self, config_contents: dict = None):
        if not config_contents:
            config_contents = {}
        self.data_dir = expand_path(config_contents.get(_DATA_DIR, DEFAULT_DATA_DIR))

        self.log_level = config_contents.get(_LOG_LEVEL, DEFAULT_LOG_LEVEL)

        self.start_mongodb = config_contents.get(
            _MONGODB, {_START_MONGODB: DEFAULT_START_MONGO_DB}
        ).get(_START_MONGODB, DEFAULT_START_MONGO_DB)

        self.crt_path = expand_path(
            config_contents.get(_SSL_CERT, DEFAULT_CERTIFICATE_PATHS).get(
                _SSL_CERT_FILE, DEFAULT_CRT_PATH
            )
        )
        self.key_path = expand_path(
            config_contents.get(_SSL_CERT, DEFAULT_CERTIFICATE_PATHS).get(
                _SSL_CERT_KEY, DEFAULT_KEY_PATH
            )
        )

    def update(self, target: dict):
        target = self._expand_config_paths(target)
        self.__dict__.update(target)

    @staticmethod
    def _expand_config_paths(config: dict) -> dict:
        config_paths = [_DATA_DIR, f"{_SSL_CERT}.{_SSL_CERT_FILE}", f"{_SSL_CERT}.{_SSL_CERT_KEY}"]

        for config_path in config_paths:
            try:
                expanded_val = expand_path(util.get(config, config_path, "."))
                util.set(config, config_path, expanded_val, ".")
            except KeyError:
                pass

        return config
