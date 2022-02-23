from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class Credentials:
    identities: Sequence[dict]
    secrets: Sequence[dict]

    @staticmethod
    def from_dict(cred_dict: dict) -> Credentials:
        return Credentials(identities=cred_dict["identities"], secrets=cred_dict["secrets"])
