import os

from common.utils.exceptions import InsecurePermissionsError
from monkey_island.setup.island_config_options import IslandConfigOptions


def setup_certificate(config_options: IslandConfigOptions) -> (str, str):
    crt_path = config_options.crt_path
    key_path = config_options.key_path

    # check paths
    for file in [crt_path, key_path]:
        if not os.path.exists(file):
            raise FileNotFoundError(f"File not found at {file}. Exiting.")

        if not has_sufficient_permissions(file):
            raise InsecurePermissionsError(f"{file} has insecure permissions. Exiting.")

    return crt_path, key_path


def has_sufficient_permissions():
    pass
