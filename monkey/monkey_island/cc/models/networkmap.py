from dataclasses import dataclass
from typing import Mapping, Sequence

from monkey_island.cc.models import Machine


@dataclass
class Arc:
    dst_machine: Machine  # noqa: F821
    status: str


# This is the most concise way to represent a graph:
# Machine id as key, Arch list as a value
# Not sure how compatible this will be with ORM objects though,
# might require more complex casting logic
@dataclass
class NetworkMap:
    nodes: Mapping[str, Sequence[Arc]]  # noqa: F821
