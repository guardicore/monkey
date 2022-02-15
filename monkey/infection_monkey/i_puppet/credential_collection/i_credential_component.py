from abc import ABC, abstractmethod

from .credential_type import CredentialType


class ICredentialComponent(ABC):
    @property
    @abstractmethod
    def credential_type(self) -> CredentialType:
        pass
