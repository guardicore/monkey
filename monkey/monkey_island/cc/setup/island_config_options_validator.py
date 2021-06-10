import os

from monkey_island.cc.setup.island_config_options import IslandConfigOptions


def raise_on_invalid_options(options: IslandConfigOptions):
    _raise_if_not_isfile(options.crt_path)
    _raise_if_not_isfile(options.key_path)


def _raise_if_not_isfile(f: str):
    if not os.path.isfile(f):
        raise FileNotFoundError(f"{f} does not exist or is not a regular file.")
