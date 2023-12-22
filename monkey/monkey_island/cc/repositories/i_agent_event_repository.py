from abc import ABC, abstractmethod
from typing import Sequence, Type, TypeVar

from monkeyevents import AbstractAgentEvent
from monkeytypes import AgentID

T = TypeVar("T", bound=AbstractAgentEvent)


class IAgentEventRepository(ABC):
    """A repository used to store and retrieve event objects"""

    @abstractmethod
    def save_event(self, event: AbstractAgentEvent):
        """
        Save an event to the repository

        :param event: The event to store in the repository
        :raises StorageError: If an error occurred while attempting to save an event
        """

    @abstractmethod
    def get_events(self) -> Sequence[AbstractAgentEvent]:
        """
        Retrieve all events stored in the repository

        :return: All stored events sorted ascending by timestamp
        :raises RetrievalError: If an error occurred while attempting to retrieve the events
        """

    @abstractmethod
    def get_events_by_type(self, event_type: Type[T]) -> Sequence[T]:
        """
        Retrieve all events with same type

        :param event_type: Type of event
        :return: Stored events that have same type, sorted ascending by timestamp
        :raises RetrievalError: If an error occurred while attempting to retrieve the event
        """

    @abstractmethod
    def get_events_by_tag(self, tag: str) -> Sequence[AbstractAgentEvent]:
        """
        Retrieve all events with same tag

        :param tag: Tag of event
        :return: Stored events that have same tag, sorted ascending by timestamp
        :raises RetrievalError: If an error occurred while attempting to retrieve the event
        """

    @abstractmethod
    def get_events_by_source(self, source: AgentID) -> Sequence[AbstractAgentEvent]:
        """
        Retrieve all events from the same source

        :param source: The ID of the agent that observed the events
        :return: Stored events that have same source, sorted ascending by timestamp
        :raises RetrievalError: If an error occurred while attempting to retrieve the event
        """

    @abstractmethod
    def reset(self):
        """
        Remove all data from the repository

        :raises RemovalError: If an error occurred while attempting to remove all events from the
                              repository
        """
