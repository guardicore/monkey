import pytest

from common.common_consts import zero_trust_consts
from monkey_island.cc.models.zero_trust.finding import Finding
from monkey_island.cc.services.zero_trust.scoutsuite.scoutsuite_zt_finding_service import ScoutSuiteZTFindingService
from monkey_island.cc.services.zero_trust.test_common.scoutsuite_finding_data import RULES, SCOUTSUITE_FINDINGS
from monkey_island.cc.test_common.fixtures import FixtureEnum


class TestScoutSuiteZTFindingService:

    @pytest.mark.usefixtures(FixtureEnum.USES_DATABASE)
    def test_process_rule(self):
        # Creates new PermissiveFirewallRules finding with a rule
        ScoutSuiteZTFindingService.process_rule(SCOUTSUITE_FINDINGS[0], RULES[0])
        findings = list(Finding.objects())
        assert len(findings) == 1
        assert findings[0].finding_type == zero_trust_consts.SCOUTSUITE_FINDING
        # Assert that details were created properly
        details = findings[0].details.fetch()
        assert len(details.scoutsuite_rules) == 1
        assert details.scoutsuite_rules[0] == RULES[0]

        # Rule processing should add rule to an already existing finding
        ScoutSuiteZTFindingService.process_rule(SCOUTSUITE_FINDINGS[0], RULES[1])
        findings = list(Finding.objects())
        assert len(findings) == 1
        assert findings[0].finding_type == zero_trust_consts.SCOUTSUITE_FINDING
        # Assert that details were created properly
        details = findings[0].details.fetch()
        assert len(details.scoutsuite_rules) == 2
        assert details.scoutsuite_rules[1] == RULES[1]

        # New finding created
        ScoutSuiteZTFindingService.process_rule(SCOUTSUITE_FINDINGS[1], RULES[1])
        findings = list(Finding.objects())
        assert len(findings) == 2
        assert findings[1].finding_type == zero_trust_consts.SCOUTSUITE_FINDING
        # Assert that details were created properly
        details = findings[1].details.fetch()
        assert len(details.scoutsuite_rules) == 1
        assert details.scoutsuite_rules[0] == RULES[1]
