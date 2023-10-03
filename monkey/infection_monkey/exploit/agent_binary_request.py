from dataclasses import dataclass
from typing import Callable, TypeAlias
from uuid import UUID

from monkeytypes import OperatingSystem

from common.types import Event

ReservationID: TypeAlias = UUID
AgentBinaryTransform: TypeAlias = Callable[[bytes], bytes]


@dataclass(frozen=True)
class AgentBinaryDownloadReservation:
    id: ReservationID
    operating_system: OperatingSystem
    transform_agent_binary: AgentBinaryTransform
    download_url: str
    download_completed: Event


@dataclass(frozen=True)
class AgentBinaryDownloadTicket:
    id: ReservationID
    download_url: str
    download_completed: Event
