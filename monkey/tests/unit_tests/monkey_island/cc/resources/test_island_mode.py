import json

import pytest


def test_island_mode_post(flask_client):
    resp = flask_client.post('/api/island-mode', data=json.dumps({"mode": "ransomware"}), follow_redirects=True)
    assert resp.status_code == 200


def test_island_mode_post__invalid_mode(flask_client):
    with pytest.raises(TypeError):
        flask_client.post('/api/island-mode', data=json.dumps({"mode": "bogus mode"}), follow_redirects=True)
