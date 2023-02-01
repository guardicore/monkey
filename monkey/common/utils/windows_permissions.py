from pathlib import Path
from typing import Any, Mapping

import ntsecuritycon
import win32api
import win32con
import win32security

ACCESS_MODE_GRANT_ACCESS = win32security.GRANT_ACCESS
ACCESS_PERMISSIONS_FULL_CONTROL = ntsecuritycon.FILE_ALL_ACCESS
INHERITANCE_OBJECT_AND_CONTAINER = (
    win32security.CONTAINER_INHERIT_ACE | win32security.OBJECT_INHERIT_ACE
)


def get_security_descriptor_for_owner_only_perms():
    user_sid = get_user_pySID_object()
    entries = [get_ace_for_owner_only_permissions(user_sid)]

    dacl = win32security.ACL()
    dacl.SetEntriesInAcl(entries)

    security_descriptor = win32security.SECURITY_DESCRIPTOR()
    security_descriptor.SetSecurityDescriptorDacl(1, dacl, 0)

    return security_descriptor


def get_ace_for_owner_only_permissions(user_sid) -> Mapping[str, Any]:
    return {
        "AccessMode": ACCESS_MODE_GRANT_ACCESS,
        "AccessPermissions": ACCESS_PERMISSIONS_FULL_CONTROL,
        "Inheritance": INHERITANCE_OBJECT_AND_CONTAINER,
        "Trustee": {
            "TrusteeType": win32security.TRUSTEE_IS_USER,
            "TrusteeForm": win32security.TRUSTEE_IS_SID,
            "Identifier": user_sid,
        },
    }


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
