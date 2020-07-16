import unittest

import mongomock
from packaging import version

import common.data.zero_trust_consts as zero_trust_consts
from monkey_island.cc.models.zero_trust.aggregate_finding import \
    AggregateFinding
from monkey_island.cc.models.zero_trust.event import Event
from monkey_island.cc.models.zero_trust.finding import Finding
from monkey_island.cc.testing.IslandTestCase import IslandTestCase


class TestAggregateFinding(IslandTestCase):

    @unittest.skipIf(version.parse(mongomock.__version__) <= version.parse("3.19.0"),
                     "mongomock version doesn't support this test")
    def test_create_or_add_to_existing(self):
        self.fail_if_not_testing_env()
        self.clean_finding_db()

        test = zero_trust_consts.TEST_MALICIOUS_ACTIVITY_TIMELINE
        status = zero_trust_consts.STATUS_VERIFY
        events = [Event.create_event("t", "t", zero_trust_consts.EVENT_TYPE_MONKEY_NETWORK)]
        self.assertEqual(len(Finding.objects(test=test, status=status)), 0)

        AggregateFinding.create_or_add_to_existing(test, status, events)

        self.assertEqual(len(Finding.objects(test=test, status=status)), 1)
        self.assertEqual(len(Finding.objects(test=test, status=status)[0].events), 1)

        AggregateFinding.create_or_add_to_existing(test, status, events)

        self.assertEqual(len(Finding.objects(test=test, status=status)), 1)
        self.assertEqual(len(Finding.objects(test=test, status=status)[0].events), 2)

    @unittest.skipIf(version.parse(mongomock.__version__) <= version.parse("3.19.0"),
                     "mongomock version doesn't support this test")
    def test_create_or_add_to_existing_2_tests_already_exist(self):
        self.fail_if_not_testing_env()
        self.clean_finding_db()

        test = zero_trust_consts.TEST_MALICIOUS_ACTIVITY_TIMELINE
        status = zero_trust_consts.STATUS_VERIFY
        event = Event.create_event("t", "t", zero_trust_consts.EVENT_TYPE_MONKEY_NETWORK)
        events = [event]
        self.assertEqual(len(Finding.objects(test=test, status=status)), 0)

        Finding.save_finding(test, status, events)

        self.assertEqual(len(Finding.objects(test=test, status=status)), 1)
        self.assertEqual(len(Finding.objects(test=test, status=status)[0].events), 1)

        AggregateFinding.create_or_add_to_existing(test, status, events)

        self.assertEqual(len(Finding.objects(test=test, status=status)), 1)
        self.assertEqual(len(Finding.objects(test=test, status=status)[0].events), 2)

        Finding.save_finding(test, status, events)

        self.assertEqual(len(Finding.objects(test=test, status=status)), 2)

        with self.assertRaises(AssertionError):
            AggregateFinding.create_or_add_to_existing(test, status, events)
