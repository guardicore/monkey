import os
import struct
import subprocess
import sys

import monkeyfs
from config import WormConfiguration
from control import ControlClient
from exploit.tools import build_monkey_commandline_explicitly
from model import DROPPER_CMDLINE_WINDOWS

__author__ = 'itay.mizeretz'

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
        with open(WormConfiguration.dropper_upgrade_win_64_temp_path, 'wb') as written_monkey_file:
            written_monkey_file.write(monkey_bin)

        depth = int(opts.depth) if opts.depth is not None else None
        monkey_options = build_monkey_commandline_explicitly(
            opts.parent, opts.tunnel, opts.server, depth, WormConfiguration.dropper_target_path)

        monkey_cmdline = DROPPER_CMDLINE_WINDOWS % {
            'dropper_path': WormConfiguration.dropper_upgrade_win_64_temp_path} + monkey_options

        print monkey_cmdline
        monkey_process = subprocess.Popen(monkey_cmdline, shell=True,
                                          stdin=None, stdout=None, stderr=None,
                                          close_fds=True, creationflags=DETACHED_PROCESS)
