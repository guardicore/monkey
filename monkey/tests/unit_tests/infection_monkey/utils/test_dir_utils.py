from infection_monkey.utils.dir_utils import get_all_files_in_directory

FILE_1 = "file.jpg.zip"
FILE_2 = "file.xyz"
SUBDIR_1 = "subdir1"
SUBDIR_2 = "subdir2"


def add_subdirs_to_dir(parent_dir):
    subdir1 = parent_dir / SUBDIR_1
    subdir2 = parent_dir / SUBDIR_2
    subdirs = [subdir1, subdir2]

    for subdir in subdirs:
        subdir.mkdir()

    return subdirs


def add_files_to_dir(parent_dir):
    file1 = parent_dir / FILE_1
    file2 = parent_dir / FILE_2
    files = [file1, file2]

    for f in files:
        f.touch()

    return files


def test_get_all_files_in_directory__no_files(tmp_path, monkeypatch):
    add_subdirs_to_dir(tmp_path)

    expected_return_value = []
    assert get_all_files_in_directory(tmp_path) == expected_return_value


def test_get_all_files_in_directory__has_files(tmp_path, monkeypatch):
    add_subdirs_to_dir(tmp_path)
    files = add_files_to_dir(tmp_path)

    expected_return_value = sorted(files)
    assert sorted(get_all_files_in_directory(tmp_path)) == expected_return_value


def test_get_all_files_in_directory__subdir_has_files(tmp_path, monkeypatch):
    subdirs = add_subdirs_to_dir(tmp_path)
    add_files_to_dir(subdirs[0])

    files = add_files_to_dir(tmp_path)

    expected_return_value = sorted(files)
    assert sorted(get_all_files_in_directory(tmp_path)) == expected_return_value
