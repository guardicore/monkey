import logging
import os
from pathlib import Path

import monkey_island.cc.services.config

__author__ = "VakarisZ"

logger = logging.getLogger(__name__)

# Where to find file names in config
PBA_WINDOWS_FILENAME_PATH = ['monkey', 'post_breach', 'PBA_windows_filename']
PBA_LINUX_FILENAME_PATH = ['monkey', 'post_breach', 'PBA_linux_filename']
PBA_UPLOAD_PATH = ['monkey_island', 'cc', 'userUploads']
UPLOADS_DIR = Path(*PBA_UPLOAD_PATH)


def remove_PBA_files():
    if monkey_island.cc.services.config.ConfigService.get_config():
        windows_filename = monkey_island.cc.services.config.ConfigService.get_config_value(PBA_WINDOWS_FILENAME_PATH)
        linux_filename = monkey_island.cc.services.config.ConfigService.get_config_value(PBA_LINUX_FILENAME_PATH)
        if linux_filename:
            remove_file(linux_filename)
        if windows_filename:
            remove_file(windows_filename)


def remove_file(file_name):
    file_path = os.path.join(UPLOADS_DIR, file_name)
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except OSError as e:
        logger.error("Can't remove previously uploaded post breach files: %s" % e)


def set_config_PBA_files(config_json):
    """
    Sets PBA file info in config_json to current config's PBA file info values.
    :param config_json: config_json that will be modified
    """
    if monkey_island.cc.services.config.ConfigService.get_config():
        linux_filename = monkey_island.cc.services.config.ConfigService.get_config_value(PBA_LINUX_FILENAME_PATH)
        windows_filename = monkey_island.cc.services.config.ConfigService.get_config_value(PBA_WINDOWS_FILENAME_PATH)
        config_json['monkey']['post_breach']['PBA_linux_filename'] = linux_filename
        config_json['monkey']['post_breach']['PBA_windows_filename'] = windows_filename
