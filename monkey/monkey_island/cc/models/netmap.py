from dataclasses import dataclass
from typing import Mapping, Sequence


# This is the most concise way to represent a graph:
# Machine id as key, Arch list as a value
# Not sure how compatible this will be with ORM objects though,
# might require more complex casting logic
@dataclass
class Netmap:
    nodes: Mapping[str, Sequence[Arch]]


@dataclass
class Arch:
    dst_machine: Machine
    status: str
