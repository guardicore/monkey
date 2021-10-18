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
    logger.info(f"Setting up data directory in {data_dir_path}.")
    _backup_current_data_dir(data_dir_path)
    create_secure_directory(str(data_dir_path))
    write_version(data_dir_path)
    logger.info("Data directory set up.")


def _backup_current_data_dir(data_dir_path: Path):
    if _is_backup_needed(data_dir_path):
        logger.debug("Data directory backup needed.")
        try:
            return _rename_data_dir(data_dir_path)
        except FileNotFoundError:
            logger.debug("No data directory found to backup, this is likely a first installation.")


def _is_backup_needed(data_dir_path: Path) -> bool:
    try:
        data_dir_version = get_version_from_dir(data_dir_path)
    except FileNotFoundError:
        logger.debug("Version file not found.")
        return True

    island_version = get_version()

    return is_version_greater(island_version, data_dir_version)


def _rename_data_dir(data_dir_path: Path):
    backup_path = _get_backup_path(data_dir_path)
    if backup_path.is_dir():
        shutil.rmtree(backup_path)
    Path(data_dir_path).replace(backup_path)
    logger.info(f"Old data directory renamed to {backup_path}.")


def _get_backup_path(data_dir_path: Path) -> Path:
    backup_dir_name = data_dir_path.name + _data_dir_backup_suffix
    return Path(data_dir_path.parent, backup_dir_name)
