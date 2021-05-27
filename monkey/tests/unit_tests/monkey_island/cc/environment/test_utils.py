import os
import shutil
import stat

import pytest

from monkey_island.cc.environment.utils import create_secure_directory, is_windows_os


@pytest.fixture
def test_path_nested(tmpdir):
    nested_path = "test1/test2/test3"
    path = os.path.join(tmpdir, nested_path)
    yield path
    try:
        shutil.rmtree(os.path.join(tmpdir, "test1"))
    except Exception:
        pass


@pytest.fixture
def test_path(tmpdir):
    test_path = "test1"
    path = os.path.join(tmpdir, test_path)
    yield path
    try:
        shutil.rmtree(path)
    except Exception:
        pass


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
