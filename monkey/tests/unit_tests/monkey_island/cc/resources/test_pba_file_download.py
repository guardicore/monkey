import pytest
from tests.common import StubDIContainer
from tests.monkey_island import FILE_CONTENTS, FILE_NAME, MockFileRepository
from tests.unit_tests.monkey_island.conftest import get_url_for_resource

from monkey_island.cc.repository import IFileRepository
from monkey_island.cc.resources import PBAFileDownload


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


def test_file_download_endpoint_500(tmp_path, open_error_flask_client):
    download_url = get_url_for_resource(PBAFileDownload, filename="test")

    resp = open_error_flask_client.get(download_url)

    assert resp.status_code == 500
