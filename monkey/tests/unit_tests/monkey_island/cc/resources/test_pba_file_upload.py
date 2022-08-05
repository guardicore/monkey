from typing import Callable

import pytest
from flask.testing import FlaskClient
from tests.common import StubDIContainer
from tests.monkey_island import InMemoryAgentConfigurationRepository, SingleFileRepository
from tests.unit_tests.monkey_island.conftest import get_url_for_resource
from tests.utils import raise_

from common import DIContainer
from monkey_island.cc.repository import IAgentConfigurationRepository, IFileRepository
from monkey_island.cc.resources import LINUX_PBA_TYPE, WINDOWS_PBA_TYPE, PBAFileUpload

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
def file_repository() -> IFileRepository:
    return SingleFileRepository()


@pytest.fixture
def agent_configuration_repository() -> IAgentConfigurationRepository:
    return InMemoryAgentConfigurationRepository()


@pytest.fixture
def flask_client(
    build_flask_client: Callable[[DIContainer], FlaskClient],
    file_repository: IFileRepository,
    agent_configuration_repository: IAgentConfigurationRepository,
) -> FlaskClient:
    container = StubDIContainer()
    container.register_instance(IFileRepository, file_repository)
    container.register_instance(IAgentConfigurationRepository, agent_configuration_repository)

    with build_flask_client(container) as flask_client:
        yield flask_client


@pytest.mark.parametrize("pba_os", [LINUX_PBA_TYPE, WINDOWS_PBA_TYPE])
def test_pba_file_upload_post(flask_client: FlaskClient, pba_os: str):
    url = get_url_for_resource(PBAFileUpload, target_os=pba_os)
    resp = flask_client.post(
        url,
        data=TEST_FILE,
        content_type="multipart/form-data; " "boundary=---------------------------" "1",
        follow_redirects=True,
    )
    assert resp.status_code == 200


def test_pba_file_upload_post__invalid(flask_client: FlaskClient):
    url = get_url_for_resource(PBAFileUpload, target_os="bogus")
    resp = flask_client.post(
        url,
        data=TEST_FILE,
        content_type="multipart/form-data; " "boundary=---------------------------" "1",
        follow_redirects=True,
    )
    assert resp.status_code == 422


@pytest.mark.parametrize("pba_os", [LINUX_PBA_TYPE, WINDOWS_PBA_TYPE])
def test_pba_file_upload_post__internal_server_error(
    flask_client: FlaskClient, pba_os: str, file_repository: IFileRepository
):
    file_repository.save_file = lambda x, y: raise_(Exception())
    url = get_url_for_resource(PBAFileUpload, target_os=pba_os)

    resp = flask_client.post(
        url,
        data=TEST_FILE,
        content_type="multipart/form-data; boundary=---------------------------1",
        follow_redirects=True,
    )
    assert resp.status_code == 500


@pytest.mark.parametrize("pba_os", [LINUX_PBA_TYPE, WINDOWS_PBA_TYPE])
def test_pba_file_upload_get__file_not_found(flask_client: FlaskClient, pba_os: str):
    url = get_url_for_resource(PBAFileUpload, target_os=pba_os, filename="bobug_mogus.py")
    resp = flask_client.get(url)
    assert resp.status_code == 404


@pytest.mark.parametrize("pba_os", [LINUX_PBA_TYPE, WINDOWS_PBA_TYPE])
def test_file_download_endpoint_500(open_error_flask_client, pba_os: str):
    url = get_url_for_resource(PBAFileUpload, target_os=pba_os, filename="bobug_mogus.py")

    resp = open_error_flask_client.get(url)

    assert resp.status_code == 500


@pytest.mark.parametrize("pba_os", [LINUX_PBA_TYPE, WINDOWS_PBA_TYPE])
def test_pba_file_upload_endpoint(flask_client: FlaskClient, pba_os: str):

    url_with_os = get_url_for_resource(PBAFileUpload, target_os=pba_os)
    resp_post = flask_client.post(
        url_with_os,
        data=TEST_FILE,
        content_type="multipart/form-data; " "boundary=---------------------------" "1",
        follow_redirects=True,
    )

    url_with_filename = get_url_for_resource(PBAFileUpload, target_os=pba_os, filename="test.py")
    resp_get = flask_client.get(url_with_filename)
    assert resp_get.status_code == 200
    assert resp_get.data == TEST_FILE_CONTENTS
    # Closing the response closes the file handle, else it can't be deleted
    resp_get.close()

    resp_delete = flask_client.delete(url_with_os, data="test.py", content_type="text/plain;")
    resp_get_del = flask_client.get(url_with_filename)

    assert resp_post.status_code == 200
    assert resp_delete.status_code == 200
    assert resp_get_del.status_code == 404


def test_pba_file_upload_endpoint__invalid(flask_client: FlaskClient):

    url_with_os = get_url_for_resource(PBAFileUpload, target_os="bogus")
    resp_post = flask_client.post(
        url_with_os,
        data=TEST_FILE,
        content_type="multipart/form-data; " "boundary=---------------------------" "1",
        follow_redirects=True,
    )

    url_with_filename = get_url_for_resource(
        PBAFileUpload, target_os="bogus", filename="bobug_mogus.py"
    )
    resp_get = flask_client.get(url_with_filename)
    resp_delete = flask_client.delete(url_with_os, data="test.py", content_type="text/plain;")
    assert resp_post.status_code == 422
    assert resp_get.status_code == 422
    assert resp_delete.status_code == 422
