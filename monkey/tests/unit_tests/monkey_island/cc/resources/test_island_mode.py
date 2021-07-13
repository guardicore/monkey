import json

import pytest

from monkey_island.cc.models.island_mode_model import IslandMode


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


@pytest.mark.usefixtures("uses_database")
def test_island_mode_post__set_model(flask_client):
    flask_client.post(
        "/api/island-mode", data=json.dumps({"mode": "ransomware"}), follow_redirects=True
    )
    assert IslandMode.objects[0].mode == "ransomware"


@pytest.mark.usefixtures("uses_database")
def test_island_mode_post__set_invalid_model(flask_client):
    flask_client.post(
        "/api/island-mode", data=json.dumps({"mode": "bogus mode"}), follow_redirects=True
    )
    assert len(IslandMode.objects) == 0
