from http import HTTPStatus
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from tests.common import StubDIContainer

from monkey_island.cc.services.log_service.flask_resources.island_log import IslandLog

ISLAND_LOG_URL = IslandLog.urls[0]
LOG_FILE_PATH = Path("test_log_file_path")


@pytest.fixture
def flask_client(build_flask_client_with_resources):
    container = StubDIContainer()
    container.register_convention(Path, "island_log_file_path", LOG_FILE_PATH)
    with build_flask_client_with_resources(container, [IslandLog]) as flask_client:
        yield flask_client


def test_island_log_endpoint__missing_log(flask_client):
    resp = flask_client.get(ISLAND_LOG_URL, follow_redirects=True)
    assert resp.status_code == HTTPStatus.NOT_FOUND
    assert resp.json == ""


def test_island_log_endpoint__error_retrieving_log(flask_client, monkeypatch):
    get_text_file_contents = MagicMock(side_effect=Exception)
    monkeypatch.setattr(
        "monkey_island.cc.services.log_service.flask_resources.island_log.get_text_file_contents",
        get_text_file_contents,
    )
    resp = flask_client.get(ISLAND_LOG_URL, follow_redirects=True)
    assert resp.status_code == HTTPStatus.OK
    assert resp.json is None


@pytest.mark.parametrize("log", ["LoremIpsum1", "SecondLoremIpsum"])
def test_island_log_endpoint(flask_client, log, monkeypatch):
    monkeypatch.setattr(
        "monkey_island.cc.services.log_service.flask_resources.island_log.get_text_file_contents",
        lambda _: log,
    )
    resp = flask_client.get(ISLAND_LOG_URL, follow_redirects=True)
    assert resp.status_code == HTTPStatus.OK
    assert resp.json == log
