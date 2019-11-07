import ctypes
import logging
import os
import pprint
import sys
import time
from ctypes import c_char_p

from infection_monkey.config import WormConfiguration
from infection_monkey.telemetry.attack.t1106_telem import T1106Telem
from common.utils.attack_utils import ScanStatus, UsageEnum
from infection_monkey.utils.startup.flag_analyzer import FlagAnalyzer
from infection_monkey.utils.startup.file_mover import FileMover
from infection_monkey.utils.startup.process_detacher import MonkeyProcessDetacher


# Linux doesn't have WindowsError
try:
    WindowsError
except NameError:
    # noinspection PyShadowingBuiltins
    WindowsError = IOError

__author__ = 'itamar'

LOG = logging.getLogger(__name__)

MOVE_FILE_DELAY_UNTIL_REBOOT = 4
DELAY_BEFORE_EXITING = 3


class MonkeyDrops(object):
    def __init__(self, args):
        self._flags = FlagAnalyzer.get_flags(args)
        self._default_server = None
        self._default_server_port = None
        self._config = {'source_path': os.path.abspath(sys.argv[0]),
                        'destination_path': self._flags.location}

    def initialize(self):
        LOG.debug("Dropper is running with config:\n%s", pprint.pformat(self._config))
        self._default_server = self._flags.server
        try:
            self._default_server_port = self._default_server.split(':')[1]
        except KeyError:
            self._default_server_port = ''

        if self._default_server:
            if self._default_server not in WormConfiguration.current_server:
                LOG.debug("Added current server: %s" % self._default_server)
                WormConfiguration.current_server = self._default_server
            else:
                LOG.debug("Default server: %s is already in command servers list" % self._default_server)

    def start(self):
        if self._config['destination_path'] is None:
            LOG.error("No destination path specified")
            return False

        FileMover.move_file(self._config['source_path'], self._config['destination_path'])

        if WormConfiguration.dropper_set_date:
            self._set_date()

        monkey_process = MonkeyProcessDetacher(self._flags, self._config['destination_path']).detach_process()

        time.sleep(DELAY_BEFORE_EXITING)
        if monkey_process.poll() is not None:
            LOG.warning("Seems like monkey died too soon")

    def cleanup(self):
        try:
            if (self._config['source_path'].lower() != self._config['destination_path'].lower()) and \
                    os.path.exists(self._config['source_path']) and \
                    WormConfiguration.dropper_try_move_first:

                # try removing the file first
                try:
                    # TODO uncomment os.remove(self._config['source_path'])
                    print()
                except Exception as exc:
                    LOG.debug("Error removing source file '%s': %s", self._config['source_path'], exc)

                    # mark the file for removal on next boot
                    dropper_source_path_ctypes = c_char_p(self._config['source_path'])
                    if 0 == ctypes.windll.kernel32.MoveFileExA(dropper_source_path_ctypes, None,
                                                               MOVE_FILE_DELAY_UNTIL_REBOOT):
                        LOG.debug("Error marking source file '%s' for deletion on next boot (error %d)",
                                  self._config['source_path'], ctypes.windll.kernel32.GetLastError())
                    else:
                        LOG.debug("Dropper source file '%s' is marked for deletion on next boot",
                                  self._config['source_path'])
                        T1106Telem(ScanStatus.USED, UsageEnum.DROPPER_WINAPI).send()
        except AttributeError:
            LOG.error("Invalid configuration options. Failing")

    def _set_date(self):
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
                os.utime(self._config['destination_path'], (ref_stat.st_atime, ref_stat.st_mtime))
            except:
                LOG.warning("Cannot set reference date to destination file")
