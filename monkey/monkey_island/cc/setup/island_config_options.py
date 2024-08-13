from __future__ import annotations

from pathlib import Path
from typing import Annotated

from monkeytoolbox import expand_path
from monkeytypes import InfectionMonkeyBaseModel
from pydantic import BeforeValidator, Field

from monkey_island.cc.server_utils.consts import (
    DEFAULT_CRT_PATH,
    DEFAULT_DATA_DIR,
    DEFAULT_KEY_PATH,
    DEFAULT_LOG_LEVEL,
    DEFAULT_START_MONGO_DB,
)

DEFAULT_ISLAND_PORT = 443


class MongoDBConfig(InfectionMonkeyBaseModel):
    start_mongodb: bool = Field(
        default=DEFAULT_START_MONGO_DB,
        description="If enabled, the MongoDB server will be started automatically with the Island.",
    )


# TODO: rename redundant ssl_certificate_file and split the classes into idividual files
class SSLCertificatesConfig(InfectionMonkeyBaseModel):
    ssl_certificate_file: Annotated[
        Path,
        Field(
            default=Path(DEFAULT_CRT_PATH),
            description="The path to the SSL certificate file that the Island server will use.",
        ),
        BeforeValidator(expand_path),
    ]
    ssl_certificate_key_file: Annotated[
        Path,
        Field(
            default=Path(DEFAULT_KEY_PATH),
            description="The path to the SSL certificate key file that the Island server will use.",
        ),
        BeforeValidator(expand_path),
    ]


class IslandConfigOptions(InfectionMonkeyBaseModel):
    data_dir: Annotated[
        Path,
        Field(
            default=DEFAULT_DATA_DIR,
            description="The directory where the Island will store runtime artifacts.",
        ),
        BeforeValidator(expand_path),
    ]
    log_level: str = Field(
        default=DEFAULT_LOG_LEVEL, description="The threshold for the Island logger."
    )
    mongodb: MongoDBConfig = Field(
        default=MongoDBConfig(), description="The MongoDB configuration for the Island server."
    )
    ssl_certificate: SSLCertificatesConfig = Field(
        default=SSLCertificatesConfig(),
        description="The SSL certificates configuration for the Island server.",
    )
    island_port: int = Field(
        default=DEFAULT_ISLAND_PORT,
        description="The port on which the Island server should listen.",
    )
