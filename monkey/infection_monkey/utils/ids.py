from uuid import getnode, uuid4

from common.types import AgentID, HardwareID


def get_agent_id() -> AgentID:
    """
    Generate an agent ID

    Subsequent calls to this function will return a different ID.
    """
    return uuid4()


def get_machine_id() -> HardwareID:
    """Get an integer that uniquely defines the machine the agent is running on"""
    return getnode()
