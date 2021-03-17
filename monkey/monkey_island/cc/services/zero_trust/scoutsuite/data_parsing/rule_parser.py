from enum import Enum

from common.utils.code_utils import get_value_from_dict
from common.utils.exceptions import RulePathCreatorNotFound
from monkey_island.cc.services.zero_trust.scoutsuite.data_parsing.rule_path_building.rule_path_creators_list import \
    RULE_PATH_CREATORS_LIST


def __build_rule_to_rule_path_creator_hashmap():
    hashmap = {}
    for rule_path_creator in RULE_PATH_CREATORS_LIST:
        for rule_name in rule_path_creator.supported_rules:
            hashmap[rule_name] = rule_path_creator
    return hashmap


RULE_TO_RULE_PATH_CREATOR_HASHMAP = __build_rule_to_rule_path_creator_hashmap()


class RuleParser:

    @staticmethod
    def get_rule_data(scoutsuite_data: dict, rule_name: Enum) -> dict:
        rule_path = RuleParser._get_rule_path(rule_name)
        return get_value_from_dict(scoutsuite_data, rule_path)

    @staticmethod
    def _get_rule_path(rule_name: Enum):
        creator = RuleParser._get_rule_path_creator(rule_name)
        return creator.build_rule_path(rule_name)

    @staticmethod
    def _get_rule_path_creator(rule_name: Enum):
        try:
            return RULE_TO_RULE_PATH_CREATOR_HASHMAP[rule_name]
        except KeyError:
            raise RulePathCreatorNotFound(f"Rule path creator not found for rule {rule_name.value}. Make sure to assign"
                                          f"this rule to any rule path creators.")
