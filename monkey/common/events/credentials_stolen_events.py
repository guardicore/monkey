from dataclasses import dataclass
from typing import Sequence

from common.credentials import Credentials

from . import AbstractEvent


@dataclass(frozen=True)
class CredentialsStolenEvent(AbstractEvent):
    """
    An event that occurs when an agent collects credentials from the victim

    Attributes:
        :param stolen_credentials: The credentials that were stolen by an agent
    """

    stolen_credentials: Sequence[Credentials]
