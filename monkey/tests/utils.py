import ctypes
import os


def is_user_admin():
    if os.name == "posix":
        return os.getuid() == 0

    return ctypes.windll.shell32.IsUserAnAdmin()


def raise_(ex):
    raise ex
