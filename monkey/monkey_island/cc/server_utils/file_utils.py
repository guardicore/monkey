import os

from monkey_island.cc.environment.utils import is_windows_os


def expand_path(path: str) -> str:
    return os.path.expandvars(os.path.expanduser(path))


def has_expected_permissions(path: str, expected_permissions: int) -> bool:
    if is_windows_os():
        # checks that admin has any permissions, user has `expected_permissions`,
        # and everyone else has no permissions

        import win32api  # noqa: E402
        import win32security  # noqa: E402

        FULL_CONTROL = 2032127
        ACE_TYPE_ALLOW = 0
        ACE_TYPE_DENY = 1

        admins_sid, _, _ = win32security.LookupAccountName("", "Administrators")
        user_sid, _, _ = win32security.LookupAccountName("", win32api.GetUserName())

        security_descriptor = win32security.GetNamedSecurityInfo(
            path, win32security.SE_FILE_OBJECT, win32security.DACL_SECURITY_INFORMATION
        )

        acl = security_descriptor.GetSecurityDescriptorDacl()

        for i in range(acl.GetAceCount()):
            ace = acl.GetAce(i)
            ace_type, _ = ace[0]  # 0 for allow, 1 for deny
            permissions = ace[1]
            sid = ace[-1]

            if sid == user_sid:
                if not (permissions == expected_permissions and ace_type == ACE_TYPE_ALLOW):
                    return False
            elif sid == admins_sid:
                continue
            # TODO: consider removing; so many system accounts/groups exist, it's likely to fail
            else:
                if not (permissions == FULL_CONTROL and ace_type == ACE_TYPE_DENY):
                    return False

        return True

    else:
        file_mode = os.stat(path).st_mode
        file_permissions = file_mode & 0o777

    return file_permissions == expected_permissions
