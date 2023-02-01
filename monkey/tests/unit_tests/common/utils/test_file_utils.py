import os
import stat

import pytest
from tests.monkey_island.utils import assert_linux_permissions, assert_windows_permissions

from common.utils.environment import is_windows_os
from common.utils.file_utils import create_secure_directory, open_new_securely_permissioned_file

if is_windows_os():
    import win32api
    import win32con
    import win32security

    from common.utils.windows_permissions import (
        ACCESS_MODE_GRANT_ACCESS,
        ACCESS_PERMISSIONS_FULL_CONTROL,
        INHERITANCE_OBJECT_AND_CONTAINER,
    )


@pytest.fixture
def test_path_nested(tmp_path):
    path = tmp_path / "test1" / "test2" / "test3"
    return path


@pytest.fixture
def test_path(tmp_path):
    test_path = "test1"
    path = tmp_path / test_path

    return path


def test_create_secure_directory__no_parent_dir(test_path_nested):
    with pytest.raises(Exception):
        create_secure_directory(test_path_nested)


def test_open_new_securely_permissioned_file__already_exists(test_path):
    os.close(os.open(test_path, os.O_CREAT, stat.S_IRWXU))
    assert os.path.isfile(test_path)

    with pytest.raises(Exception):
        with open_new_securely_permissioned_file(test_path):
            pass


def test_open_new_securely_permissioned_file__no_parent_dir(test_path_nested):
    with pytest.raises(Exception):
        with open_new_securely_permissioned_file(test_path_nested):
            pass


def test_open_new_securely_permissioned_file__write(test_path):
    TEST_STR = b"Hello World"
    with open_new_securely_permissioned_file(test_path, "wb") as f:
        f.write(TEST_STR)

    with open(test_path, "rb") as f:
        assert f.read() == TEST_STR


# Linux-only tests


@pytest.mark.skipif(is_windows_os(), reason="Tests Posix (not Windows) permissions.")
def test_create_secure_directory__already_exists_secure_linux(test_path):
    test_path.mkdir(mode=stat.S_IRWXU)
    create_secure_directory(test_path)


@pytest.mark.skipif(is_windows_os(), reason="Tests Posix (not Windows) permissions.")
def test_create_secure_directory__already_exists_insecure_linux(test_path):
    test_path.mkdir(mode=0o777)

    create_secure_directory(test_path)
    assert_linux_permissions(test_path)


@pytest.mark.skipif(is_windows_os(), reason="Tests Posix (not Windows) permissions.")
def test_create_secure_directory__perm_linux(test_path):
    create_secure_directory(test_path)

    assert_linux_permissions(test_path)


@pytest.mark.skipif(is_windows_os(), reason="Tests Posix (not Windows) permissions.")
def test_open_new_securely_permissioned_file__perm_linux(test_path):
    with open_new_securely_permissioned_file(test_path):
        pass

    st = os.stat(test_path)

    expected_mode = stat.S_IRUSR | stat.S_IWUSR
    actual_mode = st.st_mode & (stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

    assert expected_mode == actual_mode


# Windows-only tests


@pytest.fixture
def monkeypatch_get_acl_and_sid_from_path(monkeypatch):
    username = win32api.GetUserNameEx(win32con.NameSamCompatible)
    user_sid, _, _ = win32security.LookupAccountName("", username)
    acl = win32security.ACL()
    acl.SetEntriesInAcl(
        [
            {
                "AccessMode": ACCESS_MODE_GRANT_ACCESS,
                "AccessPermissions": ACCESS_PERMISSIONS_FULL_CONTROL,
                "Inheritance": INHERITANCE_OBJECT_AND_CONTAINER,
                "Trustee": {
                    "TrusteeType": win32security.TRUSTEE_IS_USER,
                    "TrusteeForm": win32security.TRUSTEE_IS_SID,
                    "Identifier": user_sid,
                },
            }
        ]
    )

    monkeypatch.setattr(
        "common.utils.windows_permissions.get_acl_and_sid_from_path", lambda _: (acl, user_sid)
    )


@pytest.mark.skipif(not is_windows_os(), reason="Tests Windows (not Posix) permissions.")
def test_create_secure_directory__already_exists_secure_windows(
    test_path, monkeypatch_get_acl_and_sid_from_path
):
    create_secure_directory(test_path)


@pytest.mark.skipif(not is_windows_os(), reason="Tests Windows (not Posix) permissions.")
def test_create_secure_directory__already_exists_insecure_windows(test_path):
    test_path.mkdir()

    with pytest.raises(Exception):
        create_secure_directory(test_path)


@pytest.mark.skipif(not is_windows_os(), reason="Tests Windows (not Posix) permissions.")
def test_create_secure_directory__perm_windows(test_path):
    create_secure_directory(test_path)

    assert_windows_permissions(test_path)


@pytest.mark.skipif(not is_windows_os(), reason="Tests Windows (not Posix) permissions.")
def test_open_new_securely_permissioned_file__perm_windows(test_path):
    with open_new_securely_permissioned_file(test_path):
        pass

    assert_windows_permissions(test_path)
