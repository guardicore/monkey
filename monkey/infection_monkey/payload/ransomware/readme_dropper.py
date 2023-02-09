import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def leave_readme(src: Path, dest: Path):
    if dest.exists():
        logger.warning(f"{dest} already exists, not leaving a new README.txt")
        return

    logger.info(f"Leaving a ransomware README file at {dest}")
    # Opening file to convert line endings
    with open(src, "r") as src_file:
        with open(dest, "w") as dst_file:
            dst_file.write(src_file.read())
