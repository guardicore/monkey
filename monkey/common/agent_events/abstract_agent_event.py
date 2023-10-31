import time
from abc import ABC
from ipaddress import IPv4Address
from typing import Annotated, FrozenSet, Union

from monkeytypes import InfectionMonkeyBaseModel, MachineID
from pydantic import Field, StringConstraints

from common.types import AgentID

EVENT_TAG_REGEX = r"^[a-zA-Z0-9._-]+$"


AgentEventTag = Annotated[str, StringConstraints(pattern=EVENT_TAG_REGEX)]


class AbstractAgentEvent(InfectionMonkeyBaseModel, ABC):
    """
    An event that was initiated or observed by an agent

    Agents perform actions and collect data. These actions and data are represented as "events".
    Subtypes of `AbstractAgentEvent` will have additional properties that provide context and
    information about the event.

    Attributes:
        :param source: The UUID of the agent that observed the event
        :param target: The target of the event (if not the local system)
        :param timestamp: The time that the event occurred (seconds since the Unix epoch)
        :param tags: The set of tags associated with the event
    """

    source: AgentID
    target: Union[MachineID, IPv4Address, None] = Field(default=None)
    timestamp: float = Field(default_factory=time.time)
    tags: FrozenSet[AgentEventTag] = Field(default_factory=frozenset)

    def __hash__(self):
        return hash((type(self), *tuple(self.__dict__.values())))
