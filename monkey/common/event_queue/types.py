from typing import Callable

from monkeyevents import AbstractAgentEvent

AgentEventSubscriber = Callable[[AbstractAgentEvent], None]
