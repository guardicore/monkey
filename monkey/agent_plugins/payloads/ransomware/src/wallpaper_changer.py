import ctypes
from pathlib import Path

from monkeytypes import OperatingSystem

SPI_SETDESKWALLPAPER = 20


class WallpaperChanger:
    IMAGE_PATH = Path(__file__).parent / "ransomware_image.png"

    def __init__(self, operating_system: OperatingSystem):
        self._operating_system = operating_system

    def change_wallpaper(self):
        if self._operating_system == OperatingSystem.WINDOWS:
            # Directly set the wallpaper for Windows OS using the source image
            ctypes.windll.user32.SystemParametersInfoW(  # type: ignore [attr-defined]
                SPI_SETDESKWALLPAPER, 0, str(self.IMAGE_PATH), 3
            )
