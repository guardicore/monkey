import pytest
from mongoengine import ValidationError

import common.common_consts.zero_trust_consts as zero_trust_consts
from monkey_island.cc.models.zero_trust.event import Event
from monkey_island.cc.models.zero_trust.finding import Finding
from monkey_island.cc.models.zero_trust.monkey_finding import MonkeyFinding
from monkey_island.cc.models.zero_trust.monkey_finding_details import MonkeyFindingDetails
from monkey_island.cc.test_common.fixtures import FixtureEnum

MONKEY_FINDING_DETAIL_MOCK = MonkeyFindingDetails()
MONKEY_FINDING_DETAIL_MOCK.events = ['mock1', 'mock2']


class TestMonkeyFinding:

    @pytest.mark.usefixtures(FixtureEnum.USES_DATABASE)
    def test_save_finding_validation(self):
        with pytest.raises(ValidationError):
            _ = MonkeyFinding.save_finding(test="bla bla",
                                           status=zero_trust_consts.STATUS_FAILED,
                                           detail_ref=MONKEY_FINDING_DETAIL_MOCK)

    @pytest.mark.usefixtures(FixtureEnum.USES_DATABASE)
    def test_save_finding_sanity(self):
        assert len(Finding.objects(test=zero_trust_consts.TEST_SEGMENTATION)) == 0

        event_example = Event.create_event(
            title="Event Title", message="event message", event_type=zero_trust_consts.EVENT_TYPE_MONKEY_NETWORK)
        monkey_details_example = MonkeyFindingDetails()
        monkey_details_example.events.append(event_example)
        monkey_details_example.save()
        MonkeyFinding.save_finding(test=zero_trust_consts.TEST_SEGMENTATION,
                                   status=zero_trust_consts.STATUS_FAILED,
                                   detail_ref=monkey_details_example)

        assert len(MonkeyFinding.objects(test=zero_trust_consts.TEST_SEGMENTATION)) == 1
        assert len(MonkeyFinding.objects(status=zero_trust_consts.STATUS_FAILED)) == 1
        assert len(Finding.objects(status=zero_trust_consts.STATUS_FAILED)) == 1
