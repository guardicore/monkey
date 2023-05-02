from pydantic import Field

from common.base_models import InfectionMonkeyBaseModel


class MimikatzOptions(InfectionMonkeyBaseModel):
    excluded_username_prefix: str = Field(
        default="",
        description="Mimikatz will not collect credentials for any user whose username"
        " starts with this prefix.",
    )
