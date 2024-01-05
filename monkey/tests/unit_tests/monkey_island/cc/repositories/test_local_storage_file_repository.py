import io
import re
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from monkeytoolbox import get_os
from monkeytypes import OperatingSystem
from tests.monkey_island.utils import assert_linux_permissions, assert_windows_permissions
from tests.utils import raise_

from monkey_island.cc import repositories
from monkey_island.cc.repositories import LocalStorageFileRepository


def os_is_windows():
    return get_os() == OperatingSystem.WINDOWS


def test_error_if_storage_directory_is_file(tmp_path):
    new_file = tmp_path / "new_file.txt"
    new_file.write_text("HelloWorld!")

    with pytest.raises(ValueError):
        LocalStorageFileRepository(new_file)


def test_directory_created(tmp_path):
    new_dir = tmp_path / "new_dir"

    LocalStorageFileRepository(new_dir)

    assert new_dir.exists() and new_dir.is_dir()


@pytest.mark.skipif(os_is_windows(), reason="Tests Posix (not Windows) permissions.")
def test_directory_permissions__linux(tmp_path):
    new_dir = tmp_path / "new_dir"

    LocalStorageFileRepository(new_dir)

    assert_linux_permissions(new_dir)


@pytest.mark.skipif(not os_is_windows(), reason="Tests Windows (not Posix) permissions.")
def test_directory_permissions__windows(tmp_path):
    new_dir = tmp_path / "new_dir"

    LocalStorageFileRepository(new_dir)

    assert_windows_permissions(new_dir)


def save_file(tmp_path, file_path_prefix=""):
    file_name = "test.txt"
    file_contents = "Hello World!"
    expected_file_path = tmp_path / file_name

    fss = LocalStorageFileRepository(tmp_path)
    fss.save_file(Path(file_path_prefix) / file_name, io.BytesIO(file_contents.encode()))

    assert expected_file_path.is_file()
    assert expected_file_path.read_text() == file_contents


def delete_file(tmp_path, file_path_prefix=""):
    file_name = "file.txt"
    file = tmp_path / file_name
    file.touch()
    assert file.is_file()

    fss = LocalStorageFileRepository(tmp_path)
    fss.delete_file(Path(file_path_prefix) / file_name)

    assert not file.exists()


def open_file(tmp_path, file_path_prefix=""):
    file_name = "test.txt"
    expected_file_contents = "Hello World!"
    expected_file_path = tmp_path / file_name
    expected_file_path.write_text(expected_file_contents)

    fss = LocalStorageFileRepository(tmp_path)
    with fss.open_file(Path(file_path_prefix) / file_name) as f:
        actual_file_contents = f.read()

    assert actual_file_contents == expected_file_contents.encode()


@pytest.mark.parametrize("fn", [save_file, open_file, delete_file])
def test_fn(tmp_path, fn):
    fn(tmp_path)


@pytest.mark.parametrize("fn", [save_file, open_file, delete_file])
def test_fn__ignore_relative_path(tmp_path, fn):
    fn(tmp_path, "../../")


@pytest.mark.parametrize("fn", [save_file, open_file, delete_file])
def test_fn__ignore_absolute_path(tmp_path, fn):
    if os_is_windows():
        fn(tmp_path, "C:\\Windows")
    else:
        fn(tmp_path, "/home/")


def test_remove_all_files(tmp_path):
    for filename in ["1.txt", "2.txt", "3.txt"]:
        (tmp_path / filename).touch()

    fss = LocalStorageFileRepository(tmp_path)
    fss.delete_all_files()

    for file in tmp_path.iterdir():
        assert False, f"{tmp_path} was expected to be empty, but contained files"


def test_remove_all_files__skip_directories(tmp_path):
    test_dir = tmp_path / "test_dir"
    test_dir.mkdir()
    for filename in ["1.txt", "2.txt", "3.txt"]:
        (tmp_path / filename).touch()

    fss = LocalStorageFileRepository(tmp_path)
    fss.delete_all_files()

    for file in tmp_path.iterdir():
        assert file.name == test_dir.name


def test_remove_nonexistant_file(tmp_path):
    fss = LocalStorageFileRepository(tmp_path)

    # This test will fail if this call raises an exception.
    fss.delete_file("nonexistant_file.txt")


def test_open_nonexistant_file(tmp_path):
    fss = LocalStorageFileRepository(tmp_path)

    with pytest.raises(repositories.FileNotFoundError):
        fss.open_file("nonexistant_file.txt")


def test_open_locked_file(tmp_path, monkeypatch):
    fss = LocalStorageFileRepository(tmp_path)

    with patch("builtins.open", Mock(side_effect=Exception())):
        with pytest.raises(repositories.RetrievalError):
            fss.open_file("locked_file.txt")


def test_delete_files_by_regex(tmp_path):
    for filename in {"xyz-1.txt", "abc-2.txt", "pqr-3.txt", "abc-4.txt", "abc-5.pdf"}:
        (tmp_path / filename).touch()

    fss = LocalStorageFileRepository(tmp_path)
    fss.delete_files_by_regex(re.compile(r"^abc-[\w-]+.txt$"))

    files = {f.name for f in tmp_path.iterdir()}
    assert files == {"xyz-1.txt", "pqr-3.txt", "abc-5.pdf"}


def test_get_all_files__empty_repository(tmp_path):
    fss = LocalStorageFileRepository(tmp_path)

    assert len(fss.get_all_file_names()) == 0


def test_get_all_files(tmp_path):
    file_names = {"f1", "f2.txt", "f3.tar.gz", "f4.so"}
    for filename in file_names:
        (tmp_path / filename).touch()

    fss = LocalStorageFileRepository(tmp_path)
    retrieved_file_names = fss.get_all_file_names()

    assert set(retrieved_file_names) == file_names


def test_get_all_files__retrieval_error(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "monkey_island.cc.repositories.local_storage_file_repository.get_all_regular_files_in_directory",  # noqa: E501
        lambda _: raise_(OSError()),
    )

    fss = LocalStorageFileRepository(tmp_path)

    with pytest.raises(repositories.RetrievalError):
        fss.get_all_file_names()
