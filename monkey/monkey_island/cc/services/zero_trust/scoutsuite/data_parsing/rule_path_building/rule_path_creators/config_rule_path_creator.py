from monkey_island.cc.services.zero_trust.scoutsuite.consts.rule_names.config_rules import \
    ConfigRules
from monkey_island.cc.services.zero_trust.scoutsuite.consts.service_consts import \
    SERVICE_TYPES
from monkey_island.cc.services.zero_trust.scoutsuite.data_parsing.rule_path_building.abstract_rule_path_creator import \
    AbstractRulePathCreator


class ConfigRulePathCreator(AbstractRulePathCreator):

    service_type = SERVICE_TYPES.CONFIG
    supported_rules = ConfigRules
