from http import HTTPStatus
from unittest.mock import MagicMock

import pytest
from tests.common import StubDIContainer

from monkey_island.cc.event_queue import IIslandEventQueue, IslandEventTopic
from monkey_island.cc.resources import ResetAgentConfiguration


@pytest.fixture
def mock_island_event_queue() -> IIslandEventQueue:
    return MagicMock(spec=IIslandEventQueue)


@pytest.fixture
def flask_client(build_flask_client, mock_island_event_queue):
    container = StubDIContainer()
    container.register_instance(IIslandEventQueue, mock_island_event_queue)

    with build_flask_client(container) as flask_client:
        yield flask_client


def test_reset_agent_configuration(flask_client, mock_island_event_queue):
    resp = flask_client.post(ResetAgentConfiguration.urls[0], follow_redirects=True)

    assert resp.status_code == HTTPStatus.OK
    mock_island_event_queue.publish.assert_called_once_with(
        IslandEventTopic.RESET_AGENT_CONFIGURATION
    )
