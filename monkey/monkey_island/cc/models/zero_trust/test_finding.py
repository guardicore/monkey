import pytest
from mongoengine import ValidationError

import common.common_consts.zero_trust_consts as zero_trust_consts
from monkey_island.cc.models.zero_trust.event import Event
from monkey_island.cc.models.zero_trust.finding import Finding
from monkey_island.cc.models.zero_trust.monkey_finding_details import MonkeyFindingDetails
from monkey_island.cc.models.zero_trust.scoutsuite_finding_details import ScoutSuiteFindingDetails
from monkey_island.cc.testing.IslandTestCase import IslandTestCase


MONKEY_FINDING_DETAIL_MOCK = MonkeyFindingDetails()
MONKEY_FINDING_DETAIL_MOCK.events = ['mock1', 'mock2']
SCOUTSUITE_FINDING_DETAIL_MOCK = ScoutSuiteFindingDetails()
SCOUTSUITE_FINDING_DETAIL_MOCK.scoutsuite_rules = []


class TestFinding(IslandTestCase):

    def test_save_finding_validation(self):
        with self.assertRaises(ValidationError):
            _ = Finding.save_finding(test="bla bla",
                                     status=zero_trust_consts.STATUS_FAILED,
                                     detail_ref=MONKEY_FINDING_DETAIL_MOCK)

        with self.assertRaises(ValidationError):
            _ = Finding.save_finding(test=zero_trust_consts.TEST_SEGMENTATION,
                                     status="bla bla",
                                     detail_ref=SCOUTSUITE_FINDING_DETAIL_MOCK)

    def test_save_finding_sanity(self):
        self.assertEqual(len(Finding.objects(test=zero_trust_consts.TEST_SEGMENTATION)), 0)

        event_example = Event.create_event(
            title="Event Title", message="event message", event_type=zero_trust_consts.EVENT_TYPE_MONKEY_NETWORK)
        monkey_details_example = MonkeyFindingDetails()
        monkey_details_example.events.append(event_example)
        Finding.save_finding(test=zero_trust_consts.TEST_SEGMENTATION,
                             status=zero_trust_consts.STATUS_FAILED, detail_ref=monkey_details_example)

        self.assertEqual(len(Finding.objects(test=zero_trust_consts.TEST_SEGMENTATION)), 1)
        self.assertEqual(len(Finding.objects(status=zero_trust_consts.STATUS_FAILED)), 1)
