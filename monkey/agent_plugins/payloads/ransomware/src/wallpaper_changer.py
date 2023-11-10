import ctypes
import logging
from pathlib import Path

from monkeytypes import OperatingSystem

from common.utils.environment import is_windows_os

SPI_SETDESKWALLPAPER = 20

logger = logging.getLogger(__name__)


class WallpaperChanger:
    WALLPAPER_PATH = Path(__file__).parent / "ransomware_wallpaper.png"

    def __init__(self, operating_system: OperatingSystem):
        self._operating_system = operating_system

    def change_wallpaper(self):
        if is_windows_os():
            logger.info("Attempting to change the wallpaper on Windows OS")
            ctypes.windll.user32.SystemParametersInfoW(  # type: ignore [attr-defined]
                SPI_SETDESKWALLPAPER, 0, str(self.WALLPAPER_PATH), 3
            )
            logger.info("Wallpaper changed")
