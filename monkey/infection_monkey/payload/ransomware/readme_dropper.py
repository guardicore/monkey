import logging
from pathlib import Path

from common.utils.environment import is_windows_os

WINDOWS_LINE_ENDING = b"\r\n"
UNIX_LINE_ENDING = b"\n"

logger = logging.getLogger(__name__)


def leave_readme(src: Path, dest: Path):
    if dest.exists():
        logger.warning(f"{dest} already exists, not leaving a new README.txt")
        return

    with open(src, "rb") as open_file:
        content = open_file.read()

    if is_windows_os():
        content = content.replace(UNIX_LINE_ENDING, WINDOWS_LINE_ENDING)

    logger.info(f"Leaving a ransomware README file at {dest}")
    with open(dest, "wb") as open_file:
        open_file.write(content)
