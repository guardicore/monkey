import io

import pytest
from tests.monkey_island import SingleFileRepository

from monkey_island.cc import repositories
from monkey_island.cc.repositories import FileRepositoryCachingDecorator


@pytest.fixture
def file_repository():
    return FileRepositoryCachingDecorator(SingleFileRepository())


def test_open_cache_file(file_repository):
    file_name = "test.txt"
    file_contents = b"Hello World!"

    file_repository.save_file(file_name, io.BytesIO(file_contents))
    assert file_repository.open_file(file_name).read() == file_contents
    assert file_repository.open_file(file_name).read() == file_contents


def test_overwrite_file(file_repository):
    file_name = "test.txt"
    file_contents_1 = b"Hello World!"
    file_contents_2 = b"Goodbye World!"

    file_repository.save_file(file_name, io.BytesIO(file_contents_1))
    assert file_repository.open_file(file_name).read() == file_contents_1

    file_repository.save_file(file_name, io.BytesIO(file_contents_2))
    assert file_repository.open_file(file_name).read() == file_contents_2


def test_delete_file(file_repository):
    file_name = "test.txt"
    file_contents = b"Hello World!"

    file_repository.save_file(file_name, io.BytesIO(file_contents))
    file_repository.delete_file(file_name)

    with pytest.raises(repositories.FileNotFoundError):
        file_repository.open_file(file_name)


def test_delete_all_files(file_repository):
    file_name = "test.txt"
    file_contents = b"Hello World!"

    file_repository.save_file(file_name, io.BytesIO(file_contents))
    file_repository.delete_all_files()

    with pytest.raises(repositories.FileNotFoundError):
        file_repository.open_file(file_name)
