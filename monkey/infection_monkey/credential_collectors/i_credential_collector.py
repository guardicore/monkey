from abc import ABC, abstractmethod
from typing import List, Mapping, Union

from .credentials import Credentials


class ICredentialCollector(ABC):
    @abstractmethod
    def collect_credentials(self, options: Union[Mapping, None]) -> List[Credentials]:
        pass
