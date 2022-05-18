from abc import ABC
from typing import Any, Mapping, Sequence


class IConfigRepository(ABC):

    # Config
    ###############################################

    # This returns the current config
    # TODO investigate if encryption should be here or where
    # TODO potentially should be a DTO as well, but it's structure is defined in schema already
    def get_config(self) -> Mapping:
        pass

    def set_config(self, config: dict):
        pass

    # Used when only a subset of config is submitted, for example only PBAFiles
    # Used by passing keys, like ['monkey', 'post_breach_actions', 'linux_filename']
    # Using a list is less ambiguous IMO, than using . notation
    def set_config_field(self, key_list: Sequence[str], value: Any):
        pass

    # Used when only a subset of config is needed, for example only PBAFiles
    # Used by passing keys, like ['monkey', 'post_breach_actions', 'linux_filename']
    # Using a list is less ambiguous IMO, than using . notation
    # TODO Still in doubt about encryption, this should probably be determined automatically
    def get_config_field(self, key_list: Sequence[str]) -> Any:
        pass
