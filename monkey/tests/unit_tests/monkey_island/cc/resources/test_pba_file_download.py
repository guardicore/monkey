import io
from typing import BinaryIO

import pytest

from common import DIContainer
from monkey_island.cc.services import FileRetrievalError, IFileStorageService

FILE_NAME = "test_file"
FILE_CONTENTS = b"HelloWorld!"


class MockFileStorageService(IFileStorageService):
    def __init__(self):
        self._file = io.BytesIO(FILE_CONTENTS)

    def save_file(self, unsafe_file_name: str, file_contents: BinaryIO):
        pass

    def open_file(self, unsafe_file_name: str) -> BinaryIO:
        if unsafe_file_name != FILE_NAME:
            raise FileRetrievalError()

        return self._file

    def delete_file(self, unsafe_file_name: str):
        pass

    def delete_all_files(self):
        pass


@pytest.fixture
def flask_client(build_flask_client, tmp_path):
    container = DIContainer()
    container.register(IFileStorageService, MockFileStorageService)

    with build_flask_client(container) as flask_client:
        yield flask_client


def test_file_download_endpoint(tmp_path, flask_client):
    resp = flask_client.get(f"/api/pba/download/{FILE_NAME}")

    assert resp.status_code == 200
    assert next(resp.response) == FILE_CONTENTS


def test_file_download_endpoint_404(tmp_path, flask_client):
    nonexistant_file_name = "nonexistant_file"

    resp = flask_client.get(f"/api/pba/download/{nonexistant_file_name}")

    assert resp.status_code == 404
