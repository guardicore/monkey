from monkey_island.cc.server_utils.file_utils import is_windows_os

if is_windows_os():
    import win32api
    import win32security

    FULL_CONTROL = 2032127
    ACE_ACCESS_MODE_GRANT_ACCESS = win32security.GRANT_ACCESS
    ACE_INHERIT_OBJECT_AND_CONTAINER = 3


def _get_acl_and_sid_from_path(path: str):
    sid, _, _ = win32security.LookupAccountName("", win32api.GetUserName())
    security_descriptor = win32security.GetNamedSecurityInfo(
        path, win32security.SE_FILE_OBJECT, win32security.DACL_SECURITY_INFORMATION
    )
    acl = security_descriptor.GetSecurityDescriptorDacl()
    return acl, sid

def assert_windows_permissions(path: str):
    acl, user_sid = _get_acl_and_sid_from_path(path)

    assert acl.GetAceCount() == 1

    ace = acl.GetExplicitEntriesFromAcl()[0]

    ace_access_mode = ace["AccessMode"]
    ace_permissions = ace["AccessPermissions"]
    ace_inheritance = ace["Inheritance"]
    ace_sid = ace["Trustee"]["Identifier"]

    assert ace_sid == user_sid
    assert ace_permissions == FULL_CONTROL and ace_access_mode == ACE_ACCESS_MODE_GRANT_ACCESS
    assert ace_inheritance == ACE_INHERIT_OBJECT_AND_CONTAINER
