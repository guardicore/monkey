from abc import ABC, abstractmethod
from typing import Mapping, Optional, Sequence

from common.credentials import Credentials


class ICredentialsCollector(ABC):
    @abstractmethod
    def collect_credentials(self, options: Optional[Mapping]) -> Sequence[Credentials]:
        pass
