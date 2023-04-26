from abc import ABC, abstractmethod
from typing import Mapping, Optional, Sequence

from common.credentials import Credentials
from common.types import Event


class ICredentialsCollector(ABC):
    @abstractmethod
    def run(self, options: Optional[Mapping], interrupt: Event) -> Sequence[Credentials]:
        pass
