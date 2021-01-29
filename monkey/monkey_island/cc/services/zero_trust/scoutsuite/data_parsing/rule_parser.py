import dpath.util

from common.utils.exceptions import RulePathCreatorNotFound
from monkey_island.cc.services.zero_trust.scoutsuite.data_parsing.rule_path_building.rule_path_creators_list import \
    RULE_PATH_CREATORS_LIST


class RuleParser:

    @staticmethod
    def get_rule_data(scoutsuite_data, rule_name):
        rule_path = RuleParser.get_rule_path(rule_name)
        return dpath.util.get(scoutsuite_data, rule_path)

    @staticmethod
    def get_rule_path(rule_name):
        creator = RuleParser.get_rule_path_creator(rule_name)
        return creator.build_rule_path(rule_name)

    @staticmethod
    def get_rule_path_creator(rule_name):
        for rule_path_creator in RULE_PATH_CREATORS_LIST:
            if rule_name in rule_path_creator.supported_rules:
                return rule_path_creator
        raise RulePathCreatorNotFound(f"Rule path creator not found for rule {rule_name.value}. Make sure to assign"
                                      f"this rule to any rule path creators.")
