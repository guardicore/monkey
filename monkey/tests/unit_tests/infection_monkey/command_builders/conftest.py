from typing import Sequence
from unittest.mock import MagicMock
from uuid import UUID

import pytest
from agentpluginapi import IAgentCommandBuilderFactory, IAgentOTPProvider
from monkeytypes import AgentID

from infection_monkey.command_builders import AgentCommandBuilderFactory


@pytest.fixture
def agent_id() -> AgentID:
    return UUID("655fd01c-5eec-4e42-b6e3-1fb738c2978d")


@pytest.fixture
def servers() -> Sequence[str]:
    return ["1.1.1.1:5000", "10.10.10.10:1234", "127.0.0.1"]


@pytest.fixture
def otp() -> str:
    return "12345"


@pytest.fixture
def agent_otp_environment_variable() -> str:
    return "AGENT_OTP"


@pytest.fixture
def agent_command_builder_factory(
    agent_id: AgentID, servers: Sequence[str], otp: str, agent_otp_environment_variable: str
) -> IAgentCommandBuilderFactory:
    mock_otp_provider = MagicMock(spec=IAgentOTPProvider)
    mock_otp_provider.get_otp.return_value = otp
    return AgentCommandBuilderFactory(
        agent_id, servers, mock_otp_provider, agent_otp_environment_variable, 2
    )
