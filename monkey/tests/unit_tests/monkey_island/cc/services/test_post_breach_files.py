import io
import os

import pytest
from tests.utils import raise_

from monkey_island.cc.services import DirectoryFileStorageService
from monkey_island.cc.services.post_breach_files import PostBreachFilesService


@pytest.fixture
def file_storage_service(tmp_path):
    return DirectoryFileStorageService(tmp_path)


@pytest.fixture(autouse=True)
def post_breach_files_service(file_storage_service):
    PostBreachFilesService.initialize(file_storage_service)


def test_remove_pba_files(file_storage_service, tmp_path):
    file_storage_service.save_file("linux_file", io.BytesIO(b""))
    file_storage_service.save_file("windows_file", io.BytesIO(b""))
    assert not dir_is_empty(tmp_path)

    PostBreachFilesService.remove_PBA_files()

    assert dir_is_empty(tmp_path)


def dir_is_empty(dir_path):
    dir_contents = os.listdir(dir_path)
    return len(dir_contents) == 0


def test_remove_failure(file_storage_service, monkeypatch):
    monkeypatch.setattr(os, "remove", lambda x: raise_(OSError("Permission denied")))

    try:
        file_storage_service.save_file("windows_file", io.BytesIO(b""))
        PostBreachFilesService.remove_PBA_files()
    except Exception as ex:
        pytest.fail(f"Unxepected exception: {ex}")
