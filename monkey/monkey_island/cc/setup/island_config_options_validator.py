import os
from pathlib import Path

from monkey_island.cc.setup.island_config_options import IslandConfigOptions


def raise_on_invalid_options(options: IslandConfigOptions):
    _raise_if_not_isfile(options.ssl_certificate.ssl_certificate_file)
    _raise_if_not_isfile(options.ssl_certificate.ssl_certificate_key_file)


def _raise_if_not_isfile(f: Path):
    if not os.path.isfile(f):
        raise FileNotFoundError(f"{f} does not exist or is not a regular file.")
