from typing import List

from common.common_consts import zero_trust_consts
from monkey_island.cc.models.zero_trust.scoutsuite_finding import ScoutSuiteFinding
from monkey_island.cc.models.zero_trust.scoutsuite_finding_details import ScoutSuiteFindingDetails
from monkey_island.cc.models.zero_trust.scoutsuite_rule import ScoutSuiteRule
from monkey_island.cc.services.zero_trust.scoutsuite.consts.scoutsuite_finding_maps import (
    ScoutSuiteFindingMap,
)
from monkey_island.cc.services.zero_trust.scoutsuite.scoutsuite_rule_service import (
    ScoutSuiteRuleService,
)


class ScoutSuiteZTFindingService:
    @staticmethod
    def process_rule(finding: ScoutSuiteFindingMap, rule: ScoutSuiteRule):
        existing_findings = ScoutSuiteFinding.objects(test=finding.test)
        assert len(existing_findings) < 2, "More than one finding exists for {}".format(
                finding.test
        )

        if len(existing_findings) == 0:
            ScoutSuiteZTFindingService._create_new_finding_from_rule(finding, rule)
        else:
            ScoutSuiteZTFindingService.add_rule(existing_findings[0], rule)

    @staticmethod
    def _create_new_finding_from_rule(finding: ScoutSuiteFindingMap, rule: ScoutSuiteRule):
        details = ScoutSuiteFindingDetails()
        details.scoutsuite_rules = [rule]
        details.save()
        status = ScoutSuiteZTFindingService.get_finding_status_from_rules(details.scoutsuite_rules)
        ScoutSuiteFinding.save_finding(finding.test, status, details)

    @staticmethod
    def get_finding_status_from_rules(rules: List[ScoutSuiteRule]) -> str:
        if len(rules) == 0:
            return zero_trust_consts.STATUS_UNEXECUTED
        elif filter(lambda x:ScoutSuiteRuleService.is_rule_dangerous(x), rules):
            return zero_trust_consts.STATUS_FAILED
        elif filter(lambda x:ScoutSuiteRuleService.is_rule_warning(x), rules):
            return zero_trust_consts.STATUS_VERIFY
        else:
            return zero_trust_consts.STATUS_PASSED

    @staticmethod
    def add_rule(finding: ScoutSuiteFinding, rule: ScoutSuiteRule):
        ScoutSuiteZTFindingService.change_finding_status_by_rule(finding, rule)
        finding.save()
        finding.details.fetch().add_rule(rule)

    @staticmethod
    def change_finding_status_by_rule(finding: ScoutSuiteFinding, rule: ScoutSuiteRule):
        rule_status = ScoutSuiteZTFindingService.get_finding_status_from_rules([rule])
        finding_status = finding.status
        new_finding_status = ScoutSuiteZTFindingService.get_finding_status_from_rule_status(
                finding_status, rule_status
        )
        if finding_status != new_finding_status:
            finding.status = new_finding_status

    @staticmethod
    def get_finding_status_from_rule_status(finding_status: str, rule_status: str) -> str:
        if (
                finding_status == zero_trust_consts.STATUS_FAILED
                or rule_status == zero_trust_consts.STATUS_FAILED
        ):
            return zero_trust_consts.STATUS_FAILED
        elif (
                finding_status == zero_trust_consts.STATUS_VERIFY
                or rule_status == zero_trust_consts.STATUS_VERIFY
        ):
            return zero_trust_consts.STATUS_VERIFY
        elif (
                finding_status == zero_trust_consts.STATUS_PASSED
                or rule_status == zero_trust_consts.STATUS_PASSED
        ):
            return zero_trust_consts.STATUS_PASSED
        else:
            return zero_trust_consts.STATUS_UNEXECUTED
