from typing import Callable

from common.events import AbstractAgentEvent

EventSubscriber = Callable[[AbstractAgentEvent], None]
