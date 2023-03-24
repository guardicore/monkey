from abc import ABC, abstractmethod

from . import IRemoteAccessClient


class IRemoteAccessClientFactory(ABC):
    @abstractmethod
    def create(self, **kwargs) -> IRemoteAccessClient:
        pass
