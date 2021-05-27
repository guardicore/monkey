import ntsecuritycon
import win32api
import win32con
import win32security


def set_perms_to_owner_only(folder_path: str) -> None:
    user = get_user_pySID_object()

    security_descriptor = win32security.GetFileSecurity(
        folder_path, win32security.DACL_SECURITY_INFORMATION
    )
    dacl = win32security.ACL()
    dacl.AddAccessAllowedAce(
        win32security.ACL_REVISION,
        ntsecuritycon.FILE_ALL_ACCESS,
        user,
    )
    security_descriptor.SetSecurityDescriptorDacl(1, dacl, 0)
    win32security.SetFileSecurity(
        folder_path, win32security.DACL_SECURITY_INFORMATION, security_descriptor
    )


def get_user_pySID_object():
    # get current user's name
    username = win32api.GetUserNameEx(win32con.NameSamCompatible)
    # pySID object for the current user
    user, _, _ = win32security.LookupAccountName("", username)

    return user
