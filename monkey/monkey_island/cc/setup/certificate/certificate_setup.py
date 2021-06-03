import logging
import os

from common.utils.exceptions import InsecurePermissionsError
from monkey_island.setup.island_config_options import IslandConfigOptions

logger = logging.getLogger(__name__)


def setup_certificate(config_options: IslandConfigOptions) -> (str, str):
    crt_path = config_options.crt_path
    key_path = config_options.key_path

    # check paths
    for file in [crt_path, key_path]:
        if not os.path.exists(file):
            raise FileNotFoundError(f"File not found at {file}. Exiting.")

        if not has_sufficient_permissions(file):
            raise InsecurePermissionsError(
                f"{file} has insecure permissions. Required permissions: r--------. Exiting."
            )

    logger.INFO(f"Using certificate path: {crt_path}, and key path: {key_path}.")

    return crt_path, key_path


def has_sufficient_permissions(path: str) -> bool:
    required_permissions = "0o400"

    file_mode = os.stat(path).st_mode
    file_permissions = oct(file_mode & 0o777)

    return file_permissions == required_permissions
