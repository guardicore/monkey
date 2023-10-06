from uuid import uuid4

from monkeytypes import AgentID, HardwareID

from common.utils.environment import get_hardware_id


def get_agent_id() -> AgentID:
    """
    Generate an agent ID

    Subsequent calls to this function will return a different ID.
    """
    return uuid4()


def get_machine_id() -> HardwareID:
    """Get an integer that uniquely defines the machine the agent is running on"""
    return get_hardware_id()
