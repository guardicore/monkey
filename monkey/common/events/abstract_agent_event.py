import time
from abc import ABC
from dataclasses import dataclass, field
from ipaddress import IPv4Address
from typing import FrozenSet, Union
from uuid import UUID, getnode


@dataclass(frozen=True)
class AbstractAgentEvent(ABC):
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

    source: UUID = field(default_factory=getnode)
    target: Union[UUID, IPv4Address, None] = field(default=None)
    timestamp: float = field(default_factory=time.time)
    tags: FrozenSet[str] = field(default_factory=frozenset)
