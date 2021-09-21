from abc import ABC, abstractmethod
from typing import Any


class FieldTypeABC(ABC):
    @staticmethod
    @abstractmethod
    def encrypt(value: Any):
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def decrypt(value: Any):
        raise NotImplementedError()
