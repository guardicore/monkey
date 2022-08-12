from dataclasses import dataclass
from typing import Sequence

from common.credentials import Credentials

from . import AbstractEvent


@dataclass(frozen=True)
class CredentialsStolenEvent(AbstractEvent):
    """
    An event that occurs when an agent collects credentials from the victim

    Attributes:
        :param stolen_credentials: The credentials which were stolen by the source agent
    """

    stolen_credentials: Sequence[Credentials]
