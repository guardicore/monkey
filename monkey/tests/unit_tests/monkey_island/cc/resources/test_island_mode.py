import json

import pytest

from monkey_island.cc.models.island_mode_model import IslandMode


@pytest.fixture(scope="function")
def uses_database():
    IslandMode.objects().delete()


def test_island_mode_post(flask_client):
    resp = flask_client.post(
        "/api/island-mode", data=json.dumps({"mode": "ransomware"}), follow_redirects=True
    )
    assert resp.status_code == 200


def test_island_mode_post__invalid_mode(flask_client):
    resp = flask_client.post(
        "/api/island-mode", data=json.dumps({"mode": "bogus mode"}), follow_redirects=True
    )
    assert resp.status_code == 404


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
