from unittest.mock import MagicMock
from uuid import UUID

import pytest
from agentpluginapi import IAgentOTPProvider

from common.command_builder import AgentCommandBuilderFactory, IAgentCommandBuilderFactory

AGENT_ID = UUID("655fd01c-5eec-4e42-b6e3-1fb738c2978d")
SERVERS = ["1.1.1.1:5000", "10.10.10.10:1234", "127.0.0.1"]
OTP = "12345"
AGENT_OTP_ENVIRONMENT_VARIABLE = "AGENT_OTP"
DEPTH = 2


@pytest.fixture
def agent_command_builder_factory() -> IAgentCommandBuilderFactory:
    mock_otp_provider = MagicMock(spec=IAgentOTPProvider)
    mock_otp_provider.get_otp.return_value = OTP
    return AgentCommandBuilderFactory(
        AGENT_ID, SERVERS, mock_otp_provider, AGENT_OTP_ENVIRONMENT_VARIABLE, DEPTH
    )
