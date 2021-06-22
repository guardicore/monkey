import os

import infection_monkey.ransomware.utils

VALID_FILE_EXTENSION_1 = "file.3ds"
VALID_FILE_EXTENSION_2 = "file.jpg.zip"
INVALID_FILE_EXTENSION_1 = "file.pqr"
INVALID_FILE_EXTENSION_2 = "file.xyz"
SUBDIR_1 = "subdir1"
SUBDIR_2 = "subdir2"


def test_get_files_to_encrypt__no_files(monkeypatch):
    all_files = []
    monkeypatch.setattr(
        "infection_monkey.ransomware.utils.get_all_files_in_directory", lambda _: all_files
    )

    expected_return_value = []
    assert infection_monkey.ransomware.utils.get_files_to_encrypt("") == expected_return_value


def test_get_files_to_encrypt__no_valid_files(monkeypatch):
    all_files = [INVALID_FILE_EXTENSION_1, INVALID_FILE_EXTENSION_2]
    monkeypatch.setattr(
        "infection_monkey.ransomware.utils.get_all_files_in_directory", lambda _: all_files
    )

    expected_return_value = []
    assert infection_monkey.ransomware.utils.get_files_to_encrypt("") == expected_return_value


def test_get_files_to_encrypt__valid_files(monkeypatch):
    all_files = [
        VALID_FILE_EXTENSION_1,
        INVALID_FILE_EXTENSION_1,
        VALID_FILE_EXTENSION_2,
        INVALID_FILE_EXTENSION_2,
    ]
    monkeypatch.setattr(
        "infection_monkey.ransomware.utils.get_all_files_in_directory", lambda _: all_files
    )

    expected_return_value = [VALID_FILE_EXTENSION_1, VALID_FILE_EXTENSION_2]
    assert infection_monkey.ransomware.utils.get_files_to_encrypt("") == expected_return_value


def test_get_all_files_in_directory__no_files(tmpdir, monkeypatch):
    subdir1 = os.path.join(tmpdir, SUBDIR_1)
    subdir2 = os.path.join(tmpdir, SUBDIR_2)
    subdirs = [subdir1, subdir2]

    for subdir in subdirs:
        os.mkdir(subdir)

    all_items_in_dir = subdirs
    monkeypatch.setattr("os.listdir", lambda _: all_items_in_dir)

    expected_return_value = []
    assert (
        infection_monkey.ransomware.utils.get_all_files_in_directory(tmpdir)
        == expected_return_value
    )


def test_get_all_files_in_directory__has_files(tmpdir, monkeypatch):
    subdir1 = os.path.join(tmpdir, SUBDIR_1)
    subdir2 = os.path.join(tmpdir, SUBDIR_2)
    subdirs = [subdir1, subdir2]

    file1 = os.path.join(tmpdir, VALID_FILE_EXTENSION_1)
    file2 = os.path.join(tmpdir, INVALID_FILE_EXTENSION_1)
    file3 = os.path.join(tmpdir, VALID_FILE_EXTENSION_2)
    file4 = os.path.join(tmpdir, INVALID_FILE_EXTENSION_2)
    files = [file1, file2, file3, file4]

    for subdir in subdirs:
        os.mkdir(subdir)

    for file in files:
        with open(file, "w") as _:
            pass

    all_items_in_dir = subdirs + files
    monkeypatch.setattr("os.listdir", lambda _: all_items_in_dir)

    expected_return_value = files
    assert (
        infection_monkey.ransomware.utils.get_all_files_in_directory(tmpdir)
        == expected_return_value
    )
