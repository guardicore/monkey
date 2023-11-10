import ctypes
import logging
from pathlib import Path

from monkeytypes import OperatingSystem

SPI_SETDESKWALLPAPER = 20

logger = logging.getLogger(__name__)

# Textless wallpaper can be downloaded from
# https://guardicore-infectionmonkey.s3.amazonaws.com/Files/Assets/ransomware_wallpaper_no_text.png


class WallpaperChanger:
    WALLPAPER_PATH = Path(__file__).parent / "ransomware_wallpaper.png"

    def __init__(self, operating_system: OperatingSystem):
        self._operating_system = operating_system

    def change_wallpaper(self):
        if self._operating_system == OperatingSystem.WINDOWS:
            logger.info("Attempting to change the wallpaper on Windows OS")
            ctypes.windll.user32.SystemParametersInfoW(  # type: ignore [attr-defined]
                SPI_SETDESKWALLPAPER, 0, str(self.WALLPAPER_PATH), 3
            )
            logger.info("Wallpaper changed")
