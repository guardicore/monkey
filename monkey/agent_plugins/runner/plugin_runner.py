from io import BytesIO
from ipaddress import IPv4Address
from multiprocessing import Event
from typing import Any, Dict
from unittest.mock import MagicMock
from uuid import UUID

from agent_plugins.exploiters.hadoop.src.plugin import Plugin
from tests.monkey_island import InMemoryFileRepository

from common import OperatingSystem
from common.event_queue import IAgentEventPublisher
from infection_monkey.model import TargetHost
from monkey_island.cc.repositories import AgentBinaryRepository
from monkey_island.cc.repositories.agent_binary_repository import (
    LINUX_AGENT_FILE_NAME,
    WINDOWS_AGENT_FILE_NAME,
)

host = TargetHost(ip=IPv4Address("10.2.2.2"), operating_system=OperatingSystem.LINUX, icmp=True)
options: Dict[str, Any] = {}
_file_repo = InMemoryFileRepository()
_file_repo.save_file(LINUX_AGENT_FILE_NAME, BytesIO(b"plugin works linux"))
_file_repo.save_file(WINDOWS_AGENT_FILE_NAME, BytesIO(b"plugin works windows"))
agent_binary_repository = AgentBinaryRepository(_file_repo)
# These parameters don't matter because we won't be executing the agent
servers = ["localhost"]
current_depth = -1
interrupt = Event()
agent_id = UUID("67460e74-02e3-11e8-b443-00163e990bdb")
agent_event_publisher = MagicMock(spec=IAgentEventPublisher)

Plugin().run(
    host=host,
    options={},
    agent_binary_repository=agent_binary_repository,
    servers=servers,
    current_depth=current_depth,
    interrupt=interrupt,
    agent_id=agent_id,
    agent_event_publisher=agent_event_publisher,
)
