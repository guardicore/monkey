import logging
import os
import struct
import subprocess
import sys

import time

import monkeyfs
from config import WormConfiguration
from control import ControlClient
from exploit.tools import build_monkey_commandline_explicitly
from model import MONKEY_CMDLINE_WINDOWS

__author__ = 'itay.mizeretz'

LOG = logging.getLogger(__name__)

if "win32" == sys.platform:
    from win32process import DETACHED_PROCESS
else:
    DETACHED_PROCESS = 0


class WindowsUpgrader(object):
    @staticmethod
    def is_64bit_os():
        return os.environ.has_key('PROGRAMFILES(X86)')

    @staticmethod
    def is_64bit_python():
        return struct.calcsize("P") == 8

    @staticmethod
    def is_windows_os():
        return sys.platform.startswith("win")

    @staticmethod
    def should_upgrade():
        return WindowsUpgrader.is_windows_os() and WindowsUpgrader.is_64bit_os() \
               and not WindowsUpgrader.is_64bit_python()

    @staticmethod
    def upgrade(opts):
        monkey_64_path = ControlClient.download_monkey_exe_by_os(True, False)
        with monkeyfs.open(monkey_64_path, "rb") as downloaded_monkey_file:
            monkey_bin = downloaded_monkey_file.read()
        with open(WormConfiguration.dropper_target_path_win_64, 'wb') as written_monkey_file:
            written_monkey_file.write(monkey_bin)

        depth = int(opts.depth) if opts.depth is not None else None
        monkey_options = build_monkey_commandline_explicitly(
            opts.parent, opts.tunnel, opts.server, depth)

        monkey_cmdline = MONKEY_CMDLINE_WINDOWS % {
            'monkey_path': WormConfiguration.dropper_target_path_win_64} + monkey_options

        monkey_process = subprocess.Popen(monkey_cmdline, shell=True,
                                          stdin=None, stdout=None, stderr=None,
                                          close_fds=True, creationflags=DETACHED_PROCESS)

        LOG.info("Executed 64bit monkey process (PID=%d) with command line: %s",
                 monkey_process.pid, monkey_cmdline)

        time.sleep(3)
        if monkey_process.poll() is not None:
            LOG.warn("Seems like monkey died too soon")
