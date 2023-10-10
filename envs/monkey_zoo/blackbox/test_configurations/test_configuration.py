from dataclasses import dataclass
from typing import Tuple

from monkeytypes import Credentials

from common.agent_configuration import AgentConfiguration


@dataclass
class TestConfiguration:
    __test__ = False
    agent_configuration: AgentConfiguration
    propagation_credentials: Tuple[Credentials, ...]
