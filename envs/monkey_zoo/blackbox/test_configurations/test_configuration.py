from dataclasses import dataclass
from typing import Tuple

from common.agent_configuration import AgentConfiguration
from common.credentials import Credentials


@dataclass
class TestConfiguration:
    agent_configuration: AgentConfiguration
    propagation_credentials: Tuple[Credentials, ...]
