from abc import ABC
from dataclasses import dataclass

from ..credential_type import CredentialType


@dataclass
class ICredentialComponent(ABC):
    type: CredentialType
