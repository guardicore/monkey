import logging
import os
import platform
import stat
import subprocess
from shutil import copyfile

import monkey_island.cc.environment.environment_singleton as env_singleton
from monkey_island.cc.resources.monkey_download import get_monkey_executable
from monkey_island.cc.server_utils.consts import MONKEY_ISLAND_ABS_PATH
from monkey_island.cc.services.utils.network_utils import local_ip_addresses

logger = logging.getLogger(__name__)


class RunLocalMonkeyService:
    DATA_DIR = None

    # TODO: A number of these services should be instance objects instead of
    # static/singleton hybrids. At the moment, this requires invasive refactoring that's
    # not a priority.
    @classmethod
    def initialize(cls, data_dir):
        cls.DATA_DIR = data_dir

    @staticmethod
    def run_local_monkey():
        # get the monkey executable suitable to run on the server
        result = get_monkey_executable(platform.system().lower(), platform.machine().lower())
        if not result:
            return False, "OS Type not found"

        src_path = os.path.join(MONKEY_ISLAND_ABS_PATH, "cc", "binaries", result["filename"])
        dest_path = os.path.join(RunLocalMonkeyService.DATA_DIR, result["filename"])

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
            port = env_singleton.env.get_island_port()

            args = [dest_path, "m0nk3y", "-s", f"{ip}:{port}"]
            subprocess.Popen(args, cwd=RunLocalMonkeyService.DATA_DIR)
        except Exception as exc:
            logger.error("popen failed", exc_info=True)
            return False, "popen failed: %s" % exc

        return True, ""
