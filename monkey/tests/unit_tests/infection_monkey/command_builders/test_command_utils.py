from uuid import UUID

import pytest
from monkeytypes import AgentID

from infection_monkey.command_builders import build_monkey_commandline_parameters
from infection_monkey.utils.ids import get_agent_id


@pytest.fixture
def agent_id() -> AgentID:
    return get_agent_id()


def test_build_monkey_commandline_parameters_arguments():
    agent_id = UUID("9614480d-471b-4568-86b5-cb922a34ed8a")
    expected = [
        "-p",
        str(agent_id),
        "-s",
        "127.127.127.127:5000,138.138.138.138:5007",
        "-d",
        "0",
        "-l",
        "C:\\windows\\abc",
    ]
    actual = build_monkey_commandline_parameters(
        agent_id,
        ["127.127.127.127:5000", "138.138.138.138:5007"],
        0,
        "C:\\windows\\abc",
    )

    assert expected == actual
