from abc import ABC, abstractmethod

from pydantic.dataclasses import dataclass

from . import CredentialComponentType


@dataclass
class ICredentialComponent(ABC):
    @property
    @abstractmethod
    def credential_type(self) -> CredentialComponentType:
        pass
