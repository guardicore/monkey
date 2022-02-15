from abc import ABC, abstractmethod
from typing import Iterable, Mapping, Optional

from .credentials import Credentials


class ICredentialCollector(ABC):
    @abstractmethod
    def collect_credentials(self, options: Optional[Mapping]) -> Iterable[Credentials]:
        pass
