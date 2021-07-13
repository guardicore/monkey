import json

import pytest
from tests.utils import raise_

from monkey_island.cc.models.island_mode_model import IslandMode
from monkey_island.cc.resources import island_mode as island_mode_resource


@pytest.fixture(scope="function")
def uses_database():
    IslandMode.objects().delete()


@pytest.mark.parametrize("mode", ["ransomware", "advanced"])
def test_island_mode_post(flask_client, mode):
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


def test_island_mode_post__set_model(flask_client, uses_database):
    flask_client.post(
        "/api/island-mode", data=json.dumps({"mode": "ransomware"}), follow_redirects=True
    )
    assert IslandMode.objects[0].mode == "ransomware"


def test_island_mode_post__set_invalid_model(flask_client, uses_database):
    flask_client.post(
        "/api/island-mode", data=json.dumps({"mode": "bogus mode"}), follow_redirects=True
    )
    assert len(IslandMode.objects) == 0
