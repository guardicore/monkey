from abc import ABC, abstractmethod

from infection_monkey.credential_collectors.credential_type import CredentialType


class ICredentialComponent(ABC):
    @property
    @abstractmethod
    def type(self) -> CredentialType:
        pass
