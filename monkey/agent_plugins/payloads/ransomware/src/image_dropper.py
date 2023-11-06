import ctypes
import logging
import shutil
from pathlib import Path

from common import OperatingSystem

SPI_SETDESKWALLPAPER = 20
logger = logging.getLogger(__name__)


class ImageDropper:
    def __init__(self, operating_system: OperatingSystem):
        self._operating_system = operating_system

    def change_wallpaper(self, src: Path, dest: Path):
        if dest.exists():
            logger.warning(f"{dest} already exists, not leaving a new image")
            return

        logger.info(f"Leaving a ransomware image at {dest}")

        if self._operating_system == OperatingSystem.WINDOWS:
            self._leave_windows_image(src, dest)
            # Set the wallpaper after successfully dropping the image for Windows OS
            ctypes.windll.user32.SystemParametersInfoW(  # type: ignore
                SPI_SETDESKWALLPAPER, 0, str(dest), 3
            )
            logger.info(f"Wallpaper set to {dest}")
        else:
            logger.warning("Not leaving an image for non-Windows systems.")

    def _leave_windows_image(self, src: Path, dest: Path):
        shutil.copyfile(src, dest)
