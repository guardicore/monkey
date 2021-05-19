import os
import sys

import ntsecuritycon
import win32api
import win32con
import win32security

from monkey_island.cc.server_utils.consts import DEFAULT_DATA_DIR

is_windows_os = sys.platform.startswith("win")


def create_data_dir(data_dir: str) -> None:
    if not os.path.isdir(data_dir):
        os.makedirs(data_dir, mode=0o700)
        if is_windows_os:  # `mode=0o700` doesn't work on Windows
            set_data_dir_security_to_read_and_write_by_owner(data_dir_path=data_dir)


def create_default_data_dir() -> None:
    if not os.path.isdir(DEFAULT_DATA_DIR):
        os.mkdir(DEFAULT_DATA_DIR, mode=0o700)
        if is_windows_os:  # `mode=0o700` doesn't work on Windows
            set_data_dir_security_to_read_and_write_by_owner(data_dir_path=DEFAULT_DATA_DIR)


def set_data_dir_security_to_read_and_write_by_owner(data_dir_path: str) -> None:
    user = get_user_pySID_object()  # current user is newly created data dir's owner

    security_descriptor = win32security.GetFileSecurity(
        data_dir_path, win32security.DACL_SECURITY_INFORMATION
    )
    dacl = win32security.ACL()
    dacl.AddAccessAllowedAce(
        win32security.ACL_REVISION,
        ntsecuritycon.FILE_GENERIC_READ | ntsecuritycon.FILE_GENERIC_WRITE,
        user,
    )
    security_descriptor.SetSecurityDescriptorDacl(1, dacl, 0)
    win32security.SetFileSecurity(
        data_dir_path, win32security.DACL_SECURITY_INFORMATION, security_descriptor
    )


def get_user_pySID_object():
    # get current user's name
    username = win32api.GetUserNameEx(win32con.NameSamCompatible)
    # pySID object for the current user
    user, _, _ = win32security.LookupAccountName("", username)

    return user
