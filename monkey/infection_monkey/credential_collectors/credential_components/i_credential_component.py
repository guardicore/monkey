from abc import ABC
from dataclasses import dataclass

from ..credential_types import CredentialTypes


@dataclass
class ICredentialComponent(ABC):
    type: CredentialTypes
    content: dict
