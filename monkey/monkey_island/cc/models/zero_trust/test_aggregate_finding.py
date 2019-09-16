from common.data.zero_trust_consts import *
from monkey_island.cc.models.zero_trust.aggregate_finding import AggregateFinding
from monkey_island.cc.models.zero_trust.event import Event
from monkey_island.cc.models.zero_trust.finding import Finding
from monkey_island.cc.testing.IslandTestCase import IslandTestCase


class TestAggregateFinding(IslandTestCase):
    def test_create_or_add_to_existing(self):
        self.fail_if_not_testing_env()
        self.clean_finding_db()

        test = TEST_MALICIOUS_ACTIVITY_TIMELINE
        status = STATUS_VERIFY
        events = [Event.create_event("t", "t", EVENT_TYPE_MONKEY_NETWORK)]
        self.assertEquals(len(Finding.objects(test=test, status=status)), 0)

        AggregateFinding.create_or_add_to_existing(test, status, events)

        self.assertEquals(len(Finding.objects(test=test, status=status)), 1)
        self.assertEquals(len(Finding.objects(test=test, status=status)[0].events), 1)

        AggregateFinding.create_or_add_to_existing(test, status, events)

        self.assertEquals(len(Finding.objects(test=test, status=status)), 1)
        self.assertEquals(len(Finding.objects(test=test, status=status)[0].events), 2)

    def test_create_or_add_to_existing_2_tests_already_exist(self):
        self.fail_if_not_testing_env()
        self.clean_finding_db()

        test = TEST_MALICIOUS_ACTIVITY_TIMELINE
        status = STATUS_VERIFY
        event = Event.create_event("t", "t", EVENT_TYPE_MONKEY_NETWORK)
        events = [event]
        self.assertEquals(len(Finding.objects(test=test, status=status)), 0)

        Finding.save_finding(test, status, events)

        self.assertEquals(len(Finding.objects(test=test, status=status)), 1)
        self.assertEquals(len(Finding.objects(test=test, status=status)[0].events), 1)

        AggregateFinding.create_or_add_to_existing(test, status, events)

        self.assertEquals(len(Finding.objects(test=test, status=status)), 1)
        self.assertEquals(len(Finding.objects(test=test, status=status)[0].events), 2)

        Finding.save_finding(test, status, events)

        self.assertEquals(len(Finding.objects(test=test, status=status)), 2)

        with self.assertRaises(AssertionError):
            AggregateFinding.create_or_add_to_existing(test, status, events)
