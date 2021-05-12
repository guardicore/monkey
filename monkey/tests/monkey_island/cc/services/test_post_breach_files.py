import os

import pytest

from monkey_island.cc.services.post_breach_files import PostBreachFilesService


def raise_(ex):
    raise ex


@pytest.fixture(autouse=True)
def custom_pba_directory(tmpdir):
    PostBreachFilesService.initialize(tmpdir)


def create_custom_pba_file(filename):
    assert os.path.isdir(PostBreachFilesService.get_custom_pba_directory())

    file_path = os.path.join(PostBreachFilesService.get_custom_pba_directory(), filename)
    open(file_path, "a").close()


def test_remove_pba_files():
    create_custom_pba_file("linux_file")
    create_custom_pba_file("windows_file")

    assert not dir_is_empty(PostBreachFilesService.get_custom_pba_directory())
    PostBreachFilesService.remove_PBA_files()
    assert dir_is_empty(PostBreachFilesService.get_custom_pba_directory())


def dir_is_empty(dir_path):
    dir_contents = os.listdir(dir_path)
    return len(dir_contents) == 0


@pytest.mark.skipif(os.name != "posix", reason="Tests Posix (not Windows) permissions.")
def test_custom_pba_dir_permissions():
    st = os.stat(PostBreachFilesService.get_custom_pba_directory())

    assert st.st_mode == 0o40700


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
