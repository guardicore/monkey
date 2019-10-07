from monkey_island.cc.services.config import ConfigService


def get_config_network_segments_as_subnet_groups():
    return [ConfigService.get_config_value(['basic_network', 'network_analysis', 'inaccessible_subnets'])]
