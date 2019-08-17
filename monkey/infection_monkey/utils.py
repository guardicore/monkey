import os
import shutil
import struct
import sys
import tempfile
import ctypes
import ctypes.wintypes

from infection_monkey.config import WormConfiguration


def get_monkey_log_path():
    return os.path.expandvars(WormConfiguration.monkey_log_path_windows) if sys.platform == "win32" \
        else WormConfiguration.monkey_log_path_linux


def get_dropper_log_path():
    return os.path.expandvars(WormConfiguration.dropper_log_path_windows) if sys.platform == "win32" \
        else WormConfiguration.dropper_log_path_linux


def is_64bit_windows_os():
    """
    Checks for 64 bit Windows OS using environment variables.
    """
    return 'PROGRAMFILES(X86)' in os.environ


def is_64bit_python():
    return struct.calcsize("P") == 8


def is_windows_os():
    return sys.platform.startswith("win")


def utf_to_ascii(string):
    # Converts utf string to ascii. Safe to use even if string is already ascii.
    udata = string.decode("utf-8")
    return udata.encode("ascii", "ignore")


def create_monkey_dir():
    """
    Creates directory for monkey and related files
    """
    if not os.path.exists(get_monkey_dir_path()):
        os.mkdir(get_monkey_dir_path())


def remove_monkey_dir():
    """
    Removes monkey's root directory
    :return True if removed without errors and False otherwise
    """
    try:
        shutil.rmtree(get_monkey_dir_path())
        return True
    except Exception:
        return False


def get_monkey_dir_path():
    return os.path.join(tempfile.gettempdir(), WormConfiguration.monkey_dir_name)


def user_token_is_admin(user_token):
    """
    using the win32 api, determine if the user with token user_token has administrator rights

    See MSDN entry here: http://msdn.microsoft.com/en-us/library/aa376389(VS.85).aspx
    """
    class SID_IDENTIFIER_AUTHORITY(ctypes.Structure):
        _fields_ = [
            ("byte0", ctypes.c_byte),
            ("byte1", ctypes.c_byte),
            ("byte2", ctypes.c_byte),
            ("byte3", ctypes.c_byte),
            ("byte4", ctypes.c_byte),
            ("byte5", ctypes.c_byte),
        ]
    nt_authority = SID_IDENTIFIER_AUTHORITY()
    nt_authority.byte5 = 5

    SECURITY_BUILTIN_DOMAIN_RID = 0x20
    DOMAIN_ALIAS_RID_ADMINS = 0x220
    administrators_group = ctypes.c_void_p()
    if ctypes.windll.advapi32.AllocateAndInitializeSid(ctypes.byref(nt_authority), 2,
        SECURITY_BUILTIN_DOMAIN_RID, DOMAIN_ALIAS_RID_ADMINS,
        0, 0, 0, 0, 0, 0, ctypes.byref(administrators_group)) == 0:
        raise Exception("AllocateAndInitializeSid failed")

    try:
        is_admin = ctypes.wintypes.BOOL()
        if ctypes.windll.advapi32.CheckTokenMembership(
                user_token, administrators_group, ctypes.byref(is_admin)) == 0:
            raise Exception("CheckTokenMembership failed")
        return is_admin.value != 0

    finally:
        ctypes.windll.advapi32.FreeSid(administrators_group)
