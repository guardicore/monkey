from monkey_island.cc.services.config import ConfigService
from common.config_value_paths import INACCESSIBLE_SUBNETS_PATH


def get_config_network_segments_as_subnet_groups():
    return [ConfigService.get_config_value(INACCESSIBLE_SUBNETS_PATH)]
