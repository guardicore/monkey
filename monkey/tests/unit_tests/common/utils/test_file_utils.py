import os
import stat

import pytest
from tests.monkey_island.utils import assert_linux_permissions, assert_windows_permissions

from common.utils.environment import is_windows_os
from common.utils.file_utils import create_secure_directory, open_new_securely_permissioned_file
from common.utils.file_utils.secure_directory import FailedDirectoryCreationError


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


def test_create_secure_directory__path_exists_as_file(test_path):
    with open(test_path, "w"):
        with pytest.raises(FailedDirectoryCreationError):
            create_secure_directory(test_path)


# Linux-only tests


@pytest.mark.skipif(is_windows_os(), reason="Tests Posix (not Windows) permissions.")
def test_create_secure_directory__already_exists_secure_linux(test_path):
    test_path.mkdir(mode=stat.S_IRWXU)
    create_secure_directory(test_path)

    assert_linux_permissions(test_path)


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


@pytest.mark.skipif(not is_windows_os(), reason="Tests Windows (not Posix) permissions.")
def test_create_secure_directory__already_exists_secure_windows(test_path):
    # creates a new secure directory
    create_secure_directory(test_path)
    # attempts to create a new secure directory when one already exists
    create_secure_directory(test_path)

    assert_windows_permissions(test_path)


@pytest.mark.skipif(not is_windows_os(), reason="Tests Windows (not Posix) permissions.")
def test_create_secure_directory__already_exists_insecure_windows(test_path):
    test_path.mkdir()
    create_secure_directory(test_path)

    assert_windows_permissions(test_path)


@pytest.mark.skipif(not is_windows_os(), reason="Tests Windows (not Posix) permissions.")
def test_create_secure_directory__perm_windows(test_path):
    create_secure_directory(test_path)

    assert_windows_permissions(test_path)


@pytest.mark.skipif(not is_windows_os(), reason="Tests Windows (not Posix) permissions.")
def test_open_new_securely_permissioned_file__perm_windows(test_path):
    with open_new_securely_permissioned_file(test_path):
        pass

    assert_windows_permissions(test_path)
