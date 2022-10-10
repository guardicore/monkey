from . import AbstractAgentEvent


class AgentShutdownEvent(AbstractAgentEvent):
    """
    An event that occurs when the Agent shuts down

    Attributes:
        :param stop_time: The time that the Agent was shut down (seconds since the Unix epoch)
    """

    stop_time: float
