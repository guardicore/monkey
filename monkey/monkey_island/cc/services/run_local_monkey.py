import logging
import os
import platform
import stat
import subprocess
from pathlib import Path
from shutil import copyfile

from monkey_island.cc.resources.monkey_download import get_agent_executable_path
from monkey_island.cc.server_utils.consts import ISLAND_PORT
from monkey_island.cc.services.utils.network_utils import local_ip_addresses

logger = logging.getLogger(__name__)


class LocalMonkeyRunService:
    DATA_DIR = None

    # TODO: A number of these services should be instance objects instead of
    # static/singleton hybrids. At the moment, this requires invasive refactoring that's
    # not a priority.
    @classmethod
    def initialize(cls, data_dir: Path):
        cls.DATA_DIR = data_dir

    @staticmethod
    def run_local_monkey():
        # get the monkey executable suitable to run on the server
        try:
            src_path = get_agent_executable_path(platform.system().lower())
        except Exception as ex:
            logger.error(f"Error running agent from island: {ex}")
            return False, str(ex)

        dest_path = LocalMonkeyRunService.DATA_DIR / src_path.name

        # copy the executable to temp path (don't run the monkey from its current location as it may
        # delete itself)
        try:
            copyfile(src_path, dest_path)
            os.chmod(dest_path, stat.S_IRWXU | stat.S_IRWXG)
        except Exception as exc:
            logger.error("Copy file failed", exc_info=True)
            return False, "Copy file failed: %s" % exc

        # run the monkey
        try:
            ip = local_ip_addresses()[0]
            port = ISLAND_PORT

            args = [str(dest_path), "m0nk3y", "-s", f"{ip}:{port}"]
            subprocess.Popen(args, cwd=LocalMonkeyRunService.DATA_DIR)
        except Exception as exc:
            logger.error("popen failed", exc_info=True)
            return False, "popen failed: %s" % exc

        return True, ""
