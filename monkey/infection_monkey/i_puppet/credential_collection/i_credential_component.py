from abc import ABC, abstractmethod

from common.common_consts.credential_component_type import CredentialComponentType


class ICredentialComponent(ABC):
    @property
    @abstractmethod
    def credential_type(self) -> CredentialComponentType:
        pass
