import os
import stat

import pytest

from monkey_island.cc.environment.utils import create_secure_directory, is_windows_os


@pytest.fixture
def test_path_nested(tmpdir):
    nested_path = "test1/test2/test3"
    path = os.path.join(tmpdir, nested_path)

    return path


@pytest.fixture
def test_path(tmpdir):
    test_path = "test1"
    path = os.path.join(tmpdir, test_path)

    return path


def test_create_secure_directory__parent_dirs(test_path_nested):
    create_secure_directory(test_path_nested, create_parent_dirs=True)
    assert os.path.isdir(test_path_nested)


def test_create_secure_directory__already_created(test_path):
    os.mkdir(test_path)
    assert os.path.isdir(test_path)
    create_secure_directory(test_path, create_parent_dirs=False)


def test_create_secure_directory__no_parent_dir(test_path_nested):
    with pytest.raises(Exception):
        create_secure_directory(test_path_nested, create_parent_dirs=False)


@pytest.mark.skipif(is_windows_os(), reason="Tests Posix (not Windows) permissions.")
def test_create_secure_directory__perm_linux(test_path_nested):
    create_secure_directory(test_path_nested, create_parent_dirs=True)
    st = os.stat(test_path_nested)
    return bool(st.st_mode & stat.S_IRWXU)


@pytest.mark.skipif(not is_windows_os(), reason="Tests Windows (not Posix) permissions.")
def test_create_secure_directory__perm_windows(test_path):
    import win32api  # noqa: E402
    import win32security  # noqa: E402

    FULL_CONTROL = 2032127
    ACE_TYPE_ALLOW = 0

    create_secure_directory(test_path, create_parent_dirs=False)

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
