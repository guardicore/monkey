import logging
import shutil
from pathlib import Path

logger = logging.getLogger(__name__)


class ReadmeDropper:
    def leave_readme(self, src: Path, dest: Path):
        if dest.exists():
            logger.warning(f"{dest} already exists, not leaving a new README.txt")
            return

        logger.info(f"Leaving a ransomware README file at {dest}")
        shutil.copyfile(src, dest)
