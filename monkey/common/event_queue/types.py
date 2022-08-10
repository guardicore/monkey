from typing import Callable

from common.events import AbstractEvent

EventSubscriber = Callable[[AbstractEvent], None]
