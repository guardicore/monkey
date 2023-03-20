from abc import ABC, abstractmethod


class ISecretVariable(ABC):
    @abstractmethod
    def get_secret_value(self) -> str:
        pass
