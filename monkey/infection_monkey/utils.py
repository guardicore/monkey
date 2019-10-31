

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
