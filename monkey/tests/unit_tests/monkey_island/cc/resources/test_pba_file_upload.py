import io
from typing import BinaryIO

import pytest
from tests.utils import raise_

from common import DIContainer
from monkey_island.cc.resources.pba_file_upload import LINUX_PBA_TYPE, WINDOWS_PBA_TYPE
from monkey_island.cc.services import FileRetrievalError, IFileStorageService

TEST_FILE_CONTENTS = b"m0nk3y"
TEST_FILE = (
    b"""-----------------------------1
Content-Disposition: form-data; name="filepond"

{}
-----------------------------1
Content-Disposition: form-data; name="filepond"; filename="test.py"
Content-Type: text/x-python

"""
    + TEST_FILE_CONTENTS
    + b"""
-----------------------------1--"""
)


@pytest.fixture
def mock_set_config_value(monkeypatch):
    monkeypatch.setattr(
        "monkey_island.cc.services.config.ConfigService.set_config_value", lambda _, __: None
    )


@pytest.fixture
def mock_get_config_value(monkeypatch):
    monkeypatch.setattr(
        "monkey_island.cc.services.config.ConfigService.get_config_value", lambda _: "test.py"
    )


class MockFileStorageService(IFileStorageService):
    def __init__(self):
        self._file = None

    def save_file(self, unsafe_file_name: str, file_contents: BinaryIO):
        self._file = io.BytesIO(file_contents.read())

    def open_file(self, unsafe_file_name: str) -> BinaryIO:
        if self._file is None:
            raise FileRetrievalError()
        return self._file

    def delete_file(self, unsafe_file_name: str):
        self._file = None

    def delete_all_files(self):
        self.delete_file("")


@pytest.fixture
def file_storage_service():
    return MockFileStorageService()


@pytest.fixture
def flask_client(build_flask_client, file_storage_service):
    container = DIContainer()
    container.register_instance(IFileStorageService, file_storage_service)

    with build_flask_client(container) as flask_client:
        yield flask_client


@pytest.mark.parametrize("pba_os", [LINUX_PBA_TYPE, WINDOWS_PBA_TYPE])
def test_pba_file_upload_post(flask_client, pba_os, mock_set_config_value):
    resp = flask_client.post(
        f"/api/file-upload/{pba_os}",
        data=TEST_FILE,
        content_type="multipart/form-data; " "boundary=---------------------------" "1",
        follow_redirects=True,
    )
    assert resp.status_code == 200


def test_pba_file_upload_post__invalid(flask_client, mock_set_config_value):
    resp = flask_client.post(
        "/api/file-upload/bogus",
        data=TEST_FILE,
        content_type="multipart/form-data; " "boundary=---------------------------" "1",
        follow_redirects=True,
    )
    assert resp.status_code == 422


@pytest.mark.parametrize("pba_os", [LINUX_PBA_TYPE, WINDOWS_PBA_TYPE])
def test_pba_file_upload_post__internal_server_error(
    flask_client, pba_os, mock_set_config_value, file_storage_service
):
    file_storage_service.save_file = lambda x, y: raise_(Exception())

    resp = flask_client.post(
        f"/api/file-upload/{pba_os}",
        data=TEST_FILE,
        content_type="multipart/form-data; boundary=---------------------------1",
        follow_redirects=True,
    )
    assert resp.status_code == 500


@pytest.mark.parametrize("pba_os", [LINUX_PBA_TYPE, WINDOWS_PBA_TYPE])
def test_pba_file_upload_get__file_not_found(flask_client, pba_os, mock_get_config_value):
    resp = flask_client.get(f"/api/file-upload/{pba_os}?load=bogus_mogus.py")
    assert resp.status_code == 404


@pytest.mark.parametrize("pba_os", [LINUX_PBA_TYPE, WINDOWS_PBA_TYPE])
def test_pba_file_upload_endpoint(
    flask_client, pba_os, mock_get_config_value, mock_set_config_value
):
    resp_post = flask_client.post(
        f"/api/file-upload/{pba_os}",
        data=TEST_FILE,
        content_type="multipart/form-data; " "boundary=---------------------------" "1",
        follow_redirects=True,
    )

    resp_get = flask_client.get(f"/api/file-upload/{pba_os}?load=test.py")
    assert resp_get.status_code == 200
    assert resp_get.data == TEST_FILE_CONTENTS
    # Closing the response closes the file handle, else it can't be deleted
    resp_get.close()

    resp_delete = flask_client.delete(
        f"/api/file-upload/{pba_os}", data="test.py", content_type="text/plain;"
    )
    resp_get_del = flask_client.get(f"/api/file-upload/{pba_os}?load=test.py")
    assert resp_post.status_code == 200

    assert resp_delete.status_code == 200

    assert resp_get_del.status_code == 404


def test_pba_file_upload_endpoint__invalid(
    flask_client, mock_set_config_value, mock_get_config_value
):
    resp_post = flask_client.post(
        "/api/file-upload/bogus",
        data=TEST_FILE,
        content_type="multipart/form-data; " "boundary=---------------------------" "1",
        follow_redirects=True,
    )
    resp_get = flask_client.get("/api/file-upload/bogus?load=test.py")
    resp_delete = flask_client.delete(
        "/api/file-upload/bogus", data="test.py", content_type="text/plain;"
    )
    assert resp_post.status_code == 422
    assert resp_get.status_code == 422
    assert resp_delete.status_code == 422
