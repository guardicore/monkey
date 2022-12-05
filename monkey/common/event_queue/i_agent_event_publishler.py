from abc import ABC, abstractmethod

from common.agent_events import AbstractAgentEvent


class IAgentEventPublisher(ABC):
    """
    Manages publishing of events from Agent's Plugins
    """

    @abstractmethod
    def publish(self, event: AbstractAgentEvent):
        """
        Publishes an event with the given data

        :param event: Event to publish
        """
