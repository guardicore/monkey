import logging

from monkey_island.cc.services.utils.file_handling import (
    ensure_file_existence,
    ensure_file_permissions,
)
from monkey_island.cc.setup.island_config_options import IslandConfigOptions

logger = logging.getLogger(__name__)


def setup_certificate(config_options: IslandConfigOptions) -> (str, str):
    crt_path = config_options.crt_path
    key_path = config_options.key_path

    for file in [crt_path, key_path]:
        ensure_file_existence(file)
        ensure_file_permissions(file)

    logger.info(f"Using certificate path: {crt_path}, and key path: {key_path}.")

    return crt_path, key_path
