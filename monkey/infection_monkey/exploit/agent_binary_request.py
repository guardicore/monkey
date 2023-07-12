from dataclasses import dataclass
from enum import Enum
from http.server import BaseHTTPRequestHandler
from pathlib import PurePath
from typing import Optional, Sequence, TypeAlias
from uuid import UUID

from common import OperatingSystem
from common.types import Event

RequestID: TypeAlias = UUID


class RequestType(Enum):
    AGENT_BINARY = "agent_binary"
    DROPPER_SCRIPT = "dropper_script"


@dataclass(frozen=True)
class AgentBinaryRequest:
    id: RequestID
    type: RequestType
    operating_system: OperatingSystem
    destination_path: Optional[PurePath]
    args: Sequence[str]
    download_url: str
    bytes_downloaded: Event


class AgentBinaryHTTPRequestHandler(BaseHTTPRequestHandler):
    @classmethod
    def register_request(cls, request: AgentBinaryRequest):
        raise NotImplementedError()

    @classmethod
    def deregister_request(cls, request_id: RequestID):
        raise NotImplementedError()
