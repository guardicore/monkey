import pytest
from mongoengine import ValidationError

import common.common_consts.zero_trust_consts as zero_trust_consts
from monkey_island.cc.models.zero_trust.finding import Finding
from monkey_island.cc.models.zero_trust.monkey_finding_details import MonkeyFindingDetails
from monkey_island.cc.models.zero_trust.scoutsuite_finding import ScoutSuiteFinding
from monkey_island.cc.models.zero_trust.scoutsuite_finding_details import ScoutSuiteFindingDetails
from monkey_island.cc.services.zero_trust.test_common.scoutsuite_finding_data import RULES
from monkey_island.cc.test_common.fixtures import FixtureEnum

MONKEY_FINDING_DETAIL_MOCK = MonkeyFindingDetails()
MONKEY_FINDING_DETAIL_MOCK.events = ['mock1', 'mock2']
SCOUTSUITE_FINDING_DETAIL_MOCK = ScoutSuiteFindingDetails()
SCOUTSUITE_FINDING_DETAIL_MOCK.scoutsuite_rules = []


class TestScoutSuiteFinding:

    @pytest.mark.usefixtures(FixtureEnum.USES_DATABASE)
    def test_save_finding_validation(self):
        with pytest.raises(ValidationError):
            _ = ScoutSuiteFinding.save_finding(test=zero_trust_consts.TEST_SEGMENTATION,
                                               status="bla bla",
                                               detail_ref=SCOUTSUITE_FINDING_DETAIL_MOCK)

    @pytest.mark.usefixtures(FixtureEnum.USES_DATABASE)
    def test_save_finding_sanity(self):
        assert len(Finding.objects(test=zero_trust_consts.TEST_SEGMENTATION)) == 0

        rule_example = RULES[0]
        scoutsuite_details_example = ScoutSuiteFindingDetails()
        scoutsuite_details_example.scoutsuite_rules.append(rule_example)
        scoutsuite_details_example.save()
        ScoutSuiteFinding.save_finding(test=zero_trust_consts.TEST_SEGMENTATION,
                                       status=zero_trust_consts.STATUS_FAILED,
                                       detail_ref=scoutsuite_details_example)

        assert len(ScoutSuiteFinding.objects(test=zero_trust_consts.TEST_SEGMENTATION)) == 1
        assert len(ScoutSuiteFinding.objects(status=zero_trust_consts.STATUS_FAILED)) == 1
        assert len(Finding.objects(status=zero_trust_consts.STATUS_FAILED)) == 1
