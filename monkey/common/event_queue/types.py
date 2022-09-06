from typing import Callable

from common.events import AbstractAgentEvent

AgentEventSubscriber = Callable[[AbstractAgentEvent], None]
