from abc import ABC, abstractmethod

from . import CredentialComponentType


class ICredentialComponent(ABC):
    @property
    @abstractmethod
    def credential_type(self) -> CredentialComponentType:
        pass
