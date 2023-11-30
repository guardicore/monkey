from typing import List

from monkeytypes import InfectionMonkeyBaseModel
from pydantic import Field


class MimikatzOptions(InfectionMonkeyBaseModel):
    excluded_username_prefixes: List[str] = Field(
        default=[],
        title="Excluded Username Prefixes",
        description="Mimikatz will not collect credentials for any user whose username"
        " starts with one of theses prefixes.",
    )
