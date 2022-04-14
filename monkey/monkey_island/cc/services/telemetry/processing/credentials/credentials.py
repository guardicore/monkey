from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence


@dataclass(frozen=True)
class Credentials:
    identities: Sequence[Mapping]
    secrets: Sequence[Mapping]
    monkey_guid: str

    @staticmethod
    def from_mapping(cred_dict: Mapping[str, Any], monkey_guid: str) -> Credentials:
        return Credentials(
            identities=cred_dict["identities"],
            secrets=cred_dict["secrets"],
            monkey_guid=monkey_guid,
        )
