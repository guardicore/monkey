import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def leave_readme(src: Path, dest: Path):
    if dest.exists():
        logger.warning(f"{dest} already exists, not leaving a new README.txt")
        return

    logger.info(f"Leaving a ransomware README file at {dest}")

    # Line endings differ on Windows and Linux. The README file may be stored with Linux line
    # endings. Using open() to open the destination files converts the line endings to Windows if
    # necessary. See https://github.com/guardicore/monkey/issues/2951.
    with open(src, "r") as src_file:
        with open(dest, "w") as dst_file:
            dst_file.write(src_file.read())
