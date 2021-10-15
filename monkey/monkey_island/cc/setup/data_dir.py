import logging
import shutil
from pathlib import Path

from common.version import get_version
from monkey_island.cc.server_utils.file_utils import create_secure_directory
from monkey_island.cc.setup.version_file_setup import (
    get_version_from_dir,
    is_version_greater,
    write_version,
)

logger = logging.getLogger(__name__)
_data_dir_backup_suffix = ".old"


def setup_data_dir(data_dir_path: Path):
    logger.info("Setting up data directory.")
    _reset_data_dir(data_dir_path)
    create_secure_directory(str(data_dir_path))
    write_version(data_dir_path)
    logger.info("Data directory set up.")


def _reset_data_dir(data_dir_path: Path):
    try:
        data_dir_version = get_version_from_dir(data_dir_path)
    except FileNotFoundError:
        logger.info("Version file not found on the data directory.")
        _backup_old_data_dir(data_dir_path)
        return

    island_version = get_version()
    logger.info(f"Version found in the data directory: {data_dir_version}")
    logger.info(f"Currently running version: {island_version}")
    if is_version_greater(island_version, data_dir_version):
        _backup_old_data_dir(data_dir_path)


def _backup_old_data_dir(data_dir_path: Path):
    logger.info("Attempting to backup old data directory.")
    try:
        backup_path = _get_backup_path(data_dir_path)
        if backup_path.is_dir():
            shutil.rmtree(backup_path)
        Path(data_dir_path).replace(backup_path)
        logger.info(f"Old data directory moved to {backup_path}.")
    except FileNotFoundError:
        logger.info("Old data directory not found, nothing to backup.")


def _get_backup_path(data_dir_path: Path) -> Path:
    backup_dir_name = data_dir_path.name + _data_dir_backup_suffix
    return Path(data_dir_path.parent, backup_dir_name)
