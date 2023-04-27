from pydantic import Field

from common.base_models import InfectionMonkeyBaseModel


class MimikatzOptions(InfectionMonkeyBaseModel):
    excluded_username_prefix: str = Field(
        default="somenewuser",
        description="A username prefix for which Mimikatz will not collect credentials.",
    )
