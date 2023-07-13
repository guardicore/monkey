from dataclasses import dataclass
from typing import Callable, TypeAlias
from uuid import UUID

from common import OperatingSystem
from common.types import Event

RequestID: TypeAlias = UUID
AgentBinaryTransform: TypeAlias = Callable[[bytes], bytes]


@dataclass(frozen=True)
class AgentBinaryDownloadReservation:
    id: RequestID
    operating_system: OperatingSystem
    transform: AgentBinaryTransform
    download_url: str
    download_completed: Event


@dataclass(frozen=True)
class AgentBinaryDownloadTicket:
    id: RequestID
    download_url: str
    download_completed: Event
