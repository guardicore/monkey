from abc import ABC, abstractmethod
from typing import Any


class ISecretVariable(ABC):
    @abstractmethod
    def get_secret_value(self) -> Any:
        pass
