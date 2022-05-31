import io
import os

import pytest
from tests.utils import raise_

from monkey_island.cc.repository import LocalStorageFileRepository
from monkey_island.cc.services.post_breach_files import PostBreachFilesService


@pytest.fixture
def local_storage_file_repository(tmp_path):
    return LocalStorageFileRepository(tmp_path)


@pytest.fixture(autouse=True)
def post_breach_files_service(local_storage_file_repository):
    PostBreachFilesService.initialize(local_storage_file_repository)


def test_remove_pba_files(local_storage_file_repository, tmp_path):
    local_storage_file_repository.save_file("linux_file", io.BytesIO(b""))
    local_storage_file_repository.save_file("windows_file", io.BytesIO(b""))
    assert not dir_is_empty(tmp_path)

    PostBreachFilesService.remove_PBA_files()

    assert dir_is_empty(tmp_path)


def dir_is_empty(dir_path):
    dir_contents = os.listdir(dir_path)
    return len(dir_contents) == 0


def test_remove_failure(local_storage_file_repository, monkeypatch):
    monkeypatch.setattr(os, "remove", lambda x: raise_(OSError("Permission denied")))

    try:
        local_storage_file_repository.save_file("windows_file", io.BytesIO(b""))
        PostBreachFilesService.remove_PBA_files()
    except Exception as ex:
        pytest.fail(f"Unxepected exception: {ex}")
