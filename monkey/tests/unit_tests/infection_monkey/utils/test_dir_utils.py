import os
from pathlib import Path

from infection_monkey.utils.dir_utils import get_all_files_in_directory

FILE_1 = "file.jpg.zip"
FILE_2 = "file.xyz"
SUBDIR_1 = "subdir1"
SUBDIR_2 = "subdir2"


def add_subdirs_to_dir(parent_dir):
    subdir1 = os.path.join(parent_dir, SUBDIR_1)
    subdir2 = os.path.join(parent_dir, SUBDIR_2)
    subdirs = [subdir1, subdir2]

    for subdir in subdirs:
        os.mkdir(subdir)

    return subdirs


def add_files_to_dir(parent_dir):
    file1 = os.path.join(parent_dir, FILE_1)
    file2 = os.path.join(parent_dir, FILE_2)
    files = [file1, file2]

    for f in files:
        Path(f).touch()

    return files


def test_get_all_files_in_directory__no_files(tmpdir, monkeypatch):
    add_subdirs_to_dir(tmpdir)

    expected_return_value = []
    assert get_all_files_in_directory(tmpdir) == expected_return_value


def test_get_all_files_in_directory__has_files(tmpdir, monkeypatch):
    add_subdirs_to_dir(tmpdir)
    files = add_files_to_dir(tmpdir)

    expected_return_value = sorted(files)
    assert sorted(get_all_files_in_directory(tmpdir)) == expected_return_value


def test_get_all_files_in_directory__subdir_has_files(tmpdir, monkeypatch):
    subdirs = add_subdirs_to_dir(tmpdir)
    add_files_to_dir(subdirs[0])

    files = add_files_to_dir(tmpdir)

    expected_return_value = sorted(files)
    assert sorted(get_all_files_in_directory(tmpdir)) == expected_return_value
