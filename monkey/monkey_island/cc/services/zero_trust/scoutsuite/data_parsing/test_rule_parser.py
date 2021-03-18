from enum import Enum

import pytest

from common.utils.exceptions import RulePathCreatorNotFound
from monkey_island.cc.services.zero_trust.scoutsuite.consts.rule_names.ec2_rules import EC2Rules
from monkey_island.cc.services.zero_trust.scoutsuite.consts.service_consts import SERVICES
from monkey_island.cc.services.zero_trust.scoutsuite.data_parsing.rule_parser import RuleParser
from monkey_island.cc.services.zero_trust.test_common.raw_scoutsute_data import RAW_SCOUTSUITE_DATA


class ExampleRules(Enum):
    NON_EXSISTENT_RULE = 'bogus_rule'


ALL_PORTS_OPEN = EC2Rules.SECURITY_GROUP_ALL_PORTS_TO_ALL

EXPECTED_RESULT = {'description': 'Security Group Opens All Ports to All',
                   'path': 'ec2.regions.id.vpcs.id.security_groups.id.rules.id.protocols.id.ports.id.cidrs.id.CIDR',
                   'level': 'danger',
                   'display_path': 'ec2.regions.id.vpcs.id.security_groups.id',
                   'items': [
                       'ec2.regions.ap-northeast-1.vpcs.vpc-abc.security_groups.'
                       'sg-abc.rules.ingress.protocols.ALL.ports.1-65535.cidrs.0.CIDR'],
                   'dashboard_name': 'Rules', 'checked_items': 179, 'flagged_items': 2, 'service': 'EC2',
                   'rationale': 'It was detected that all ports in the security group are open <...>',
                   'remediation': None, 'compliance': None, 'references': None}


def test_get_rule_data():
    # Test proper parsing of the raw data to rule
    results = RuleParser.get_rule_data(RAW_SCOUTSUITE_DATA[SERVICES], ALL_PORTS_OPEN)
    assert results == EXPECTED_RESULT

    with pytest.raises(RulePathCreatorNotFound):
        RuleParser.get_rule_data(RAW_SCOUTSUITE_DATA[SERVICES], ExampleRules.NON_EXSISTENT_RULE)
    pass
