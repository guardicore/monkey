import pytest
from mongoengine import ValidationError

import common.common_consts.zero_trust_consts as zero_trust_consts
from monkey_island.cc.models.zero_trust.event import Event


class TestEvent:
    def test_create_event(self):
        with pytest.raises(ValidationError):
            _ = Event.create_event(
                title=None,  # title required
                message="bla bla",
                event_type=zero_trust_consts.EVENT_TYPE_MONKEY_NETWORK
            )

        with pytest.raises(ValidationError):
            _ = Event.create_event(
                title="skjs",
                message="bla bla",
                event_type="Unknown"  # Unknown event type
            )

        # Assert that nothing is raised.
        _ = Event.create_event(
            title="skjs",
            message="bla bla",
            event_type=zero_trust_consts.EVENT_TYPE_MONKEY_NETWORK
        )
