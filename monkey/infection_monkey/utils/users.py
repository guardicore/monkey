from infection_monkey.utils.linux.users import get_linux_commands_to_add_user
from infection_monkey.utils.windows.users import get_windows_commands_to_add_user


SECURITY_BUILTIN_DOMAIN_RID = 0x20
DOMAIN_ALIAS_RID_ADMINS = 0x220


def get_commands_to_add_user(username, password):
    linux_cmds = get_linux_commands_to_add_user(username)
    windows_cmds = get_windows_commands_to_add_user(username, password)
    return linux_cmds, windows_cmds


def user_token_is_admin_windows(user_token):
    import ctypes.wintypes
    """
    using the win32 api, determine if the user with token user_token has administrator rights

    See MSDN entry here: http://msdn.microsoft.com/en-us/library/aa376389(VS.85).aspx
    """
    class SidIdentifierAuthority(ctypes.Structure):
        _fields_ = [
            ("byte0", ctypes.c_byte),
            ("byte1", ctypes.c_byte),
            ("byte2", ctypes.c_byte),
            ("byte3", ctypes.c_byte),
            ("byte4", ctypes.c_byte),
            ("byte5", ctypes.c_byte),
        ]
    nt_authority = SidIdentifierAuthority()
    nt_authority.byte5 = 5

    administrators_group = ctypes.c_void_p()
    if ctypes.windll.advapi32.AllocateAndInitializeSid(ctypes.byref(nt_authority),
                                                       2,
                                                       SECURITY_BUILTIN_DOMAIN_RID,
                                                       DOMAIN_ALIAS_RID_ADMINS,
                                                       0, 0, 0, 0, 0, 0,
                                                       ctypes.byref(administrators_group)) == 0:
        raise Exception("AllocateAndInitializeSid failed")

    try:
        is_admin = ctypes.wintypes.BOOL()
        if ctypes.windll.advapi32.CheckTokenMembership(
                user_token, administrators_group, ctypes.byref(is_admin)) == 0:
            raise Exception("CheckTokenMembership failed")
        return is_admin.value != 0

    finally:
        ctypes.windll.advapi32.FreeSid(administrators_group)
