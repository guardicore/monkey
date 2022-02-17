from abc import ABC, abstractmethod

from common.common_consts.credentials_type import CredentialsType


class ICredentialComponent(ABC):
    @property
    @abstractmethod
    def credential_type(self) -> CredentialsType:
        pass
