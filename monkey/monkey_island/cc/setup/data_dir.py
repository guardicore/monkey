import logging
import os
import shutil
from pathlib import Path

from common.utils.file_utils import create_secure_directory
from common.version import get_version
from monkey_island.cc.setup.env_utils import is_running_on_docker
from monkey_island.cc.setup.version_file_setup import get_version_from_dir, write_version

logger = logging.getLogger(__name__)


class IncompatibleDataDirectory(Exception):
    pass


def setup_data_dir(data_dir_path: Path):
    logger.info(f"Setting up data directory at {data_dir_path}.")
    if _is_data_dir_old(data_dir_path):
        logger.info("Version in data directory does not match the Island's version.")
        _handle_old_data_directory(data_dir_path)
    create_secure_directory(data_dir_path)
    write_version(data_dir_path)
    logger.info(f"Data directory set up in {data_dir_path}.")


def _is_data_dir_old(data_dir_path: Path) -> bool:
    dir_exists = data_dir_path.exists()

    if is_running_on_docker():
        return _is_docker_data_dir_old(data_dir_path)

    if not dir_exists or _is_directory_empty(data_dir_path):
        return False

    return _data_dir_version_mismatch_exists(data_dir_path)


def _is_docker_data_dir_old(data_dir_path: Path) -> bool:
    if _data_dir_version_mismatch_exists(data_dir_path):
        if _is_directory_empty(data_dir_path):
            return False
        else:
            raise IncompatibleDataDirectory(
                "Found an old volume. "
                "You must create an empty volume for each docker container "
                "as specified in setup documentation: "
                "https://techdocs.akamai.com/infection-monkey/docs/docker/"
            )
    else:
        return False


def _is_directory_empty(path: Path) -> bool:
    return not os.listdir(path)


def _handle_old_data_directory(data_dir_path: Path) -> None:
    should_delete_data_directory = _prompt_user_to_delete_data_directory(data_dir_path)
    if should_delete_data_directory:
        shutil.rmtree(data_dir_path)
        logger.info(f"{data_dir_path} was deleted.")
    else:
        raise IncompatibleDataDirectory(
            "Unable to set up data directory. Please backup and delete the existing data directory"
            f" ({data_dir_path}). Then, try again. To learn how to restore and use a backup, please"
            " refer to the documentation."
        )


def _prompt_user_to_delete_data_directory(data_dir_path: Path) -> bool:
    user_response = input(
        f"\nExisting data directory ({data_dir_path}) needs to be deleted."
        " All data from previous runs will be lost. Proceed to delete? (y/n) "
    )
    print()
    if user_response.lower() in {"y", "yes"}:
        return True
    return False


def _data_dir_version_mismatch_exists(data_dir_path: Path) -> bool:
    try:
        data_dir_version = get_version_from_dir(data_dir_path)
    except FileNotFoundError:
        logger.debug("Version file not found.")
        return True

    island_version = get_version()

    return island_version != data_dir_version
