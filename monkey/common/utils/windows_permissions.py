from typing import Any, Mapping

import ntsecuritycon
import win32api
import win32security

ACCESS_MODE_GRANT_ACCESS = win32security.GRANT_ACCESS
ACCESS_PERMISSIONS_FULL_CONTROL = ntsecuritycon.FILE_ALL_ACCESS
INHERITANCE_OBJECT_AND_CONTAINER = (
    win32security.CONTAINER_INHERIT_ACE | win32security.OBJECT_INHERIT_ACE
)


def get_security_descriptor_for_owner_only_permissions():
    user_sid = _get_user_pySID_object()
    entries = [_get_ace_for_owner_only_permissions(user_sid)]

    dacl = win32security.ACL()
    dacl.SetEntriesInAcl(entries)

    security_descriptor = win32security.SECURITY_DESCRIPTOR()
    security_descriptor.SetSecurityDescriptorControl(
        win32security.SE_DACL_PROTECTED, win32security.SE_DACL_PROTECTED
    )
    security_descriptor.SetSecurityDescriptorDacl(1, dacl, 0)

    return security_descriptor


def _get_user_pySID_object():
    # Note: We do this using the process handle and token instead of by account name, as some SIDs
    # have no corresponding account name, such as a logon SID that identifies a logon session. This
    # is particularly an issue when using the SMB exploiter. See issue #3173.
    process_handle = win32api.GetCurrentProcess()
    token_handle = win32security.OpenProcessToken(process_handle, win32security.TOKEN_ALL_ACCESS)

    sid, _ = win32security.GetTokenInformation(token_handle, win32security.TokenUser)

    return sid


def _get_ace_for_owner_only_permissions(user_sid) -> Mapping[str, Any]:
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
