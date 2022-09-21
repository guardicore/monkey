from http import HTTPStatus
from unittest.mock import MagicMock

import pytest
from tests.common import StubDIContainer
from tests.monkey_island import InMemorySimulationRepository

from monkey_island.cc.event_queue import IIslandEventQueue
from monkey_island.cc.models import IslandMode
from monkey_island.cc.repository import ISimulationRepository
from monkey_island.cc.resources.island_mode import IslandMode as IslandModeResource


@pytest.fixture
def flask_client(build_flask_client):
    container = StubDIContainer()

    in_memory_simulation_repository = InMemorySimulationRepository()
    container.register_instance(ISimulationRepository, in_memory_simulation_repository)

    def wrap_in_memory_simulation_repository_set_mode(topic, event):
        mode = event
        in_memory_simulation_repository.set_mode(mode)

    mock_island_event_queue = MagicMock(spec=IIslandEventQueue)
    mock_island_event_queue.publish.side_effect = wrap_in_memory_simulation_repository_set_mode
    container.register_instance(IIslandEventQueue, mock_island_event_queue)

    with build_flask_client(container) as flask_client:
        yield flask_client


@pytest.mark.parametrize(
    "mode",
    [IslandMode.RANSOMWARE.value, IslandMode.ADVANCED.value, IslandMode.UNSET.value],
)
def test_island_mode_post(flask_client, mode):
    resp = flask_client.put(
        IslandModeResource.urls[0],
        json=mode,
        follow_redirects=True,
    )
    assert resp.status_code == HTTPStatus.NO_CONTENT


def test_island_mode_post__invalid_mode(flask_client):
    resp = flask_client.put(
        IslandModeResource.urls[0],
        json="bogus mode",
        follow_redirects=True,
    )
    assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_island_mode_post__internal_server_error(build_flask_client):
    container = StubDIContainer()

    with build_flask_client(container) as flask_client:
        resp = flask_client.put(
            IslandModeResource.urls[0],
            json=IslandMode.RANSOMWARE.value,
            follow_redirects=True,
        )

    assert resp.status_code == HTTPStatus.INTERNAL_SERVER_ERROR


@pytest.mark.parametrize("mode", [IslandMode.RANSOMWARE.value, IslandMode.ADVANCED.value])
def test_island_mode_endpoint(flask_client, mode):
    flask_client.put(
        IslandModeResource.urls[0],
        json=mode,
        follow_redirects=True,
    )
    resp = flask_client.get(IslandModeResource.urls[0], follow_redirects=True)
    assert resp.status_code == HTTPStatus.OK
    assert resp.json == mode


def test_island_mode_endpoint__invalid_mode(flask_client):
    resp_post = flask_client.put(
        IslandModeResource.urls[0],
        json="bogus_mode",
        follow_redirects=True,
    )
    resp_get = flask_client.get(IslandModeResource.urls[0], follow_redirects=True)
    assert resp_post.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert resp_get.json == IslandMode.UNSET.value
