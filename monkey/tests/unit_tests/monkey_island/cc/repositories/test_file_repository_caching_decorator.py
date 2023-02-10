import io
import re
from copy import copy

import pytest
from tests.monkey_island import InMemoryFileRepository, SingleFileRepository

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


FILE_NAMES = {"f1", "f2", "f3"}


@pytest.fixture
def in_memory_file_repository():
    repository = InMemoryFileRepository()

    for fname in FILE_NAMES:
        repository.save_file(fname, io.BytesIO(b""))

    return repository


@pytest.fixture
def multi_file_repository(in_memory_file_repository):
    return FileRepositoryCachingDecorator(in_memory_file_repository)


def test_get_all_file_names(multi_file_repository):
    retrieved_file_names = multi_file_repository.get_all_file_names()

    assert set(retrieved_file_names) == FILE_NAMES


def test_get_all_file_names__caching(multi_file_repository, in_memory_file_repository):
    retrieved_file_names_1 = multi_file_repository.get_all_file_names()
    # We're bypassing the caching decorator by directly modifying the repository it decorates. This
    # should leave the cache in the decorator untouched, proving that the caching works.
    in_memory_file_repository.delete_all_files()
    retrieved_file_names_2 = multi_file_repository.get_all_file_names()

    assert set(retrieved_file_names_1) == FILE_NAMES
    assert set(retrieved_file_names_2) == FILE_NAMES


def test_get_all_file_names__save_file_resets_cache(multi_file_repository):
    retrieved_file_names_1 = multi_file_repository.get_all_file_names()
    multi_file_repository.save_file("f4", io.BytesIO(b""))
    retrieved_file_names_2 = multi_file_repository.get_all_file_names()

    assert retrieved_file_names_2 != retrieved_file_names_1
    assert len(retrieved_file_names_2) == len(FILE_NAMES) + 1


def test_get_all_file_names__delete_file_resets_cache(multi_file_repository):
    file_to_delete = copy(FILE_NAMES).pop()

    retrieved_file_names_1 = multi_file_repository.get_all_file_names()
    multi_file_repository.delete_file(file_to_delete)
    retrieved_file_names_2 = multi_file_repository.get_all_file_names()

    assert retrieved_file_names_2 != retrieved_file_names_1
    assert len(retrieved_file_names_2) == len(FILE_NAMES) - 1


def test_get_all_file_names__delete_all_files_resets_cache(multi_file_repository):
    retrieved_file_names_1 = multi_file_repository.get_all_file_names()
    multi_file_repository.delete_all_files()
    retrieved_file_names_2 = multi_file_repository.get_all_file_names()

    assert retrieved_file_names_2 != retrieved_file_names_1
    assert len(retrieved_file_names_2) == 0


def test_get_all_file_names__delete_files_by_regex_resets_cache(multi_file_repository):
    retrieved_file_names_1 = multi_file_repository.get_all_file_names()
    multi_file_repository.delete_files_by_regex(re.compile(r"f\d"))
    retrieved_file_names_2 = multi_file_repository.get_all_file_names()

    assert retrieved_file_names_2 != retrieved_file_names_1
    assert len(retrieved_file_names_2) == 0
