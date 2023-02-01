from pathlib import Path

import ntsecuritycon
import win32api
import win32con
import win32security

FULL_CONTROL = 2032127
ACE_ACCESS_MODE_GRANT_ACCESS = win32security.GRANT_ACCESS
ACE_INHERIT_OBJECT_AND_CONTAINER = 3


def get_security_descriptor_for_owner_only_perms():
    user_sid = get_user_pySID_object()
    security_descriptor = win32security.SECURITY_DESCRIPTOR()
    dacl = win32security.ACL()

    entries = [
        {
            "AccessMode": win32security.GRANT_ACCESS,
            "AccessPermissions": ntsecuritycon.FILE_ALL_ACCESS,
            "Inheritance": win32security.CONTAINER_INHERIT_ACE | win32security.OBJECT_INHERIT_ACE,
            "Trustee": {
                "TrusteeType": win32security.TRUSTEE_IS_USER,
                "TrusteeForm": win32security.TRUSTEE_IS_SID,
                "Identifier": user_sid,
            },
        }
    ]
    dacl.SetEntriesInAcl(entries)

    security_descriptor.SetSecurityDescriptorDacl(1, dacl, 0)

    return security_descriptor


def get_acl_and_sid_from_path(path: Path):
    sid, _, _ = win32security.LookupAccountName("", win32api.GetUserName())
    security_descriptor = win32security.GetNamedSecurityInfo(
        str(path), win32security.SE_FILE_OBJECT, win32security.DACL_SECURITY_INFORMATION
    )
    acl = security_descriptor.GetSecurityDescriptorDacl()
    return acl, sid


def get_user_pySID_object():
    # get current user's name
    username = win32api.GetUserNameEx(win32con.NameSamCompatible)
    # pySID object for the current user
    user, _, _ = win32security.LookupAccountName("", username)

    return user
