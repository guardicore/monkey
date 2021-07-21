import json

import pytest
from tests.utils import raise_

from monkey_island.cc.models.island_mode_model import IslandMode
from monkey_island.cc.resources import island_mode as island_mode_resource


@pytest.fixture(scope="function")
def uses_database():
    IslandMode.objects().delete()


@pytest.mark.parametrize("mode", ["ransomware", "advanced"])
def test_island_mode_post(flask_client, mode, monkeypatch):
    monkeypatch.setattr(
        "monkey_island.cc.resources.island_mode.update_config_on_mode_set",
        lambda _: None,
    )
    resp = flask_client.post(
        "/api/island-mode", data=json.dumps({"mode": mode}), follow_redirects=True
    )
    assert resp.status_code == 200


def test_island_mode_post__invalid_mode(flask_client):
    resp = flask_client.post(
        "/api/island-mode", data=json.dumps({"mode": "bogus mode"}), follow_redirects=True
    )
    assert resp.status_code == 422


@pytest.mark.parametrize("invalid_json", ["42", "{test"])
def test_island_mode_post__invalid_json(flask_client, invalid_json):
    resp = flask_client.post("/api/island-mode", data="{test", follow_redirects=True)
    assert resp.status_code == 400


def test_island_mode_post__internal_server_error(monkeypatch, flask_client):
    monkeypatch.setattr(island_mode_resource, "set_mode", lambda x: raise_(Exception()))

    resp = flask_client.post(
        "/api/island-mode", data=json.dumps({"mode": "ransomware"}), follow_redirects=True
    )
    assert resp.status_code == 500


@pytest.mark.parametrize("mode", ["ransomware", "advanced"])
def test_island_mode_endpoint(flask_client, uses_database, mode):
    flask_client.post("/api/island-mode", data=json.dumps({"mode": mode}), follow_redirects=True)
    resp = flask_client.get("/api/island-mode", follow_redirects=True)
    assert resp.status_code == 200
    assert json.loads(resp.data)["mode"] == mode


def test_island_mode_endpoint__invalid_mode(flask_client, uses_database):
    resp_post = flask_client.post(
        "/api/island-mode", data=json.dumps({"mode": "bogus_mode"}), follow_redirects=True
    )
    resp_get = flask_client.get("/api/island-mode", follow_redirects=True)
    assert resp_post.status_code == 422
    assert json.loads(resp_get.data)["mode"] is None
