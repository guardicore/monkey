
import os
import sys
import ctypes
import shutil
import logging
from data import resource_path

__author__ = 'itamar'

LOG = logging.getLogger(__name__)

SPI_SETDESKWALLPAPER = 20
SPIF_UPDATEINIFILE = 0x01
SPIF_SENDCHANGE = 0x02

class ChangeDesktopAction(object):
    def __init__(self, desktop_image):
        self._desktop_image = resource_path(desktop_image)

        assert os.path.exists(self._desktop_image), "desktop image %s is missing" % (self._desktop_image, )

    def do_action(self):
        ctypes_desktop_img = ctypes.c_char_p(self._desktop_image)

        # set the image
        if not bool(ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, ctypes_desktop_img, SPIF_SENDCHANGE | SPIF_UPDATEINIFILE)):
            LOG.warn("Error setting desktop wallpaper image to '%s' (error %d)",
                     ctypes_desktop_img.value, ctypes.windll.kernel32.GetLastError())
        else:
            LOG.debug("Desktop wallpaper image is set to %r", ctypes_desktop_img.value)

    def undo_action(self):
        if not bool(ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, "" , SPIF_SENDCHANGE | SPIF_UPDATEINIFILE)):
            LOG.warn("Error resetting desktop wallpaper image (error %d)",
                     ctypes.windll.kernel32.GetLastError())
        else:
            LOG.debug("Desktop wallpaper image reset")