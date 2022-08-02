from abc import ABC
from dataclasses import dataclass
from ipaddress import IPv4Address
from typing import FrozenSet, Union
from uuid import UUID


@dataclass(frozen=True)
class AbstractEvent(ABC):
    """
    An event that was initiated or observed by an agent

    Agents perform actions and collect data. These actions and data are represented as "events".
    Subtypes of `AbstractEvent` will have additional properties that provide context and information
    about the event.

    Attributes:
        :param source: The UUID of the agent that observed the event
        :param target: The target of the event (if not the local system)
        :param timestamp: The time that the event occurred (seconds since the Unix epoch)
        :param tags: The set of tags associated with the event
    """

    source: UUID
    target: Union[UUID, IPv4Address, None]
    timestamp: float
    tags: FrozenSet[str]
