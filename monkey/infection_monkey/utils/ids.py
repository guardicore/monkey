from uuid import UUID, getnode, uuid4

from common.types import HardwareID

_id = None


def get_agent_id() -> UUID:
    """
    Get the agent ID for the current running agent

    Each time an agent process starts, the return value of this function will be unique. Subsequent
    calls to this function from within the same process will have the same return value.
    """
    global _id
    if _id is None:
        _id = uuid4()

    return _id


def get_machine_id() -> HardwareID:
    """Get an integer that uniquely defines the machine the agent is running on"""
    return getnode()
