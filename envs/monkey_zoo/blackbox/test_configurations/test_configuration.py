from dataclasses import dataclass
from typing import Tuple

from common.configuration import AgentConfiguration
from common.credentials import Credentials


@dataclass
class TestConfiguration:
    agent_configuration: AgentConfiguration
    propagation_credentials: Tuple[Credentials, ...]
