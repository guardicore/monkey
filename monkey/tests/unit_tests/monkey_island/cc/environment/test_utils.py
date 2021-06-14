import os
import stat

import pytest

from monkey_island.cc.environment.utils import (
    create_secure_directory,
    create_secure_file,
    is_windows_os,
)


@pytest.fixture
def test_path_nested(tmpdir):
    path = os.path.join(tmpdir, "test1", "test2", "test3")
    return path


@pytest.fixture
def test_path(tmpdir):
    test_path = "test1"
    path = os.path.join(tmpdir, test_path)

    return path


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
    assert (st.st_mode & 0o777) == stat.S_IRWXU


@pytest.mark.skipif(not is_windows_os(), reason="Tests Windows (not Posix) permissions.")
def test_create_secure_directory__perm_windows(test_path):
    import win32api
    import win32security

    FULL_CONTROL = 2032127
    ACE_TYPE_ALLOW = 0

    create_secure_directory(test_path)

    user_sid, _, _ = win32security.LookupAccountName("", win32api.GetUserName())
    security_descriptor = win32security.GetNamedSecurityInfo(
        test_path, win32security.SE_FILE_OBJECT, win32security.DACL_SECURITY_INFORMATION
    )
    acl = security_descriptor.GetSecurityDescriptorDacl()

    assert acl.GetAceCount() == 1

    ace = acl.GetAce(0)
    ace_type, _ = ace[0]  # 0 for allow, 1 for deny
    permissions = ace[1]
    sid = ace[-1]

    assert sid == user_sid
    assert permissions == FULL_CONTROL and ace_type == ACE_TYPE_ALLOW


def test_create_secure_file__already_created(test_path):
    os.close(os.open(test_path, os.O_CREAT, 0o700))
    assert os.path.isfile(test_path)
    create_secure_file(test_path)


def test_create_secure_file__no_parent_dir(test_path_nested):
    with pytest.raises(Exception):
        create_secure_file(test_path_nested)


@pytest.mark.skipif(is_windows_os(), reason="Tests Posix (not Windows) permissions.")
def test_create_secure_file__perm_linux(test_path):
    create_secure_file(test_path)
    st = os.stat(test_path)
    assert (st.st_mode & 0o777) == stat.S_IRWXU


@pytest.mark.skipif(not is_windows_os(), reason="Tests Windows (not Posix) permissions.")
def test_create_secure_file__perm_windows(test_path):
    import win32api
    import win32security

    FULL_CONTROL = 2032127
    ACE_TYPE_ALLOW = 0

    create_secure_file(test_path)

    user_sid, _, _ = win32security.LookupAccountName("", win32api.GetUserName())
    security_descriptor = win32security.GetNamedSecurityInfo(
        test_path, win32security.SE_FILE_OBJECT, win32security.DACL_SECURITY_INFORMATION
    )
    acl = security_descriptor.GetSecurityDescriptorDacl()

    assert acl.GetAceCount() == 1

    ace = acl.GetAce(0)
    ace_type, _ = ace[0]  # 0 for allow, 1 for deny
    permissions = ace[1]
    sid = ace[-1]

    assert sid == user_sid
    assert permissions == FULL_CONTROL and ace_type == ACE_TYPE_ALLOW
