from abc import ABC, abstractmethod
from typing import Type, Union

from common.agent_event_serializers import IAgentEventSerializer
from common.agent_events import AbstractAgentEvent


class IAgentEventSerializerRegistry(ABC):
    @abstractmethod
    def __setitem__(
        self, event_class: Type[AbstractAgentEvent], event_serializer: IAgentEventSerializer
    ):
        pass

    @abstractmethod
    def __getitem__(
        self, event_class: Union[str, Type[AbstractAgentEvent]]
    ) -> IAgentEventSerializer:
        pass
