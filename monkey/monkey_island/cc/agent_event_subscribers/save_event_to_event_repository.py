import logging

from common.events import AbstractAgentEvent
from monkey_island.cc.repository import IEventRepository, StorageError

logger = logging.getLogger(__name__)


class save_event_to_event_repository:
    def __init__(self, event_repository: IEventRepository):
        self._event_repository = event_repository

    def __call__(self, event: AbstractAgentEvent):
        try:
            self._event_repository.save_event(event)
        except StorageError as err:
            logger.error(f"Error occured storing event {event}: {err}")
