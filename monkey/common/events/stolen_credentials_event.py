from dataclasses import dataclass
from typing import Sequence

from common.credentials import Credentials

from . import AbstractEvent


@dataclass(frozen=True)
class StolenCredentialsEvent(AbstractEvent):
    """
    An event that was initiated/observed when an agent collects credentials from the victim.

    Attributes:
        :param stolen_credentials: The credentials which were stolen by the source agent
    """

    stolen_credentials: Sequence[Credentials]
