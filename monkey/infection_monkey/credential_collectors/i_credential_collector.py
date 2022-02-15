from abc import ABC, abstractmethod
from typing import List

from .credentials import Credentials


class ICredentialCollector(ABC):
    @abstractmethod
    def collect_credentials(self) -> List[Credentials]:
        pass
