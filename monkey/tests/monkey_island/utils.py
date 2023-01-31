from pathlib import WindowsPath

from common.utils.environment import is_windows_os

if is_windows_os():
    from common.utils.windows_permissions import (
        ACE_ACCESS_MODE_GRANT_ACCESS,
        ACE_INHERIT_OBJECT_AND_CONTAINER,
        FULL_CONTROL,
        get_acl_and_sid_from_path,
    )
else:
    import os
    import stat


def assert_windows_permissions(path: WindowsPath):
    acl, user_sid = get_acl_and_sid_from_path(path)

    assert acl.GetAceCount() == 1

    ace = acl.GetExplicitEntriesFromAcl()[0]

    ace_access_mode = ace["AccessMode"]
    ace_permissions = ace["AccessPermissions"]
    ace_inheritance = ace["Inheritance"]
    ace_sid = ace["Trustee"]["Identifier"]

    assert ace_sid == user_sid
    assert ace_permissions == FULL_CONTROL and ace_access_mode == ACE_ACCESS_MODE_GRANT_ACCESS
    assert ace_inheritance == ACE_INHERIT_OBJECT_AND_CONTAINER


def assert_linux_permissions(path: str):
    st = os.stat(path)

    expected_mode = stat.S_IRWXU
    actual_mode = st.st_mode & (stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

    assert expected_mode == actual_mode
