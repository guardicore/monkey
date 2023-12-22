from http import HTTPStatus
from unittest.mock import MagicMock
from uuid import UUID

import pytest
from tests.common import StubDIContainer

from common import AgentHeartbeat
from monkey_island.cc.event_queue import IIslandEventQueue, IslandEventTopic

AGENT_ID = UUID("7029dfac-8f87-490b-9a82-e5d005040d99")
TIMESTAMP = 123


@pytest.fixture
def mock_island_event_queue() -> IIslandEventQueue:
    return MagicMock(spec=IIslandEventQueue)


@pytest.fixture
def flask_client(build_flask_client, mock_island_event_queue):
    container = StubDIContainer()
    container.register_instance(IIslandEventQueue, mock_island_event_queue)

    with build_flask_client(container) as flask_client:
        yield flask_client


def test_agent_heartbeat_post(flask_client, mock_island_event_queue):
    heartbeat = AgentHeartbeat(timestamp=TIMESTAMP)
    resp = flask_client.post(
        f"/api/agent/{AGENT_ID}/heartbeat",
        json=heartbeat.to_json_dict(),
        follow_redirects=True,
    )

    assert resp.status_code == HTTPStatus.NO_CONTENT
    mock_island_event_queue.publish.assert_called_once_with(
        IslandEventTopic.AGENT_HEARTBEAT, agent_id=AGENT_ID, heartbeat=heartbeat
    )


@pytest.mark.parametrize("request_json", [{"???": 0}, {"timestamp": []}])
def test_agent_heartbeat_post__bad_request(flask_client, mock_island_event_queue, request_json):
    resp = flask_client.post(
        f"/api/agent/{AGENT_ID}/heartbeat", json=request_json, follow_redirects=True
    )

    assert resp.status_code == HTTPStatus.BAD_REQUEST
    mock_island_event_queue.publish.assert_not_called()
