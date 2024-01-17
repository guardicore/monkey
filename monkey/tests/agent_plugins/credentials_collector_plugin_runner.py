import logging
import os
import sys
from ipaddress import IPv4Address
from multiprocessing import Event
from typing import Any, Dict, List
from unittest.mock import MagicMock
from uuid import UUID

script_path = os.path.realpath(os.path.dirname(__file__))
monkey_path = os.path.realpath(os.path.join(script_path, "..", ".."))
sys.path.insert(0, monkey_path)

# Change this import to use this script with different plugins
from agent_plugins.credentials_collectors.chrome.src.plugin import Plugin  # noqa: E402
from agentpluginapi import TargetHost  # noqa: E402
from monkeytypes import OperatingSystem  # noqa: E402
from monkeytypes import Credentials, Password, Username  # noqa: E402

from common.event_queue import IAgentEventPublisher  # noqa: E402

logging.basicConfig(level=logging.DEBUG)

# Modify these variables as needed
CREDENTIALS: List[Credentials] = [
    Credentials(identity=Username(username="m0nk3y"), secret=Password(password="Ivrrw5zEzs"))
]
CREDENTIALS_COLLECTOR_OPTIONS: Dict[str, Any] = {}
TARGET_HOST = TargetHost(
    ip=IPv4Address("10.2.2.14"), operating_system=OperatingSystem.LINUX, icmp=True
)

agent_event_publisher = MagicMock(spec=IAgentEventPublisher)

# These parameters don't matter because we won't be executing the agent
servers = ["localhost"]
current_depth = -1
interrupt = Event()
agent_id = UUID("67460e74-02e3-11e8-b443-00163e990bdb")

plugin = Plugin(
    plugin_name="Test",
    agent_id=agent_id,
    agent_event_publisher=agent_event_publisher,
)

credentials = plugin.run(
    host=TARGET_HOST,
    options=CREDENTIALS_COLLECTOR_OPTIONS,
    interrupt=interrupt,
)

print(credentials)
