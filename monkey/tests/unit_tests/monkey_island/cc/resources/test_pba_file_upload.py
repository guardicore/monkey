import pytest
from tests.utils import raise_

from monkey_island.cc.resources.pba_file_upload import LINUX_PBA_TYPE, WINDOWS_PBA_TYPE
from monkey_island.cc.services.post_breach_files import PostBreachFilesService

TEST_FILE = b"""-----------------------------1
Content-Disposition: form-data; name="filepond"

{}
-----------------------------1
Content-Disposition: form-data; name="filepond"; filename="test.py"
Content-Type: text/x-python

m0nk3y
-----------------------------1--"""


@pytest.fixture(autouse=True)
def custom_pba_directory(tmpdir):
    PostBreachFilesService.initialize(tmpdir)


@pytest.fixture
def fake_set_config_value(monkeypatch):
    monkeypatch.setattr(
        "monkey_island.cc.services.config.ConfigService.set_config_value", lambda _, __: None
    )


@pytest.fixture
def fake_get_config_value(monkeypatch):
    monkeypatch.setattr(
        "monkey_island.cc.services.config.ConfigService.get_config_value", lambda _: "test.py"
    )


@pytest.mark.parametrize("pba_os", [LINUX_PBA_TYPE, WINDOWS_PBA_TYPE])
def test_pba_file_upload_post(flask_client, pba_os, monkeypatch, fake_set_config_value):
    resp = flask_client.post(
        f"/api/fileUpload/{pba_os}",
        data=TEST_FILE,
        content_type="multipart/form-data; " "boundary=---------------------------" "1",
        follow_redirects=True,
    )
    assert resp.status_code == 200


def test_pba_file_upload_post__invalid(flask_client, monkeypatch, fake_set_config_value):
    resp = flask_client.post(
        "/api/fileUpload/bogus",
        data=TEST_FILE,
        content_type="multipart/form-data; " "boundary=---------------------------" "1",
        follow_redirects=True,
    )
    assert resp.status_code == 422


@pytest.mark.parametrize("pba_os", [LINUX_PBA_TYPE, WINDOWS_PBA_TYPE])
def test_pba_file_upload_post__internal_server_error(
    flask_client, pba_os, monkeypatch, fake_set_config_value
):
    monkeypatch.setattr(
        "monkey_island.cc.resources.pba_file_upload.FileUpload.upload_pba_file",
        lambda x, y: raise_(Exception()),
    )

    resp = flask_client.post(
        f"/api/fileUpload/{pba_os}",
        data=TEST_FILE,
        content_type="multipart/form-data; boundary=---------------------------1",
        follow_redirects=True,
    )
    assert resp.status_code == 500


@pytest.mark.parametrize("pba_os", [LINUX_PBA_TYPE, WINDOWS_PBA_TYPE])
def test_pba_file_upload_get__file_not_found(
    flask_client, pba_os, monkeypatch, fake_get_config_value
):
    resp = flask_client.get(f"/api/fileUpload/{pba_os}?load=bogus_mogus.py")
    assert resp.status_code == 404


@pytest.mark.parametrize("pba_os", [LINUX_PBA_TYPE, WINDOWS_PBA_TYPE])
def test_pba_file_upload_endpoint(
    flask_client, pba_os, monkeypatch, fake_get_config_value, fake_set_config_value
):
    resp_post = flask_client.post(
        f"/api/fileUpload/{pba_os}",
        data=TEST_FILE,
        content_type="multipart/form-data; " "boundary=---------------------------" "1",
        follow_redirects=True,
    )
    resp_get = flask_client.get(f"/api/fileUpload/{pba_os}?load=test.py")
    resp_delete = flask_client.delete(
        f"/api/fileUpload/{pba_os}", data="test.py", content_type="text/plain;"
    )
    assert resp_post.status_code == 200
    assert resp_get.status_code == 200
    assert resp_get.data.decode() == "m0nk3y"
    assert resp_delete.status_code == 200


def test_pba_file_upload_endpoint__invalid(
    flask_client, monkeypatch, fake_set_config_value, fake_get_config_value
):
    resp_post = flask_client.post(
        "/api/fileUpload/bogus",
        data=TEST_FILE,
        content_type="multipart/form-data; " "boundary=---------------------------" "1",
        follow_redirects=True,
    )
    resp_get = flask_client.get("/api/fileUpload/bogus?load=test.py")
    resp_delete = flask_client.delete(
        "/api/fileUpload/bogus", data="test.py", content_type="text/plain;"
    )
    assert resp_post.status_code == 422
    assert resp_get.status_code == 422
    assert resp_delete.status_code == 422
