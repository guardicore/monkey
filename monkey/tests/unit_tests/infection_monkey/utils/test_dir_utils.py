import os

from infection_monkey.utils.dir_utils import get_all_files_in_directory

FILE_1 = "file.jpg.zip"
FILE_2 = "file.xyz"
SUBDIR_1 = "subdir1"
SUBDIR_2 = "subdir2"


def test_get_all_files_in_directory__no_files(tmpdir, monkeypatch):
    subdir1 = os.path.join(tmpdir, SUBDIR_1)
    subdir2 = os.path.join(tmpdir, SUBDIR_2)
    subdirs = [subdir1, subdir2]

    for subdir in subdirs:
        os.mkdir(subdir)

    all_items_in_dir = subdirs
    monkeypatch.setattr("os.listdir", lambda _: all_items_in_dir)

    expected_return_value = []
    assert get_all_files_in_directory(tmpdir) == expected_return_value


def test_get_all_files_in_directory__has_files(tmpdir, monkeypatch):
    subdir1 = os.path.join(tmpdir, SUBDIR_1)
    subdir2 = os.path.join(tmpdir, SUBDIR_2)
    subdirs = [subdir1, subdir2]

    file1 = os.path.join(tmpdir, FILE_1)
    file2 = os.path.join(tmpdir, FILE_2)
    files = [file1, file2]

    for subdir in subdirs:
        os.mkdir(subdir)

    for file in files:
        with open(file, "w") as _:
            pass

    all_items_in_dir = subdirs + files
    monkeypatch.setattr("os.listdir", lambda _: all_items_in_dir)

    expected_return_value = files
    assert get_all_files_in_directory(tmpdir) == expected_return_value
