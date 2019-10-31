from mongoengine import ValidationError

from common.data.zero_trust_consts import EVENT_TYPE_MONKEY_NETWORK
from monkey_island.cc.models.zero_trust.event import Event
from monkey_island.cc.testing.IslandTestCase import IslandTestCase


class TestEvent(IslandTestCase):
    def test_create_event(self):
        self.fail_if_not_testing_env()
        self.clean_finding_db()

        with self.assertRaises(ValidationError):
            _ = Event.create_event(
                title=None,  # title required
                message="bla bla",
                event_type=EVENT_TYPE_MONKEY_NETWORK
            )

        with self.assertRaises(ValidationError):
            _ = Event.create_event(
                title="skjs",
                message="bla bla",
                event_type="Unknown"  # Unknown event type
            )

        # Assert that nothing is raised.
        _ = Event.create_event(
            title="skjs",
            message="bla bla",
            event_type=EVENT_TYPE_MONKEY_NETWORK
        )
