import os

import pytest

from monkey_island.cc.environment.windows_permissions import set_perms_to_owner_only


@pytest.mark.skipif(os.name == "posix", reason="Tests Windows (not Posix) permissions.")
def test_set_perms_to_owner_only(tmpdir):
    import win32api  # noqa: E402
    import win32security  # noqa: E402

    folder = str(tmpdir)

    set_perms_to_owner_only(folder)

    FULL_CONTROL = 2032127
    ACE_TYPE_ALLOW = 0

    user_sid, _, _ = win32security.LookupAccountName("", win32api.GetUserName())
    security_descriptor = win32security.GetNamedSecurityInfo(
        folder, win32security.SE_FILE_OBJECT, win32security.DACL_SECURITY_INFORMATION
    )
    acl = security_descriptor.GetSecurityDescriptorDacl()

    assert acl.GetAceCount() == 1

    ace = acl.GetAce(0)
    ace_type, _ = ace[0]  # 0 for allow, 1 for deny
    permissions = ace[1]
    sid = ace[-1]

    assert sid == user_sid
    assert permissions == FULL_CONTROL and ace_type == ACE_TYPE_ALLOW
