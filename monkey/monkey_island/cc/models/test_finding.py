from datetime import datetime

from mongoengine import ValidationError

from common.data.zero_trust_consts import TEST_SEGMENTATION, STATUS_CONCLUSIVE, NETWORKS
from finding import Finding, UnknownTest
from monkey_island.cc.models.event import Event

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
        self.clean_monkey_db()

        with self.assertRaises(ValidationError):
            _ = Finding.save_finding(test="bla bla", status="Conclusive", events=[])

        with self.assertRaises(ValidationError):
            _ = Finding.save_finding(test=TEST_SEGMENTATION, status="bla bla", events=[])

    def test_save_finding_sanity(self):
        self.fail_if_not_testing_env()
        self.clean_monkey_db()

        self.assertEquals(len(Finding.objects(test=TEST_SEGMENTATION)), 0)

        event_example = Event(timestamp=datetime.now(), title="Event Title", message="event message", event_type="monkey_network_action")
        Finding.save_finding(test=TEST_SEGMENTATION, status=STATUS_CONCLUSIVE, events=[event_example])

        self.assertEquals(len(Finding.objects(test=TEST_SEGMENTATION)), 1)
        self.assertEquals(len(Finding.objects(status=STATUS_CONCLUSIVE)), 1)
