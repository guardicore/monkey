import os

import pytest
from tests.monkey_island.utils import assert_windows_permissions
from tests.utils import raise_

from monkey_island.cc.server_utils.file_utils import is_windows_os
from monkey_island.cc.services.post_breach_files import PostBreachFilesService


@pytest.fixture(autouse=True)
def custom_pba_directory(tmpdir):
    PostBreachFilesService.initialize(tmpdir)


def create_custom_pba_file(filename):
    PostBreachFilesService.save_file(filename, b"")


def test_remove_pba_files():
    create_custom_pba_file("linux_file")
    create_custom_pba_file("windows_file")

    assert not dir_is_empty(PostBreachFilesService.get_custom_pba_directory())
    PostBreachFilesService.remove_PBA_files()
    assert dir_is_empty(PostBreachFilesService.get_custom_pba_directory())


def dir_is_empty(dir_path):
    dir_contents = os.listdir(dir_path)
    return len(dir_contents) == 0


@pytest.mark.skipif(is_windows_os(), reason="Tests Posix (not Windows) permissions.")
def test_custom_pba_dir_permissions_linux():
    st = os.stat(PostBreachFilesService.get_custom_pba_directory())

    assert st.st_mode == 0o40700


@pytest.mark.skipif(not is_windows_os(), reason="Tests Windows (not Posix) permissions.")
def test_custom_pba_dir_permissions_windows():
    pba_dir = PostBreachFilesService.get_custom_pba_directory()

    assert_windows_permissions(pba_dir)


def test_remove_failure(monkeypatch):
    monkeypatch.setattr(os, "remove", lambda x: raise_(OSError("Permission denied")))

    try:
        create_custom_pba_file("windows_file")
        PostBreachFilesService.remove_PBA_files()
    except Exception as ex:
        pytest.fail(f"Unxepected exception: {ex}")


def test_remove_nonexistant_file(monkeypatch):
    monkeypatch.setattr(os, "remove", lambda x: raise_(FileNotFoundError("FileNotFound")))

    try:
        PostBreachFilesService.remove_file("/nonexistant/file")
    except Exception as ex:
        pytest.fail(f"Unxepected exception: {ex}")


def test_save_file():
    FILE_NAME = "test_file"
    FILE_CONTENTS = b"hello"
    PostBreachFilesService.save_file(FILE_NAME, FILE_CONTENTS)

    expected_file_path = os.path.join(PostBreachFilesService.get_custom_pba_directory(), FILE_NAME)

    assert os.path.isfile(expected_file_path)
    assert FILE_CONTENTS == open(expected_file_path, "rb").read()
