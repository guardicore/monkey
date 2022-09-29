from unittest.mock import MagicMock

import pytest

from common.event_queue import IAgentEventQueue


@pytest.fixture
def mock_agent_event_queue() -> IAgentEventQueue:
    return MagicMock(spec=IAgentEventQueue)
