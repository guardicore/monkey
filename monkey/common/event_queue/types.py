from typing import Callable

from common.agent_events import AbstractAgentEvent

AgentEventSubscriber = Callable[[AbstractAgentEvent], None]
