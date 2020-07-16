from mongoengine import ValidationError

import common.data.zero_trust_consts as zero_trust_consts
from monkey_island.cc.models.zero_trust.event import Event
from monkey_island.cc.models.zero_trust.finding import Finding
from monkey_island.cc.testing.IslandTestCase import IslandTestCase


class TestFinding(IslandTestCase):
    """
    Make sure to set server environment to `testing` in server.json! Otherwise this will mess up your mongo instance and
    won't work.

    Also, the working directory needs to be the working directory from which you usually run the island so the
    server.json file is found and loaded.
    """

    def test_save_finding_validation(self):
        self.fail_if_not_testing_env()
        self.clean_finding_db()

        with self.assertRaises(ValidationError):
            _ = Finding.save_finding(test="bla bla", status=zero_trust_consts.STATUS_FAILED, events=[])

        with self.assertRaises(ValidationError):
            _ = Finding.save_finding(test=zero_trust_consts.TEST_SEGMENTATION, status="bla bla", events=[])

    def test_save_finding_sanity(self):
        self.fail_if_not_testing_env()
        self.clean_finding_db()

        self.assertEqual(len(Finding.objects(test=zero_trust_consts.TEST_SEGMENTATION)), 0)

        event_example = Event.create_event(
            title="Event Title", message="event message", event_type=zero_trust_consts.EVENT_TYPE_MONKEY_NETWORK)
        Finding.save_finding(test=zero_trust_consts.TEST_SEGMENTATION,
                             status=zero_trust_consts.STATUS_FAILED, events=[event_example])

        self.assertEqual(len(Finding.objects(test=zero_trust_consts.TEST_SEGMENTATION)), 1)
        self.assertEqual(len(Finding.objects(status=zero_trust_consts.STATUS_FAILED)), 1)
