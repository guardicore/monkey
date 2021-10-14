import logging
import shutil

from common.version import get_version
from monkey_island.cc.server_utils.file_utils import create_secure_directory
from monkey_island.cc.setup.version_file_setup import (
    get_version_from_dir,
    is_version_greater,
    write_version,
)

logger = logging.getLogger(__name__)


def setup_data_dir(data_dir_path: str):
    logger.info("Setting up data directory.")
    _reset_data_dir(data_dir_path)
    create_secure_directory(data_dir_path)
    write_version(data_dir_path)
    logger.info("Data directory set up.")


def _reset_data_dir(data_dir_path: str):
    try:
        data_dir_version = get_version_from_dir(data_dir_path)
    except FileNotFoundError:
        logger.info("Version file not found on the data directory.")
        _remove_data_dir(data_dir_path)
        return

    island_version = get_version()
    logger.info(f"Version found in the data directory: {data_dir_version}")
    logger.info(f"Currently running version: {island_version}")
    if is_version_greater(island_version, data_dir_version):
        _remove_data_dir(data_dir_path)


def _remove_data_dir(data_dir_path: str):
    logger.info("Attempting to remove data directory.")
    try:
        shutil.rmtree(data_dir_path)
        logger.info("Data directory removed.")
    except FileNotFoundError:
        logger.info("Data directory not found, nothing to remove.")
