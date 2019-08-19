from mongoengine import ValidationError

from common.data.zero_trust_consts import EVENT_TYPE_ISLAND
from monkey_island.cc.models.zero_trust.event import Event
from monkey_island.cc.testing.IslandTestCase import IslandTestCase


class TestEvent(IslandTestCase):
    def test_create_event(self):
        self.fail_if_not_testing_env()
        self.clean_finding_db()

        with self.assertRaises(ValidationError):
            Event.create_event(
                title=None,  # title required
                message="bla bla",
                event_type=EVENT_TYPE_ISLAND
            )

        with self.assertRaises(ValidationError):
            Event.create_event(
                title="skjs",
                message="bla bla",
                event_type="Unknown"  # Unknown event type
            )

        _ = Event.create_event(
            title="skjs",
            message="bla bla",
            event_type=EVENT_TYPE_ISLAND
        )
