from copy import deepcopy

from monkey_island.cc.services.zero_trust.scoutsuite.consts.rule_consts import RULE_LEVEL_WARNING, RULE_LEVEL_DANGER
from monkey_island.cc.services.zero_trust.scoutsuite.scoutsuite_rule_service import ScoutSuiteRuleService
from monkey_island.cc.services.zero_trust.test_common.scoutsuite_finding_data import RULES

example_scoutsuite_data = {
    'checked_items': 179,
    'compliance': None,
    'dashboard_name': 'Rules',
    'description': 'Security Group Opens All Ports to All',
    'flagged_items': 2,
    'items': [
        'ec2.regions.eu-central-1.vpcs.vpc-0ee259b1a13c50229.security_groups.sg-035779fe5c293fc72'
        '.rules.ingress.protocols.ALL.ports.1-65535.cidrs.2.CIDR',
        'ec2.regions.eu-central-1.vpcs.vpc-00015526b6695f9aa.security_groups.sg-019eb67135ec81e65'
        '.rules.ingress.protocols.ALL.ports.1-65535.cidrs.0.CIDR'
    ],
    'level': 'danger',
    'path': 'ec2.regions.id.vpcs.id.security_groups.id.rules.id.protocols.id.ports.id.cidrs.id.CIDR',
    'rationale': 'It was detected that all ports in the security group are open, and any source IP address'
                 ' could send traffic to these ports, which creates a wider attack surface for resources '
                 'assigned to it. Open ports should be reduced to the minimum needed to correctly',
    'references': [],
    'remediation': None,
    'service': 'EC2'
}


def test_get_rule_from_rule_data():
    assert ScoutSuiteRuleService.get_rule_from_rule_data(example_scoutsuite_data) == RULES[0]


def test_is_rule_dangerous():
    test_rule = deepcopy(RULES[0])
    assert ScoutSuiteRuleService.is_rule_dangerous(test_rule)

    test_rule.level = RULE_LEVEL_WARNING
    assert not ScoutSuiteRuleService.is_rule_dangerous(test_rule)

    test_rule.level = RULE_LEVEL_DANGER
    test_rule.items = []
    assert not ScoutSuiteRuleService.is_rule_dangerous(test_rule)


def test_is_rule_warning():
    test_rule = deepcopy(RULES[0])
    assert not ScoutSuiteRuleService.is_rule_warning(test_rule)

    test_rule.level = RULE_LEVEL_WARNING
    assert ScoutSuiteRuleService.is_rule_warning(test_rule)

    test_rule.items = []
    assert not ScoutSuiteRuleService.is_rule_warning(test_rule)
