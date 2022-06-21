import io
from typing import BinaryIO

import pytest
from tests.common import StubDIContainer
from tests.unit_tests.monkey_island.conftest import get_url_for_resource

from monkey_island.cc.repository import FileNotFoundError, IFileRepository
from monkey_island.cc.resources.pba_file_download import PBAFileDownload

FILE_NAME = "test_file"
FILE_CONTENTS = b"HelloWorld!"


class MockFileRepository(IFileRepository):
    def __init__(self):
        self._file = io.BytesIO(FILE_CONTENTS)

    def save_file(self, unsafe_file_name: str, file_contents: BinaryIO):
        pass

    def open_file(self, unsafe_file_name: str) -> BinaryIO:
        if unsafe_file_name != FILE_NAME:
            raise FileNotFoundError()

        return self._file

    def delete_file(self, unsafe_file_name: str):
        pass

    def delete_all_files(self):
        pass


@pytest.fixture
def flask_client(build_flask_client):
    container = StubDIContainer()
    container.register(IFileRepository, MockFileRepository)

    with build_flask_client(container) as flask_client:
        yield flask_client


def test_file_download_endpoint(tmp_path, flask_client):
    download_url = get_url_for_resource(PBAFileDownload, filename=FILE_NAME)
    resp = flask_client.get(download_url)

    assert resp.status_code == 200
    assert next(resp.response) == FILE_CONTENTS


def test_file_download_endpoint_404(tmp_path, flask_client):
    nonexistant_file_name = "nonexistant_file"
    download_url = get_url_for_resource(PBAFileDownload, filename=nonexistant_file_name)

    resp = flask_client.get(download_url)

    assert resp.status_code == 404
