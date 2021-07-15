import logging
import shutil
from pathlib import Path

LOG = logging.getLogger(__name__)


def leave_readme(src: Path, dest: Path):
    if dest.exists():
        LOG.warning(f"{dest} already exists, not leaving a new README.txt")
        return

    _copy_readme_file(src, dest)


def _copy_readme_file(src: Path, dest: Path):
    LOG.info(f"Leaving a ransomware README file at {dest}")

    try:
        shutil.copyfile(src, dest)
    except Exception as ex:
        LOG.warning(f"An error occurred while attempting to leave a README.txt file: {ex}")
