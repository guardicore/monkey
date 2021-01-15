from ..abstract_rule_path_creator import AbstractRulePathCreator
from ....consts.rule_names.config_rules import ConfigRules
from ....consts.service_consts import SERVICE_TYPES


class ConfigRulePathCreator(AbstractRulePathCreator):

    service_type = SERVICE_TYPES.CONFIG
    supported_rules = ConfigRules
