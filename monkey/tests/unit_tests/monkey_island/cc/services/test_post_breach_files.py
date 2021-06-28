import os

import pytest

from monkey_island.cc.server_utils.file_utils import is_windows_os
from monkey_island.cc.services.post_breach_files import PostBreachFilesService

if is_windows_os():
    import win32api
    import win32security

    FULL_CONTROL = 2032127
    ACE_ACCESS_MODE_GRANT_ACCESS = win32security.GRANT_ACCESS
    ACE_INHERIT_OBJECT_AND_CONTAINER = 3


def raise_(ex):
    raise ex


@pytest.fixture(autouse=True)
def custom_pba_directory(tmpdir):
    PostBreachFilesService.initialize(tmpdir)


def create_custom_pba_file(filename):
    PostBreachFilesService.save_file(filename, b"")


def test_remove_pba_files():
    create_custom_pba_file("linux_file")
    create_custom_pba_file("windows_file")

    assert not dir_is_empty(PostBreachFilesService.get_custom_pba_directory())
    PostBreachFilesService.remove_PBA_files()
    assert dir_is_empty(PostBreachFilesService.get_custom_pba_directory())


def dir_is_empty(dir_path):
    dir_contents = os.listdir(dir_path)
    return len(dir_contents) == 0


@pytest.mark.skipif(os.name != "posix", reason="Tests Posix (not Windows) permissions.")
def test_custom_pba_dir_permissions_linux():
    st = os.stat(PostBreachFilesService.get_custom_pba_directory())

    assert st.st_mode == 0o40700


def _get_acl_and_sid_from_path(path: str):
    sid, _, _ = win32security.LookupAccountName("", win32api.GetUserName())
    security_descriptor = win32security.GetNamedSecurityInfo(
        path, win32security.SE_FILE_OBJECT, win32security.DACL_SECURITY_INFORMATION
    )
    acl = security_descriptor.GetSecurityDescriptorDacl()
    return acl, sid


@pytest.mark.skipif(os.name == "posix", reason="Tests Windows (not Posix) permissions.")
def test_custom_pba_dir_permissions_windows():
    pba_dir = PostBreachFilesService.get_custom_pba_directory()

    acl, user_sid = _get_acl_and_sid_from_path(pba_dir)

    assert acl.GetAceCount() == 1

    ace = acl.GetExplicitEntriesFromAcl()[0]

    ace_access_mode = ace["AccessMode"]
    ace_permissions = ace["AccessPermissions"]
    ace_inheritance = ace["Inheritance"]
    ace_sid = ace["Trustee"]["Identifier"]

    assert ace_sid == user_sid
    assert ace_permissions == FULL_CONTROL and ace_access_mode == ACE_ACCESS_MODE_GRANT_ACCESS
    assert ace_inheritance == ACE_INHERIT_OBJECT_AND_CONTAINER


def test_remove_failure(monkeypatch):
    monkeypatch.setattr(os, "remove", lambda x: raise_(OSError("Permission denied")))

    try:
        create_custom_pba_file("windows_file")
        PostBreachFilesService.remove_PBA_files()
    except Exception as ex:
        pytest.fail(f"Unxepected exception: {ex}")


def test_remove_nonexistant_file(monkeypatch):
    monkeypatch.setattr(os, "remove", lambda x: raise_(FileNotFoundError("FileNotFound")))

    try:
        PostBreachFilesService.remove_file("/nonexistant/file")
    except Exception as ex:
        pytest.fail(f"Unxepected exception: {ex}")


def test_save_file():
    FILE_NAME = "test_file"
    FILE_CONTENTS = b"hello"
    PostBreachFilesService.save_file(FILE_NAME, FILE_CONTENTS)

    expected_file_path = os.path.join(PostBreachFilesService.get_custom_pba_directory(), FILE_NAME)

    assert os.path.isfile(expected_file_path)
    assert FILE_CONTENTS == open(expected_file_path, "rb").read()
