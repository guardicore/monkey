from abc import ABC, abstractmethod

from .credentials import Credentials


class ICredentialCollector(ABC):
    @abstractmethod
    def collect_credentials(self) -> Credentials:
        pass
