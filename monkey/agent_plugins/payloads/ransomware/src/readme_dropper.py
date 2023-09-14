import logging
import shutil
from pathlib import Path

from common import OperatingSystem

logger = logging.getLogger(__name__)


class ReadmeDropper:
    def __init__(self, operating_system: OperatingSystem):
        self._operating_system = operating_system

    def leave_readme(self, src: Path, dest: Path):
        if dest.exists():
            logger.warning(f"{dest} already exists, not leaving a new README.txt")
            return

        logger.info(f"Leaving a ransomware README file at {dest}")

        if self._operating_system == OperatingSystem.WINDOWS:
            self._leave_windows_readme(src, dest)
        else:
            self._leave_posix_readme(src, dest)

    def _leave_windows_readme(self, src: Path, dest: Path):
        with open(src, "rb") as src_file:
            posix_readme = src_file.read()

        windows_readme = posix_readme.replace(b"\n", b"\r\n")

        with open(dest, "wb") as dest_file:
            dest_file.write(windows_readme)

    def _leave_posix_readme(self, src: Path, dest: Path):
        shutil.copyfile(src, dest)
