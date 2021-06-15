import os
import stat

import pytest

from monkey_island.cc.server_utils.file_utils import (
    create_secure_directory,
    create_secure_file,
    expand_path,
    is_windows_os,
)

if is_windows_os():
    import win32api
    import win32security

    FULL_CONTROL = 2032127
    ACE_TYPE_ALLOW = 0


def test_expand_user(patched_home_env):
    input_path = os.path.join("~", "test")
    expected_path = os.path.join(patched_home_env, "test")

    assert expand_path(input_path) == expected_path


def test_expand_vars(patched_home_env):
    input_path = os.path.join("$HOME", "test")
    expected_path = os.path.join(patched_home_env, "test")

    assert expand_path(input_path) == expected_path


@pytest.fixture
def test_path_nested(tmpdir):
    path = os.path.join(tmpdir, "test1", "test2", "test3")
    return path


@pytest.fixture
def test_path(tmpdir):
    test_path = "test1"
    path = os.path.join(tmpdir, test_path)

    return path


def _get_acl_and_sid_from_path(path: str):
    sid, _, _ = win32security.LookupAccountName("", win32api.GetUserName())
    security_descriptor = win32security.GetNamedSecurityInfo(
        path, win32security.SE_FILE_OBJECT, win32security.DACL_SECURITY_INFORMATION
    )
    acl = security_descriptor.GetSecurityDescriptorDacl()
    return acl, sid


def test_create_secure_directory__already_created(test_path):
    os.mkdir(test_path)
    assert os.path.isdir(test_path)
    create_secure_directory(test_path)


def test_create_secure_directory__no_parent_dir(test_path_nested):
    with pytest.raises(Exception):
        create_secure_directory(test_path_nested)


@pytest.mark.skipif(is_windows_os(), reason="Tests Posix (not Windows) permissions.")
def test_create_secure_directory__perm_linux(test_path):
    create_secure_directory(test_path)
    st = os.stat(test_path)

    expected_mode = stat.S_IRWXU
    actual_mode = st.st_mode & (stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

    assert expected_mode == actual_mode


@pytest.mark.skipif(not is_windows_os(), reason="Tests Windows (not Posix) permissions.")
def test_create_secure_directory__perm_windows(test_path):
    create_secure_directory(test_path)

    acl, user_sid = _get_acl_and_sid_from_path(test_path)

    assert acl.GetAceCount() == 1

    ace = acl.GetAce(0)
    ace_type, _ = ace[0]  # 0 for allow, 1 for deny
    permissions = ace[1]
    sid = ace[-1]

    assert sid == user_sid
    assert permissions == FULL_CONTROL and ace_type == ACE_TYPE_ALLOW


def test_create_secure_file__already_created(test_path):
    os.close(os.open(test_path, os.O_CREAT, stat.S_IRWXU))
    assert os.path.isfile(test_path)
    create_secure_file(test_path)  # test fails if any exceptions are thrown


def test_create_secure_file__no_parent_dir(test_path_nested):
    with pytest.raises(Exception):
        create_secure_file(test_path_nested)


@pytest.mark.skipif(is_windows_os(), reason="Tests Posix (not Windows) permissions.")
def test_create_secure_file__perm_linux(test_path):
    create_secure_file(test_path)
    st = os.stat(test_path)

    expected_mode = stat.S_IRUSR | stat.S_IWUSR
    actual_mode = st.st_mode & (stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

    assert expected_mode == actual_mode


@pytest.mark.skipif(not is_windows_os(), reason="Tests Windows (not Posix) permissions.")
def test_create_secure_file__perm_windows(test_path):
    create_secure_file(test_path)

    acl, user_sid = _get_acl_and_sid_from_path(test_path)

    assert acl.GetAceCount() == 1

    ace = acl.GetAce(0)
    ace_type, _ = ace[0]  # 0 for allow, 1 for deny
    permissions = ace[1]
    sid = ace[-1]

    assert sid == user_sid
    assert permissions == FULL_CONTROL and ace_type == ACE_TYPE_ALLOW
