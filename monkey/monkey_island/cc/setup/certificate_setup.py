import logging

from monkey_island.cc.services.utils.file_handling import (
    ensure_file_existence,
    ensure_file_permissions,
)

logger = logging.getLogger(__name__)


def setup_certificate(crt_path: str, key_path: str) -> (str, str):
    for file in [crt_path, key_path]:
        ensure_file_existence(file)
        ensure_file_permissions(file)

    logger.info(f"Using certificate path: {crt_path}, and key path: {key_path}.")

    return crt_path, key_path
