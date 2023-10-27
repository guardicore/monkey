from __future__ import annotations

from types import MappingProxyType as ImmutableMapping
from typing import Mapping, Optional

from common.utils.file_utils import expand_path
from monkey_island.cc.server_utils.consts import (
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
NODE_PORT = "node_port"


class IslandConfigOptions:
    def __init__(self, config_contents: Mapping[str, Mapping] = ImmutableMapping({})):
        self.data_dir = DEFAULT_DATA_DIR
        self.log_level = DEFAULT_LOG_LEVEL
        self.start_mongodb = DEFAULT_START_MONGO_DB
        self.crt_path = DEFAULT_CRT_PATH
        self.key_path = DEFAULT_KEY_PATH
        self.node_port: Optional[int] = None

        self._expand_paths()

        self.update(config_contents)

    def update(self, config_contents: Mapping[str, Mapping]):
        self.data_dir = config_contents.get(_DATA_DIR, self.data_dir)

        self.log_level = config_contents.get(_LOG_LEVEL, self.log_level)
        self.node_port = config_contents.get(NODE_PORT, self.node_port)

        self.start_mongodb = config_contents.get(
            _MONGODB, {_START_MONGODB: self.start_mongodb}
        ).get(_START_MONGODB, self.start_mongodb)

        self.crt_path = config_contents.get(_SSL_CERT, {_SSL_CERT_FILE: self.crt_path}).get(
            _SSL_CERT_FILE, self.crt_path
        )
        self.key_path = config_contents.get(_SSL_CERT, {_SSL_CERT_KEY: self.key_path}).get(
            _SSL_CERT_KEY, self.key_path
        )

        self._expand_paths()

    def _expand_paths(self):
        self.data_dir = expand_path(str(self.data_dir))
        self.crt_path = expand_path(str(self.crt_path))
        self.key_path = expand_path(str(self.key_path))
