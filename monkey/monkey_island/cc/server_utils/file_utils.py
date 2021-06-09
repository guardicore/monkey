import os

from monkey_island.cc.environment.utils import is_windows_os


def expand_path(path: str) -> str:
    return os.path.expandvars(os.path.expanduser(path))


def has_expected_permissions(path: str, expected_permissions: int) -> bool:
    if is_windows_os():
        import win32api  # noqa: E402
        import win32security  # noqa: E402

        admins_sid, _, _ = win32security.LookupAccountName("", "Administrators")
        user_sid, _, _ = win32security.LookupAccountName("", win32api.GetUserName())

        security_descriptor = win32security.GetNamedSecurityInfo(
            path, win32security.SE_FILE_OBJECT, win32security.DACL_SECURITY_INFORMATION
        )

        acl = security_descriptor.GetSecurityDescriptorDacl()

        for i in range(acl.GetAceCount()):
            ace = acl.GetAce(i)
            sid = ace[-1]
            permissions = ace[1]
            if sid == user_sid:
                if oct(permissions & 0o777) != expected_permissions:
                    return False
            elif sid == admins_sid:
                continue
            else:
                if oct(permissions) != 0:  # everyone but user & admins should have no permissions
                    return False

        return True

    else:
        file_mode = os.stat(path).st_mode
        file_permissions = file_mode & 0o777

    return file_permissions == expected_permissions
